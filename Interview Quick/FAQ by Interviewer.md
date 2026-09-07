1. Synchronize
2. Why do we use the Thread Pool Executor
3. Common problem u faced in production and how did u overcame that
4. Async and Transactional annotations of the spring boot.
5. What are the design patterns used in the distributed systems, with pros and cons and also what all have u used.
6. How do and at what levels do u ensure the idempotency
7. What design patterns have u used
8. SOLID principals and all about Java OOPS concepts

# Java OOP & Core Concepts — Interview Practice Set

Built around the three questions you got wrong: abstract class default methods calling abstract methods, private field access across instances, and pass-by-value with object reassignment. Each section below drills the same underlying concept from a different angle, since interviewers tend to circle back with variants once they find a soft spot.

Try to answer before checking your instinct against the "concept tested" line. The cheat-sheet at the end is for quick review, not for reading first.

---

## 1. Abstract Classes, Interfaces & Default Methods

**Q1 (yours).** Abstract class has abstract method `A()` and concrete method `B()`. Can `B()` call `A()`? Compile error or not?
*Concept: a method call only needs a valid signature at compile time; the actual implementation resolves via dynamic dispatch at runtime.*

**Q2.** Two interfaces `X` and `Y` both declare `default void greet()`. A class implements both without overriding `greet()`. What happens?
*Concept: the "diamond problem" for default methods — Java forces you to override and disambiguate; it will NOT pick one arbitrarily (compile error).*

**Q3.** Can an interface have a `private` method (Java 9+)? What's it for if you can never call it from outside?
*Concept: private interface methods exist to let default/static methods share code without exposing it in the public API.*

**Q4.** A subclass and its parent interface both define `static` methods with the same name. Can you override a static interface method?
*Concept: static methods are never polymorphic — they can't be overridden, only hidden, and interface statics aren't inherited at all (must call via interface name).*

**Q5.** Can an abstract class have a constructor if it can never be instantiated directly? Why would it need one?
*Concept: constructors in abstract classes run via `super()` from concrete subclasses — used to initialize common state.*

**Q6.** You create an anonymous class extending an abstract class, overriding the abstract method inline. Inside that override, can it call a private method of the abstract class?
*Concept: private methods aren't overridable but are still callable/inherited-in-scope from the same class body; anonymous class body is separate from the abstract class body.*

---

## 2. Access Modifiers & Encapsulation Traps

**Q7 (yours).** `Person.compareAge(Person other)` accesses `other.age` where `age` is private. Compile error?
*Concept: `private` is scoped to the class (all instances), not the object — well-known idiom in `equals()`, `compareTo()`, copy constructors.*

**Q8.** `Student extends Person`. Inside `Student`, can you access `person.age` directly, even though `Student` inherits from `Person`?
*Concept: subclass access to a parent's private field is denied — private members aren't inherited/visible at all, regardless of relationship.*

