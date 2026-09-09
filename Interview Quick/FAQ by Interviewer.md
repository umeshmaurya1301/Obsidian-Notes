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



# Streams Collectors, Java Version Features & Type System — Interview Practice Set

Covers four things that tend to get asked back-to-back once a Streams question lands well: multi-level `Collectors.groupingBy`, what actually shipped in each major LTS (8 → 17 → 21 → 25), sealed classes, and the marker-interface family (`Serializable`, `Cloneable`, etc.). Interviewers chain these because "you used `groupingBy` cleanly" invites "okay, what Java version introduced streams, and what's new since then."

---

## 1. `Collectors.groupingBy` + Downstream Collectors

**Q1 (reference example).** Group employees by department and compute the average salary per department.
```java
class Employee {
    private String name;
    private String department;
    private double salary;
    // constructor, getters
}

List<Employee> employees = List.of(
        new Employee("John", "IT", 50000),
        new Employee("Alice", "IT", 70000),
        new Employee("Bob", "HR", 40000),
        new Employee("Carol", "HR", 60000)
);

Map<String, Double> avgSalaryByDept =
        employees.stream()
                 .collect(Collectors.groupingBy(
                         Employee::getDepartment,
                         Collectors.averagingDouble(Employee::getSalary)
                 ));
// {IT=60000.0, HR=50000.0}
```
*Concept tested: `groupingBy(classifier, downstream)` is a two-stage collector — the classifier partitions elements into buckets (a `Map<K, List<T>>` by default), and the downstream collector (`averagingDouble` here) reduces each bucket instead of leaving it as a raw list. This is the standard "grouping + downstream collector" pattern interviewers want to see you reach for by reflex.*

**Q2.** Rewrite Q1 to get the *highest-paid* employee per department instead of the average.
*Concept tested: swap the downstream collector for `Collectors.maxBy(Comparator.comparingDouble(Employee::getSalary))` — result type becomes `Map<String, Optional<Employee>>` since `maxBy`/`minBy` must handle an empty bucket, which `averagingDouble` doesn't need to (it defaults to `0.0`).*

**Q3.** Group employees by department, but instead of a `Map<String, Double>`, produce `Map<String, List<String>>` of just employee names.
*Concept tested: `Collectors.mapping(Employee::getName, Collectors.toList())` as the downstream collector — `mapping()` lets you transform each element *before* it's reduced by another downstream collector, useful when you don't want the full object in the result.*

**Q4.** Group employees by department *and* by seniority level (a two-level grouping) — `Map<String, Map<String, List<Employee>>>`.
*Concept tested: nest `groupingBy` as the downstream of another `groupingBy` — `groupingBy(Employee::getDepartment, groupingBy(Employee::getSeniority))`; this is the most common follow-up once single-level grouping is shown, testing whether you understand downstream collectors compose recursively.*

**Q5.** Why does `groupingBy` return a `HashMap` by default, and how do you force a specific map type (e.g., `TreeMap` for sorted department names) or a specific bucket type (e.g., `TreeSet` instead of `ArrayList`)?
*Concept tested: the 3-arg overload `groupingBy(classifier, mapFactory, downstream)` — `mapFactory` is a `Supplier<M>` like `TreeMap::new`; default is `HashMap::new` + `ArrayList::new`, which is why iteration order isn't guaranteed unless you override it.*

**Q6.** What's the difference between `Collectors.toMap()` and `Collectors.groupingBy()` when the classifier can produce duplicate keys?
*Concept tested: `toMap()` throws `IllegalStateException` on a duplicate key unless you supply a merge function (3rd arg); `groupingBy()` never throws for duplicates because it's designed around buckets (a `List`) from the start — this is a common "why did my toMap throw at runtime" debugging question.*

**Q7.** `Collectors.partitioningBy()` vs `Collectors.groupingBy()` with a boolean classifier — functionally similar, so why does `partitioningBy` exist as a separate collector?
*Concept tested: `partitioningBy` always returns a `Map<Boolean, List<T>>` with *both* `true` and `false` keys present even if one bucket is empty (backed by a specialized `Partition` map, not a general `HashMap`), whereas `groupingBy` with a boolean classifier would simply omit a key that never occurred — matters if downstream code assumes both keys always exist.*

