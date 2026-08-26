# 🎯 Interview Quick — Question Bank

> [!info] How to use this note
> Questions collected from real interview rounds, grouped by theme. Each entry keeps the **question**, what the interviewer is actually testing, and the **follow-up chain** that usually comes after it. Answers are deliberately short — this is a revision/recall note, not a textbook.

## 📚 Index

| # | Section | Focus |
|---|---------|-------|
| A | [[#🔥 Section A — Production, Observability & Failure Handling\|Section A]] | Metrics, memory leaks, Kafka/Redis/DB failure, traffic spikes |
| B | [[#🗄️ Section B — Database Operations & Query Debugging\|Section B]] | Online DDL, query optimization, deadlocks, UNION, N+1 |
| C | [[#🔒 Section C — Locking, High Contention & Ledgers\|Section C]] | `FOR UPDATE`, hot-wallet TPS, sharded counters, double-entry |
| D | [[#☕ Section D — Round 1: Core Java, OOP & Concurrency\|Section D]] | Coding + language internals + JMM + Loom |
| E | [[#✈️ Section E — Round 2: System Design (Flight Booking)\|Section E]] | Dynamic pricing, Redis, double booking, scaling, async |
| F | [[#🛠️ Section F — Round 3: Software Development Practices\|Section F]] | Kafka, PII/PCI, Spring Security, Kubernetes, Istio |

---

# 🔥 Section A — Production, Observability & Failure Handling

## Q1 — Metrics & Monitoring in Your Project

> In your current project how do you check metrics? What all metrics do you monitor?

#### Possible Follow-ups (continued)

##### JVM Metrics

* Heap vs Stack?
* What is Young Gen / Old Gen?
* What is GC pause time?
* Which GC are you using?
* How do you identify memory pressure?
* What does heap utilization tell you?

##### Infrastructure Metrics

* CPU utilization
* Memory utilization
* Disk I/O
* Network I/O
* Container restarts
* Pod health
* Node health

##### Database Metrics

* DB connection pool utilization
* Query latency
* Slow queries
* Deadlocks
* Lock waits
* Active connections

##### Kafka Metrics

* Consumer lag
* Messages/sec
* Rebalance count
* Failed messages
* DLQ size
* Producer throughput

##### Redis Metrics

* Memory usage
* Eviction count
* Hit ratio
* Miss ratio
* Connected clients
* Latency

#### Technologies They May Ask

* Prometheus
* Grafana
* ELK
* Datadog
* New Relic
* CloudWatch

---

### Related Questions

#### Easy

* What is observability?
* Difference between logs and metrics?
* Difference between metrics and traces?

#### Medium

* How would you monitor a Spring Boot application?
* How do you detect latency issues?
* How do you create alerts?

#### Advanced

* How do you design observability for a payment system?
* How do you monitor microservices dependencies?

---

### DSA (sometimes asked indirectly)

Not directly DSA, but these are common production-oriented problems:

* Sliding Window Maximum (LC 239)
* Moving Average from Data Stream (LC 346)
* Design Hit Counter (LC 362)
* Design Circular Queue (LC 622)

---

## Q2 — Behaviour on Kafka / Redis / DB Failure

> How will your system behave in case of Kafka failure, Redis failure, DB failure, etc.?

---

### What Interviewer is Testing

This is a **resiliency/fault tolerance** question.

They want to know whether you think beyond happy path.

---

### Kafka Failure Follow-ups

#### Producer Side

* What if Kafka is down?
* What happens to producer requests?
* How many retries should be configured?
* What if retries also fail?

#### Consumer Side

* What if consumer crashes?
* What if consumer processes message but crashes before commit?
* What causes duplicate processing?
* How do you handle idempotency?

#### Broker Side

* What happens if leader broker dies?
* What is ISR?
* How is new leader selected?
* What if all replicas die?

#### Delivery Semantics

* At Most Once
* At Least Once
* Exactly Once

You were already asked these recently, so this is clearly a hot area.

---

### Redis Failure Follow-ups

#### Cache Failure

* What happens when Redis goes down?
* Does application stop working?
* Does traffic go to DB?

#### Cache Patterns

* Cache Aside
* Read Through
* Write Through
* Write Back

#### Cache Problems

* Cache Penetration
* Cache Avalanche
* Cache Stampede

#### Scaling

* Redis Replication
* Redis Sentinel
* Redis Cluster

---

### Database Failure Follow-ups

#### Availability

* Primary DB crashes?
* Read replica crashes?
* Connection pool exhausted?

#### Consistency

* What happens to in-flight transactions?
* How do you recover?

#### Performance

* Sudden increase in DB connections?
* Slow query causing outage?

#### Scaling

* Read replicas
* Sharding
* Partitioning

---

### Cross-System Follow-ups

#### Circuit Breaker

* What is circuit breaker?
* Why use Resilience4j?
* Open/Half-Open/Closed states?

#### Retry

* When should retry be used?
* Why can retries be dangerous?

#### Fallback

* What is graceful degradation?
* How do you return partial responses?

#### Bulkhead

* What is bulkhead pattern?

---

### Related LeetCode

Not direct, but interviewers often mix these concepts with design questions:

* Design Twitter (LC 355)
* LRU Cache (LC 146)
* LFU Cache (LC 460)
* Design Log Storage System (LC 635)
* Design Hit Counter (LC 362)

---

## Q3 — Identifying a Memory Leak

> How do you identify memory leakage?

---

### What Interviewer is Testing

* JVM internals
* Production debugging
* GC understanding

---

### Immediate Follow-ups

#### Symptoms

* How do you know memory leak exists?
* What metrics indicate memory leak?
* CPU increase or memory increase?
* How does application behave?

#### JVM

* Heap dump?
* Thread dump?
* GC logs?
* MAT tool?
* VisualVM?
* JProfiler?

#### Analysis

* Which objects are growing?
* Why aren't they being garbage collected?
* What is retained heap?

#### Common Causes

* Static collections
* Unclosed resources
* ThreadLocal leaks
* Infinite caches
* Listener leaks

#### Kubernetes

* Pod restart due to OOMKilled?
* Difference between memory leak and high memory usage?

---

### Related Questions

* What is OutOfMemoryError?
* Heap dump vs thread dump?
* Young GC vs Full GC?
* Why does Full GC become frequent?

---

### DSA Topics Often Connected

* LRU Cache (LC 146)
* LFU Cache (LC 460)
* Design In-Memory File System (LC 588)

Reason: memory management discussions often move into cache design.

---

## Q4 — Handling a Sudden Traffic Spike

> What about sudden spike?

---

### What Interviewer is Testing

* Scalability
* Capacity planning
* Traffic management

---

### Follow-ups

#### Detection

* How do you identify spike?
* Which metrics alert first?

#### Protection

* Rate Limiting
* Throttling
* Queueing
* Load Balancing

#### Scaling

* Horizontal scaling
* Vertical scaling
* Auto-scaling

#### Database

* How do you protect DB from spike?
* Read replicas?
* Caching?

#### Kafka

* Can Kafka absorb spikes?
* What happens when lag increases?

#### API Layer

* 10x traffic suddenly comes.
* What breaks first?

This exact question often becomes:

> Your TPS suddenly increased from 1k to 20k. What happens?

---

### Related System Design Questions

* Design URL Shortener
* Design Payment Gateway
* Design Notification System
* Design Rate Limiter

---

## Q5 — Kafka Partitions, Consumers & Rebalancing

> Kafka related questions about partition assignment, consumers and so on.

---

### Must Know Follow-ups

#### Partitioning

* Why partitions?
* How is partition selected?
* Key-based partitioning?
* Round robin partitioning?

#### Consumers

* One partition can be consumed by how many consumers?
* One consumer can consume how many partitions?
* What happens when consumers increase?

#### Consumer Groups

* Why consumer groups?
* How is load distributed?

#### Rebalancing

* What triggers rebalance?
* Why is rebalance expensive?
* Cooperative rebalance vs eager rebalance?

#### Offset Management

* Auto commit vs manual commit?
* Where are offsets stored?
* What happens if offset commit fails?

#### Ordering

* Is ordering guaranteed?
* Across partitions?
* Within partition?

#### Replication

* Leader replica
* Follower replica
* ISR
* Leader election

#### Reliability

* Producer acks=0,1,all
* Min ISR
* Idempotent producer
* Exactly-once semantics

---

### Related LeetCode (Closest Concepts)

These aren't Kafka questions directly, but they train the same thinking:

#### Queues / Streams

* Moving Average from Data Stream (LC 346)
* Design Hit Counter (LC 362)
* Sliding Window Maximum (LC 239)

#### Producer Consumer

* Print in Order (LC 1114)
* Building H2O (LC 1117)
* Bounded Blocking Queue (LC 1188)

---

## 🎯 Big Picture — What This Round Tested

This interviewer was primarily testing:

1. Observability
2. JVM Internals
3. Kafka Internals
4. Failure Handling
5. Scalability
6. Production Ownership

This is a very common **SDE-2 Backend Java interview pattern**. The next round from the same interviewer type would likely include:

* Circuit Breaker
* Retry strategies
* Idempotency
* Distributed transactions
* Kafka consumer lag debugging
* Database bottleneck debugging
* Cache stampede
* Connection pool tuning
* Thread pool tuning
* p95/p99 latency analysis
* GC tuning
* HLD of payment/notification/order systems

Those are the areas I'd prioritize after this question set.

---

# 🗄️ Section B — Database Operations & Query Debugging

> [!warning] Status
> Raw backlog from a production-debugging round — answer sketches below, still worth deepening.

## B1 — Detecting Memory Leakage in Production

> How do you detect memory leakage in a production system? What if it is a **large** system? What if it is **distributed and large**?

* Single node → heap dump + MAT, GC logs, retained heap growing across Full GCs.
* Large system → which node/service leaks? Per-pod memory trend, OOMKilled restart count.
* Distributed → correlate across services, continuous/sampling profilers (async-profiler, JFR, Pyroscope), leak in a shared library vs one service.
* Full follow-up chain in [[#Q3 — Identifying a Memory Leak|Q3]].

## B2 — Adding a Column + Backfill on a Multi-Million-Row Table

> You have to add a column and then update it on a very large table with millions of rows, without impacting the DB. How do different databases handle this?

* Add a **nullable column with no default** → metadata-only in MySQL 8 / PostgreSQL 11+.
* Backfill in **batches** (e.g. 10k rows, small sleep between batches), driven by PK ranges — never `OFFSET`.
* Watch replication lag and throttle the backfill on it.
* Tooling: `pt-online-schema-change`, `gh-ost` (MySQL); `CREATE INDEX CONCURRENTLY` (Postgres).
* Follow-ups: which locks are taken? What happens on replicas? Rollback plan?

## B3 — Dropping a Column on a Huge Table

> Same as B2, but when **deleting** a column.

* Expand–contract: stop reading → stop writing → drop.
* MySQL: `ALGORITHM=INPLACE` where supported; Postgres: `DROP COLUMN` is metadata-only but leaves dead space (`pg_repack` / `VACUUM FULL`).
* Risk: an older pod or an ORM still doing `SELECT *`.

## B4 — Renaming a Column on a Huge Table

> Same as B2, but when **renaming** a column.

* Never rename in place on a live system: **add new → dual-write → backfill → switch reads → drop old**.
* A direct rename breaks every in-flight deployment (old pods still reference the old name).

## B5 — Query Optimization: How Do You Identify the Problem?

> How will you do DB query optimization? How will you identify slow queries?

* Slow query log / `pg_stat_statements` / Performance Insights → rank by **total** time, not per-call time.
* `EXPLAIN ANALYZE` → seq scan vs index scan, estimated vs actual rows, join order, spills.
* Index design: selectivity, composite column order, covering index, index-only scan.
* Anti-patterns: function on an indexed column, implicit cast, leading-wildcard `LIKE`, `SELECT *`, long `OR` chains.
* Then: pagination strategy, N+1 (see [[#B7 — The N+1 Query Problem|B7]]), connection pool saturation.

## B6 — UNION and Related Set Operations

> What is `UNION` and related stuff?

* `UNION` (dedupes → sort/hash → costly) vs `UNION ALL` (no dedupe, fast — the default choice).
* `INTERSECT`, `EXCEPT` / `MINUS`.
* Rules: same column count, compatible types, `ORDER BY` only on the final result.
* Perf trick: splitting a non-sargable `OR` into two indexed queries joined by `UNION ALL` is often much faster.
* Follow-up: `UNION` vs `JOIN` — combining **rows** vs combining **columns**.

## B7 — The N+1 Query Problem

> What is the N+1 problem?

* 1 query for parents + N queries for each parent's children — usually lazy-loaded JPA associations.
* Detect: SQL statement count per request, Hibernate statistics, APM span count.
* Fix: `JOIN FETCH`, `@EntityGraph`, `@BatchSize`, DTO projections, or one extra `IN (...)` query.
* Trade-offs: `JOIN FETCH` + pagination → in-memory paging warning; multiple collection fetches → cartesian product.

## B8 — Detecting and Preventing Deadlocks in Production

> How will you detect a deadlock in a production system, and how do you prevent it?

* Detect: DB deadlock log (`SHOW ENGINE INNODB STATUS`, Postgres `deadlock detected`), a deadlock-rate metric + alert, thread dump for Java-level deadlocks.
* Prevent: **consistent lock ordering**, short transactions, lower isolation where safe, lock a sorted key set, retry on the deadlock error code with idempotency.
* Scenario version of this question: [[#C1 — Pessimistic Locking & Deadlock Redesign|C1]].

---

# 🔒 Section C — Locking, High Contention & Ledgers

> [!example] Domain
> Payments / wallet flavoured — the round where the interviewer pushes from "just take a lock" to "the lock **is** the bottleneck".

## C1 — Pessimistic Locking & Deadlock Redesign

> If Transaction A locks Account 1 then Account 2, and Transaction B locks Account 2 then Account 1 using `SELECT ... FOR UPDATE`, a deadlock occurs. How does the DB engine detect it, and how would you redesign the application logic to prevent deadlocks completely?

* Detection: wait-for graph + cycle detection → engine kills the cheaper victim (MySQL `1213`, Postgres `40P01`).
* Fix #1: **deterministic lock ordering** — always lock accounts sorted by ID.
* Fix #2: single atomic UPDATE instead of read-then-write.
* Fix #3: serialize per account (queue / Kafka partition key) so one worker owns the account.
* Follow-ups: lock wait timeout vs deadlock timeout; safe retry guarded by an idempotency key.

## C2 — `FOR UPDATE` vs `FOR SHARE` vs `SKIP LOCKED`

> What is the difference between `SELECT ... FOR UPDATE`, `SELECT ... FOR SHARE`, and `SELECT ... FOR UPDATE SKIP LOCKED`? When would you use `SKIP LOCKED` (e.g. job queues)?

* `FOR UPDATE` → exclusive row lock; other writers and lockers block.
* `FOR SHARE` → shared lock; readers coexist, writers block. Classic deadlock source when a shared lock is upgraded.
* `SKIP LOCKED` → skips already-locked rows instead of waiting → ideal for **pull-based job queues / transactional outbox**: N workers each grab a disjoint batch with near-zero contention.
* `NOWAIT` → fail fast instead of skipping.

## C3 — Flash Sale / Hot Wallet: 20k TPS on One Account

> Design a balance-deduction system for an enterprise merchant wallet receiving 20,000 TPS on a **single** account ID. Why will a single-row pessimistic or optimistic lock fail, and what architecture would you propose?

* Why locks fail: one row = one serialization point. Pessimistic → lock queue + timeouts; optimistic → CAS retries approach 100% failure under contention.
* Options:
  * **Sharded / bucketed counters** — split the balance into N sub-balances; each request hits one shard.
  * **Redis + Lua** atomic deduct in memory, **write-behind** to the DB ledger.
  * **Event streaming** — partition by account ID, one single-threaded consumer per partition (ordering, no locks).
* Trade-offs: exactness vs latency, recovery after cache loss, replay/idempotency on the stream.

## C4 — Atomic Deduction Across Sharded Balances

> If you shard a balance across 10 slots, how do you handle an atomic deduction when the requested amount exceeds any single slot's balance but is less than the total?

* Fast path: deduct from one slot. Slow path only for the rare large amount.
* Slow path options: rebalance/merge slots first; or reserve-then-commit across slots (saga) with compensation on partial failure; or escalate to a coordinator lock over all slots.
* Follow-up: how do you keep the total authoritative? A sweeper job that re-shards and reconciles slot balances.

## C5 — Why Append-Only Ledgers Instead of Mutable Balances

> Why do financial systems avoid mutable balance columns in favour of append-only ledgers? How do you guarantee zero drift between journal entries and point-in-time balance snapshots?

* A mutable balance loses history — no audit trail, unrecoverable from a bad write.
* Double-entry: every movement is a debit + a credit; the invariant is `SUM(entries) = 0`.
* Balance is **derived** (`SUM` of entries) or stored as a snapshot row carrying `last_entry_id`, so any snapshot is reproducible.
* Zero drift: snapshot + delta recomputation, plus a periodic job asserting `snapshot == SUM(entries up to that id)`.

## C6 — Reconciliation Between Write-Behind Cache and DB Ledger

> How do you implement reconciliation to detect anomalies between async write-behind caches (Redis) and the persistent DB ledger?

* Every cache mutation carries a monotonic sequence / txn id → the log is replayable.
* Periodic recon job compares cache balance vs `SUM(ledger)` per account and emits a drift metric.
* Failure classes: missing writes (replay from the stream), duplicate writes (idempotency key on ledger insert), out-of-order (sequence gap check).
* Alert on any non-zero drift; auto-heal only via an explicit adjustment entry, never a silent overwrite.

---

# ☕ Section D — Round 1: Core Java, OOP & Concurrency

> [!info] Round shape
> Two warm-up coding problems, then a deep dive into language semantics, OO design, and modern concurrency (JMM → Loom).

## D1 — Group Birds by Color 💻

> Given a list of `Bird` objects with properties `name` and `color`, group the birds by their colour.

**Core answer**

```java
Map<String, List<String>> byColor = birds.stream()
        .collect(Collectors.groupingBy(
                Bird::color,
                Collectors.mapping(Bird::name, Collectors.toList())));
```

**Follow-ups they push into**

* Do it without Streams (`computeIfAbsent` on a `HashMap`).
* Keep insertion order → `groupingBy(..., LinkedHashMap::new, toList())`.
* Count instead of collect → `Collectors.counting()`.
* Thread-safe / parallel → `groupingByConcurrent` + `ConcurrentHashMap`; why `parallelStream()` rarely helps here.
* Null colours → `groupingBy` throws NPE on a null key; handle with `Optional.ofNullable(...).orElse("UNKNOWN")`.
* Complexity: O(n) time, O(n) space.

## D2 — Valid Parentheses 💻

> Given a string containing `()`, `{}`, `[]`, determine whether the brackets are balanced and valid.

**Core answer** — stack; push openers, pop and match on closers, valid only if the stack ends empty.

```java
boolean isValid(String s) {
    Deque<Character> st = new ArrayDeque<>();
    Map<Character, Character> pair = Map.of(')', '(', ']', '[', '}', '{');
    for (char c : s.toCharArray()) {
        if (pair.containsKey(c)) {
            if (st.isEmpty() || st.pop() != pair.get(c)) return false;
        } else {
            st.push(c);
        }
    }
    return st.isEmpty();
}
```

**Follow-ups**

* Why `ArrayDeque` over `Stack` (legacy, synchronized, `Vector`-backed).
* O(n) time, O(n) space; worst case all openers.
* Variants: minimum insertions to balance (LC 921/1541), longest valid parentheses (LC 32), with wildcard `*` (LC 678).
* Related: [[#D1 — Group Birds by Color 💻|D1]] and this pair are the standard "can you still code?" screen.

## D3 — String Immutability and Thread Safety

> Explain how String immutability works in Java and how it contributes to thread safety.

* `String` holds a `private final byte[]` (since JDK 9, compact strings) never handed out; every "modification" returns a new instance.
* Immutable → no visible state transition → **safely shared between threads without synchronization**; safe publication guaranteed by final fields (JMM final-field freeze).
* Other benefits: string pool interning, cached `hashCode`, safe as a `HashMap` key, safe for class loading / file paths / security checks (no TOCTOU).
* Follow-ups: `String` vs `StringBuilder` vs `StringBuffer`; why `StringBuilder` is *not* thread safe; `intern()` and where the pool lives (heap since JDK 7); why passwords go in `char[]`, not `String`.

## D4 — Java Pass-by-Value Semantics

> Explain how parameter passing works in Java and why Java is strictly pass-by-value.

* Java **always** copies the argument: primitives copy the value, objects copy the **reference value** (the pointer), not the object.
* So mutating through the reference is visible to the caller; **reassigning** the parameter is not.
* Classic proof: a `swap(a, b)` method cannot swap the caller's variables.
* Follow-ups: why people call it "pass by reference" and why that's wrong; how this interacts with `final` parameters; effectively-final capture in lambdas; arrays as objects.

## D5 — Shallow Copy vs Deep Copy

> Differentiate shallow copy from deep copy in Java, explaining how object references are handled in each.

| | Shallow copy | Deep copy |
|---|---|---|
| Nested objects | **Shared** references | Recursively duplicated |
| Cost | Cheap | Expensive |
| Mutation of a nested field | Visible in both copies | Isolated |
| Typical source | `Object.clone()`, copy constructor copying fields as-is | Manual recursive copy, serialization round-trip, mapper libs |

* Immutable nested fields (`String`, boxed types, records of immutables) make a shallow copy effectively deep.
* Follow-ups: defensive copies in getters/constructors; `List.copyOf` / `Collections.unmodifiableList` (view vs copy); how records help.

## D6 — Usage and Mechanics of `Object.clone()`

> Explain the mechanics, pitfalls, and implementation requirements of `Object.clone()` and the `Cloneable` interface.

* `Cloneable` is a **marker** interface — it doesn't declare `clone()`; `Object.clone()` throws `CloneNotSupportedException` if the class doesn't implement it.
* Mechanics: `clone()` is a native, field-for-field (shallow) copy that **bypasses constructors**; override it public and call `super.clone()`, then deep-copy mutable fields.
* Pitfalls: `final` fields can't be reassigned after `super.clone()`; a superclass's `clone()` returns the wrong runtime type if written badly; interacts badly with inheritance and invariants.
* Effective Java: **prefer a copy constructor or static factory** (`new Foo(other)`) over `clone()`.
* Follow-ups: covariant return types in `clone()`; cloning arrays (`arr.clone()` is the idiomatic exception); serialization-based copies and their cost.

## D7 — SOLID Principles in Java

> Explain each SOLID principle and give examples of how they are applied in Java development.

| Principle | One-liner | Java example |
|---|---|---|
| **S** — Single Responsibility | One reason to change | Split `OrderService` doing pricing + persistence + email |
| **O** — Open/Closed | Extend without modifying | Strategy for `PaymentMethod`; add UPI without touching existing code |
| **L** — Liskov Substitution | Subtypes honour the supertype contract | `Square extends Rectangle` breaks it; `List` vs immutable list throwing on `add` |
| **I** — Interface Segregation | Many small interfaces > one fat one | Split a `Repository` doing read + write + batch |
| **D** — Dependency Inversion | Depend on abstractions | Constructor-inject a `PaymentGateway` interface (Spring DI) |

* Follow-ups: where SOLID conflicts with simplicity (over-abstraction); how Spring embodies DIP; SRP at class vs module level; LSP violations in real code.

## D8 — Java Reflection API

> What is the Reflection API, how is it used, and what are its pros, cons, and performance implications?

* Inspect/modify classes, fields, methods, annotations at runtime: `Class.forName`, `getDeclaredMethods`, `setAccessible(true)`, `Method.invoke`.
* Used by: Spring (DI, AOP proxies), Hibernate, Jackson, JUnit, mocking libraries.
* Cons: no compile-time safety, breaks refactoring, bypasses encapsulation, hostile to GraalVM native-image and to the module system (`--add-opens`, strong encapsulation since JDK 16/17).
* Performance: `Method.invoke` is far slower than a direct call (boxing, access checks, no inlining) — cache `Method`/`Field` objects; prefer `MethodHandles` / `LambdaMetafactory`, or annotation processing at compile time.
* Follow-ups: how does Spring create beans? Proxy types (JDK dynamic proxy vs CGLIB); can reflection break immutability of `String`? (Yes — which is why `setAccessible` is a security concern.)

## D9 — Java Exception Handling Improvements

> Discuss best practices and modern improvements in Java exception handling (try-with-resources, multi-catch, …).

* **try-with-resources** (7): auto-`close()` in reverse order, suppressed exceptions via `getSuppressed()`; effectively-final resources allowed since 9.
* **Multi-catch** (7): `catch (IOException | SQLException e)` — `e` is effectively final.
* **Precise rethrow** (7): compiler narrows the declared throws.
* **Helpful NullPointerExceptions** (14+): tells you which expression was null.
* Best practices: catch specific over `Exception`; never swallow; don't use exceptions for control flow; wrap with context, don't lose the cause; unchecked for programming errors, checked for recoverable; fail fast; log **or** rethrow, not both.
* Spring angle: `@ControllerAdvice` + `@ExceptionHandler`, `ProblemDetail` (RFC 7807), translating `DataAccessException`.
* Follow-ups: checked vs unchecked debate; exceptions in streams/lambdas; performance of `fillInStackTrace` and when to disable it.

## D10 — Java Memory Model and Concurrency

> Explain the Java Memory Model (JMM), happens-before relationships, memory visibility, and how `volatile` and `synchronized` work.

* JMM defines **when a write by one thread becomes visible to another** — not just locking, but reordering rules for compiler/CPU.
* **happens-before** edges: program order in a thread; unlock → subsequent lock of the same monitor; `volatile` write → subsequent read; `Thread.start()` → the thread's actions; thread's actions → `join()`; constructor's final-field writes → publication.
* `volatile` → visibility + ordering (no caching in registers, no reordering across it), **but not atomicity** (`count++` is still broken).
* `synchronized` → mutual exclusion **plus** the same visibility guarantees; reentrant; biased/thin/fat lock evolution.
* Consequences: double-checked locking needs `volatile`; safe publication; why `final` fields are safe without sync.
* Follow-ups: `AtomicInteger`/CAS and the ABA problem; `LongAdder` under contention; false sharing / `@Contended`; `ThreadLocal` and leaks.

## D11 — ExecutorService vs CompletableFuture vs Virtual Threads

> Compare `ExecutorService`, `CompletableFuture`, and Virtual Threads (Project Loom).

| | `ExecutorService` | `CompletableFuture` | Virtual Threads (JDK 21) |
|---|---|---|---|
| Model | Pool of platform threads + task queue | Async **composition** over some executor | Cheap JVM-scheduled threads (M:N onto carriers) |
| Style | Blocking, `Future.get()` | Non-blocking chaining (`thenApply`, `thenCompose`, `allOf`) | Blocking code that **scales** |
| Sweet spot | Bounded CPU-bound work | Fan-out/fan-in, pipelines, timeouts | High-concurrency **I/O**-bound work |
| Cost | ~1 MB stack per thread | Same threads, better orchestration | ~KBs; millions of threads feasible |

* Loom pins a carrier thread on `synchronized` blocks over I/O (improved in JDK 24) and on native calls → prefer `ReentrantLock`.
* Virtual threads should **not** be pooled — create one per task (`newVirtualThreadPerTaskExecutor`).
* Structured concurrency (`StructuredTaskScope`) as the successor to manual `CompletableFuture.allOf`.
* Follow-ups: which one for a 200-call fan-out? What breaks in `ThreadLocal`-heavy code? How do you limit concurrency without a pool (semaphore)?

## D12 — Connection Pooling vs Virtual Threads

> How do Virtual Threads change connection pooling and resource-management strategy in Java backend services?

* Old model: thread pool size ≈ the natural concurrency limit; the DB pool was rarely the first bottleneck.
* With virtual threads the thread pool no longer throttles anything → **the connection pool becomes the real limiter**, and thousands of threads can queue on `HikariPool.getConnection()`.
* Consequences: size Hikari by **DB capacity**, not by app threads; set connection timeouts aggressively; add semaphores/bulkheads per downstream; watch pool wait-time metrics.
* Still pool connections (a DB connection is an expensive OS/DB-side resource) — virtual threads remove the need to pool *threads*, not *connections*.
* Follow-ups: pinning caused by JDBC drivers using `synchronized`; `ThreadLocal`-based transaction context vs scoped values; back-pressure design.

## D13 — Local Variable Type Inference (`var`)

> Explain `var` for local variable type inference, its limitations and best practices.

* JDK 10; compile-time inference only — **not** dynamic typing, the variable still has a static type.
* Allowed: local variables with an initializer, for/for-each loop variables, try-with-resources, lambda parameters (`var` in `(var a, var b) ->`, JDK 11).
* **Not** allowed: fields, method parameters, return types, `var x = null`, without an initializer, array initializer shorthand (`var a = {1,2}`), or as a lambda/method-ref target.
* Gotchas: infers the concrete type (`var list = new ArrayList<String>()` → `ArrayList`, not `List`); infers `int` for numeric literals; can infer non-denotable types (anonymous class, intersection type).
* Best practice: use it when the RHS makes the type obvious; avoid it when it hides the type (`var result = service.process()`).
* Follow-ups: `var` vs `val`/Kotlin; interaction with diamond `<>`; readability arguments in code review.

---

# ✈️ Section E — Round 2: System Design (Flight Booking)

> [!example] Round shape
> One HLD anchor question, then four drill-downs that are really "can you handle contention, cache, scale, and async failure?"

## E1 — Design a Flight Booking System with Dynamic Pricing

> Design a Flight Booking System.

**Scope first:** search, seat hold, booking, payment, ticketing, cancellation/refund. Non-goals: loyalty, ancillaries.

**Core services**

* Search / Inventory service (read-heavy, cache-fronted)
* Pricing service (dynamic price = base fare × demand × seats-left × time-to-departure)
* Booking service (hold → confirm, owns the seat inventory)
* Payment service (external PSP, async callbacks)
* Ticketing / Notification (async consumers)

**Data model:** `flight`, `flight_inventory(flight_id, class, total, available, version)`, `seat_hold(id, flight_id, seat, expires_at)`, `booking`, `payment`, `ledger`.

**Key flows:** search (cache) → hold seat with TTL → payment → confirm booking → emit `BookingConfirmed` → ticket + notify. Hold expiry releases inventory.

**Follow-ups:** read/write ratio (search ≫ booking, ~1000:1), idempotent booking API, GDS/third-party inventory sync, pricing consistency between the quoted price and the charged price (quote token with expiry).

## E2 — Redis Caching, Distributed Counters and TTL

> How would you use Redis caching, distributed counters, and TTL to handle high-frequency search traffic and demand-based pricing?

* **Search cache:** key `search:{from}:{to}:{date}:{class}`, short TTL (30–60s), cache-aside; a stale price is fine because the final price is re-quoted at booking.
* **Demand counters:** `INCR search:count:{flight}:{window}` with TTL per window → searches-per-minute feeds the pricing multiplier. Sliding window with per-minute buckets.
* **Seat-left counter:** `DECR` in Redis for the fast path, DB as the source of truth (see [[#E3 — Preventing Double Booking and Managing Seat Inventory|E3]]).
* **Holds:** `SET hold:{flight}:{seat} {userId} NX EX 600` — Redis TTL *is* the hold expiry; NX gives atomic acquire.
* **Problems to name:** cache stampede (mutex/single-flight + jittered TTL), penetration (negative caching / bloom filter), avalanche (staggered TTLs), hot key (local caffeine L1 + Redis L2).
* Follow-ups: eviction policy (`allkeys-lru`), memory sizing, Redis Cluster hash tags to keep a flight's keys on one slot, why Lua for multi-key atomicity.

## E3 — Preventing Double Booking and Managing Seat Inventory

> How do you maintain DB consistency, prevent double booking, and manage seat inventory under high-concurrency booking?

* **Optimistic locking** (preferred for moderate contention): `UPDATE inventory SET available = available - 1, version = version + 1 WHERE flight_id = ? AND version = ? AND available > 0` — 0 rows updated → retry.
* **Pessimistic:** `SELECT ... FOR UPDATE` on the inventory row — simple, but serializes a hot flight (see [[#C3 — Flash Sale / Hot Wallet: 20k TPS on One Account|C3]] for why this breaks at high TPS).
* **Unique constraint** on `(flight_id, seat_no)` in `booking` as the last line of defence — the DB refuses the second insert no matter what the app does.
* **Two-phase hold:** Redis `SET NX EX` hold → payment → confirm inside a DB transaction; expired holds released by a sweeper (and by the TTL).
* **Idempotency:** client-supplied `Idempotency-Key` → unique index on it; a retried booking returns the original result.
* Follow-ups: isolation levels (RC vs RR, phantom reads on seat maps), overbooking policy as a deliberate business feature, distributed transaction across payment + booking → **saga with compensation**, not 2PC.

## E4 — Scalability, Load Balancing and Horizontal Scaling

> Why are load balancers needed, how is horizontal scaling achieved, and how are scalability and availability ensured?

* **LB purpose:** distribute traffic, health-check and eject bad instances, TLS termination, enable zero-downtime rolling deploys.
* Layers: L4 (TCP, fast) vs L7 (HTTP-aware routing, path/header based); algorithms — round robin, least connections, consistent hashing (sticky-ish without sessions).
* **Horizontal scaling** needs **stateless** app instances → session/state to Redis or JWT; sticky sessions are a smell.
* Scale the tiers separately: search (read replicas + cache) scales far beyond booking (write-bound).
* **Availability:** multi-AZ, N+1 capacity, health checks + readiness probes, HPA on CPU/RPS/lag, graceful shutdown draining.
* Data tier: read replicas, partitioning by route/date, sharding by `flight_id`.
* Follow-ups: what breaks first at 10×? (See [[#Q4 — Handling a Sudden Traffic Spike|Q4]].) CAP trade-off during a partition; global traffic via DNS/GeoLB/anycast.

## E5 — Asynchronous Processing and Event Failure Handling

> How do you handle asynchronous processing for payment and booking events, including failures and retries?

* **Transactional outbox**: write the booking + the event row in one DB transaction; a relay publishes to Kafka → no lost or phantom events (dual-write problem solved).
* Consumers: ticketing, email/SMS, analytics, loyalty — each an independent consumer group.
* **Retries:** bounded retry with exponential backoff + jitter; non-retryable errors go straight to DLQ; retry topics (`orders.retry.5m`, `retry.30m`) to avoid head-of-line blocking.
* **DLQ**: alert on depth, replay tooling, poison-message quarantine.
* **Idempotent consumers**: dedupe by `event_id` in a processed-events table — at-least-once delivery makes duplicates a certainty.
* **Payment specifics:** PSP webhook may arrive before/after your own confirmation; reconcile with a scheduled status poll; timeouts must never auto-fail a payment that actually succeeded → pending state + reconciliation.
* Follow-ups: exactly-once semantics and its real cost; ordering guarantees per partition key (`booking_id`); saga compensation when ticketing fails after payment succeeded.

---

# 🛠️ Section F — Round 3: Software Development Practices

## F1 — Kafka Producer/Consumer Architecture and Reliability

> Explain core Kafka concepts — producers, consumers, config (`acks`, `batch.size`, `linger.ms`) — and performance/reliability tuning.

* **Producer knobs**
  * `acks=0|1|all` — durability vs latency; `all` + `min.insync.replicas=2` is the safe pairing.
  * `batch.size` (bytes per partition batch) + `linger.ms` (wait to fill it) → throughput vs latency knob.
  * `compression.type` (lz4/zstd) — compresses the batch, big win with batching.
  * `enable.idempotence=true`, `max.in.flight.requests=5` → no duplicates, order preserved on retry.
  * `retries`, `delivery.timeout.ms`, `buffer.memory`, `max.block.ms`.
* **Consumer knobs:** `max.poll.records`, `max.poll.interval.ms` (slow processing → rebalance storm), `fetch.min.bytes`, `enable.auto.commit=false` + manual commit after processing.
* **Reliability:** replication factor 3, ISR, leader election, at-least-once by default, transactions for exactly-once.
* Deep follow-up chain already captured in [[#Q5 — Kafka Partitions, Consumers & Rebalancing|Q5]].

## F2 — PII/PCI Protection and Compliance in Event-Driven Systems

> How do you ensure PII/PCI compliance and protect sensitive information before publishing events?

* **Don't publish what you don't need** — events carry IDs and references, not raw PAN/Aadhaar/CVV. (CVV must never be stored at all.)
* **Tokenization / vaulting:** replace the PAN with a token; only the vault (PCI-scoped) can detokenize. Keeps the rest of the estate out of PCI scope.
* **Masking** for display/logs (`4111 **** **** 1111`), **field-level encryption** (envelope encryption with a KMS DEK/KEK) for anything that must travel.
* **In transit / at rest:** TLS everywhere, encrypted Kafka volumes, ACLs per topic, separate topics + stricter retention for sensitive events.
* **Governance:** schema registry with a PII annotation on fields, log scrubbers, data-retention/right-to-erasure (crypto-shredding: delete the key, not the records), audit trail of who read what.
* Follow-ups: how do you erase data from an immutable log? (Crypto-shredding / compacted topic with tombstones.) How do you test compliance? Who reviews the schema?

## F3 — Spring Security Architecture and Custom Filtering

> Explain how JWT authentication is implemented in Spring Boot using `SecurityFilterChain`.

* **Architecture:** `DelegatingFilterProxy` → `FilterChainProxy` → the matched `SecurityFilterChain` → an ordered filter list; `SecurityContextHolder` (ThreadLocal) carries the `Authentication`.
* **JWT flow:** login endpoint authenticates via `AuthenticationManager` → issues a signed JWT → each subsequent request hits a custom `OncePerRequestFilter` that parses/validates the token, builds an `Authentication`, and sets it on the context.
* Registration: `http.addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class)`, `sessionManagement(STATELESS)`, `csrf.disable()` for token APIs, `authorizeHttpRequests` rules.
* Modern config: `@Bean SecurityFilterChain` (the `WebSecurityConfigurerAdapter` era is over); or use `oauth2ResourceServer().jwt()` with a JWKS endpoint instead of a hand-rolled filter.
* **Authorization:** `@PreAuthorize`, method security, roles vs authorities, `AccessDeniedHandler`, `AuthenticationEntryPoint`.
* Follow-ups: access vs refresh tokens; how do you revoke a stateless JWT? (Short TTL + a denylist / token version claim.) Where do you store it on the client? Symmetric (HS256) vs asymmetric (RS256) and key rotation.

## F4 — Kubernetes Architecture, Pod Lifecycles and Scaling

> Explain the relationship between Deployments, ReplicaSets and Pods.

* **Deployment** declares the desired state and manages rollouts → creates a **ReplicaSet** per pod-template revision → the ReplicaSet keeps N **Pods** running. Rollout = new RS scaled up while the old RS scales down; rollback = scale the previous RS back.
* Pod lifecycle: `Pending → Running → Succeeded/Failed`; `restartPolicy`; init containers; `CrashLoopBackOff`, `ImagePullBackOff`, `OOMKilled`.
* Probes: **liveness** (restart me), **readiness** (send me traffic), **startup** (give me time to boot) — mixing these up causes restart loops during a slow start.
* Resources: `requests` (scheduling) vs `limits` (throttle/kill); CPU throttling vs memory OOMKill.
* Scaling: HPA (CPU/memory/custom metrics like Kafka lag via KEDA), VPA, Cluster Autoscaler; `PodDisruptionBudget` to survive node drains.
* Follow-ups: rolling update `maxSurge`/`maxUnavailable`; graceful shutdown (`preStop` + `terminationGracePeriodSeconds` + draining in-flight requests); StatefulSet vs Deployment.

## F5 — Canary Deployments with Istio

> How do you implement a canary deployment running v1 and v2 simultaneously?

* Two Deployments with the same app label and different `version` labels (`v1`, `v2`); one Service selects both.
* **DestinationRule** defines subsets `v1`/`v2` from those labels; **VirtualService** splits weights: 95/5 → 80/20 → 50/50 → 100.
* Header/user-based routing for internal dogfooding before any percentage traffic.
* Guardrails: watch p99 latency + error rate per subset (Prometheus/Kiali), automated promotion/rollback via Flagger/Argo Rollouts, instant rollback = set weight back to 0.
* Istio extras that make it real: mTLS between subsets, retries/timeouts, circuit breaking (`outlierDetection`), fault injection to test the canary.
* Follow-ups: canary vs blue-green vs feature flags; how do you canary a **schema** change? (Backwards-compatible DB first — expand/contract, see [[#B4 — Renaming a Column on a Huge Table|B4]].) Sticky sessions during a split.
