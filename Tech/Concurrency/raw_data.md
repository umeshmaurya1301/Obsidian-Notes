Good question, and there's a real trap in it that interviewers like. Let me start with the mechanism, then the part most people get wrong.

## First, partitioning ≠ sharding

Since we just covered sharding, keep these separate:

| | Partitioning | Sharding |
|---|---|---|
| Scope | One database node | Multiple database nodes |
| Managed by | The DB engine, transparently | Your application / a proxy layer |
| Query view | One logical table | Application must route to the right node |
| Solves | Large table size, maintenance, scan cost | Total capacity, cross-node scale |

Partitioning splits **one table into N physical sub-tables** on the same server. The application still queries `ledger_entries` and never sees the partitions.

## The mechanism that makes search fast: partition pruning

```sql
CREATE TABLE ledger_entries (
    entry_id    BIGINT AUTO_INCREMENT,
    txn_id      VARCHAR(64) NOT NULL,
    account_id  VARCHAR(50) NOT NULL,
    amount      DECIMAL(20,4) NOT NULL,
    created_at  DATETIME NOT NULL,
    PRIMARY KEY (entry_id, created_at),
    KEY idx_account_time (account_id, created_at)
)
PARTITION BY RANGE (TO_DAYS(created_at)) (
    PARTITION p2026_06 VALUES LESS THAN (TO_DAYS('2026-07-01')),
    PARTITION p2026_07 VALUES LESS THAN (TO_DAYS('2026-08-01')),
    PARTITION p2026_08 VALUES LESS THAN (TO_DAYS('2026-09-01')),
    PARTITION p2026_09 VALUES LESS THAN (TO_DAYS('2026-10-01')),
    PARTITION pmax     VALUES LESS THAN MAXVALUE
);
```

Now this query:

```sql
SELECT * FROM ledger_entries
WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01'
  AND account_id = 'POOL_001';
```

The optimizer reads the `created_at` predicate, compares it against each partition's range boundaries, and concludes that **only `p2026_08` can possibly contain matching rows**. It never opens the other partitions at all.

```
EXPLAIN output:
partitions: p2026_08          ← one partition, not five
```

That's partition pruning. The engine eliminated ~80% of the table before doing any index work.

## Why this is actually faster (the honest version)

There are three separate benefits, and they're not equally important.

**1. Fewer pages to scan (the biggest win for range queries).**
For "give me all of August", an unpartitioned table walks the index and reads scattered pages across the whole 1-billion-row structure. A partitioned table reads one contiguous ~83-million-row partition. Far fewer pages touched.

**2. Smaller indexes fit in the buffer pool (the underrated win).**
Each partition has its **own** B+ tree index. If you mostly query recent data, only the last month or two of index pages stay hot in memory. On an unpartitioned table, the single giant index competes for buffer pool space across all historical data, so your cache hit rate is worse.

**3. Shallower trees (real, but smaller than people claim).**
With a typical fanout of ~500 entries per 16KB page:
- 1 billion rows → log₅₀₀(10⁹) ≈ 3.4 → **4 levels**
- 83 million rows → log₅₀₀(8.3×10⁷) ≈ 2.9 → **3 levels**

One fewer level, so roughly 25% fewer I/Os per point lookup. Real, but modest. A lot of blog posts overstate this. If an interviewer asks "why is a partitioned index faster," leading with buffer-pool residency and page-scan reduction rather than tree height shows you actually understand the numbers.

## The trap: queries without the partition key get SLOWER

This is what they're likely testing.

MySQL and Postgres both use **local indexes** on partitioned tables. Each partition has its own independent index. There is no single global index spanning all partitions.

So this query:

```sql
SELECT * FROM ledger_entries WHERE txn_id = 'UPI700';
```

has no `created_at` predicate. The optimizer cannot prune anything, so it must search **every partition's index separately**:

```
EXPLAIN output:
partitions: p2026_06,p2026_07,p2026_08,p2026_09,pmax    ← all of them
```

Five index lookups instead of one. **This is slower than the same query on an unpartitioned table**, which would have done a single lookup on one large index.

The rule to state clearly:

> Partitioning helps only queries that filter on the partition key. Queries that don't include it pay an N-partition penalty. So you partition by the column your dominant query pattern actually filters on, and you accept that secondary access paths get worse.

## The constraint that can silently break your idempotency