---

## 2. Java Version Features — 8 → 17 → 21 → 25

**Q8.** What are the headline Java 8 features, beyond just "lambdas"?
*Concept tested: the full picture interviewers expect —*
- *Lambda expressions + functional interfaces (`java.util.function`: `Function`, `Predicate`, `Supplier`, `Consumer`, etc.), `@FunctionalInterface`*
- *Stream API (`java.util.stream`) — sequential and parallel*
- *Default & static methods on interfaces (enables Stream API's own evolution without breaking implementors)*
- *`Optional<T>`*
- *New Date/Time API (`java.time` — `LocalDate`, `LocalDateTime`, `Instant`, `Duration`) replacing the mutable, not-thread-safe `Date`/`Calendar`*
- *Method references (`Class::method`)*
- *`CompletableFuture` for composable async*
- *Nashorn JS engine (later removed in Java 15)*

**Q9.** What shipped between Java 9 and Java 17 that most reshaped everyday code (not just JVM internals)?
*Concept tested: this is the "what changed even though I skipped straight to 17" question —*
- *`var` local-type inference (10)*
- *Switch **expressions** (`->` syntax, multi-label case, `yield`) (14)*
- *Text blocks (`"""`) (15)*
- *Records (16) — compact immutable data carriers with auto-generated constructor/accessors/`equals`/`hashCode`/`toString`*
- *Pattern matching for `instanceof` (16) — `if (obj instanceof String s)` binds `s` directly*
- *Sealed classes/interfaces finalized (17)*
- *Helpful NullPointerExceptions (14) — messages now say *which* variable was null*
- *Strong encapsulation of JDK internals by default (17, JEP 403) — `--illegal-access` escape hatches removed*

**Q10.** What's the single biggest Java 21 feature, and why does it matter more than most language-syntax changes?
*Concept tested: **virtual threads** (Project Loom, JEP 444) — lightweight threads managed by the JVM (not 1:1 OS threads), letting simple thread-per-request blocking code scale to millions of concurrent threads without the usual platform-thread memory/context-switch cost; it's a runtime/concurrency-model shift, not just syntax sugar, so it directly threatens (and complements) reactive frameworks like WebFlux for I/O-bound workloads. Also in 21: pattern matching for `switch` finalized, record patterns finalized (destructuring in `case`), sequenced collections (`SequencedCollection`/`SequencedMap` — `getFirst()`/`getLast()`/`reversed()` uniformly), generational ZGC, and string templates (preview).*

**Q11.** What did Java 25 (the current LTS as of late 2025) bring, and what's still preview vs. finalized?
*Concept tested: expect breadth, not memorized exactness —*
- *Flexible constructor bodies finalized — statements allowed before `super()`/`this()` under restrictions*
- *Module import declarations finalized (`import module java.base;`)*
- *Compact source files / instance `main` methods finalized — no `public static void main(String[] args)` boilerplate needed for simple/launch-single-file programs*
- *Scoped values finalized (structured, immutable alternative to `ThreadLocal` for virtual-thread-heavy code)*
- *Stream gatherers finalized (custom intermediate stream operations beyond the fixed built-in set)*
- *Ahead-of-time class loading/linking and command-line ergonomics — faster startup*
- *Primitive types in patterns/`instanceof`/`switch` — still preview*
- *Vector API — still incubating across many releases*
*The interview-safe framing: "virtual threads and structured/scoped concurrency primitives are still the center of gravity post-21; 25 is mostly about finishing and hardening that story (scoped values, AOT startup) plus reducing ceremony (compact source files, flexible constructors, module imports)."*

**Q12.** If asked "which Java version are you actually using in production, and why haven't you moved to the newest," what's a defensible answer?
*Concept tested: interviewers are checking pragmatism, not version-chasing — a reasonable answer cites LTS-only upgrade policy (8 → 11 → 17 → 21, skipping non-LTS releases), dependency/framework compatibility lag (Spring Boot version support matrix), and virtual threads specifically being a strong, concrete reason to prioritize a 21 migration for I/O-heavy services.*

---

## 3. Sealed Classes

**Q13.** What is a sealed class/interface, and what problem does it solve that `final` and package-private constructors don't?
*Concept tested: `sealed` restricts *which* classes may extend/implement a type via an explicit `permits` clause — unlike `final` (which allows zero subclasses), sealed allows a known, closed *set* of subclasses declared up front, giving you controlled extensibility instead of an all-or-nothing choice.*

**Q14.** Syntax check — what must every permitted subclass of a sealed class declare, and why?
*Concept tested: each direct subclass must itself be declared `final`, `sealed` (with its own further-restricted `permits`), or `non-sealed` (reopening it to unrestricted extension) — this is mandatory, not optional, so the type hierarchy's openness is explicit at every level rather than silently inherited.*
```java
public sealed interface Shape permits Circle, Square, Triangle {}
public final class Circle implements Shape { /* ... */ }
public final class Square implements Shape { /* ... */ }
public non-sealed class Triangle implements Shape { /* ... */ } // reopened — anyone can extend Triangle
```

**Q15.** Why do sealed classes pair so naturally with pattern matching for `switch`?
*Concept tested: because the compiler knows the *exhaustive* set of permitted subtypes, a `switch` over a sealed type's subtypes can be verified exhaustive at compile time with no `default` branch needed — add a new permitted subclass later and every non-exhaustive switch over it becomes a compile error, catching missed-case bugs immediately instead of at runtime.*
```java
static double area(Shape s) {
    return switch (s) {
        case Circle c -> Math.PI * c.radius() * c.radius();
        case Square sq -> sq.side() * sq.side();
        case Triangle t -> 0.5 * t.base() * t.height();
        // no default needed — compiler knows these are the only 3 possibilities
    };
}
```

**Q16.** How do sealed classes compare to a plain `enum` for modeling a fixed set of variants?
*Concept tested: `enum` constants are all the *same type* with the same fields — sealed classes let each permitted subtype carry *different* fields/behavior (e.g., `Circle` has a radius, `Square` has a side) while still being a closed, exhaustively-switchable set — effectively Java's answer to algebraic data types / tagged unions.*

**Q17.** Can a sealed interface be implemented by a `record`? What does combining sealed + records typically model?
*Concept tested: yes — records are implicitly `final`, so they satisfy the sealed hierarchy's closure requirement directly; `sealed interface Shape` with `record Circle(double radius) implements Shape {}` etc. is the idiomatic Java pattern for closed, immutable data variants, paired with record patterns (Java 21) for destructuring in `switch`.*

---

## 4. Serializable & Marker Interfaces

**Q18.** What is a "marker interface," and why does `Serializable` have zero methods?
*Concept tested: a marker interface carries no methods/fields — its sole purpose is to tag a class with metadata the JVM or a framework checks via `instanceof`/reflection at runtime (e.g., `ObjectOutputStream` checks `obj instanceof Serializable` before allowing serialization). It's a type-system-level flag, not a behavioral contract.*

**Q19.** Name the classic marker interfaces in the JDK and what each one signals.
*Concept tested:*
- *`Serializable` — object's state may be converted to/from a byte stream*
- *`Cloneable` — permits `Object.clone()` to do a field-for-field copy instead of throwing `CloneNotSupportedException`*
- *`Remote` (RMI) — object's methods may be invoked from a different JVM*
- *`RandomAccess` — signals a `List` supports fast O(1) indexed access (e.g., `ArrayList`), letting algorithms choose index-loop vs. iterator strategy*
- *`EventListener` — base marker for all listener interfaces in AWT/Swing*

**Q20.** Why is `Cloneable` widely considered a broken/badly-designed marker interface?
*Concept tested: `Cloneable` doesn't actually declare `clone()` — the method lives on `Object` as `protected`, so implementing `Cloneable` alone doesn't give you a public `clone()` method; you still must override `clone()` yourself and change its visibility, and forgetting to implement `Cloneable` while calling `super.clone()` throws `CloneNotSupportedException` at runtime, not compile time. Effective Java's well-known advice is to avoid `Cloneable`/`clone()` entirely and use a copy constructor or static factory instead.*

**Q21.** What is `serialVersionUID`, and what happens if you omit it?
*Concept tested: a `private static final long serialVersionUID` explicitly versions a `Serializable` class's serialized form — if omitted, the JVM computes one implicitly from the class's structure (fields, methods, etc.) at compile time, which is compiler/JVM-implementation-dependent; the danger is that a minor, compatible code change (e.g., adding a method) can silently change the computed UID, causing `InvalidClassException` when deserializing objects written by an older version of the class.*

**Q22.** What does the `transient` keyword do, and why would you mark a field transient in a `Serializable` class?
*Concept tested: `transient` excludes a field from the default serialization process — used for fields that are either not serializable themselves (e.g., a `Socket`, `Thread`, or a database `Connection` handle), derived/cacheable state that shouldn't be persisted, or sensitive data (passwords, keys) that shouldn't be written to a byte stream at all.*

**Q23.** How does `Externalizable` differ from `Serializable`, and when would you choose it?
*Concept tested: `Externalizable` extends `Serializable` but is *not* a marker interface — it declares `writeExternal()`/`readExternal()`, handing you full manual control over the byte format (versus the JVM's default reflection-based field serialization); chosen when you need custom, more compact, or format-stable serialization, at the cost of writing and maintaining that logic yourself, including a mandatory public no-arg constructor for the deserializing side to invoke.*

**Q24.** Why did marker interfaces fall out of favor for new APIs in favor of annotations (e.g., `@FunctionalInterface`, `@Deprecated`, or custom annotations checked via reflection)?
*Concept tested: annotations can carry parameters/metadata (`@Deprecated(since="9", forRemoval=true)`) where a marker interface can only ever be present-or-absent; annotations also don't consume a slot in Java's single-inheritance class hierarchy and can target things interfaces can't (fields, parameters, local variables) — marker interfaces persist mainly for legacy/JVM-checked cases (`Serializable`, `Cloneable`) where the check happens via `instanceof` in JVM-level code predating annotations (pre-Java 5).*

**Q25.** Is `@FunctionalInterface` a marker interface? Why or why not?
*Concept tested: no — it's an annotation, not an interface at all; it's a compile-time-only assertion "this interface has exactly one abstract method," enforced by the compiler (fails to compile if violated), whereas a marker interface is a real supertype checked at runtime via `instanceof`. Easy trap for candidates who conflate "marker" (tagging concept) with the specific mechanism (interface vs. annotation).*

---

## Quick-Review Cheat Sheet

- **`groupingBy(classifier, downstream)`** composes — downstream can be `averagingDouble`, `counting`, `mapping`, `maxBy`/`minBy`, or another `groupingBy` for multi-level grouping. Default map/bucket types are `HashMap`/`ArrayList`; override via the 3-arg `mapFactory` overload.
- **`toMap` throws on duplicate keys by default; `groupingBy` never does** — buckets absorb duplicates naturally.
- **`partitioningBy` always yields both `true`/`false` keys; `groupingBy` with a boolean classifier may omit one.**
- **Java 8** = lambdas, Streams, functional interfaces, default/static interface methods, `Optional`, `java.time`, method references.
- **Java 9→17** = `var`, switch expressions, text blocks, records, pattern matching for `instanceof`, sealed classes (17), strong JDK encapsulation (17).
- **Java 21** = virtual threads (the headline), pattern matching for `switch` + record patterns finalized, sequenced collections, generational ZGC.
- **Java 25** = flexible constructor bodies, module imports, compact source files/instance `main`, scoped values, stream gatherers finalized — mostly hardening the post-21 concurrency/ergonomics story.
- **Sealed classes** = closed, explicit `permits` set; every subclass must itself be `final`/`sealed`/`non-sealed`; pairs with exhaustive `switch` pattern matching (no `default` needed); often combined with `record` for algebraic-data-type-style modeling.
- **Marker interface** = zero-method interface used as a runtime `instanceof` tag (`Serializable`, `Cloneable`, `Remote`, `RandomAccess`). `Cloneable` is the textbook example of the pattern done badly — prefer copy constructors over `clone()`.
- **`serialVersionUID`** should always be declared explicitly — an implicit one is fragile to innocuous code changes. **`transient`** opts a field out of default serialization.
- **Annotations superseded marker interfaces** for new APIs because they carry parameters and don't cost a hierarchy slot — `@FunctionalInterface` is an annotation, not a marker interface, despite the naming similarity.


