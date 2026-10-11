`@Transactional` looks like one annotation. Underneath it's a **proxy**, a **`ThreadLocal`**, and a **commit sequence** — and every production incident involving it traces back to one of those three things breaking.

> [!info] Where this fits
> This note is the **internals-and-incidents** companion. The rules you configure — propagation, isolation, rollback, `readOnly` — already have a full treatment in [[10. Transactions]]; don't relearn them here.
>
> - **What the annotation configures** (propagation table, isolation table, rollback rules, `readOnly`, self-invocation) → [[10. Transactions]]
> - **Flush vs commit, the action queue, `save()` family** → [[8. Dirty Checking and Flush]]
> - **Isolation anomalies and lock types in depth** → [[9. Database Concurrency]]
> - **What a rollback can't undo, outbox, idempotency, in-doubt commits** → [[11. Transaction Boundaries]]
> - **Why an `@Async`/thread-pool call loses the transaction** → [[4. Executors and Thread Pools]]
>
> This note is *how the proxy actually does it*, and *what happens when the mechanism meets an unreliable network* — the two things a payments-backend interview digs into once you've recited the propagation table correctly.

> [!info] The through-line of this note
> One machine, three failure surfaces.
>
> 1. At startup, Spring wraps your bean in a **proxy** (§1) whose `invoke()` is a plain try/commit/rollback block (§2) — nothing magic, just placed for you.
> 2. That proxy's only real trick is **binding a connection to the current thread** via `ThreadLocal` (§3), so every repository call in the method reuses it. Everything downstream — `REQUIRES_NEW` suspending it (§5), async work never seeing it (§6) — is a consequence of that one `ThreadLocal`.
> 3. Commit is not one step: it's **flush, then `connection.commit()`** (§4) — two network round trips, two places for the world to intervene, which is exactly where §7 and §8's production incidents live.
>
> One line to anchor everything: **the proxy binds a connection to a thread and commits it in two steps — every bug in this note is something happening between those steps that the proxy can't see.**

---

## Short Notes

---

### 1. Proxy Creation at Startup

- `@EnableTransactionManagement` (auto-enabled by Spring Boot the moment a `PlatformTransactionManager` bean exists) registers a `BeanPostProcessor` — `InfrastructureAdvisorAutoProxyCreator`
- During bean initialization it scans every bean for `@Transactional` methods/classes and, if found, **wraps it in a proxy** — CGLIB subclass proxy by default, or a JDK dynamic proxy if the bean only exposes an interface
- ⭐ **The bean you `@Autowired` is not your class.** It's a proxy holding a reference to your class

---

### 2. The Interceptor Chain

Calling a `@Transactional` method actually calls the proxy, which routes through `TransactionInterceptor` — an `Advice`, the same mechanism as `@Around`:

```java
public Object invoke(MethodInvocation invocation) {
    TransactionAttribute txAttr = getTransactionAttribute(invocation.getMethod());
    PlatformTransactionManager tm = determineTransactionManager(txAttr);

    TransactionStatus status = tm.getTransaction(txAttr);   // begin/join
    Object result;
    try {
        result = invocation.proceed();                       // your actual method
    } catch (Exception ex) {
        tm.rollback(status);                                  // if it matches the rollback rule
        throw ex;
    }
    tm.commit(status);
    return result;
}
```

- This is exactly the `@Around`-advice pattern — `invocation.proceed()` is the join point
- ⚠️ **Only calls that pass through this proxy ever reach this method.** Self-invocation (`this.method()`) skips it entirely → [[10. Transactions]] §9

---

### 3. Thread-Bound Connection — `TransactionSynchronizationManager` ⭐

`tm.getTransaction(txAttr)` does, in order:

1. Checks whether a transaction is already active on the current thread (this is what propagation reads)
2. If not, obtains a `Connection` from the `DataSource`
3. `connection.setAutoCommit(false)`
4. Applies the isolation level if one was specified
5. **Binds the connection to the current thread** — a `ThreadLocal<Map<DataSource, ConnectionHolder>>` inside `TransactionSynchronizationManager`

```text
ThreadLocal<Map<DataSource, ConnectionHolder>>
        │
        └── current thread → { myDataSource → ConnectionHolder(connection) }
```