This connects directly back to the unique-key work we did earlier, and it's the kind of detail that wins interviews.

**MySQL requires every unique index (including the primary key) to contain all columns of the partitioning expression.**

So on a table partitioned by `created_at`, this is **rejected**:

```sql
UNIQUE KEY uk_idem (idem_key)      -- ERROR: partition column not included
```

You're forced to write:

```sql
UNIQUE KEY uk_idem (idem_key, created_at)
```

Which no longer guarantees that `idem_key` is globally unique. The same key inserted on a different date lands in a different partition and **will not conflict**. Your duplicate-key protection, the whole mechanism we traced through implicit locks and commit-wait, quietly stops protecting you.

Postgres declarative partitioning has the same restriction: unique constraints on a partitioned table must include the partition key.

**Practical consequence:** do not partition your `idempotency_keys` table by date. Keep it unpartitioned (with a separate cleanup job), or partition it by `HASH(idem_key)` so the unique constraint can legitimately include the partition column. Partition the ledger by date, since the ledger's uniqueness is naturally scoped by transaction anyway. Raising this unprompted is a strong signal that you've thought past the textbook answer.

## The benefit that's often the real reason people partition: maintenance

For a ledger or audit table with a retention policy:

```sql
-- Partitioned: instant metadata operation
ALTER TABLE ledger_entries DROP PARTITION p2025_09;
```

```sql
-- Unpartitioned: hours of work
DELETE FROM ledger_entries WHERE created_at < '2025-10-01';
```

That `DELETE` scans and deletes millions of rows, generates enormous undo log volume, holds locks, blows out replication lag on your replicas, and leaves the table bloated so you then need an `OPTIMIZE TABLE` / `VACUUM FULL`. The `DROP PARTITION` is a file unlink and a catalog update. Milliseconds.

In payments, where you're often required to retain N years and purge beyond that, this alone frequently justifies partitioning even before considering query speed.

Same applies in reverse for archival: detach an old partition, move it to cold storage, done. No row-by-row export.

## One thing partitioning does NOT solve

Tying back to your previous question: **date partitioning does not help write contention.** All new inserts go into the newest partition, so the hot spot just moves from "the whole table" to "the current partition." If anything it concentrates it. If write contention is the problem, you need `PARTITION BY HASH(account_id)` or the intra-account bucketing we discussed, not date ranges.

Don't let an interviewer's "would partitioning help here?" pull you into agreeing when the answer is no.

## Postgres syntax, for completeness

```sql
CREATE TABLE ledger_entries (
    entry_id    BIGSERIAL,
    txn_id      VARCHAR(64) NOT NULL,
    account_id  VARCHAR(50) NOT NULL,
    amount      NUMERIC(20,4) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE ledger_2026_08 PARTITION OF ledger_entries
    FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');
```

Postgres prunes at plan time, and also at **execution time** for parameterized/prepared queries where the value isn't known until runtime. Worth mentioning if asked about prepared statements.

## When not to partition

- Table under roughly 50–100 million rows. The overhead usually isn't worth it.
- Your dominant queries don't filter on any single natural partition key.
- Too many partitions. Each one costs planning time and open file handles; hundreds of partitions can make the optimizer itself slow.

## One-liner for the interview

> "Date partitioning speeds up search through **partition pruning**: the optimizer reads the date predicate, eliminates partitions that can't match, and only searches the remaining one's local index. The wins are fewer pages scanned and better buffer-pool residency for recent data, plus near-instant retention drops. The catch is that indexes are local per partition, so any query that doesn't filter on the partition key has to search every partition and ends up slower than it would be unpartitioned. And in MySQL, every unique key must include the partition column, which can silently weaken a uniqueness guarantee you were relying on."
> 
> 
> 
> 
> Yes, you're exactly right — and it's worth stating precisely why, since "partitioning is always a tradeoff" is true but a bit generic for an interview answer. The sharper version:

## Your scenario, confirmed

```sql
-- Table partitioned by month on created_at
SELECT * FROM txn_log WHERE txn_id = 'UPI700';
```

If `txn_id` lookups are your **dominant query pattern**, and the query has no `created_at` filter, then month-partitioning **actively hurts** every single one of those lookups:

- Unpartitioned: 1 index traversal (~3-4 B+ tree levels)
- Partitioned by month, say 24 months of data: **24 separate index traversals**, one per partition, because each partition has its own local index and MySQL/Postgres can't prune anything without a value on the partition key

So yes — you'd be making your **most frequent query pattern** slower to gain a benefit (retention/pruning) that only helps a query pattern (date-range scans) you said isn't the dominant one. That's a bad trade for this table.

## The rule to state cleanly

> **Partition by the column your most frequent/critical queries actually filter on — not by whatever column "feels natural" like a date.** If 90% of your traffic is point lookups by `txn_id`, and only 10% is "give me last month's transactions," partitioning by date optimizes for the minority pattern and penalizes the majority one.

## What you'd actually do instead, a few real options

**Option 1 — Don't partition at all.**
If it's genuinely a hot, well-indexed `txn_id` lookup table, a single well-tuned unique/secondary index on `txn_id` might outperform any partitioning scheme. Partitioning isn't mandatory just because a table is large — this is worth saying explicitly, since a lot of candidates assume "big table → must partition."

**Option 2 — Partition by `HASH(txn_id)` instead of by date.**
```sql
PARTITION BY HASH(txn_id) PARTITIONS 32;
```
Now a `WHERE txn_id = 'UPI700'` query hashes the value, the optimizer computes exactly which one of the 32 partitions it lives in, and prunes to **that single partition** — you get the "smaller index, better buffer pool residency" benefit *for the query pattern you actually have*. The cost: you lose the nice "drop old partition" retention trick, since hash partitions don't correspond to time ranges — old and new rows are mixed together in every partition.

**Option 3 — Keep both patterns fast: composite index instead of repartitioning.**
If you're already partitioning by month for retention reasons (which is often a real, separate requirement in payments — "keep 7 years, purge after"), you don't have to abandon that. Instead, make sure `txn_id` lookups don't have to hit all partitions by **also including something that lets pruning happen**, if the caller can supply it — e.g., if your `txn_id` itself embeds a date/timestamp component (a lot of real payment reference IDs do, like a UPI RRN which is often time-derived), you can extract the date from the ID in application code and pass it as an additional filter, letting the optimizer prune even though the user only "asked for" `txn_id`.

**Option 4 — Accept the date partitioning, but add a global lookup index outside the partitioned table.**
A small separate table: `txn_id_index(txn_id PRIMARY KEY, created_at)` — no partitioning, single index, tiny row size. Point lookups hit this table first to get the `created_at`, then query the big partitioned table with **both** `txn_id` and `created_at`, letting it prune to one partition. Essentially manually building the "global index" that MySQL/Postgres partitioned tables don't give you natively. More moving parts, but it lets you keep date-based retention **and** fast point lookups.

## The honest tradeoff statement for the interview

> "Yes — if the dominant query pattern is a point lookup by `txn_id` with no date component, month-based partitioning would hurt that pattern, because local indexes mean every partition has to be searched. I'd either not partition at all, partition by `HASH(txn_id)` if lookups are what matters most, or if I still need date-based retention for compliance, add a small unpartitioned lookup table that maps `txn_id → created_at` so the app can supply the pruning key even when the caller only has the transaction id."

This is exactly the kind of answer — "I know the default technique, and I know precisely when *not* to use it, and here are two concrete alternatives" — that separates a senior response from someone reciting "partitioning improves performance."


Yes, that's exactly the right direction — this is a well-known real pattern (essentially a **CQRS-style read model**), and it sidesteps the whole point-lookup-vs-range-scan conflict we just discussed by giving each table a query pattern it's actually optimized for. Let's work through it properly.

## Why this works

- **`txn_log` (OLTP, primary):** stays unpartitioned, optimized for `txn_id` point lookups, serves live transaction processing. No compromise made for reporting needs.
- **`txn_log_reporting` (OLAP-ish, derived):** partitioned by date, optimized for "show me all transactions in August," "sum by day," dashboards, batch reconciliation, admin views. No compromise made for point-lookup needs.

Two tables, two access patterns, two index/partition strategies — each fully optimized for its own job instead of one table trying to serve both and doing neither well. This is a genuinely strong architectural instinct.

## How to actually sync it — three real options, in order of typical preference

**1. CDC (Change Data Capture) — the production-grade answer**

```
txn_log (MySQL) → binlog → Debezium → Kafka topic → consumer → txn_log_reporting
```

