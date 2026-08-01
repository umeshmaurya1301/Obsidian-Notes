# ACID, Isolation, MVCC & Concurrency Control — Complete Notes

---

# Why ACID Came Into Picture

Before ACID, databases had four major problems:

## 1. Partial Updates (Atomicity)

Transfer ₹300 from Alice to Bob.

```sql
UPDATE accounts
SET balance = balance - 300
WHERE id = 'Alice';

-- Crash

UPDATE accounts
SET balance = balance + 300
WHERE id = 'Bob';
```

Result

```
Alice = 700
Bob = 500
```

₹300 disappeared.

Solution:

> Atomicity (All or Nothing)

---

## 2. Invalid Data (Consistency)

Examples

```
Balance = -500

Account Type = Unknown

Duplicate Primary Keys
```

Need database rules.

Solution:

> Consistency

---

## 3. Concurrent Users (Isolation)

Two users update same account simultaneously.

Both read

```
1000
```

One writes

```
700
```

Another writes

```
500
```

Final balance

```
500
```

Correct should be

```
200
```

Solution:

> Isolation

---

## 4. Crash after Commit (Durability)

Database says

```
Commit Successful
```

Immediately power failure.

After restart

```
Transaction Lost
```

Solution

> Durability

---

# ACID

| Property    | Purpose                                  |
| ----------- | ---------------------------------------- |
| Atomicity   | All or Nothing                           |
| Consistency | Valid State → Valid State                |
| Isolation   | Concurrent transactions behave correctly |
| Durability  | Committed data survives crash            |

---

# Why Interviews Focus on Isolation

Atomicity

Consistency

Durability

are mostly handled internally by the database.

Backend engineers mostly deal with

* concurrent users
* race conditions
* locking
* deadlocks
* performance

Hence interviews focus heavily on Isolation.

---

# Isolation Means

Transactions should behave

> As if they are executing alone

even when hundreds execute together.

---

# Why Not Run Transactions One By One?

Suppose

```
10000 users
```

Serial execution

```
T1

↓

T2

↓

T3
```

Very slow.

Need

```
Correctness

+

Concurrency
```

Isolation is the balance.

---

# Isolation Anomalies

These came first.

Isolation Levels were designed later to solve them.

---

## 1. Dirty Read

T1 updates

```
Balance = 500
```

Not committed.

T2 reads

```
500
```

Later

T1 Rollback

Actual balance

```
1000
```

T2 read invalid data.

---

## 2. Non Repeatable Read

T1

```
Read Salary

1000
```

T2

```
Update Salary

1500

Commit
```

T1 reads again

```
1500
```

Same row changed.

---

## 3. Phantom Read

T1

```
SELECT

Employees

Salary > 5000

5 rows
```

T2 inserts

```
Salary = 8000
```

Commit

T1 executes same query

Gets

```
6 rows
```

New row appeared.

---

## 4. Lost Update

T1

```
Read

1000
```

T2

```
Read

1000
```

Both update.

Last writer wins.

One update lost.

---

# Isolation Levels

| Isolation Level  | Dirty Read | Non Repeatable | Phantom       | Lost Update* |
| ---------------- | ---------- | -------------- | ------------- | ------------ |
| Read Uncommitted | ❌          | ❌              | ❌             | ❌            |
| Read Committed   | ✅          | ❌              | ❌             | Depends      |
| Repeatable Read  | ✅          | ✅              | Depends on DB | Usually      |
| Serializable     | ✅          | ✅              | ✅             | ✅            |

*Lost update handling depends on the database implementation and SQL pattern.

---

# Repeatable Read

Guarantee

> Same row always returns same value inside one transaction.

Example

```
Balance = 1000
```

T1 reads

```
1000
```

T2

updates

```
300

Commit
```

T1 reads again

Still gets

```
1000
```

Reason

Snapshot.

---

# Serializable

Guarantee

Transactions behave

```
T1

↓

T2

↓

T3
```

Even if database internally runs them concurrently.

May abort transactions.

Highest correctness.

Lowest concurrency.

---