**Q9.** A method parameter is declared as `Object other`, but you pass a `Person` at runtime. Inside the method (written in `Person`'s class body), can you do `other.age`?
*Concept: access is checked against the declared/static type of the reference, not the runtime type — you must cast first.*

**Q10.** An inner (nested) class accesses a private field of its enclosing outer class instance. Allowed?
*Concept: opposite trap from Q8 — nested classes DO get private access to the enclosing class (nestmates since Java 11), often assumed blocked.*

**Q11.** Reflection: `field.get(obj)` on a private field without calling `setAccessible(true)` first. Compiles fine — what happens at runtime?
*Concept: private access is enforced at runtime by reflection too, not just compile time — throws `IllegalAccessException`.*

---

## 3. Pass-by-Value, References & Object Mutation

**Q12 (yours).** Method receives an object reference, reassigns it to a new object (`x = new Counter(2)`), then mutates the new object. Does the caller see any change?
*Concept: Java is always pass-by-value, even for references — reassigning the parameter never touches the caller's variable, only mutating the originally-referenced object does.*

**Q13.** Write a `swap(Person a, Person b)` method that tries to swap two `Person` references. Does it work as the caller expects?
*Concept: same trap as Q12 in disguise — classic "why doesn't my swap function work" interview follow-up.*

**Q14.** Inside a method, you do `str = str + "abc"` on a `String` parameter. Caller's original string — changed or not? Why is this different from an array or `StringBuilder`?
*Concept: `String` is immutable, so `+` creates a new object and rebinds the local reference — same reassignment trap, but rooted in immutability rather than object semantics generally.*

**Q15.** Method takes `int[] arr`, does `arr[0] = 99`. Caller's array — changed? Now method does `arr = new int[]{1,2,3}` instead. Changed?
*Concept: mutating the referenced array vs. reassigning the reference — same rule as objects, applied to arrays.*

**Q16.** `Integer a = 100, b = 100; System.out.println(a == b);` then same with `1000` instead of `100`. Two different outputs — why?
*Concept: Integer caching pool (-128 to 127) via `Integer.valueOf()` — autoboxing reuses cached objects only in that range, so `==` behaves inconsistently by coincidence of value.*

---

## 4. equals(), hashCode() & Object Identity

**Q17.** You override `equals()` but not `hashCode()`. You put the object in a `HashSet`, then check `set.contains(equalObject)`. Does it find it?
*Concept: the equals/hashCode contract — unequal hashCodes send equal objects to different buckets, breaking hash-based collections even though `.equals()` alone says they match.*

**Q18.** `String s1 = new String("abc"); String s2 = "abc"; s1 == s2` vs `s1.equals(s2)` — explain both results.
*Concept: string pool vs heap-allocated string objects — `new String()` deliberately bypasses interning.*

---

## 5. Static Context, Method Hiding vs Overriding

**Q19.** Parent and child both declare a `static` method with the same signature. You call it via a Parent-typed reference pointing to a Child object. Which runs?
*Concept: static methods are resolved by declared (compile-time) type, not dynamic dispatch — this is "hiding," not "overriding," and it's the single most common polymorphism trick question.*

**Q20.** Same setup as Q19, but with an instance *field* instead of a method (`Parent.x` vs `Child.x`). Which value do you get via a Parent-typed reference?
*Concept: fields never participate in polymorphism at all — resolved purely by declared type, always.*

**Q21.** A parent class constructor calls an overridable method that the subclass has overridden, and that override reads a subclass field. What value does it see?
*Concept: classic bug — subclass fields aren't initialized yet when the parent constructor runs, so the override sees default values (0/null), not the field's real initializer.*

---

## 6. Constructors & Initialization Order

**Q22.** Given a 3-level class hierarchy each with static blocks, instance initializer blocks, and constructors — what's the exact execution order when you instantiate the deepest subclass?
*Concept: static blocks (once, top-down, on class load) → then per-instantiation: parent instance blocks → parent constructor → child instance blocks → child constructor.*

**Q23.** Can a constructor call both `this(...)` and `super(...)`?
*Concept: no — only one explicit constructor-call statement is allowed, and it must be the first statement, so you must choose one (the other happens implicitly/transitively).*

---

## 7. Exceptions in Overriding

**Q24.** Parent's method declares `throws IOException`. Can the overriding method in the subclass declare `throws Exception` instead?
*Concept: an override can only throw the same, narrower, or no checked exceptions — never a broader one; unchecked exceptions are unrestricted either way.*

**Q25.** A method has a `try` block that returns a value, and a `finally` block that also returns a value. Which one wins?
*Concept: `finally`'s return silently overrides the `try` block's return — a well-known footgun, and also swallows any exception in flight.*

---

## 8. Generics & Type Erasure

**Q26.** Inside `class Box<T>`, why can't you write `new T()` or `new T[10]`?
*Concept: type erasure — generic type info doesn't exist at runtime, so the JVM has no `T` to instantiate.*

**Q27.** Can you overload two methods as `void process(List<String> l)` and `void process(List<Integer> l)` in the same class?
*Concept: both erase to `process(List l)` at compile time — duplicate method signature, compile error.*

---

## Quick-Review Cheat Sheet

- **Private access** = scoped to class body + declared type of the reference, never to "self" and never inherited by subclasses.
- **Pass-by-value always** — reassigning a parameter inside a method never affects the caller; only mutating the object it already points to does.
- **Static anything (methods, fields hidden the same way)** = resolved by declared type at compile time, no dynamic dispatch. Only *instance methods* get polymorphism.
- **Fields never override** — only instance methods do.
- **equals() and hashCode() are a pair** — override one, override both, or hash-based collections silently break.
- **Immutability (String, Integer, wrapper types)** turns "mutation" bugs into "reassignment" bugs — same root cause as pass-by-value confusion.
- **Overriding + exceptions**: narrower or equal checked exceptions only, never broader.
- **Generics are erased at runtime** — no `new T()`, no runtime-type-based overloads.



# Kafka Interview Practice Set — Payments Systems Focus

Built around the two questions you got asked: what you configured for idempotency/retry/DLQ, and what problems Kafka itself caused and how you solved them. Payments interviewers usually probe both halves — "show me you can build reliable delivery" and "show me you've actually operated this in production and hit real failure modes," not just textbook Kafka. Grouped so you can rehearse each half separately.

---

## 1. Producer-Side Reliability & Delivery Guarantees

**Q1 (yours, expanded).** Walk through every config you'd set on a payment-events producer for reliability: `acks`, `enable.idempotence`, `retries`, `max.in.flight.requests.per.connection`, `delivery.timeout.ms`. What does each actually protect against?
*Concept tested: idempotent producer prevents duplicate sends on retry (via producer ID + sequence number per partition), `acks=all` protects against data loss on broker failure, `max.in.flight=5` (with idempotence on) is the max that still preserves ordering.*

**Q2.** Idempotent producer only guarantees no duplicates *within a single producer session*. What happens if the producer process crashes and restarts — could you still get duplicates downstream?
*Concept tested: producer-level idempotence resets on a new producer instance/session; end-to-end dedup for payments needs an idempotency key at the application/message level, not just the producer.*

**Q3.** Why would you use Kafka transactions (`transactional.id`, `initTransactions`) instead of plain idempotent producer for a payment flow that writes to a DB and publishes an event?
*Concept tested: the dual-write problem — writing to DB and publishing to Kafka isn't atomic; solved via Kafka transactions with a transactional outbox, or the outbox pattern with a separate relay (e.g., Debezium/CDC) reading committed DB rows.*

**Q4.** If you set `retries` high on the producer to handle transient broker issues, what's the tradeoff you're accepting?
*Concept tested: higher retries + `max.in.flight > 1` without idempotence risks reordering; also higher `delivery.timeout.ms` delays failure detection upstream (e.g., your REST caller times out before Kafka does).*

---

## 2. Retry & DLQ Design

**Q5 (yours).** Describe your retry + DLQ setup for payment processing end to end. Where does a message go after N failed retries, and what decides "retry" vs "DLQ immediately"?
*Concept tested: distinguish retryable errors (downstream timeout, transient DB lock) from non-retryable ones (malformed payload, business rule violation) — the latter should skip straight to DLQ, not burn retry budget.*

**Q6.** In-topic retry (re-publish to the same topic) vs a dedicated retry topic (or a chain of retry topics with increasing delay) vs an in-memory/blocking retry inside the consumer — what are the tradeoffs?
*Concept tested: in-memory retry blocks partition progress (head-of-line blocking) if the message keeps failing; separate retry topics with backoff (retry-5s, retry-30s, retry-5m) avoid blocking the main topic and let you tune backoff per stage.*

**Q7.** A single malformed/"poison" message is stuck at the front of a partition and the consumer keeps crashing trying to process it. How do you stop it from blocking every message behind it?
*Concept tested: catch deserialization/processing exceptions explicitly, route the specific offset to DLQ, and manually advance the offset past it rather than letting the exception propagate and stall the whole partition.*

**Q8.** How do you reprocess messages sitting in a DLQ once the downstream issue is fixed? What has to be true about the DLQ message for that to be safe in a payments context?
*Concept tested: DLQ messages need enough context (original headers, retry count, failure reason, original partition/offset) to replay safely and idempotently — replaying a payment message twice must not double-process it.*

**Q9.** Would you alert on DLQ volume, or just let it accumulate? What threshold logic makes sense for a payments pipeline specifically?
*Concept tested: DLQ growth in payments usually needs near-real-time alerting (not just a dashboard) since a stuck payment is a customer-facing/compliance issue, not just an engineering metric.*

---

## 3. Ordering, Partitioning & Idempotency in Payments

**Q10.** How do you guarantee all events for the same transaction/payment are processed in order?
*Concept tested: partition key = transaction ID (or account/user ID) so all related events land on the same partition, since Kafka only guarantees order within a partition, never across partitions.*

**Q11.** If retries can cause a message to be redelivered, how do you make the *consumer* idempotent, independent of what the producer already did?
*Concept tested: application-level dedup — unique idempotency key + DB unique constraint, or a dedup cache (Redis with TTL) checked before processing, since "exactly-once" from Kafka's transport layer alone doesn't cover side effects like a second debit call.*

**Q12.** Why is at-least-once + idempotent consumer usually preferred over trying to achieve strict exactly-once semantics across the whole pipeline (including external payment gateway calls)?
*Concept tested: Kafka's exactly-once (transactions) only covers Kafka-to-Kafka or Kafka-to-DB via the same transaction coordinator — it can't make an external HTTP call to a PSP exactly-once, so idempotency has to be enforced at that boundary regardless.*

**Q13.** You increase partition count on a topic to scale consumers. What breaks for messages that rely on partition-based ordering?
*Concept tested: changing partition count changes the key→partition hash mapping for all future messages, so ordering guarantees for a given key can be silently broken mid-flight unless you plan the migration carefully.*

---

## 4. Consumer Groups & Rebalancing Problems

**Q14.** What causes a consumer group rebalance, and why are frequent rebalances a problem in a payments pipeline specifically?
*Concept tested: rebalances (consumer join/leave, session timeout, slow poll loop) pause the whole group during a stop-the-world rebalance in the classic protocol — during that pause, no messages in that group are processed at all, adding latency to payment settlement.*

**Q15.** A consumer is periodically kicked out of the group and rejoins, even though the process never crashed. What's the likely cause and how did you fix it?
*Concept tested: processing time per poll batch exceeding `max.poll.interval.ms` — classic fix is either shrinking `max.poll.records`, moving heavy work off the poll thread, or tuning the interval; conflating this with `session.timeout.ms` (heartbeat-related) is a common mistake to avoid.*

**Q16.** Auto-commit vs manual offset commit — which did you choose for payment processing, and why?
*Concept tested: auto-commit can commit an offset before processing actually completes (risking message loss on crash), so manual commit-after-successful-processing is standard for anything with financial consequences.*

**Q17.** What's the difference in guarantees between committing the offset *before* vs *after* the message is fully processed and its side effects are durable?
*Concept tested: commit-before risks silent message loss on crash (at-most-once); commit-after risks reprocessing on crash (at-least-once) — payments should pick the latter and rely on idempotency to absorb the reprocessing.*

---

## 5. Operational Failures — "What Problems Did Kafka Cause You"

**Q18 (yours).** Kafka gives you async decoupling and durability, but what did it cost you operationally? Give a concrete incident, not a generic answer.
*Concept tested: interviewers want a specific failure mode + your diagnosis + your fix — e.g., consumer lag spike during a traffic burst, broker disk filling up, ISR shrinking below `min.insync.replicas` causing producer errors, or a schema change breaking consumers silently.*

**Q19.** `min.insync.replicas` and `acks=all` are both set for durability. A broker goes down and ISR shrinks below the configured minimum. What happens to your producer, and how should your application react?
*Concept tested: producer starts throwing `NotEnoughReplicasException` — the application needs an explicit fallback (fail fast, queue locally, alert) rather than silently swallowing the error, since a payment event failing to publish is not something to drop.*

**Q20.** How do you monitor consumer lag, and what's your actual response when lag starts climbing under load — scale consumers, or is it more nuanced than that?
*Concept tested: lag can climb from under-provisioned consumers OR from a slow downstream dependency (DB, external API) — blindly adding consumers doesn't help if partition count is already the bottleneck, or if the real constraint is downstream throughput.*

**Q21.** A producer's schema changes (new required field, or a type change) and downstream consumers start failing deserialization. How do you prevent this, and how did you actually handle it if it happened?
*Concept tested: schema registry with compatibility rules (backward/forward compatible evolution), and for an incident already in progress — dead-lettering the unparseable messages plus a hotfix/rollback rather than losing them.*

**Q22.** What's the operational cost of running a "Kafka multi-broker with DLQ" setup that a simpler synchronous REST call between services doesn't have?
*Concept tested: cluster ops (broker sizing, replication, partition rebalancing), harder distributed tracing across an async boundary, eventual consistency semantics leaking into product behavior, and DLQ workflows needing their own monitoring/replay tooling — this is the "tradeoffs" half of the question, not just benefits.*

---

## Quick-Review Cheat Sheet

**Producer reliability configs:** `acks=all`, `enable.idempotence=true`, `max.in.flight.requests.per.connection≤5` (with idempotence), `retries=MAX`, `delivery.timeout.ms` set deliberately.

**Consumer reliability:** manual offset commit after processing, `max.poll.records` tuned to processing time, idempotent handling via app-level dedup key.

**DLQ pattern:** classify retryable vs non-retryable errors → bounded retries with backoff (separate retry topics, not blocking in-memory loops) → DLQ with enough metadata to safely replay → active alerting on DLQ volume, not passive dashboards.

**Ordering:** guaranteed only within a partition; key by transaction/account ID; partition count changes can silently break key→partition mapping.

**Exactly-once reality check:** Kafka transactions cover Kafka↔Kafka/DB; anything crossing an external HTTP boundary (PSP call) still needs application-level idempotency — "exactly-once" is never truly end-to-end for free.

**Common production failure modes to have a story for:** rebalance storms from slow poll loops, ISR shrinkage under `min.insync.replicas`, consumer lag from downstream slowness (not just under-scaling), schema evolution breaking consumers, poison messages stalling a partition.



# MDC (Mapped Diagnostic Context) & Logging Correlation — Interview Practice Set

MDC questions come up whenever you mention "correlation ID," "request tracing across microservices," or "how do you debug a single request across logs." Interviewers use it to probe whether you actually understand `ThreadLocal` semantics under thread pools/async code, not just that you called `MDC.put()` somewhere. Group below goes from basics → constants/keys design → thread pool & async leaks → propagation across boundaries (Kafka, WebClient, reactive) → cleanup discipline.

---

## 1. What MDC Actually Is

**Q1.** What is MDC, and what data structure backs it under the hood?
*Concept tested: MDC (SLF4J API, backed by Logback/Log4j2) is a `ThreadLocal<Map<String,String>>` per thread — it lets you stamp every log line on the current thread with key/value context (e.g., `traceId`, `userId`) without passing them explicitly through every method signature.*

**Q2.** How does a value put into MDC actually reach the log output? Where's the wiring?
*Concept tested: the appender's log pattern references `%X{key}` (Logback) or `%X{key}` (Log4j2) — the pattern layout reads from the calling thread's MDC map at format time, so if the pattern doesn't reference the key, `MDC.put()` is silently useless for that appender.*

**Q3.** Why should MDC keys be defined as named constants (e.g., `MdcKeys.TRACE_ID`, `MdcKeys.USER_ID`) instead of raw string literals scattered across the codebase?
*Concept tested: a typo'd key string (`"traceld"` vs `"traceId"`) silently breaks correlation with no compile-time error — centralizing keys as constants (often an `enum` or `final class` of `public static final String`) makes them grep-able, renameable, and reusable between the filter that sets them and the appender pattern that reads them.*

**Q4.** What's a sane, minimal set of MDC constants for a payments-style microservice, and why those specifically?
*Concept tested: typically `traceId`/`correlationId` (cross-service request identity), `requestId` (per-hop identity), `userId`/`merchantId` (business context for support debugging), and sometimes `spanId` if layering manual MDC on top of a tracer — the key design principle is "only what you'll actually filter/search logs by," since every key adds to every log line's size.*

---

## 2. Thread Pools & the Classic MDC Leak

**Q5 (high-frequency).** A request sets `MDC.put("traceId", "abc")` in a servlet filter, then hands work off to an `ExecutorService` thread pool. Does the worker thread see `traceId` in its logs?
*Concept tested: no — MDC is `ThreadLocal`, and the pooled worker thread is a *different* thread than the one that ran the filter; without explicit propagation, the async task's logs have no `traceId` at all (empty, not wrong).*

**Q6.** Now the opposite bug: a thread pool thread processed request A (`traceId=abc`), didn't clear MDC, got returned to the pool, and later picked up request B. What do request B's logs show?
*Concept tested: MDC leak/bleed — because thread pool threads are reused, a forgotten `MDC.clear()` in a `finally` block means the next task on that same thread inherits the *stale* previous value, silently mislabeling B's logs as `abc`. This is worse than Q5's blank case because it's wrong data, not missing data.*

**Q7.** What's the correct pattern to fix Q5 — propagate MDC context into a submitted `Runnable`/`Callable`?
*Concept tested: capture `MDC.getCopyOfContextMap()` on the calling thread before submitting, then inside the task do `MDC.setContextMap(captured)` at the start and `MDC.clear()` in a `finally` — SLF4J's `MDC.getCopyOfContextMap()` returns `null` if nothing was set, so guard for that before calling `setContextMap`.*

**Q8.** Why is wrapping the `ExecutorService` in an `MdcTaskDecorator` (or overriding `execute()`) preferred over manually copying MDC at every call site?
*Concept tested: centralizing the copy-set-clear dance in one decorator (Spring's `TaskDecorator` for `ThreadPoolTaskExecutor`, or a custom `ExecutorService` wrapper) prevents every future call site from having to remember it — a single missed call site reintroduces the Q6 leak.*

**Q9.** Does `@Async` in Spring propagate MDC automatically?
*Concept tested: no, not out of the box — `@Async` methods run on a separate `TaskExecutor` thread, so you need a `TaskDecorator` bean (as in Q8) wired into the executor config, or a library like `micrometer-context-propagation`, otherwise every `@Async` method silently loses correlation context.*

**Q10.** In a `CompletableFuture.supplyAsync(...).thenApply(...)` chain using the common `ForkJoinPool`, at which stage(s) can MDC context be lost?
*Concept tested: every `.thenApply`/`.thenCompose` stage can potentially hop to a different pool thread (unless it runs synchronously because the prior stage was already complete) — so MDC can silently disappear mid-chain, not just at the first hop; each async stage needs its own context capture/restore if you want guarantees.*

---

## 3. Cleanup Discipline & Lifecycle

**Q11.** Where exactly should `MDC.clear()` (or `MDC.remove(key)`) go, and why does it matter more in a thread-pooled server than in a short-lived script?
*Concept tested: must go in a `finally` block (or a servlet `Filter`'s `finally`, or `try-with-resources` via `MDC.putCloseable`) so it runs even on exception — in a thread pool the thread survives the request and gets reused, so a missed clear leaks into the next unrelated request (Q6); in a throwaway process the thread just dies, masking the same bug.*

**Q12.** What does `MDC.putCloseable(key, value)` give you that plain `MDC.put(key, value)` doesn't?
*Concept tested: it returns an `MDC.MDCCloseable` implementing `AutoCloseable`, so you can do `try (var ignored = MDC.putCloseable("traceId", id)) { ... }` and get guaranteed removal via try-with-resources — removes the "forgot the finally" failure mode entirely for scoped usage.*

**Q13.** Should `MDC.clear()` wipe everything, or should you prefer `MDC.remove(key)` for specific keys? When would clearing everything be wrong?
*Concept tested: `clear()` wipes the whole map, which is fine at the outermost boundary (top of a filter's finally) but wrong mid-request if you nested a scoped context (e.g., a sub-task added `batchId` temporarily) — clearing everything there would also wipe the outer `traceId` that later code still needs, so scoped `remove()` or a save/restore of the *previous* map is safer for nested contexts.*

---

## 4. Propagation Across Service & Protocol Boundaries

**Q14.** A request comes in via a REST controller, and downstream it makes a `WebClient`/`RestTemplate` call to another service. How do you make sure the same `traceId` shows up in both services' logs?
*Concept tested: MDC itself never crosses the network — you must explicitly read `MDC.get(TRACE_ID)` and set it as an outgoing HTTP header (e.g., `X-Trace-Id` or `traceparent` if using W3C trace context), then a filter/interceptor on the receiving service reads that header and calls `MDC.put()` before processing.*

**Q15.** How does this change for a Kafka producer/consumer instead of synchronous HTTP?
*Concept tested: same principle, different transport — write the correlation ID into Kafka message *headers* (not the payload, to avoid coupling business schema to tracing) on produce, and a consumer interceptor reads the header and populates MDC before the listener method runs; without this, async Kafka processing has zero correlation to the request that published the event.*

**Q16.** You're using Spring Cloud Sleuth / Micrometer Tracing (Brave or OpenTelemetry) — do you still need to hand-roll MDC propagation?
*Concept tested: these libraries already auto-populate MDC with `traceId`/`spanId` and instrument common async boundaries (executors, WebClient, Kafka) for you — hand-rolling `MDC.put("traceId", ...)` alongside them risks a second, inconsistent ID; the interview-safe answer is "use the tracer's context as the source of truth, only add custom *business* keys (userId, merchantId) manually on top."*

**Q17.** In a reactive stack (WebFlux/Project Reactor), why does plain `ThreadLocal`-based MDC break down, and what's the fix?
*Concept tested: Reactor operators can hop across the event-loop/scheduler threads mid-chain (similar to Q10 but far more frequent), so `ThreadLocal` MDC set at subscribe time doesn't reliably appear later in the chain — the fix is Reactor's `Context` (or Micrometer's `ContextSnapshot`/`context-propagation` library) which threads context through the reactive pipeline and only writes it into MDC right before each log statement via a hook (`Hooks.onEachOperator` / `Schedulers` instrumentation), not persistent `ThreadLocal` state.*

---

## 5. Debugging & Production Scenarios

**Q18.** In production, you see log lines with the *wrong* `userId` stamped on them intermittently, only during high load. What's your first hypothesis and how do you confirm it?
*Concept tested: classic MDC-leak-under-pool-reuse (Q6) — confirm by checking whether the executor/thread pool involved has a missing `clear()`/decorator, and whether the mislabeled lines cluster on thread names that are reused across requests (thread pool naming like `pool-2-thread-7` recurring with different traceIds is the tell).*

**Q19.** Logs occasionally show blank `traceId=` fields for what should be a downstream call within the same request. What are the two most likely causes, and how do you tell them apart?
*Concept tested: (1) the call crossed an async/thread-pool boundary without propagation (Q5/Q9/Q10) — look for the log line's thread name changing mid-request with no traceId; (2) the request never had a traceId set in the first place (e.g., missed by a filter ordering issue — the MDC-populating filter registered *after* another filter that already logs) — check filter/interceptor `@Order`.*

**Q20.** Why is putting high-cardinality or large values (e.g., full request payload, PII) into MDC a bad idea, beyond just log size?
*Concept tested: MDC values get stamped onto *every* log line for that thread/request, multiplying storage and search-index cost across a whole request's log volume, and if the value is PII, it now leaks into every appender/sink (including log aggregators, DLQ log copies, etc.) rather than a single deliberate log statement.*

---

## Quick-Review Cheat Sheet

- **MDC = `ThreadLocal<Map<String,String>>`** — scoped to the *thread*, not the request, not the object. This single fact explains every trick question in this set.
- **Keys should be constants**, not string literals — a typo'd key breaks correlation silently, with no compile error.
- **Thread pools are the #1 gotcha**: async work needs explicit MDC copy-in/clear-out (`TaskDecorator`, wrapped `ExecutorService`, or a tracing library) or you get either blank context (Q5) or leaked/stale context onto the wrong request (Q6) — leaked is worse because it's wrong data, not missing data.
- **Always clear in `finally`**, or use `MDC.putCloseable` with try-with-resources — a thread that outlives the request (pool reuse) will carry stale MDC into the next task otherwise.
- **MDC never crosses a network or message boundary on its own** — must be serialized to an HTTP header or Kafka message header on the way out, and re-populated by a filter/interceptor on the way in.
- **Reactive/Reactor breaks plain MDC** — use `Context`/context-propagation, not raw `ThreadLocal`, since operators hop schedulers.
- **Prefer a tracing library's context (Sleuth/Micrometer Tracing) as source of truth** for `traceId`/`spanId`; layer custom business keys (userId, merchantId) manually on top rather than reinventing trace IDs.
- **Don't put PII or large payloads in MDC** — it multiplies across every log line for the thread/request lifetime.


