
1. How do u detect memory leakage in a production system. What if it is a large system. what if it is distributed and large as well.
2. you have to add a column and then update in a very large table with millions of rows, how will u do without impacting the DB. how diff diff Databases handles this.
3. Question 2 but when deleting a columns.
4. Question be renaming the column.
5. DB query optimization. how will u identify
6. How will u detect Deadlock in production system and how to prevent

---

# Question 1

> In your current project how do you check metrics? What all metrics do you monitor?

### Possible Follow-ups (continued)

#### JVM Metrics

* Heap vs Stack?
* What is Young Gen / Old Gen?
* What is GC pause time?
* Which GC are you using?
* How do you identify memory pressure?
* What does heap utilization tell you?

#### Infrastructure Metrics

* CPU utilization
* Memory utilization
* Disk I/O
* Network I/O
* Container restarts
* Pod health
* Node health

#### Database Metrics

* DB connection pool utilization
* Query latency
* Slow queries
* Deadlocks
* Lock waits
* Active connections

#### Kafka Metrics

* Consumer lag
* Messages/sec
* Rebalance count
* Failed messages
* DLQ size
* Producer throughput

#### Redis Metrics

* Memory usage
* Eviction count
* Hit ratio
* Miss ratio
* Connected clients
* Latency

### Technologies They May Ask

* Prometheus
* Grafana
* ELK
* Datadog
* New Relic
* CloudWatch

---

## Related Questions

### Easy

* What is observability?
* Difference between logs and metrics?
* Difference between metrics and traces?

### Medium

* How would you monitor a Spring Boot application?
* How do you detect latency issues?
* How do you create alerts?

### Advanced

* How do you design observability for a payment system?
* How do you monitor microservices dependencies?

---

## DSA (sometimes asked indirectly)

Not directly DSA, but these are common production-oriented problems:

* Sliding Window Maximum (LC 239)
* Moving Average from Data Stream (LC 346)
* Design Hit Counter (LC 362)
* Design Circular Queue (LC 622)

---

# Question 2

> How will your system behave in case of Kafka failure, Redis failure, DB failure, etc.?

---

## What Interviewer is Testing

This is a **resiliency/fault tolerance** question.

They want to know whether you think beyond happy path.

---

## Kafka Failure Follow-ups

### Producer Side

* What if Kafka is down?
* What happens to producer requests?
* How many retries should be configured?
* What if retries also fail?

### Consumer Side

* What if consumer crashes?
* What if consumer processes message but crashes before commit?
* What causes duplicate processing?
* How do you handle idempotency?

### Broker Side

* What happens if leader broker dies?
* What is ISR?
* How is new leader selected?
* What if all replicas die?

### Delivery Semantics

* At Most Once
* At Least Once
* Exactly Once

You were already asked these recently, so this is clearly a hot area.

---

## Redis Failure Follow-ups

### Cache Failure

* What happens when Redis goes down?
* Does application stop working?
* Does traffic go to DB?

### Cache Patterns

* Cache Aside
* Read Through
* Write Through
* Write Back

### Cache Problems

* Cache Penetration
* Cache Avalanche
* Cache Stampede

### Scaling

* Redis Replication
* Redis Sentinel
* Redis Cluster

---

## Database Failure Follow-ups

### Availability

* Primary DB crashes?
* Read replica crashes?
* Connection pool exhausted?

### Consistency

* What happens to in-flight transactions?
* How do you recover?

### Performance

* Sudden increase in DB connections?
* Slow query causing outage?

### Scaling

* Read replicas
* Sharding
* Partitioning

---

## Cross-System Follow-ups

### Circuit Breaker

* What is circuit breaker?
* Why use Resilience4j?
* Open/Half-Open/Closed states?

### Retry

* When should retry be used?
* Why can retries be dangerous?

### Fallback

* What is graceful degradation?
* How do you return partial responses?

### Bulkhead

* What is bulkhead pattern?

---

## Related LeetCode

Not direct, but interviewers often mix these concepts with design questions:

* Design Twitter (LC 355)
* LRU Cache (LC 146)
* LFU Cache (LC 460)
* Design Log Storage System (LC 635)
* Design Hit Counter (LC 362)

---

# Question 3

> How do you identify memory leakage?

---

## What Interviewer is Testing

* JVM internals
* Production debugging
* GC understanding

---

## Immediate Follow-ups

### Symptoms

* How do you know memory leak exists?
* What metrics indicate memory leak?
* CPU increase or memory increase?
* How does application behave?

### JVM

* Heap dump?
* Thread dump?
* GC logs?
* MAT tool?
* VisualVM?
* JProfiler?

### Analysis

* Which objects are growing?
* Why aren't they being garbage collected?
* What is retained heap?

### Common Causes

* Static collections
* Unclosed resources
* ThreadLocal leaks
* Infinite caches
* Listener leaks

### Kubernetes

* Pod restart due to OOMKilled?
* Difference between memory leak and high memory usage?

---

## Related Questions

* What is OutOfMemoryError?
* Heap dump vs thread dump?
* Young GC vs Full GC?
* Why does Full GC become frequent?

---

## DSA Topics Often Connected

* LRU Cache (LC 146)
* LFU Cache (LC 460)
* Design In-Memory File System (LC 588)

Reason: memory management discussions often move into cache design.

---

# Question 4

> What about sudden spike?

---

## What Interviewer is Testing

* Scalability
* Capacity planning
* Traffic management

---

## Follow-ups

### Detection

* How do you identify spike?
* Which metrics alert first?

### Protection

* Rate Limiting
* Throttling
* Queueing
* Load Balancing

### Scaling

* Horizontal scaling
* Vertical scaling
* Auto-scaling

### Database

* How do you protect DB from spike?
* Read replicas?
* Caching?

### Kafka

* Can Kafka absorb spikes?
* What happens when lag increases?

### API Layer

* 10x traffic suddenly comes.
* What breaks first?

This exact question often becomes:

> Your TPS suddenly increased from 1k to 20k. What happens?

---

## Related System Design Questions

* Design URL Shortener
* Design Payment Gateway
* Design Notification System
* Design Rate Limiter

---

# Question 5

> Kafka related questions about partition assignment, consumers and so on.

---

## Must Know Follow-ups

### Partitioning

* Why partitions?
* How is partition selected?
* Key-based partitioning?
* Round robin partitioning?

### Consumers

* One partition can be consumed by how many consumers?
* One consumer can consume how many partitions?
* What happens when consumers increase?

### Consumer Groups

* Why consumer groups?
* How is load distributed?

### Rebalancing

* What triggers rebalance?
* Why is rebalance expensive?
* Cooperative rebalance vs eager rebalance?

### Offset Management

* Auto commit vs manual commit?
* Where are offsets stored?
* What happens if offset commit fails?

### Ordering

* Is ordering guaranteed?
* Across partitions?
* Within partition?

### Replication

* Leader replica
* Follower replica
* ISR
* Leader election

### Reliability

* Producer acks=0,1,all
* Min ISR
* Idempotent producer
* Exactly-once semantics

---

# Related LeetCode (Closest Concepts)

These aren't Kafka questions directly, but they train the same thinking:

### Queues / Streams

* Moving Average from Data Stream (LC 346)
* Design Hit Counter (LC 362)
* Sliding Window Maximum (LC 239)

### Producer Consumer

* Print in Order (LC 1114)
* Building H2O (LC 1117)
* Bounded Blocking Queue (LC 1188)

---

### Big Picture

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