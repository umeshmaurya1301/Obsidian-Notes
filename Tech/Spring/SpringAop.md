AOP (Aspect-Oriented Programming) in Spring Boot is a programming paradigm that lets you separate **cross-cutting concerns** — logic that would otherwise be scattered across many classes — into standalone modules called **aspects**.

### The problem it solves

Things like logging, transaction management, security checks, and performance monitoring tend to repeat across many methods/classes. Without AOP, you'd sprinkle the same boilerplate everywhere, mixing business logic with infrastructure logic.

### Core concepts

- **Aspect**: A module that encapsulates a cross-cutting concern (e.g., `LoggingAspect`).
- **Join point**: A point during execution where an aspect can be applied — typically a method call in Spring AOP.
- **Advice**: The actual action taken at a join point. Types:
  - `@Before` — runs before the method executes
  - `@After` — runs after the method completes (regardless of outcome)
  - `@AfterReturning` — runs after successful method return
  - `@AfterThrowing` — runs if the method throws an exception
  - `@Around` — wraps the method entirely, controlling whether/when it executes
- **Pointcut**: An expression that defines *which* join points an advice applies to (e.g., all methods in a package, methods annotated with `@Transactional`).
- **Weaving**: The process of linking aspects with the target objects. Spring AOP does this at runtime using proxies (JDK dynamic proxies or CGLIB).

### Example

```java
@Aspect
@Component
public class LoggingAspect {

    @Around("execution(* com.card91.service.*.*(..))")
    public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = joinPoint.proceed(); // actually calls the target method
        long elapsed = System.currentTimeMillis() - start;
        System.out.println(joinPoint.getSignature() + " executed in " + elapsed + "ms");
        return result;
    }
}
```

This pointcut expression `execution(* com.card91.service.*.*(..))` matches any method in any class under `com.card91.service`, and the `@Around` advice wraps every matched call with timing logic — no changes needed in the service classes themselves.

### How Spring uses AOP internally

Spring Boot relies heavily on AOP under the hood for things you already use:
- `@Transactional` — wraps methods with transaction begin/commit/rollback logic
- `@Cacheable`, `@Async`, `@Retryable` — all implemented via proxy-based AOP
- Security annotations like `@PreAuthorize`

### Important caveat: self-invocation

Since Spring AOP is **proxy-based**, advice is only triggered when a method is called **from outside the bean, through the proxy**. If a method inside the same class calls another method annotated with `@Transactional` (or any AOP-advised method) directly (`this.method()`), the proxy is bypassed and the advice won't apply. This trips up a lot of people using `@Transactional` or custom aspects in Spring Boot — worth keeping in mind given the backend work you do.

Want me to go into pointcut expression syntax in more depth, or compare Spring AOP vs full AspectJ (compile-time weaving)?