- Debezium tails MySQL's binlog (or Postgres's WAL) and emits an event for every insert/update/delete, near real-time (typically sub-second to a few seconds lag).
- A consumer applies these events to the partitioned reporting table.
- **Why this is usually the right answer in an interview:** it doesn't add any load to `txn_log` beyond what replication already costs the DB, doesn't require the app to remember to "also write to the reporting table," and naturally fits your existing Kafka stack from the orchestrator project.

**2. Application-level dual write — simplest, but has a real correctness problem**

```java
saveToTxnLog(txn);
saveToReportingTable(txn);   // separate write, separate table
```

- **The problem:** these are two separate writes with no atomicity between them (unless the reporting table is in the *same* database and you wrap both in one transaction — but you said this is a synced/derived table, implying it might be a separate DB/replica). If the app crashes between the two writes, the reporting table silently drifts from the source of truth.
- Worth naming this weakness even if you wouldn't pick this approach — it shows you understand the failure mode, not just the happy path.

**3. Periodic batch ETL job — simplest to build, highest staleness**

```sql
-- Runs every N minutes
INSERT INTO txn_log_reporting
SELECT * FROM txn_log
WHERE updated_at > :last_sync_watermark;
```

- Easiest to implement, but "periodically" means you're explicitly accepting staleness — minutes of lag, not seconds.
- Fine for a table that only feeds an admin dashboard people don't expect to be real-time. Not fine if "reporting" secretly means "reconciliation that needs to match NPCI within seconds."

**The honest answer for a payments system specifically:** CDC is usually right, because reconciliation and admin visibility in a financial system tend to have tighter freshness expectations than people initially state, and CDC gives you near-real-time without hammering the primary DB with a polling query every N minutes.

## What partitioning strategy fits the reporting table

Now this table's dominant query pattern really is date-driven — "this month's report," "last quarter's reconciliation," "purge data older than 7 years" — so **date-range partitioning is now the correct choice**, unlike on `txn_log`:

```sql
CREATE TABLE txn_log_reporting (
    entry_id     BIGINT,
    txn_id       VARCHAR(64) NOT NULL,
    account_id   VARCHAR(50) NOT NULL,
    amount       DECIMAL(20,4) NOT NULL,
    status       VARCHAR(20) NOT NULL,
    created_at   DATETIME NOT NULL,
    PRIMARY KEY (entry_id, created_at),
    KEY idx_txn (txn_id, created_at)   -- still add this, see below
)
PARTITION BY RANGE (TO_DAYS(created_at)) (
    PARTITION p2026_07 VALUES LESS THAN (TO_DAYS('2026-08-01')),
    PARTITION p2026_08 VALUES LESS THAN (TO_DAYS('2026-09-01')),
    PARTITION pmax     VALUES LESS THAN MAXVALUE
);
```

Notice `idx_txn` includes `txn_id` **and** `created_at` — even on the reporting table, if someone occasionally does look up a specific `txn_id` here (e.g., an admin drilling into one transaction from a report), you still pay the all-partitions penalty unless they also know roughly which month to filter on. That's usually fine for a reporting table since it's not your hot path.

## Things worth stating explicitly, since they're exactly what shows real design maturity here

**1. You're trading consistency for query performance, and that's the correct trade — for this table.**
The reporting table is **eventually consistent**, not strongly consistent. That's fine because nobody making a real-time debit decision should ever query it — it's read-only, analytics/admin-facing. Say this explicitly: "the reporting table is intentionally eventually consistent, and that's an acceptable trade because it's never on the write path or the balance-check path."

**2. Never let the reporting table become a dependency for correctness.**
If someone later says "let's just check the reporting table for reconciliation instead of the ledger, it's easier to query" — that's a bug waiting to happen, because CDC lag or a stuck consumer means the reporting table could be minutes behind during exactly the incident where accuracy matters most. Reconciliation against NPCI should hit the ledger/source of truth, not the derived table.

**3. Watermark/lag monitoring is mandatory, not optional.**
You need to know *how* stale the reporting table currently is — track `MAX(created_at)` in the reporting table vs the source, alert if lag exceeds a threshold. Otherwise an admin looking at a "report" has no idea if they're seeing 2 seconds old or 2 hours old data because the CDC consumer silently died.