# How Databases Implement Isolation

There are two major techniques

```
Locks

+

MVCC
```

---

# Locks

Oldest mechanism.

---

## Shared Lock

Used for Reads.

```
T1 Read

T2 Read

T3 Read
```

Allowed simultaneously.

---

## Exclusive Lock

Used for Updates.

```
T1 Update

↓

Lock

↓

T2 Wait

↓

T3 Wait
```

Only one writer.

---

# Lock Compatibility

| Existing  | New Read | New Write |
| --------- | -------- | --------- |
| Shared    | ✅        | ❌         |
| Exclusive | ❌        | ❌         |

---

# Problems with Locks

Readers wait.

Writers wait.

Deadlocks.

Lower throughput.

Needed better solution.

---

# MVCC

Multi Version Concurrency Control.

Idea

Never overwrite immediately.

Create multiple versions.

Example

```
Version 1

Balance = 1000
```

Update

Instead of replacing

Create

```
Version 2

Balance = 300
```

Readers can still see Version 1.

---

# Snapshot

When transaction starts

Database remembers

```
Current visible versions
```

Like taking a photograph.

Future updates don't change your photograph.

---

# Timeline

```
10:00

T1 Starts

Snapshot

Balance = 1000

----------------

10:01

T2

Updates

300

Commit

----------------

10:02

T1 Reads

Still sees

1000
```

---

# Important

MVCC is only for Reads.

Not Writes.

Many people misunderstand this.

---

# Three Transactions Example

Initial

```
Balance = 1000
```

```
T1 Reads 1000

T2 Reads 1000

T3 Reads 1000
```

All want

```
Withdraw 700
```

---

Without protection

Everyone computes

```
300
```

Writes

```
300

300

300
```

Final balance

```
300
```

Three withdrawals happened.

Wrong.

---

# What PostgreSQL Actually Does

All three read

```
1000
```

using snapshots.

No problem.

When T2 reaches UPDATE

It acquires

```
Exclusive Row Lock
```

T1

```
WAIT
```

T3

```
WAIT
```

T2 commits.

Balance

```
300
```

Now T1 wakes.

Database **does not blindly update using the old snapshot**.

It checks the current row before applying the update.

---

# PostgreSQL Protection Mechanisms

## 1. MVCC

Readers never block writers.

---

## 2. Row Level Lock

Only one writer.

---

## 3. Row Recheck (EvalPlanQual)

Waiting transaction rechecks latest row version before updating.

Prevents lost updates.

---

## 4. UPDATE Uses Current Row

Instead of

```
1000 - 700
```

Database effectively uses

```
300 - 700
```

after the waiting transaction resumes.

---

## 5. Business Condition

Best production solution.

```sql
UPDATE account
SET balance = balance - 700
WHERE id = 1
AND balance >= 700;
```

If balance becomes

```
300
```

Rows updated

```
0
```

Application knows

```
Insufficient Balance
```

---

## 6. CHECK Constraint

```sql
CHECK(balance >= 0)
```

Database rejects

```
-400
```

---

## 7. Serializable Isolation

Conflicting transaction

```
Serialization Failure
```

Application retries.

---

## 8. SELECT ... FOR UPDATE

Locks row immediately.

Other transactions wait before modifying.

---

## 9. Optimistic Locking

Application layer.

Version column.

```sql
UPDATE account
SET version = version + 1
WHERE version = 5;
```

If

```
0 rows updated
```

Retry.

---

# MVCC vs Optimistic vs Pessimistic Locking

This is a common interview question.

---

## MVCC

Purpose

Consistent Reads.

Readers don't wait.

Built into database.

---

## Optimistic Locking

Purpose

Detect write conflicts.

No waiting.

Version column.

Retry if conflict.

Good for

* User Profile
* CMS
* Product Details

---

## Pessimistic Locking

Purpose

Prevent write conflicts.

Acquire lock first.

Others wait.

Good for

* Banking
* Wallet
* Ticket Booking
* Inventory

---

# Relationship