- This is the entire mechanism behind "multiple repository calls in one `@Transactional` method share one DB transaction." Every `JpaRepository`/`JdbcTemplate` call on that thread checks this map **first**, before ever asking the pool for a connection
- It also means the guarantee is **per-thread**, not per-method-call — which is exactly what makes §5 and §6 true

---

### 4. Commit Sequence — Flush, Then Commit

When your method returns normally, `tm.commit(status)` does two separate things, in order:

```text
1. entityManager.flush()   ← Hibernate sends ALL pending SQL over the JDBC connection
2. connection.commit()    ← the actual DB commit — THIS is what makes it durable
3. connection released back to pool, ThreadLocal cleared
```

- ⭐ `save()` inside a `@Transactional` method only **queues** the entity. The `INSERT`/`UPDATE` is sent during the flush that happens automatically right before commit — not when you called `save()`. Full mechanics of that queue → [[8. Dirty Checking and Flush]]
- This two-step shape is why §7 and §8 below are two genuinely different failure scenarios, not one — the connection can die **during step 1** or **between step 2 and its acknowledgment**

---

### 5. `REQUIRES_NEW` Under the Hood

- Implemented by **suspending** the current thread's `ConnectionHolder` (not releasing it), obtaining a fresh connection, running independently, then **restoring** the suspended one when the inner transaction finishes
- This is why it holds two pool connections at once → [[10. Transactions]] §5, [[18. Production Problems]]

---

### 6. Async Work Loses the Bound Connection ⭐

- The binding in §3 is **per-thread**. `@Async`, a manually spawned thread, or a Kafka consumer callback launched from inside a `@Transactional` method runs on a **different** thread and simply does not see the `ConnectionHolder`
- It silently opens its own connection (own transaction) — or fails outright, depending on config. Either way, it is **not** part of your transaction
- Same root cause as self-invocation (§2): a Spring mechanism keyed on *how the call arrives* stops working the moment the call arrives differently. Full treatment of thread-pool/`@Async` behaviour → [[4. Executors and Thread Pools]]

---

### 7. Production Incident: Connection Dies Mid-Flush

Flush (§4 step 1) is `PreparedStatement.executeUpdate()` calls over the connection. If the connection dies here:

1. The JDBC driver throws (`SQLTransientConnectionException`, MySQL's `CommunicationsException`, `PSQLException`, …)
2. Hibernate wraps it as `JDBCException` → Spring's exception-translation layer turns it into `DataAccessResourceFailureException` / `JpaSystemException` — **unchecked**, so it propagates straight out of `invocation.proceed()`
3. `TransactionInterceptor` calls `tm.rollback(status)` — which may itself throw or no-op, because the connection is already dead
4. ⭐ **That doesn't matter.** No `COMMIT` was ever sent, so the database itself detects the dropped connection and rolls back the open transaction server-side (InnoDB and Postgres both do this) — you get all-or-nothing with no cooperation from your rollback call
5. HikariCP's validation check marks the physical connection broken and discards it
6. The caller sees a `TransactionSystemException` — the operation looks like it failed completely, and from the DB's point of view, it did

**No partial writes reach durable storage.** This is the clean failure case.

---

### 8. Production Incident: The In-Doubt Commit ⭐

The dangerous case is the connection dying **after** `COMMIT` is sent but **before the acknowledgment is received** (§4, between step 2 and step 3):

```text
driver sends COMMIT  →  DB commits it (durable, on the DB side)
                     →  ack packet lost (network blip / connection reset)
your JVM sees a SQLException/timeout, with NO WAY to know if the commit landed
```

- Spring treats this like any other failure and logs an exception — the transaction *looks* failed from the application's side. **But the data is actually committed.**
- This is an **in-doubt transaction** — a fundamental limit of any client/server protocol over an unreliable network, not a bug you can fix locally. It's the same failure class 2PC/XA never actually escapes → [[11. Transaction Boundaries]] §10
- ⭐ It's precisely why a payments system can't trust a local exception as ground truth: a status-check API, reconciliation cycle, or idempotency key at the boundary is what resolves the ambiguity, not a smarter try/catch → [[11. Transaction Boundaries]] §9–§11
- Naive "retry on any exception" here is how double-debits happen — the first attempt may have already committed

---

### 9. `saveAndFlush()` Visibility Across Threads

`saveAndFlush()` sends the `UPDATE` immediately, but flush ≠ commit ([[8. Dirty Checking and Flush]] §3):

- The DB takes an **exclusive row lock** and writes the new version, keeping the **old version** visible via MVCC (Postgres row versions, InnoDB's undo log)
- A second thread on a different connection querying that row: `READ_COMMITTED` and `REPEATABLE_READ` both see the **old value** — only `READ_UNCOMMITTED` would see the flushed-but-uncommitted one. Full anomaly table → [[9. Database Concurrency]]
- ⚠️ If the second thread instead **writes** to that row, it **blocks** on the row lock held since flush, until the first transaction commits or rolls back — a common latency spike on a hot row (e.g. a merchant balance under concurrent debits)

---

### SDE-2 Interview Priority

**Must Know**: the bean you inject is a proxy, `TransactionInterceptor` is a try/commit/rollback wrapper, the connection is bound to the **thread** via `TransactionSynchronizationManager`'s `ThreadLocal`, commit = flush then `connection.commit()`, async work runs on a different thread and never sees the bound connection, connection loss mid-flush is a clean failure (server-side rollback), the **in-doubt commit** (ack lost after a landed commit) and why it needs an idempotency key / status check, not a retry

**Nice To Know**: `InfrastructureAdvisorAutoProxyCreator`, `REQUIRES_NEW` suspending/restoring the `ConnectionHolder`, `saveAndFlush()` taking a row lock visible to writers but not readers on other connections, HikariCP discarding a broken physical connection

**Advanced**: exception-translation chain (`JDBCException` → `DataAccessResourceFailureException`/`JpaSystemException`), why 2PC doesn't actually remove the in-doubt window, the general shape of "detect vs. resolve" ambiguity in any commit protocol over a network

---
---

# Detailed Explanation

---

## Proxy Creation at Startup

When Spring sees `@EnableTransactionManagement` — auto-enabled by Spring Boot the instant a `PlatformTransactionManager` bean exists on the classpath/context — it registers a `BeanPostProcessor` called `InfrastructureAdvisorAutoProxyCreator`. During bean initialization this checks every bean for `@Transactional` methods or classes, and if it finds one, wraps the bean in a proxy: a CGLIB subclass proxy by default, or a JDK dynamic proxy if the bean only implements an interface.

The practical consequence is easy to miss: **the object you `@Autowired` into a controller is not your `SettlementService` — it's a generated subclass wrapping it.** Every other behaviour in this note follows from that one substitution.

---

## The Interceptor Chain

A call to a `@Transactional` method goes to the proxy first, which invokes `TransactionInterceptor` — the same `Advice` mechanism as `@Around` in Spring AOP. Its `invoke()` does, roughly:

```java
public Object invoke(MethodInvocation invocation) {
    TransactionAttribute txAttr = getTransactionAttribute(invocation.getMethod());
    PlatformTransactionManager tm = determineTransactionManager(txAttr);

    TransactionStatus status = tm.getTransaction(txAttr);   // begin/join tx
    Object result;
    try {
        result = invocation.proceed();                       // call your actual method
    } catch (Exception ex) {
        tm.rollback(status);                                  // if it's a matching exception
        throw ex;
    }
    tm.commit(status);
    return result;
}
```

There's nothing exotic here — it's the same try/commit/rollback block you'd write by hand around raw JDBC, generated for you and placed at the method boundary. `invocation.proceed()` is the join point: everything your method body does happens between `getTransaction()` and `commit()`.

The one thing worth internalising precisely: this method only runs when the call arrives **through the proxy**. `this.someTransactionalMethod()` from inside the same bean calls the real object directly — `TransactionInterceptor.invoke()` never executes, no transaction begins, and there's no exception to tell you so → [[10. Transactions]] §9.

---

## Thread-Bound Connection — `TransactionSynchronizationManager`

`tm.getTransaction(txAttr)` is where the real mechanism lives:

1. Checks whether a transaction is already active on the current thread — this check is what propagation (`REQUIRED` join vs. start new, etc.) actually reads.
2. If not, obtains a `Connection` from the `DataSource`.
3. Sets `connection.setAutoCommit(false)`.
4. Applies the isolation level, if one was specified on the annotation.
5. **Binds the connection to the current thread** via `TransactionSynchronizationManager`, backed by a `ThreadLocal<Map<DataSource, ConnectionHolder>>`.

```text
Thread "http-nio-8080-exec-3"
        │
        ▼
ThreadLocal map:  { myDataSource → ConnectionHolder(connection#42) }
        │
        ▼
walletRepo.findById(...)   → checks this map first → reuses connection#42
ledgerRepo.save(...)       → checks this map first → reuses connection#42
```

This is the entire answer to "how do multiple repository calls inside one `@Transactional` method participate in a single database transaction": they never ask the connection pool at all. They ask the `ThreadLocal` first, find an entry, and reuse it. The pool is only consulted once, at the top, by the proxy itself.

Stated as a rule, because everything else in this note is a corollary of it: **the transaction lives on the thread, not on the method call.** Anything that changes threads mid-flight — a suspended transaction, a spawned async task — leaves that binding behind.

---

## Commit Sequence — Flush, Then Commit

`tm.commit(status)`, when your method returns without a rollback-triggering exception, is not a single atomic step:

```text
1. invocation.proceed() returns successfully
2. tm.commit(status) is called
3. Spring's JpaTransactionManager calls entityManager.flush()
      ← Hibernate sends ALL pending SQL to the DB over the bound connection
4. Then calls connection.commit()
      ← the actual JDBC/DB commit — this is what makes it durable
5. Connection released back to pool, ThreadLocal cleared
```

Concretely: calling `save()` inside a `@Transactional` method only registers the entity as managed and queues an `INSERT`/`UPDATE` in Hibernate's action queue. Nothing reaches the database at that point. The SQL is sent during the flush that happens automatically as step 3 of commit — the full mechanics of *when* Hibernate decides to flush, and in what order, live in [[8. Dirty Checking and Flush]]; this note only needs the fact that flush and commit are two separate network-facing steps.

That separation is the reason the two production incidents below (§7, §8) are genuinely different failure modes rather than one: a connection can die *during* step 3, or it can die *between* steps 4 and the client receiving confirmation of it. Same commit call, two different windows, two different consequences.

---

## `REQUIRES_NEW` Under the Hood

`REQUIRES_NEW` is implemented directly in terms of the `ThreadLocal` from the previous section: the current thread's `ConnectionHolder` is **suspended** (kept, not discarded), a fresh connection is obtained and bound in its place, the inner method runs and commits/rolls back independently, and then the original `ConnectionHolder` is **restored** as the thread's active binding.

That's why it holds two pool connections simultaneously for the duration of the inner call — the outer one isn't released, only set aside. The consequences (pool exhaustion under a loop, self-deadlock on a row the outer transaction already holds) are covered in [[10. Transactions]] §5 and [[18. Production Problems]]; the mechanism above is *why* those consequences exist.

---

## Async Work Loses the Bound Connection

Because the binding is keyed on the **current thread**, any work that hops threads from inside a `@Transactional` method — `@Async`, a manually created `Thread`, a `CompletableFuture.supplyAsync`, a Kafka consumer callback fired from a listener — runs on a thread whose `ThreadLocal` map has no entry for your `DataSource`. It doesn't inherit your transaction; it doesn't even know one exists.

What actually happens next depends on configuration, but neither outcome is "it joins your transaction": it either silently opens its own connection and its own (uncoordinated) transaction, or the call fails if a transaction was mandated. Either way, work you assumed was covered by your `@Transactional` boundary is not, and if the outer method later rolls back, the async side effect already happened and stays happened.

This is the identical failure shape as self-invocation in §2 — a Spring mechanism that depends on *how* a call arrives stops working the instant the call arrives some other way — just triggered by a thread hop instead of a direct method call. The async/thread-pool specifics (executor decorators, `TaskDecorator`, MDC propagation alongside it) are covered in [[4. Executors and Thread Pools]].

---

## Production Incident: Connection Dies Mid-Flush

Recall flush (§4, step 3) is Hibernate calling `PreparedStatement.executeUpdate()` for every queued statement, over the bound connection. If the connection dies during that call:

1. The JDBC driver throws a `SQLException` — `SQLTransientConnectionException`, MySQL's `CommunicationsException`, Postgres's `PSQLException`, depending on the driver.
2. Hibernate wraps it as a `JDBCException`; Spring's exception-translation layer converts that into `DataAccessResourceFailureException` or `JpaSystemException`. Both are **unchecked**, so they propagate straight out of `invocation.proceed()` inside `TransactionInterceptor.invoke()`.
3. The interceptor's catch block calls `tm.rollback(status)` — which may itself throw, or silently do nothing, because the connection is already unusable.
4. **That failure doesn't matter.** No `COMMIT` packet was ever sent. The database server itself notices the dropped connection and rolls back whatever was open on its side — both MySQL InnoDB and PostgreSQL do this unconditionally. You get all-or-nothing behaviour even though your own rollback call never actually succeeded.
5. HikariCP's connection validation marks that physical connection as broken and evicts it, handing the next borrower a fresh one.
6. The original caller sees a `TransactionSystemException` bubble up. The operation looks like it completely failed — and from the database's point of view, it did.

The important takeaway: **this is the clean case.** No partial writes ever reach durable storage, and the failure the caller sees matches reality.

---

## Production Incident: The In-Doubt Commit

The dangerous case is the connection dying in the *other* commit window — between `connection.commit()` being sent (§4, step 4) and its acknowledgment arriving back at the client:

1. The driver sends the `COMMIT` packet.
2. The database actually commits — the write is durable on the DB side.
3. The acknowledgment packet back to the client is lost — a network blip, a connection reset at exactly that moment.
4. Your JVM sees a timeout or `SQLException` and has **no way to locally distinguish** "the commit never reached the server" from "the commit landed and only the ack was lost."
5. Spring treats it like any other exception: logs it, the transaction *looks* failed from the caller's side.
6. **The data is, in fact, committed.**

This is called an **in-doubt transaction**, and it is not a bug to be fixed with better exception handling — it's a structural limit of any client/server commit protocol running over a network that can drop packets. It's the same window 2PC/XA coordinators get stuck in when a participant is "prepared" and the coordinator disappears → [[11. Transaction Boundaries]] §10.

This is exactly why NPCI/UPI-style payment systems never rely on the caller's local exception as ground truth. If a caller (an acquirer bank, or your own service on the other end of a PSP call) doesn't get a clean synchronous success, it does not assume failure and blindly retry — it calls a **status-check API**, or waits for a **reconciliation** file, because the underlying write might already have gone through even though the client-side call errored. The resolution lives entirely at the boundary — idempotency keys, conditional updates, reconciliation — not in a smarter try/catch around the commit call → [[11. Transaction Boundaries]] §9–§11 walks the full payment-flow shape this produces. Naive "retry on any exception" in this ambiguous case is precisely how double-debits happen.

---

## `saveAndFlush()` Visibility Across Threads

`saveAndFlush()` forces the `UPDATE` to be sent immediately, but flush is still not commit ([[8. Dirty Checking and Flush]] §3): the transaction stays open and rollback is still possible.

Mechanically, for an `UPDATE`, the database engine takes an **exclusive row lock** and writes the new row version while keeping the old version available through MVCC — Postgres via row versions plus the visibility map, MySQL InnoDB via the undo log. A second thread on a *different* connection reading that row:

- Under **`READ_COMMITTED`** (Postgres/Oracle default) — takes a fresh snapshot per query, sees only what was committed before that query started → sees the **old** value.
- Under **`REPEATABLE_READ`** (MySQL InnoDB default) — snapshot taken at transaction start, held for its duration → also sees the **old** value.
- Only under **`READ_UNCOMMITTED`** would it perform a dirty read and see the flushed-but-uncommitted value — a level essentially nobody runs in production.

So in virtually every realistic setup, flush is invisible to other transactions' reads; only `COMMIT` makes the new row version visible to new snapshots. Full anomaly-by-anomaly detail is in [[9. Database Concurrency]].

One detail that does show up under load: if that second thread instead tries to **write** to the same row while the first transaction is still open, it doesn't error and it doesn't see a stale value — it **blocks**, waiting on the row lock held since flush, until the first transaction commits or rolls back. On a hot row (a merchant's running balance updated by many concurrent transactions) this is a common source of latency spikes and lock contention, independent of anything going wrong logically.

---

## ❓ Interview Questions

### Q1. What is the object you `@Autowired` when a bean has `@Transactional` methods?

A generated proxy (CGLIB subclass, or a JDK dynamic proxy for an interface-typed bean) wrapping your actual object, created by `InfrastructureAdvisorAutoProxyCreator` at startup — not your class directly.

### Q2. How do multiple repository calls inside one `@Transactional` method end up in the same database transaction?

The proxy binds the connection to the current thread via `TransactionSynchronizationManager`'s `ThreadLocal<Map<DataSource, ConnectionHolder>>`. Every repository call checks that map first and reuses the bound connection instead of asking the pool.

### Q3. Is commit one step or two?

Two: `entityManager.flush()` sends all pending SQL over the bound connection, then `connection.commit()` makes it durable. `save()` alone only queues the SQL; it's sent at the flush that happens right before commit.

### Q4. Why doesn't a Kafka consumer callback launched from inside a `@Transactional` method participate in that transaction?

It runs on a different thread, and the connection binding is a `ThreadLocal` keyed to the thread that started the transaction. The callback's thread has no entry in that map, so it either opens its own uncoordinated connection or fails — it never joins the caller's transaction.

### Q5. A connection drops while Hibernate is flushing. What state is the data in?

Clean failure. No `COMMIT` was sent, so the database itself rolls back whatever was open on its side (InnoDB and Postgres both do this on connection loss), regardless of whether Spring's own `rollback()` call succeeds. No partial writes are ever durable.

### Q6. A connection drops right after `COMMIT` is sent, and the client sees an exception. Did the write happen?

Unknown from the client's side — this is an in-doubt transaction. The commit may have landed on the DB before the ack was lost. The application cannot resolve this locally; it needs an idempotency key or a status-check/reconciliation mechanism at the boundary, because blindly retrying risks double-applying an already-committed write.

### Q7. If a transaction calls `saveAndFlush()` but hasn't committed, does another thread reading that row see the new value?

No, under the isolation levels almost everyone runs (`READ_COMMITTED`, `REPEATABLE_READ`). The row lock and the new version exist, but MVCC keeps the old version visible to other transactions' reads until commit. Only `READ_UNCOMMITTED` would show the flushed-but-uncommitted value.

### Q8. What happens if a second transaction tries to *write* to a row that's been flushed but not committed by the first?

It blocks on the row lock held since flush, until the first transaction commits or rolls back — it doesn't error and doesn't see a stale value, it simply waits. This is a common latency source on hot rows under concurrent load.

---

> [!tip] ⚡ Quick Recall
> - The bean you inject is a **proxy** (`InfrastructureAdvisorAutoProxyCreator`, CGLIB/JDK dynamic proxy), not your object.
> - `TransactionInterceptor.invoke()` is a plain **try → `proceed()` → commit/rollback** block, same mechanism as `@Around`.
> - The connection is bound to the **thread** via `TransactionSynchronizationManager`'s `ThreadLocal` — this is *the* mechanism behind everything else in this note.
> - Commit is **two steps**: `entityManager.flush()` (sends SQL) then `connection.commit()` (makes it durable). `save()` alone only queues.
> - `REQUIRES_NEW` **suspends** the `ConnectionHolder` and restores it after — hence two connections held at once.
> - **Async work runs on a different thread and never sees the bound connection** — same failure shape as self-invocation, triggered by a thread hop instead of a direct call.
> - Connection dies **during flush** → clean failure, DB rolls back server-side, nothing partial persists.
> - Connection dies **after commit, before the ack** → **in-doubt transaction** — data may already be committed. Only an idempotency key / status check / reconciliation resolves it, never a retry alone.
> - `saveAndFlush()` takes a row lock and is invisible to other transactions' **reads** under normal isolation, but blocks other transactions' **writes** to that row until commit.

---

Related: [[10. Transactions]] · [[8. Dirty Checking and Flush]] · [[9. Database Concurrency]] · [[11. Transaction Boundaries]] · [[4. Executors and Thread Pools]] · [[1. JDBC Fundamentals]] · [[18. Production Problems]] · [[0. JPA Roadmap]]