**4. This is the same pattern as a read replica, one level more customized.**
A plain MySQL read replica already solves "don't load the primary with reporting queries," but it's schema-identical to the primary, so it inherits the primary's *unpartitioned* structure and doesn't get you partition pruning. What you're describing is a **purpose-built derived table** — same replication *idea* as a read replica, but with a schema/partitioning scheme optimized specifically for the reporting query shape, not just a copy. Worth drawing that distinction if asked "isn't this just a read replica" — it's a materialized, reshaped view, not a byte-for-byte replica.

## Confirmed answer

> "Yes — this is the right direction, and it's essentially a CQRS read-model pattern: keep the OLTP table (`txn_log`) unpartitioned and optimized for point lookups by `txn_id`, and maintain a separate, derived, date-partitioned table for reporting, synced via CDC (Debezium/binlog → Kafka) for near-real-time freshness with minimal load on the primary. The key discipline is treating the reporting table as strictly read-only and eventually consistent — it should never be in the path of a balance check or reconciliation-for-correctness, only used for dashboards and analytics — and you need lag/watermark monitoring so staleness is visible rather than silent."

This is genuinely a strong design instinct on your part — recognizing "one table, one job" instead of forcing a single schema to serve two conflicting access patterns is exactly the kind of thing that reads as senior-level judgment in a design interview.


