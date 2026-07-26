## 1) Core foundations

These are must-know first:

- Concurrency vs parallelism
- Process vs thread
- Thread lifecycle and states
- Context switching
- Race condition
- Critical section
- Deadlock, livelock, starvation
- Memory visibility
- Happens-before

## 2) Java thread basics

- `Thread` and `Runnable`
- `Callable` and `Future`
- `Thread.sleep()`, `yield()`, `join()`
- Thread interruption
- Daemon vs user threads
- `ThreadLocal`

## 3) Synchronization

- `synchronized` block and method
- Intrinsic lock / monitor lock
- `volatile`
- `wait()`, `notify()`, `notifyAll()`
- `Lock` interface
- `ReentrantLock`
- `ReadWriteLock`

## 4) Executors and thread pools

This is very important in real systems:

- `Executor`, `ExecutorService`, `ScheduledExecutorService`
- `ThreadPoolExecutor`
- Fixed vs cached vs single-thread pools
- Queueing behavior
- Rejection policies
- `ForkJoinPool` basics

## 5) Concurrent utilities

- `AtomicInteger`, `AtomicLong`, `AtomicBoolean`
- `AtomicReference`
- `LongAdder`, `DoubleAdder`
- `CountDownLatch`
- `CyclicBarrier`
- `Semaphore`
- `Phaser` basics
- `Condition`

## 6) Concurrent collections

- `ConcurrentHashMap`
- `BlockingQueue`
- `ConcurrentLinkedQueue`
- `CopyOnWriteArrayList`
- `CopyOnWriteArraySet`

## 7) Async programming

- `CompletableFuture`
- Chaining
- Combining futures
- Exception handling in async flows

## 8) Modern Java concurrency

- Virtual Threads
- Structured Concurrency
- Scoped Values

## 9) Database concurrency

Very important for backend work:

- ACID, especially isolation
- Read committed, repeatable read, serializable
- Optimistic locking
- Pessimistic locking
- Deadlocks in DB
- `SELECT ... FOR UPDATE`

## 10) Distributed concurrency basics

- Idempotency
- Distributed locking basics
- Redis lock basics
- Eventual consistency
- CAP theorem
- Ordering in Kafka / queues

## 11) Transaction boundaries

Where a rollback stops helping — the most under-taught area, and heavily asked:

- Transaction scope: what one rollback actually undoes
- Rollback rules and `@Transactional` propagation
- Safe retries (rebuilding entities, backoff with jitter)
- The dual-write problem
- Transactional outbox
- Saga and compensating transactions
- Idempotent consumers
- Two-phase commit (2PC / XA) and why it's avoided

## What to learn deeply vs lightly

### Learn deeply

- `synchronized`, `volatile`, `wait/notify`
- Deadlock and race conditions
- ExecutorService and ThreadPoolExecutor
- ConcurrentHashMap
- BlockingQueue
- CompletableFuture
- DB isolation and locking
- Idempotency
- `@Transactional` semantics and transaction boundaries
- Transactional outbox

### Learn moderately

- ReentrantLock
- ReadWriteLock
- Atomic classes
- CountDownLatch, CyclicBarrier, Semaphore
- Redis locking
- Kafka ordering and consumer concurrency
- Saga and compensating transactions

### Just know the basics

- Phaser
- StampedLock
- ForkJoinPool internals
- Virtual threads
- Structured concurrency
- Raft, Paxos, STM, CSP, Actor model
- 2PC / XA (know why it's avoided, not how to run it)

## Best order to study

1. Thread basics and race conditions
2. synchronized / volatile / wait-notify
3. Executors and thread pools
4. Concurrent collections and atomics
5. CompletableFuture
6. DB locking and isolation
7. Transaction boundaries, outbox, idempotency
8. Redis/Kafka concurrency basics
9. Modern Java concurrency