```
MVCC

↓

Makes Reads Fast

-------------------

Optimistic Locking

↓

Detect Conflicts

-------------------

Pessimistic Locking

↓

Prevent Conflicts
```

They are complementary, not competitors.

---

# MySQL Uses MVCC?

Yes.

More accurate statement

> **MySQL's InnoDB storage engine uses MVCC.**

Not every MySQL storage engine supports MVCC.

---

# Storage Engines

MySQL has multiple storage engines.

Examples

```
InnoDB

MyISAM

Memory
```

Storage engine is responsible for

* storing data
* indexes
* locks
* transactions
* crash recovery

---

# InnoDB

Default MySQL Storage Engine.

Provides

* ACID
* MVCC
* Row Locks
* Foreign Keys
* Crash Recovery
* Undo Logs
* Redo Logs

---

# PostgreSQL vs MySQL MVCC

## PostgreSQL

Stores multiple row versions.

```
1000

↓

300
```

Old version remains until VACUUM removes it.

---

## MySQL InnoDB

Stores current row.

Previous version stored in

```
Undo Logs
```

Old transaction reconstructs previous value.

---

# Do Both Use Locks?

Yes.

MVCC does NOT eliminate locks.

```
Reads

↓

MVCC

Writes

↓

Exclusive Row Locks
```

---

# Major Databases

| Database     | MVCC                        | Row Locks |
| ------------ | --------------------------- | --------- |
| PostgreSQL   | ✅                           | ✅         |
| MySQL InnoDB | ✅                           | ✅         |
| Oracle       | ✅                           | ✅         |
| SQL Server   | Optional Snapshot Isolation | ✅         |

---

# Interview One-Liners

### What is MVCC?

> MVCC allows multiple versions of a row so readers can access a consistent snapshot without blocking writers.

---

### Does MVCC eliminate locks?

> No. MVCC removes most read-write blocking. Conflicting writes still require row-level locks.

---

### What is Snapshot?

> A snapshot is the consistent view of the database that a transaction sees throughout its execution, depending on the isolation level.

---

### What is InnoDB?

> InnoDB is MySQL's default transactional storage engine. It implements ACID, MVCC, row-level locking, crash recovery, foreign keys, undo logs, and redo logs.

---

### Difference Between MVCC and Optimistic Locking?

> MVCC provides consistent reads inside the database. Optimistic locking is an application-level strategy that detects concurrent update conflicts using a version field.

---

### Difference Between MVCC and Pessimistic Locking?

> MVCC improves read concurrency. Pessimistic locking prevents conflicting writes by locking resources before modification.

---

# Final Mental Model

```text
                    Client Request
                          │
                          ▼
                 BEGIN TRANSACTION
                          │
                          ▼
                Read Operations
                          │
                 Uses MVCC Snapshot
                          │
          Readers Don't Block Writers
                          │
                          ▼
                UPDATE / DELETE
                          │
          Acquire Exclusive Row Lock
                          │
                          ▼
       Waiting Transactions Queue Here
                          │
                          ▼
      Recheck Latest Row Version (if needed)
                          │
                          ▼
      Business Rules / Constraints Evaluated
                          │
                          ▼
                    COMMIT / ROLLBACK
                          │
                          ▼
            Redo Logs Persist Changes
            Undo Logs Support Rollback/MVCC
```

---

# Key Takeaways

1. **ACID** was introduced to solve failures, invalid data, concurrency issues, and crash recovery.
2. **Isolation** is the most discussed ACID property because concurrent transactions are common in real-world systems.
3. Learn **anomalies first**, then **isolation levels**.
4. **MVCC** is a read concurrency mechanism, **not** a replacement for locking.
5. **Writes still use row-level locks** in MVCC databases.
6. **PostgreSQL** stores multiple row versions; **MySQL InnoDB** reconstructs old versions using undo logs.
7. **Optimistic locking** detects conflicts after they occur, while **pessimistic locking** prevents conflicts by locking first.
8. Production financial systems typically combine **transactions, row locks, SQL conditions (`WHERE balance >= ?`), constraints, and retries** to ensure correctness under heavy concurrency.
