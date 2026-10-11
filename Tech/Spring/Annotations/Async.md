`@Async` follows the exact same AOP-proxy pattern as `@Transactional` — same weaving mechanism, different interceptor. Let's go through it end-to-end, including where it intersects with what we just discussed on transactions and threads.

## 1. Setup

You need `@EnableAsync` on a config class (or it's auto-configured in Spring Boot if you define a `TaskExecutor` bean). Just like `@EnableTransactionManagement`, this registers a `BeanPostProcessor` — specifically `AsyncAnnotationBeanPostProcessor` — that scans every bean for `@Async` methods and wraps the containing bean in a **proxy** (CGLIB or JDK dynamic proxy), same as before.

## 2. What happens on a call

When you call an `@Async` method through the proxy:

1. The proxy intercepts the call via `AsyncExecutionInterceptor` (an `Advice`, same family as `TransactionInterceptor`).
2. Instead of running your method body on the caller's thread, the interceptor wraps it in a `Callable`/`Runnable` and **submits it to a `TaskExecutor`** (a thread pool).
3. **The calling thread returns immediately** — it does not block waiting for the async method to finish (unless you explicitly block on the returned `Future`).
4. Your actual method body executes later, on a thread pulled from that pool.

## 3. Which thread pool?

By default, if you haven't defined one, Spring uses `SimpleAsyncTaskExecutor` — which is dangerous in production: **it creates a brand-new thread per task, with no pooling and no bound.** Under load this can exhaust OS threads and crash the process. Always define your own:

```java
@Configuration
@EnableAsync
public class AsyncConfig {
    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(50);
        executor.setQueueCapacity(200);
        executor.setThreadNamePrefix("async-exec-");
        executor.initialize();
        return executor;
    }
}
```

You can point a specific method at a specific pool: `@Async("taskExecutor")` — useful if you want to isolate, say, Kafka-callback-triggered async work from webhook-notification async work so one doesn't starve the other.

## 4. Return types

- **`void`**: fire-and-forget. Caller has zero visibility into success/failure — exceptions vanish unless you configure an `AsyncUncaughtExceptionHandler`.
- **`Future<T>` / `ListenableFuture<T>`**: caller can `.get()` to block and retrieve the result or exception later.
- **`CompletableFuture<T>`**: the modern, preferred choice — supports chaining (`.thenApply`, `.thenCompose`, `.exceptionally`) without blocking.

```java
@Async
public CompletableFuture<String> processPayment(String txnId) {
    // runs on the async thread pool
    return CompletableFuture.completedFuture(result);
}
```

## 5. The critical gotcha, tying back to what you asked earlier

Since `@Async` genuinely switches execution to a **different thread**, and Spring's transaction binding uses a **`ThreadLocal`** (`TransactionSynchronizationManager`) — the async method does **not** see any transaction or DB connection that was open on the calling thread. Two consequences:

- If the calling method was `@Transactional` and called an `@Async` method, the async method runs **outside** that transaction entirely — it will use its own connection (opening a new implicit transaction if it does any DB work, or none at all if not marked `@Transactional` itself).
- If the calling method's transaction later rolls back, **the async method's work is unaffected** — it already ran independently and can't be rolled back by the caller's transaction. This is a very common bug: people call an async audit-log or notification method from inside a transactional service method, expecting it to roll back together, and it doesn't.

## 6. Self-invocation — same rule as `@Transactional`

Because it's proxy-based AOP, calling an `@Async` method via `this.method()` from within the same class bypasses the proxy → runs synchronously on the calling thread, silently. This is one of the most common "why isn't my `@Async` working" bugs.

## 7. Exception handling

For `void` methods, an uncaught exception is swallowed by the executor thread unless you register:

```java
@Override
public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
    return (throwable, method, params) -> log.error("Async failure in {}", method.getName(), throwable);
}
```

(via implementing `AsyncConfigurer`). For `Future`/`CompletableFuture` returns, the exception is captured in the future object itself and only surfaces when you call `.get()` or use `.exceptionally()`.

## Relevance to your Kafka-heavy UPI Switch work

A few things worth being deliberate about given your stack:
- If a Kafka consumer's `@KafkaListener` method calls an `@Async` method and then acks the offset immediately, you can ack **before** the async work actually finishes — creating a false sense of "processed" if that async task later fails.
- Thread pool sizing matters a lot under UPI-scale throughput — an undersized queue + pool means `TaskRejectedException` under burst load; you'd want a `CallerRunsPolicy` or an explicit backpressure strategy rather than silently dropping requests.
- MDC (logging context — trace IDs, txn IDs) does **not** propagate to the new async thread by default, since `ThreadLocal` doesn't cross threads. You'd need a `TaskDecorator` to copy MDC context into the async thread manually — very relevant if you're correlating logs across an NPCI transaction lifecycle.