Good time to ask this — we already established one crucial exception (a single hot pool account isn't solved by sharding). Let's build the complete picture.

## What sharding actually is, precisely

Splitting one logical table's rows across **multiple independent database instances/nodes**, each with its own compute, memory, and storage. Unlike partitioning (one node, transparent to queries), sharding requires your **application or a routing layer** to know which node holds which data.

```
Shard 1: account_id % 4 == 0  → DB Node A
Shard 2: account_id % 4 == 1  → DB Node B
Shard 3: account_id % 4 == 2  → DB Node C
Shard 4: account_id % 4 == 3  → DB Node D
```

The fundamental thing sharding buys you that partitioning cannot: **more total CPU, memory, and disk I/O capacity**, because you're adding machines, not just reorganizing files on one machine. Partitioning optimizes access patterns on fixed hardware; sharding scales the hardware itself.

---

## When sharding is useful

**1. Total data volume exceeds one machine's capacity.**
If your `customer_accounts` table has 500 million rows and the working set no longer fits in any single server's RAM/buffer pool, no amount of indexing or partitioning fixes that — you need more machines. This is the textbook case.

**2. Write throughput exceeds one machine's ceiling, and the writes are naturally spread across many independent keys.**
This is the important nuance from our earlier discussion: sharding helps when contention is spread across **many different rows/accounts**, not concentrated on one. Millions of customers each making occasional transactions → shard by `customer_id`, and each shard only has to handle its slice of total traffic. Each customer's own transactions are still fully serialized correctly on their shard, but different customers don't compete with each other at all.

**3. Natural, stable partition key with even distribution.**
`customer_id`, `merchant_id`, `tenant_id` in a multi-tenant SaaS — anything where rows genuinely belong to independent "owners" who rarely interact across shards. This is the single strongest predictor of "sharding will work cleanly" — if your data has an obvious, evenly-distributed ownership key, shard on it.

**4. Read scale beyond what read replicas can provide.**
Read replicas help, but every replica still has to apply every write eventually — replication is still bounded by single-primary write throughput and eventually by replica lag under heavy write load. Sharding gives you independent write capacity per shard, which indirectly also gives more total read capacity.

**5. Regulatory/data-residency requirements.**
Real, common in fintech: EU customer data must stay in EU, Indian data in India (data localization requirements are actually a real constraint for UPI-adjacent systems). Sharding by geography isn't really about performance at all here — it's a hard compliance requirement, and it's worth naming this as a completely different *reason* to shard than throughput.

**6. Isolating blast radius / noisy neighbors.**
If one large merchant's traffic spikes 50× during a sale event, on a shared unsharded DB that traffic can degrade performance for every other customer. Sharding contains that merchant's load to their own shard(s) — other customers are unaffected. This is often underrated as a reason; it's about **fault isolation**, not just raw throughput.

---

## When sharding is NOT useful — and is actively the wrong answer

**1. A single hot row/entity (our pool account case).**
Already covered — one logical account always maps to exactly one shard, so sharding does nothing for it. The fix is intra-entity bucketing, single-writer + batching, or the reservation pattern — not sharding.

**2. Queries that need to join or aggregate across shards.**
```sql
SELECT SUM(balance) FROM accounts WHERE region = 'APAC';
```
If `accounts` is sharded by `account_id`, this query has to hit **every shard**, gather partial results, and merge them in application code (scatter-gather). This is slow, complex, and every join that used to be a single SQL `JOIN` becomes application-level stitching. If your dominant query patterns are broad aggregates/joins across the whole dataset, sharding actively makes this worse — same "wrong key, wrong query pattern" trap as partitioning by the wrong column, just at a much higher operational cost.

**3. Data volume is well within a single node's capacity.**
If the whole dataset is a few million rows and fits comfortably in RAM with room to grow for years, sharding adds massive operational complexity (routing layer, cross-shard transactions, rebalancing, N times the ops/monitoring/backup burden) for zero real benefit. This is one of the most common real-world mistakes — premature sharding "because we might need scale eventually." Worth saying explicitly: **don't shard until you've exhausted vertical scaling, read replicas, indexing, and partitioning** — sharding should be closer to a last resort than a first instinct, because of the operational cost.

**4. Strong cross-entity transactional consistency requirements.**
If your business logic frequently needs an ACID transaction spanning two accounts that might land on different shards — e.g., an atomic transfer between Account A on Shard 1 and Account B on Shard 3 — you lose the simple single-node transaction guarantee. You either need **distributed transactions** (2PC — slow, fragile, rarely used in practice for this reason) or a **saga pattern** (eventual consistency with compensating actions — more common, but genuinely harder to reason about and debug). If your domain is full of these cross-entity atomic operations, sharding introduces a categorically harder correctness problem than anything we've discussed so far in this conversation.

**5. Uneven/unpredictable partition key distribution (hotspot shards).**
If you shard by `merchant_id` but one merchant does 40% of total platform volume, that merchant's shard becomes a hotspot no different from the original hot-row problem — you've just moved it up one level. Sharding only delivers even load distribution if the key you chose is actually evenly distributed in practice, not just in theory.

**6. Rebalancing pain with a poorly chosen scheme.**
Plain `hash(key) % N` sharding (not consistent hashing) means adding or removing a node reshuffles almost all your data — exactly the problem consistent hashing exists to solve, which we covered earlier. If you're going to shard, you need to decide upfront whether you're using range-based, hash-based (with consistent hashing), or directory-based (lookup-table) shard assignment — getting this wrong makes every future rebalance an operational nightmare.

---

## The specific case worth highlighting: your UPI/pool-account domain

Bringing this back to what we designed together:

| Table | Shard by? | Why / why not |
|---|---|---|
| `customer_accounts` (millions of customers) | **Yes** — shard by `customer_id` | Naturally distributed, high total volume, each customer largely independent |
| `pool_account` (one entity, high TPS) | **No** — sharding doesn't touch this | It's one row; use intra-account bucketing + single-writer instead |
| `ledger_entries` | **Maybe** — shard by `account_id` if volume is enormous, but often partitioning by date on one large node is enough first | Depends on whether the bottleneck is total volume or write concurrency |
| Cross-account transfer (customer → pool) | **Sharding makes this harder** | If customer and pool are on different shards, this transaction now spans shards — needs saga/compensating logic instead of a simple local transaction |

That last row is a great thing to raise proactively if this domain comes up: "if I shard customer accounts by customer_id, every debit-from-customer-credit-to-pool transaction now potentially spans two shards, so I'd need to handle that with a saga rather than a local ACID transaction" — that's the kind of forward-looking tradeoff awareness interviewers are fishing for.

---

## One-liner for the interview

> "Shard when you have genuinely distributed ownership — many independent entities like customers or tenants — and you've exhausted vertical scaling, replicas, and partitioning first. Don't shard for a single hot entity, for workloads dominated by cross-entity joins/aggregates, or for datasets that comfortably fit one node — in those cases sharding adds massive operational and consistency complexity for little or no real benefit, and can even introduce new problems like cross-shard transactions that didn't exist before."

The strongest framing to lead with, if asked cold: **"Sharding solves a capacity problem — too much data or too much aggregate load for one machine. It does not solve a contention problem on a single entity, and it actively creates a consistency problem for anything that spans shards."** That one sentence, backed by the pool-account example we already built together, is a very complete-sounding answer.