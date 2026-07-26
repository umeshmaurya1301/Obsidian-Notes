Excellent. The first three chapters are the **foundation** of everything that comes later. If you deeply understand these, `ThreadPoolExecutor` (the hardest topic) becomes much easier.

---

# Module 4 – Chapter 1: Why Thread Pools Exist ⭐⭐⭐⭐⭐

## The Problem Before Java 5

Suppose you have a simple task:

```java
new Thread(() -> {
    System.out.println("Processing Order");
}).start();
```

Looks harmless.

Now imagine a Spring Boot application.

Your e-commerce website receives:

```
10,000 requests/minute
```

If you do:

```java
new Thread(task).start();
```

for every request,

you create

```
10,000 threads.
```

This becomes a disaster.

---

# Why?

Because a thread is **not free**.

Creating a thread involves the JVM **and** the Operating System.

When you write

```java
new Thread(task).start();
```

the following happens:

```
Application

↓

JVM creates Thread object

↓

JVM requests OS

↓

Operating System creates native thread

↓

Allocate thread stack

↓

Initialize scheduler data

↓

Register thread

↓

Start execution
```

Creating a thread is much more expensive than creating a normal Java object.

---

# What Resources Does a Thread Consume?

Each thread needs:

- Thread stack (often around 1 MB by default, JVM/OS dependent)
    
- Native OS thread
    
- Scheduler metadata
    
- Thread Local Storage (TLS)
    
- CPU scheduling time
    

Suppose:

```
1000 Threads
```

Each thread has a 1 MB stack.

Memory consumed just for stacks:

```
1000 MB

≈ 1 GB
```

Before your application stores even a single business object.

---

# Context Switching

Suppose only

```
8 CPU cores
```

exist.

But

```
500 Threads
```

are runnable.

Can all run together?

No.

CPU keeps switching.

```
Thread A

↓

Thread B

↓

Thread C

↓

Thread D

↓

...
```

Every switch means:

- Save registers
    
- Save program counter
    
- Load another thread
    
- Update scheduler
    

This is called

```
Context Switching
```

Too many threads

↓

Too many context switches

↓

Lower performance.

---

# Short-Lived Threads

Imagine

```
Receive Request

↓

Create Thread

↓

Run for 20 ms

↓

Destroy Thread
```

Then repeat

```
10,000 times.
```

Most time is spent creating and destroying threads instead of doing useful work.

---

# Real Production Example

Imagine a food delivery company.

Bad approach:

Every order

↓

Hire a new delivery person

↓

Deliver

↓

Fire the delivery person

↓

Next order

Ridiculous.

Instead,

keep delivery persons ready.

Assign them new deliveries.

Exactly what thread pools do.

---

# Thread Pool Intuition

Instead of

```
Task 1 → New Thread

Task 2 → New Thread

Task 3 → New Thread

Task 4 → New Thread
```

We create

```
Thread 1

Thread 2

Thread 3
```

once.

Then

```
Task 1 → Thread 1

Task 2 → Thread 2

Task 3 → Thread 3

Task 4 waits

↓

Thread 1 becomes free

↓

Task 4 executes
```

Threads are **reused**.

---

# Benefits

## 1. Thread Reuse

No repeated creation.

---

## 2. Less Memory

10 worker threads

instead of

1000 temporary threads.

---

## 3. Less Context Switching

Only a limited number of active threads.

---

## 4. Better Throughput

CPU spends time doing work instead of creating threads.

---

## 5. Controlled Concurrency

Instead of

```
Unlimited Threads
```

you can say

```
Maximum 20 worker threads.
```

Very important in production.

---

# Tomcat Example

Suppose your Spring Boot application uses embedded Tomcat.

You receive

```
500 HTTP Requests
```

Tomcat **does not** create 500 threads.

Instead

```
Tomcat Thread Pool

↓

200 Worker Threads

↓

500 Requests
```

First 200 requests

↓

Immediately execute.

Remaining 300

↓

Wait in queue.

As workers become free,

new requests start.

This prevents the server from crashing due to excessive thread creation.

---

# Interview Questions

### Why shouldn't we use `new Thread()` for every request?

Because:

- Thread creation is expensive.
    
- Threads consume memory.
    
- Excessive context switching hurts performance.
    
- No reuse.
    
- No lifecycle management.
    

---

### What problem do thread pools solve?

They reuse a limited number of worker threads to execute many tasks efficiently.

---

# Revision Sheet

- Threads are expensive.
    
- Thread creation involves the OS.
    
- Too many threads increase context switching.
    
- Thread pools reuse worker threads.
    
- Tomcat processes requests using a thread pool.
    

---

# Module 4 – Chapter 2: Executor Framework ⭐⭐⭐⭐⭐

Thread pools solve the problem.

Now Java needed a **standard way** to submit work.

That's why the **Executor Framework** was introduced in Java 5.

---

# Before Executor

Suppose

```java
Thread t = new Thread(task);

t.start();
```

Your code decides:

- Create thread.
    
- Start thread.
    
- Manage thread.
    

Business logic and thread management are tightly coupled.

---

# New Idea

Instead of saying

```
Create a thread
```

say

```
Please execute this task.
```

Someone else decides

- which thread
    
- when
    
- how
    

This is the Executor Framework.

---

# Executor Interface

Smallest interface

```java
public interface Executor {

    void execute(Runnable command);

}
```

Only one method.

```
execute()
```

---

# Why?

Old style

```
Task

↓

Thread

↓

Execution
```

New style

```
Task

↓

Executor

↓

Worker Thread

↓

Execution
```

The task doesn't know who executes it.

This separation is called **decoupling task submission from task execution**.

---

# Simple Example

```java
Executor executor = command -> command.run();

executor.execute(() -> {
    System.out.println("Hello");
});
```

Here, the executor simply runs the task in the current thread. In practice, most executors use worker threads from a pool.

---

# Executor Hierarchy

```
Executor
      │
      ▼
ExecutorService
      │
      ▼
ScheduledExecutorService
```

Everything in Java concurrency builds on this hierarchy.

---

# Executor

Only

```
execute()
```

Fire-and-forget.

No result.

---

# ExecutorService

Adds

```
submit()

shutdown()

shutdownNow()

invokeAll()

invokeAny()
```

Much more powerful.

We'll study this next.

---

# ScheduledExecutorService

Supports

```
Run after 5 seconds

Run every minute

Run every hour
```

Used in schedulers.

---

# Real Spring Boot Example

Suppose user uploads a file.

Controller

```
Upload

↓

Save File

↓

Generate Thumbnail

↓

Send Email
```

Generating thumbnails and sending emails can be submitted to an executor so the HTTP request returns sooner.

---

# Why Executor Was Introduced

Without Executor

Business code manages threads.

With Executor

Business code only submits work.

Thread management is centralized.

---

# Interview Questions

### What is Executor?

A simple interface that decouples task submission from task execution.

---

### Difference between Thread and Executor?

Thread represents a specific thread of execution.

Executor represents a mechanism to execute tasks, often using a thread pool.

---

# Revision Sheet

- Executor has one method: `execute(Runnable)`.
    
- Executor separates tasks from thread management.
    
- Executor is the base of the Executor Framework.
    
- `ExecutorService` extends `Executor`.
    
- `ScheduledExecutorService` extends `ExecutorService`.
    

---

# Module 4 – Chapter 3: Executors Utility Class ⭐⭐⭐⭐⭐

Creating a `ThreadPoolExecutor` directly is verbose.

Example:

```java
ExecutorService service =
    new ThreadPoolExecutor(
        ...
    );
```

Lots of configuration.

Java provides a helper class:

```java
Executors
```

It creates common thread pool configurations for you.

---

# Executors Utility Class

```java
ExecutorService service =
    Executors.newFixedThreadPool(5);
```

Done.

Internally,

it creates a configured `ThreadPoolExecutor`.

Think of it as a **factory class**.

---

# Available Factory Methods

```
Executors

↓

newFixedThreadPool()

newCachedThreadPool()

newSingleThreadExecutor()

newScheduledThreadPool()

newWorkStealingPool()
```

Let's understand each one.

---

## 1. Fixed Thread Pool ⭐⭐⭐⭐⭐

```java
ExecutorService service =
    Executors.newFixedThreadPool(3);
```

Creates exactly

```
3 Worker Threads
```

Suppose

10 tasks arrive.

```
Task 1 → Thread 1

Task 2 → Thread 2

Task 3 → Thread 3
```

Remaining

```
Task 4

Task 5

...

Task 10
```

Wait in a queue.

As a worker becomes free,

the next queued task runs.

### Best For

- Stable workloads
    
- Web servers
    
- Database operations
    

---

## 2. Cached Thread Pool ⭐⭐⭐⭐☆

```java
Executors.newCachedThreadPool();
```

Behavior:

```
Task arrives

↓

Idle thread available?

↓

Yes → Reuse

↓

No → Create new thread
```

There is effectively **no fixed upper limit** on the number of threads created by this executor (subject to system resources).

Great for:

- Many short-lived asynchronous tasks.
    

Danger:

A sudden spike in requests can create a very large number of threads, leading to memory pressure and excessive context switching.

---

## 3. Single Thread Executor ⭐⭐⭐⭐☆

```java
Executors.newSingleThreadExecutor();
```

Exactly

```
One Worker Thread
```

Tasks execute one after another.

```
Task 1

↓

Task 2

↓

Task 3
```

Useful when task ordering matters.

Examples:

- Sequential logging
    
- Processing events in order
    

---

## 4. Scheduled Thread Pool ⭐⭐⭐⭐⭐

```java
ScheduledExecutorService service =
    Executors.newScheduledThreadPool(2);
```

Supports delayed and periodic tasks.

Example:

```
Run after 5 seconds.

Run every minute.
```

We'll study its scheduling methods in detail later.

---

## 5. Work Stealing Pool ⭐⭐⭐⭐☆

```java
Executors.newWorkStealingPool();
```

Built on the `ForkJoinPool`.

Each worker thread has its own queue.

If one worker becomes idle,

it can **steal work** from another worker's queue.

```
Thread A

Queue A

↓

Empty

↓

Steal

↓

Queue B
```

Excellent for divide-and-conquer algorithms and parallel computation.

---

# Why Are `Executors` Factory Methods Sometimes Discouraged?

This is a very common interview question.

For example:

```java
Executors.newFixedThreadPool(10)
```

uses an **unbounded queue** by default.

If tasks arrive faster than they are processed:

```
10 Threads Busy

↓

Queue grows

↓

Memory grows

↓

Possible OutOfMemoryError
```

Similarly,

```java
newCachedThreadPool()
```

can create a very large number of threads under heavy load.

For production systems, many teams prefer creating a `ThreadPoolExecutor` directly so they can explicitly configure:

- Core pool size
    
- Maximum pool size
    
- Queue type and size
    
- Rejection policy
    
- Thread factory
    

We'll learn exactly how in Chapter 4.

---

# Interview Questions

### Does `Executors.newFixedThreadPool()` always create all threads immediately?

No. Threads are generally created as tasks arrive, up to the configured pool size.

---

### Which pool preserves task order?

`newSingleThreadExecutor()` executes tasks sequentially in submission order.

---

### Why avoid `Executors` in production?

Because the default configurations (such as unbounded queues or potentially unbounded thread creation) may not be appropriate for production workloads.

---

# Revision Sheet

- `Executors` is a factory class.
    
- `newFixedThreadPool()` → fixed number of workers.
    
- `newCachedThreadPool()` → creates threads as needed and reuses idle ones.
    
- `newSingleThreadExecutor()` → sequential execution.
    
- `newScheduledThreadPool()` → delayed and periodic execution.
    
- `newWorkStealingPool()` → uses work stealing for parallel tasks.
    
- For production, `ThreadPoolExecutor` often provides safer and more explicit configuration.
    

---

## Module 4 Progress

We've completed:

- ✅ Chapter 1 – Why Thread Pools Exist
    
- ✅ Chapter 2 – Executor Framework
    
- ✅ Chapter 3 – Executors Utility Class
    

The **next chapter (ThreadPoolExecutor)** is the core of the Executor Framework. Once you understand it, you'll understand how almost every Java server—including Spring Boot, Tomcat, Kafka consumers, and many asynchronous frameworks—manages concurrent work internally.











Excellent. These next **three chapters (4, 5, and 6)** are the **heart of Java Concurrency**. Almost every SDE-2 Java interview will ask questions from these topics.

Think of them like this:

```text
Executor
      ↓
ThreadPoolExecutor
      ↓
BlockingQueue
```

Everything else (Spring Boot @Async, Kafka consumers, CompletableFuture, etc.) is built on top of these.

---

# Module 4 – Chapter 4: ThreadPoolExecutor ⭐⭐⭐⭐⭐

So far we've used:

```java
ExecutorService service =
    Executors.newFixedThreadPool(5);
```

Looks simple.

But internally, Java actually creates a **ThreadPoolExecutor**.

In reality:

```java
ExecutorService service =
    new ThreadPoolExecutor(...);
```

The `Executors` class is just a factory.

---

# Why Do We Need ThreadPoolExecutor?

Imagine you're running a restaurant.

You have:

- Workers
    
- Waiting customers
    
- Maximum seating capacity
    
- Rules for handling extra customers
    

Exactly the same happens in a thread pool.

---

# ThreadPoolExecutor Components

It consists of six major components.

```text
                Task
                 │
                 ▼
        ThreadPoolExecutor
                 │
 ┌───────────────┼────────────────┐
 │               │                │
 ▼               ▼                ▼
Core Threads   Task Queue    Max Threads
                 │
                 ▼
        Rejection Policy
                 │
                 ▼
          Thread Factory
```

Let's study each.

---

## 1. Core Pool Size

```java
corePoolSize = 4;
```

These are your permanent workers.

Suppose

```text
Core Pool = 4
```

Tasks arrive.

```text
Task 1 → Worker 1

Task 2 → Worker 2

Task 3 → Worker 3

Task 4 → Worker 4
```

All immediately start.

---

## 2. Maximum Pool Size

Suppose

```text
Core = 4

Maximum = 8
```

Initially only

```text
4 workers
```

exist.

Extra workers are created **only when needed**.

Maximum workers

```text
8
```

Never more.

---

## 3. Keep Alive Time

Suppose

Temporary workers

```text
Worker 5

Worker 6

Worker 7
```

become idle.

Question:

Should they stay forever?

No.

After

```text
keepAliveTime
```

they are destroyed.

This saves memory.

---

## 4. Work Queue

Suppose

Core workers busy.

New task arrives.

Where should it go?

Answer

Queue.

```text
Worker 1 Busy

Worker 2 Busy

Worker 3 Busy

Worker 4 Busy

↓

Queue
```

We'll study queues in Chapter 6.

---

## 5. Thread Factory

Responsible for creating threads.

Default

```java
Executors.defaultThreadFactory();
```

Custom factory lets you:

- name threads
    
- set daemon status
    
- priority
    
- uncaught exception handler
    

Example

```text
payment-worker-1

payment-worker-2

payment-worker-3
```

Very useful in logs.

---

## 6. Rejection Handler

Suppose

Everything full.

```text
Core Full

↓

Queue Full

↓

Maximum Threads Full
```

Now

New task arrives.

What should happen?

That's decided by the rejection handler.

We'll study all policies in Chapter 7.

---

# Constructor

The full constructor

```java
ThreadPoolExecutor(
    corePoolSize,
    maximumPoolSize,
    keepAliveTime,
    unit,
    workQueue,
    threadFactory,
    handler
)
```

Looks scary.

After Chapters 4–7,

every parameter will feel natural.

---

# Interview Questions

### Difference between Core Pool Size and Maximum Pool Size?

Core threads are the baseline workers.

Maximum threads are additional workers created only when the queue can't accept more work (depending on the queue type and executor configuration).

---

### Can maximumPoolSize be smaller than corePoolSize?

No.

---

# Revision

- Core threads stay alive (by default).
    
- Maximum threads handle bursts.
    
- Queue stores waiting tasks.
    
- ThreadFactory creates workers.
    
- RejectionHandler handles overload.
    

---

# Module 4 – Chapter 5: Internal Working of ThreadPoolExecutor ⭐⭐⭐⭐⭐

This chapter explains **what actually happens** when you call:

```java
executor.execute(task);
```

This is one of the most common interview questions.

---

# Step 1

Task arrives.

```text
Task
```

↓

ThreadPoolExecutor.

---

# Step 2

Ask

```text
Core Thread Available?
```

Suppose

```text
Core = 4

Running = 2
```

Then

```text
Create Worker 3

Execute Task
```

Easy.

---

# Step 3

Suppose

```text
Core = 4

Running = 4
```

All workers busy.

Now

Task goes to queue.

```text
Queue

Task 5
```

---

# Step 4

Queue Full?

If

No

↓

Task waits.

---

# Step 5

Queue Full?

Yes.

Now ask

```text
Can we create extra worker?
```

Suppose

```text
Maximum = 8

Current = 5
```

Yes.

Create Worker 6.

Execute task.

---

# Step 6

Suppose

```text
Current Workers = 8

Maximum = 8

Queue Full
```

Now

No space.

No workers.

Reject task.

---

# Complete Flow

```text
Task Arrives
      │
      ▼
Core Threads Full?
      │
 ┌────┴────┐
 │         │
No        Yes
 │         │
 ▼         ▼
Create     Queue Task
Core       │
Thread      ▼
        Queue Full?
          │
     ┌────┴────┐
     │         │
    No        Yes
     │         │
     ▼         ▼
   Wait    Max Threads?
               │
        ┌──────┴──────┐
        │             │
       No            Yes
        │             │
        ▼             ▼
 Create Extra      Reject Task
 Worker
```

---

# Example

Configuration

```text
Core = 2

Maximum = 4

Queue = 2
```

Tasks

```text
Task 1
Task 2
Task 3
Task 4
Task 5
Task 6
Task 7
```

Execution

Task 1

↓

Worker 1

Task 2

↓

Worker 2

Task 3

↓

Queue

Task 4

↓

Queue

Queue now full.

Task 5

↓

Worker 3

Task 6

↓

Worker 4

Maximum reached.

Task 7

↓

Rejected.

---

# Worker Thread Lifecycle

Worker created

↓

Waits for task

↓

Executes task

↓

Looks for another task

↓

Queue empty?

↓

Wait

↓

Idle timeout?

↓

Destroy (if above core size)

Notice

Workers don't die after every task.

They keep taking new tasks.

That's why they're called **worker threads**.

---

# Why Is This Efficient?

Instead of

```text
Task

↓

Create Thread

↓

Destroy Thread
```

we have

```text
Task

↓

Existing Worker

↓

Next Task

↓

Next Task

↓

Next Task
```

One worker

handles hundreds of tasks.

---

# Interview Question

### Does ThreadPoolExecutor create all threads immediately?

No.

It creates them **on demand**, generally up to the core pool size first.

---

# Revision

- Core threads first.
    
- Queue next.
    
- Extra workers after queue is full (depending on configuration).
    
- Reject when maximum capacity is exhausted.
    

---

# Module 4 – Chapter 6: BlockingQueue ⭐⭐⭐⭐⭐

Without `BlockingQueue`

there is **no ThreadPoolExecutor**.

It is the bridge between

```text
Task Submission

↓

Worker Threads
```

---

# Why Not Use Queue?

Imagine

Producer

```text
Add Task
```

Consumer

```text
Take Task
```

Using a normal queue

Problem

```text
Queue Empty

↓

Consumer keeps checking
```

called

Busy Waiting.

Waste of CPU.

---

# BlockingQueue Solution

If queue empty

Consumer

Sleeps automatically.

When task arrives

Consumer

Wakes automatically.

No CPU wasted.

---

# Producer Consumer Model

```text
Producer

↓

BlockingQueue

↓

Consumer
```

Producer

puts tasks.

Consumers

take tasks.

Exactly how ThreadPoolExecutor works.

---

# Main Methods

## put()

```java
queue.put(task);
```

If queue full

Producer waits.

---

## take()

```java
queue.take();
```

If queue empty

Consumer waits.

---

## offer()

```java
queue.offer(task);
```

Returns

```text
true
```

if inserted,

otherwise

```text
false
```

Doesn't block by default.

---

## poll()

```java
queue.poll();
```

Returns

Task

or

```text
null
```

Doesn't block by default.

---

# Popular Implementations

---

## ArrayBlockingQueue

Fixed size.

```text
Capacity = 100
```

Cannot grow.

Good when you want to strictly limit memory usage.

---

## LinkedBlockingQueue

Linked list based.

Can be bounded or effectively unbounded (if no capacity is specified).

Frequently used in thread pools.

---

## PriorityBlockingQueue

Highest priority first.

Example

```text
Critical

High

Medium

Low
```

Workers process higher-priority tasks first.

---

## DelayQueue

Tasks become available only after a delay expires.

Useful for

- cache expiration
    
- retries
    
- scheduling
    

---

## SynchronousQueue ⭐⭐⭐⭐⭐

One of the favorite interview topics.

It has

```text
Capacity = 0
```

No storage.

Producer

```text
Task
```

↓

Immediately handed to

Worker.

If no worker ready

Producer waits (or, in the context of some executors, a new worker may be created if allowed).

This queue is used by

```java
Executors.newCachedThreadPool()
```

to support direct handoff.

---

# ThreadPool Example

Worker

```text
take()
```

↓

Wait

Producer

```text
put(task)
```

↓

Worker wakes

↓

Executes task

Simple.

---

# Interview Questions

### Why BlockingQueue instead of Queue?

Because it blocks producers or consumers when appropriate, avoiding busy waiting and simplifying coordination.

---

### Difference between put() and offer()?

|put()|offer()|
|---|---|
|Waits if full|Returns `false` if full (default behavior)|

---

### Difference between take() and poll()?

|take()|poll()|
|---|---|
|Waits if empty|Returns `null` if empty (default behavior)|

---

# Revision

- `BlockingQueue` coordinates producers and consumers.
    
- `put()` blocks when full.
    
- `take()` blocks when empty.
    
- `offer()` and `poll()` are non-blocking by default.
    
- `SynchronousQueue` stores no elements and performs direct handoff.
    
- `ThreadPoolExecutor` relies on a `BlockingQueue` to hold pending tasks.
    

---

# Module 4 Progress

We have now completed:

- ✅ Chapter 1 – Why Thread Pools Exist
    
- ✅ Chapter 2 – Executor Framework
    
- ✅ Chapter 3 – Executors Utility Class
    
- ✅ Chapter 4 – ThreadPoolExecutor
    
- ✅ Chapter 5 – Internal Working of ThreadPoolExecutor
    
- ✅ Chapter 6 – BlockingQueue
    

The **next three chapters (7, 8, and 9)** are where you'll learn **what happens when a thread pool is overloaded**, **how to get results back from asynchronous tasks**, and **why `Callable` exists instead of just `Runnable`**. These topics are asked very frequently in Java backend interviews.





Excellent. These next **three chapters (7, 8, and 9)** are among the **most frequently asked Java backend interview topics**. They answer three important questions:

1. **What happens when a thread pool is overloaded?**
    
2. **How do I get a return value from an asynchronous task?**
    
3. **Why do we need `Callable` when we already have `Runnable`?**
    

---

# Module 4 – Chapter 7: Rejection Policies ⭐⭐⭐⭐⭐

Suppose we configure:

```text
Core Pool Size = 2
Maximum Pool Size = 4
Queue Capacity = 2
```

Now imagine 7 tasks arrive.

Execution:

```text
Task 1 → Worker 1

Task 2 → Worker 2

Task 3 → Queue

Task 4 → Queue

Task 5 → Worker 3

Task 6 → Worker 4

Task 7 → ??
```

Workers?

Full.

Queue?

Full.

Maximum threads?

Reached.

Now what?

The answer is:

> **RejectedExecutionHandler**

---

# Why Do We Need Rejection Policies?

Imagine a restaurant.

```text
20 Tables

↓

All Occupied

↓

50 Customers Arrive
```

Restaurant cannot magically create more tables.

It must decide:

- Reject customers
    
- Ask them to wait
    
- Replace someone
    
- Make them serve themselves
    

ThreadPoolExecutor has the same problem.

---

# Java's Built-in Rejection Policies

There are four standard policies.

---

# 1. AbortPolicy (Default) ⭐⭐⭐⭐⭐

Behavior

```text
Task Arrives

↓

Pool Full

↓

Throw Exception
```

Exception:

```java
RejectedExecutionException
```

Example

```java
ThreadPoolExecutor executor =
    new ThreadPoolExecutor(
        2,
        4,
        60,
        TimeUnit.SECONDS,
        new ArrayBlockingQueue<>(2),
        new ThreadPoolExecutor.AbortPolicy()
    );
```

Best when:

- Losing a task is unacceptable.
    
- You want immediate visibility that the system is overloaded.
    

Example:

- Banking transactions
    
- Payment processing
    

---

# 2. CallerRunsPolicy ⭐⭐⭐⭐⭐

Instead of rejecting,

the calling thread executes the task.

```text
Main Thread

↓

submit(task)

↓

Pool Full

↓

Main Thread executes task
```

Why?

It naturally slows down the producer.

This is called **backpressure**.

---

Example

Suppose

Main Thread submits

1000 tasks.

Pool becomes full.

Instead of creating more threads,

Main Thread starts working.

Now it cannot submit tasks quickly.

System stabilizes.

---

Real-world usage

Very useful in:

- Web servers
    
- Message processing
    
- Kafka producers
    

because it naturally reduces request submission speed.

---

# 3. DiscardPolicy

Behavior

```text
Pool Full

↓

Ignore Task
```

No exception.

Nothing.

Task simply disappears.

Dangerous.

Usually only acceptable when occasional data loss is acceptable.

Example:

- Analytics
    
- Debug logging
    
- Metrics collection
    

Not suitable for business-critical operations.

---

# 4. DiscardOldestPolicy

Behavior

Queue

```text
Task A

Task B

Task C
```

New Task D arrives.

Policy removes

```text
Task A
```

Then inserts

```text
Task D
```

Oldest waiting task is discarded.

Useful only in very specialized situations.

---

# Which Policy Should You Use?

|Policy|Good For|
|---|---|
|AbortPolicy|Banking, payments, critical operations|
|CallerRunsPolicy|Backpressure, stable throughput|
|DiscardPolicy|Logs, metrics, telemetry|
|DiscardOldestPolicy|Rarely used; specialized workloads|

---

# Custom Rejection Handler

You can implement your own.

Example

```java
class MyHandler implements RejectedExecutionHandler {

    @Override
    public void rejectedExecution(
            Runnable r,
            ThreadPoolExecutor executor) {

        System.out.println("Task Rejected");

    }

}
```

Production examples:

- Send task to Kafka
    
- Store in database
    
- Retry later
    
- Send alert
    

---

# Interview Questions

### Which rejection policy is default?

```text
AbortPolicy
```

---

### Which policy provides backpressure?

```text
CallerRunsPolicy
```

---

### Why is CallerRunsPolicy useful?

It slows the producer instead of dropping tasks or creating more threads.

---

# Revision

- Rejection happens only after:
    
    - Core threads are busy.
        
    - Queue is full.
        
    - Maximum threads are busy.
        
- Default = AbortPolicy.
    
- CallerRunsPolicy provides backpressure.
    
- Custom handlers are common in production.
    

---

# Module 4 – Chapter 8: Future ⭐⭐⭐⭐⭐

Until now

```java
executor.execute(task);
```

Question

How do we know

- when task finishes?
    
- whether it succeeded?
    
- what value it returned?
    

We can't.

That's why Java introduced

```text
Future
```

---

# The Idea

Imagine ordering food.

Restaurant gives you

```text
Token #42
```

You don't immediately get the food.

You get something representing the future result.

That's exactly what a Future is.

---

# Creating Future

Instead of

```java
executor.execute(task);
```

Use

```java
Future<Integer> future =
    executor.submit(task);
```

Notice

```text
submit()

↓

Future
```

---

# Getting Result

```java
Integer result =
    future.get();
```

Behavior

```text
Task Finished?

↓

Yes

↓

Return Result
```

Otherwise

```text
Wait

↓

Task Completes

↓

Return Result
```

---

# Example

```java
ExecutorService executor =
    Executors.newFixedThreadPool(2);

Future<Integer> future =
    executor.submit(() -> {

        Thread.sleep(2000);

        return 100;

    });

System.out.println("Doing other work...");

Integer value = future.get();

System.out.println(value);
```

Output

```text
Doing other work...

(wait ~2 seconds)

100
```

Notice

Main thread is free to do other work before calling `get()`.

---

# isDone()

Suppose

Don't want to block.

```java
future.isDone();
```

Returns

```text
true

or

false
```

Useful for polling, although polling is often less efficient than callbacks or completion stages.

---

# cancel()

Suppose

User cancels request.

```java
future.cancel(true);
```

Attempts to cancel the task.

If already completed,

nothing happens.

If running,

interruption is requested.

---

# isCancelled()

Checks

```java
future.isCancelled();
```

Returns

```text
true

or

false
```

---

# Timeout

Instead of

```java
future.get();
```

Use

```java
future.get(5, TimeUnit.SECONDS);
```

Behavior

```text
Finished?

↓

Yes

↓

Return
```

Otherwise

```text
5 Seconds

↓

TimeoutException
```

Very common in production.

---

# execute() vs submit()

This is a favorite interview question.

|execute()|submit()|
|---|---|
|No result|Returns Future|
|Runnable only|Runnable or Callable|
|Exceptions go to thread's uncaught exception handler|Exceptions are captured and rethrown from `Future.get()` as `ExecutionException`|
|Fire-and-forget|Track task lifecycle|

---

# Real Example

Suppose

Payment

↓

Generate PDF

↓

Send Email

Main request shouldn't wait.

Submit asynchronously.

Later

```java
future.get();
```

if result is needed.

---

# Interview Questions

### Does Future make execution asynchronous?

No.

The executor executes the task asynchronously.

`Future` is simply a handle to observe or retrieve the result.

---

### Does get() block?

Yes.

Until task finishes,

unless timeout version is used.

---

# Revision

- `submit()` returns `Future`.
    
- `get()` waits for completion.
    
- `isDone()` checks completion.
    
- `cancel()` attempts cancellation.
    
- `get(timeout)` prevents waiting forever.
    

---

# Module 4 – Chapter 9: Callable ⭐⭐⭐⭐⭐

Until now

We used

```java
Runnable
```

Problem

Runnable

```java
public interface Runnable {

    void run();

}
```

Question

Can it return a value?

No.

Can it throw checked exceptions?

No.

---

# Why Callable?

Suppose

Need to calculate

```text
Total Sales
```

Need result.

Runnable cannot return.

Java introduced

```java
Callable<V>
```

---

# Interface

```java
public interface Callable<V> {

    V call() throws Exception;

}
```

Notice

- Returns value
    
- Can throw checked exceptions
    

---

# Example

```java
Callable<Integer> task = () -> {

    return 500;

};
```

Submit

```java
Future<Integer> future =
    executor.submit(task);
```

Retrieve

```java
Integer value =
    future.get();
```

Output

```text
500
```

---

# Callable vs Runnable

|Runnable|Callable|
|---|---|
|`run()`|`call()`|
|No return value|Returns value|
|Cannot throw checked exceptions|Can throw checked exceptions|
|Used with `execute()`|Usually used with `submit()`|

---

# Why Doesn't execute() Accept Callable?

Because

```text
Callable

↓

Returns Value
```

But

```text
execute()

↓

Returns Nothing
```

No place to receive the result.

So

```text
Callable

↓

submit()

↓

Future
```

---

# Exception Handling

Runnable

```java
executor.execute(() -> {

    throw new RuntimeException();

});
```

Exception is handled by the executing thread's uncaught exception mechanism.

Callable

```java
Future<Integer> future =
    executor.submit(() -> {

        throw new IOException();

    });
```

Later

```java
future.get();
```

throws

```text
ExecutionException
```

whose cause is the original exception.

---

# Real Spring Boot Example

Suppose

Three APIs

```text
User API

Order API

Payment API
```

Call simultaneously.

Each

returns data.

Perfect use case

```text
Callable

↓

Future

↓

Combine Results
```

(We'll later see that `CompletableFuture` often provides a cleaner approach.)

---

# Interview Questions

### Difference between Runnable and Callable?

Runnable performs work without returning a result.

Callable performs work and returns a result, and can throw checked exceptions.

---

### Can Callable run without ExecutorService?

Not directly like `Runnable`. It is typically submitted to an `ExecutorService`, which returns a `Future`.

---

### Why does Callable return Future?

Because the task executes asynchronously, so the result may not be available immediately.

---

# Revision

- `Callable` returns a value.
    
- `Callable` can throw checked exceptions.
    
- Submit a `Callable` using `submit()`.
    
- `submit()` returns a `Future`.
    
- `Future.get()` retrieves the result.
    

---

# Module 4 Progress

We've now completed:

- ✅ Chapter 1 – Why Thread Pools Exist
    
- ✅ Chapter 2 – Executor Framework
    
- ✅ Chapter 3 – Executors Utility Class
    
- ✅ Chapter 4 – ThreadPoolExecutor
    
- ✅ Chapter 5 – Internal Working of ThreadPoolExecutor
    
- ✅ Chapter 6 – BlockingQueue
    
- ✅ Chapter 7 – Rejection Policies
    
- ✅ Chapter 8 – Future
    
- ✅ Chapter 9 – Callable
    

The next three chapters (10–12) cover **FutureTask**, **ScheduledExecutorService**, and **ThreadFactory**. These topics connect the Executor Framework to real-world scheduling, task orchestration, and production observability.






Absolutely. Let's build a **complete example** that combines **ExecutorService + Callable + Future**. This is the pattern you'll see in real applications and interviews.

---

# Example 1: Basic Flow (ExecutorService + Callable + Future)

Suppose you want to calculate the square of a number asynchronously.

```java
import java.util.concurrent.*;

public class Main {

    public static void main(String[] args) throws Exception {

        // Step 1: Create a thread pool
        ExecutorService executor = Executors.newFixedThreadPool(2);

        // Step 2: Create a Callable task
        Callable<Integer> task = () -> {
            System.out.println("Calculating...");
            Thread.sleep(2000);      // Simulate long work
            return 25;
        };

        // Step 3: Submit the task
        Future<Integer> future = executor.submit(task);

        System.out.println("Main thread is doing other work...");

        // Step 4: Get the result
        Integer result = future.get();

        System.out.println("Result = " + result);

        // Step 5: Shutdown the executor
        executor.shutdown();
    }
}
```

### Output

```
Main thread is doing other work...
Calculating...
(wait 2 seconds)
Result = 25
```

---

# What Happens Internally?

When you call

```java
Future<Integer> future = executor.submit(task);
```

internally the flow is

```
                submit(task)
                      │
                      ▼
            ExecutorService
                      │
                      ▼
             ThreadPoolExecutor
                      │
              Worker Thread
                      │
              Executes Callable
                      │
             Returns Integer (25)
                      │
               Stores inside Future
                      │
        future.get() returns 25
```

Notice something important:

The **Callable never returns directly to the main thread**.

Instead

```
Callable
    │
returns value
    │
Future stores it
    │
Main thread later calls get()
```

This is why `Future` exists.

---

# Example 2: Multiple Callable Tasks

Suppose you have three services.

- User Service
    
- Order Service
    
- Payment Service
    

Instead of calling them one after another, you execute them in parallel.

```java
import java.util.concurrent.*;

public class Main {

    public static void main(String[] args) throws Exception {

        ExecutorService executor = Executors.newFixedThreadPool(3);

        Callable<String> userTask = () -> {
            Thread.sleep(2000);
            return "User Loaded";
        };

        Callable<String> orderTask = () -> {
            Thread.sleep(1000);
            return "Orders Loaded";
        };

        Callable<String> paymentTask = () -> {
            Thread.sleep(3000);
            return "Payments Loaded";
        };

        Future<String> userFuture = executor.submit(userTask);
        Future<String> orderFuture = executor.submit(orderTask);
        Future<String> paymentFuture = executor.submit(paymentTask);

        System.out.println("Main thread is free...");

        System.out.println(userFuture.get());
        System.out.println(orderFuture.get());
        System.out.println(paymentFuture.get());

        executor.shutdown();
    }
}
```

### Output

```
Main thread is free...

(after ~2 seconds)
User Loaded

Orders Loaded

(after ~3 seconds)
Payments Loaded
```

Although the `orderTask` finishes first (1 second), the first `get()` is on `userFuture`, so the main thread waits for the user task before printing anything. The payment result is printed last because it takes the longest.

---

# Timeline

Suppose

```
Time = 0 sec

submit(User)
submit(Order)
submit(Payment)
```

Immediately

```
Thread 1 → User Task

Thread 2 → Order Task

Thread 3 → Payment Task
```

Execution

```
0s ---------------------------->

Thread 1
User
==================== (2s)

Thread 2
Order
========== (1s)

Thread 3
Payment
============================== (3s)
```

The tasks run **concurrently**.

The main thread blocks **only when it calls `get()`**.

---

# Example 3: Checking Completion Without Blocking

Sometimes you don't want to stop your main thread.

```java
ExecutorService executor = Executors.newSingleThreadExecutor();

Future<Integer> future = executor.submit(() -> {

    Thread.sleep(3000);

    return 500;

});

while (!future.isDone()) {

    System.out.println("Still processing...");

    Thread.sleep(500);

}

System.out.println("Result = " + future.get());

executor.shutdown();
```

Output

```
Still processing...
Still processing...
Still processing...
Still processing...
Still processing...

Result = 500
```

The main thread keeps checking until the task completes.

---

# Real Spring Boot Example

Imagine an e-commerce application.

To build the checkout page, you need:

- User Details
    
- Cart Details
    
- Available Coupons
    

Sequential execution:

```
User API      → 2 sec

Cart API      → 2 sec

Coupon API    → 2 sec

Total = 6 sec
```

Using `Callable` + `ExecutorService` + `Future`:

```java
Future<User> user = executor.submit(userTask);

Future<Cart> cart = executor.submit(cartTask);

Future<List<Coupon>> coupons = executor.submit(couponTask);
```

All three APIs execute in parallel.

```
User API
================

Cart API
================

Coupon API
================

Total ≈ 2 seconds
```

Instead of waiting **6 seconds**, the user waits roughly **2 seconds** (assuming the calls are independent and sufficient resources are available).

---

# Complete Relationship

```
                Callable
                    │
      Defines the work to be done
                    │
                    ▼
        ExecutorService.submit()
                    │
                    ▼
          ThreadPoolExecutor
                    │
            Worker Thread executes
                    │
                    ▼
            Result stored in Future
                    │
                    ▼
              future.get()
                    │
                    ▼
             Result returned
```

---

## Interview Tip

A very common interview question is:

**"Explain the relationship between `Callable`, `Future`, and `ExecutorService`."**

A concise answer is:

- **Callable** defines a task that returns a result and may throw checked exceptions.
    
- **ExecutorService** accepts the task, schedules it on a worker thread, and manages execution.
    
- **Future** represents the pending result of that asynchronous task and lets you retrieve it later using `get()`, check completion with `isDone()`, or attempt cancellation with `cancel()`.






Excellent. These next **three chapters (10, 11, and 12)** move us from the basic Executor Framework into **real production usage**. You'll learn how Java schedules tasks, customizes worker threads, and how `FutureTask` ties everything together.

---

# Module 4 – Chapter 10: FutureTask ⭐⭐⭐⭐☆

Until now we've learned:

- `Runnable` → no return value
    
- `Callable` → returns value
    
- `Future` → represents the result
    

Now the question is:

> **Who connects all these together?**

The answer is:

```java
FutureTask<V>
```

It is one of the most important internal classes in Java concurrency.

---

# Why FutureTask?

Suppose we have

```java
Callable<Integer> task = () -> 100;
```

Question:

Can Thread execute Callable directly?

No.

A `Thread` executes a `Runnable`.

So Java needed an adapter.

```
Callable
    │
    ▼
FutureTask
    │
Implements Runnable
    │
    ▼
Thread / Executor
```

FutureTask bridges the gap.

---

# Class Hierarchy

```text
Runnable
     ▲
     │
RunnableFuture
     ▲
     │
 FutureTask
```

`RunnableFuture` is simply

```text
Runnable

+

Future
```

Therefore

FutureTask is BOTH

- Runnable
    
- Future
    

This is the key interview point.

---

# Example

```java
import java.util.concurrent.*;

public class Main {

    public static void main(String[] args) throws Exception {

        Callable<Integer> callable = () -> {
            Thread.sleep(2000);
            return 500;
        };

        FutureTask<Integer> futureTask =
                new FutureTask<>(callable);

        Thread thread = new Thread(futureTask);

        thread.start();

        System.out.println("Doing other work...");

        Integer result = futureTask.get();

        System.out.println(result);
    }
}
```

Output

```
Doing other work...
(wait 2 sec)
500
```

Notice

We never used ExecutorService.

FutureTask works directly with Thread.

---

# FutureTask with ExecutorService

```java
ExecutorService executor =
        Executors.newFixedThreadPool(2);

Callable<Integer> task = () -> 100;

FutureTask<Integer> futureTask =
        new FutureTask<>(task);

executor.execute(futureTask);

System.out.println(futureTask.get());

executor.shutdown();
```

FutureTask behaves like a Runnable.

---

# Internal Flow

```
Callable
     │
FutureTask
     │
ExecutorService
     │
Worker Thread
     │
Stores Result
     │
futureTask.get()
```

---

# Why Doesn't submit() Need FutureTask Explicitly?

When you write

```java
Future<Integer> future =
        executor.submit(callable);
```

internally Java does something similar to:

```java
FutureTask<Integer> ft =
        new FutureTask<>(callable);

executor.execute(ft);

return ft;
```

You don't see it because the Executor framework creates it for you.

---

# FutureTask States

A FutureTask internally moves through states like:

```
NEW
   │
RUNNING
   │
COMPLETED

or

CANCELLED
```

When

```java
futureTask.get();
```

is called,

- if completed → return result
    
- otherwise → wait
    

---

# Interview Questions

### Why FutureTask?

Because Thread understands Runnable, not Callable.

FutureTask adapts Callable into a Runnable while also acting as a Future.

---

### Can FutureTask run only once?

Yes.

Once completed,

calling

```java
run()
```

again has no effect.

---

# Revision

- FutureTask implements Runnable and Future.
    
- Bridges Callable and Thread.
    
- Used internally by ExecutorService.
    
- Can also be used directly with Thread.
    

---

# Module 4 – Chapter 11: ScheduledExecutorService ⭐⭐⭐⭐⭐

Suppose you want to

- send email after 5 minutes
    
- refresh cache every minute
    
- run cleanup every midnight
    

Should you write

```java
while(true){

    Thread.sleep(60000);

    refreshCache();

}
```

No.

Java already provides

```java
ScheduledExecutorService
```

---

# What is ScheduledExecutorService?

It extends

```
Executor
      │
ExecutorService
      │
ScheduledExecutorService
```

It executes tasks

- later
    
- periodically
    

---

# Creating Scheduler

```java
ScheduledExecutorService scheduler =
        Executors.newScheduledThreadPool(2);
```

---

# 1. schedule()

Run once after a delay.

```java
scheduler.schedule(
    () -> System.out.println("Hello"),
    5,
    TimeUnit.SECONDS
);
```

Timeline

```
0 sec

↓

Wait

↓

5 sec

↓

Execute
```

---

# 2. scheduleAtFixedRate()

Run every fixed interval.

Example

```java
scheduler.scheduleAtFixedRate(

    () -> System.out.println("Running"),

    2,

    5,

    TimeUnit.SECONDS
);
```

Meaning

```
Initial Delay = 2 sec

Then every 5 sec
```

Timeline

```
2

↓

7

↓

12

↓

17
```

The next execution is based on the **scheduled start time**, not on when the previous execution finished.

---

# 3. scheduleWithFixedDelay()

Runs after a fixed delay from the **end** of the previous execution.

```java
scheduler.scheduleWithFixedDelay(

    () -> System.out.println("Running"),

    2,

    5,

    TimeUnit.SECONDS
);
```

Suppose task takes

```
3 seconds
```

Timeline

```
Start at 2s

Run 3s

Finish at 5s

↓

Wait 5s

↓

Start again at 10s
```

---

# Fixed Rate vs Fixed Delay

Suppose task duration

```
3 seconds
```

Fixed Rate

```
Start

↓

Every 5 seconds
```

```
2

↓

7

↓

12

↓

17
```

Fixed Delay

```
Run

↓

Finish

↓

Wait 5 sec

↓

Run Again
```

```
2

↓

5

↓

10

↓

13

↓

18
```

Notice

Fixed Delay waits **after completion**.

---

# Real Examples

### Fixed Rate

Good for

- Heartbeats
    
- Metrics collection
    
- Monitoring
    
- Health checks
    

---

### Fixed Delay

Good for

- Cleanup jobs
    
- Cache refresh
    
- Log processing
    

where each execution should finish before the delay countdown begins.

---

# Shutdown

Always

```java
scheduler.shutdown();
```

Otherwise scheduler threads continue running.

---

# Interview Questions

### Difference between Fixed Rate and Fixed Delay?

Fixed Rate measures from the scheduled start time.

Fixed Delay measures from the completion of the previous execution.

---

### Which one is safer?

For long-running tasks,

Fixed Delay often avoids overlapping scheduling pressure because each delay starts after the previous execution completes.

---

# Revision

- schedule() → one-time execution.
    
- scheduleAtFixedRate() → periodic based on schedule.
    
- scheduleWithFixedDelay() → periodic after completion.
    

---

# Module 4 – Chapter 12: ThreadFactory ⭐⭐⭐⭐☆

Suppose your logs show

```
Thread-1

Thread-2

Thread-3
```

Question

Which thread belongs to

- Payment Service?
    
- Kafka Consumer?
    
- Email Worker?
    

Impossible to know.

That's why ThreadFactory exists.

---

# What is ThreadFactory?

It controls

- thread creation
    
- thread names
    
- daemon flag
    
- priority
    
- uncaught exception handler
    

Instead of Java creating threads,

you decide how they're created.

---

# Default Factory

```java
ExecutorService executor =
    Executors.newFixedThreadPool(3);
```

Internally

```
Executors.defaultThreadFactory()
```

creates worker threads.

Names like

```
pool-1-thread-1

pool-1-thread-2
```

---

# Custom ThreadFactory

```java
class MyThreadFactory implements ThreadFactory {

    private int count = 1;

    @Override
    public Thread newThread(Runnable r) {

        Thread t = new Thread(r);

        t.setName("payment-worker-" + count++);

        return t;
    }
}
```

Using it

```java
ExecutorService executor =
        new ThreadPoolExecutor(

                2,
                4,
                60,
                TimeUnit.SECONDS,
                new LinkedBlockingQueue<>(),
                new MyThreadFactory(),
                new ThreadPoolExecutor.AbortPolicy()
        );
```

Now logs show

```
payment-worker-1

payment-worker-2

payment-worker-3
```

Much easier to debug.

---

# Setting Daemon Threads

Inside factory

```java
t.setDaemon(true);
```

Useful for background tasks that shouldn't prevent JVM shutdown.

---

# Setting Priority

```java
t.setPriority(Thread.MAX_PRIORITY);
```

Rarely used in server applications because thread scheduling is largely controlled by the operating system.

---

# Uncaught Exception Handler

```java
t.setUncaughtExceptionHandler(
    (thread, ex) -> {
        System.out.println(
            thread.getName() +
            " failed: " +
            ex.getMessage()
        );
    }
);
```

Now unexpected thread failures are logged consistently.

---

# Spring Boot Example

Suppose

```
Email Service
```

Configure

```
email-worker-1

email-worker-2
```

Kafka

```
kafka-consumer-1

kafka-consumer-2
```

Payment

```
payment-worker-1

payment-worker-2
```

Thread dumps become much easier to understand.

---

# Interview Questions

### Why use ThreadFactory?

To customize worker thread creation instead of accepting the default configuration.

---

### Most common customization?

Thread names.

They're invaluable for debugging production issues.

---

# Revision

- ThreadFactory creates worker threads.
    
- Customize thread names.
    
- Configure daemon status.
    
- Configure priority.
    
- Configure uncaught exception handlers.
    

---

# Module 4 Progress

We've now completed **12 of 18 chapters**.

Completed:

- ✅ Why Thread Pools Exist
    
- ✅ Executor Framework
    
- ✅ Executors Utility Class
    
- ✅ ThreadPoolExecutor
    
- ✅ Internal Working
    
- ✅ BlockingQueue
    
- ✅ Rejection Policies
    
- ✅ Future
    
- ✅ Callable
    
- ✅ FutureTask
    
- ✅ ScheduledExecutorService
    
- ✅ ThreadFactory
    

---

## Remaining Chapters (The Production Side)

The final six chapters focus on operating thread pools effectively in real systems:

1. ⭐ **Thread Pool Tuning** (one of the most important SDE-2 topics)
    
2. ⭐ **Graceful Shutdown**
    
3. ⭐ **Thread Pool Monitoring**
    
4. ⭐ **Common Production Mistakes**
    
5. ⭐ **Spring Boot @Async**
    
6. ⭐ **Complete Interview Revision**
    

These chapters connect the Executor Framework to real-world backend services and production deployments.





Excellent question. This is exactly where many Java developers get confused because **Future**, **FutureTask**, and **CompletableFuture** sound very similar, but they solve different problems.

Let's build the intuition from scratch.

---

# Step 1: We started with Thread

```java
Thread t = new Thread(() -> {
    System.out.println("Hello");
});

t.start();
```

Question:

Can this return a value?

```
No.
```

Can I ask later whether it finished?

```
No.
```

Can I cancel it easily?

```
No.
```

So Java introduced **Callable**.

---

# Step 2: Callable

```java
Callable<Integer> task = () -> {
    return 100;
};
```

Great.

Now it can return

```
100
```

But another problem appears.

## Question

Who will execute this Callable?

A Thread can only execute a **Runnable**.

Thread internally does something like:

```java
runnable.run();
```

There is **no**

```java
callable.call();
```

inside Thread.

So this won't compile:

```java
Callable<Integer> task = () -> 100;

Thread t = new Thread(task);   // ❌
```

because

```
Thread expects Runnable

Callable is NOT Runnable
```

---

# This is where FutureTask comes in

FutureTask acts like an **adapter**.

```
Callable
     │
     ▼
FutureTask
     │
Implements Runnable
     │
     ▼
Thread
```

FutureTask says:

> "Don't worry Thread, I look like a Runnable."

Internally, FutureTask does something like:

```java
public void run() {

    result = callable.call();

}
```

So Thread only sees

```java
run()
```

but FutureTask secretly executes

```java
call()
```

and stores the result.

---

# Think of FutureTask as an Adapter

Imagine you have

```
Indian Plug
```

but the wall socket is

```
US Socket
```

You need an adapter.

```
Indian Plug
      │
      ▼
Adapter
      │
      ▼
US Socket
```

Similarly

```
Callable
      │
      ▼
FutureTask
      │
      ▼
Thread
```

FutureTask adapts Callable to Runnable.

---

# Why does it also implement Future?

Suppose

```java
Callable<Integer> task = () -> 100;
```

After execution,

where should

```
100
```

go?

FutureTask stores it.

Then

```java
futureTask.get();
```

returns

```
100
```

So FutureTask has **two jobs**:

1. Execute Callable
    
2. Store Result
    

That's why it implements

```
Runnable

+

Future
```

---

# Then why don't we use FutureTask everywhere?

Because Java hides it.

When you write

```java
Future<Integer> future =
        executor.submit(callable);
```

Internally, Java roughly does this:

```java
FutureTask<Integer> ft =
        new FutureTask<>(callable);

executor.execute(ft);

return ft;
```

The Executor creates the FutureTask for you.

So you rarely create one yourself.

---

# Then why does FutureTask exist?

Mostly because **ExecutorService needs an internal implementation of Future**.

Think of Future like this.

```
Future

↓

Interface
```

Interfaces cannot store data.

Someone must implement it.

FutureTask is Java's implementation.

Exactly like

```
List

↓

ArrayList
```

You write

```java
List<String> list =
        new ArrayList<>();
```

Similarly

```
Future<Integer>

↓

FutureTask<Integer>
```

---

# Then where does CompletableFuture come in?

Now another problem appears.

Suppose

```java
Future<User> future =
        executor.submit(userTask);
```

Later

```java
User user = future.get();
```

Problem

```
get()
```

blocks.

If the task takes

```
10 seconds
```

your thread waits

```
10 seconds.
```

Future is passive.

It cannot say

> "When I'm done, do this."

It only says

> "Come back later and ask me."

---

# CompletableFuture solves this

Instead of

```java
User user = future.get();
```

you can write

```java
CompletableFuture
    .supplyAsync(() -> loadUser())
    .thenApply(user -> user.getName())
    .thenAccept(System.out::println);
```

Now nobody blocks.

When one stage finishes,

the next stage automatically starts.

---

# Timeline Comparison

## Future

```
Start Task

↓

Work

↓

Main Thread waits

↓

Result
```

---

## CompletableFuture

```
Start Task

↓

Work

↓

Task finishes

↓

Automatically start next task

↓

Automatically start next task

↓

Done
```

No manual

```java
get()
```

between every step.

---

# Think of Them Like Delivery Services

## Future

You order pizza.

Restaurant gives you

```
Token #25
```

You keep asking

```
Ready?

Ready?

Ready?
```

Eventually

```
Yes.

Take Pizza.
```

---

## CompletableFuture

Restaurant says

```
We'll text you
when it's ready.
```

You continue living your life.

When pizza is ready,

you automatically get notified.

Much smarter.

---

# Why FutureTask Exists (One-Line Answer)

> **FutureTask is the concrete implementation that converts a Callable into a Runnable while also storing its result as a Future.**

It exists mainly to bridge these worlds:

```
Callable
      │
      ▼
FutureTask
      │
      ▼
Runnable
      │
      ▼
Thread / Executor
```

---

# What You Should Remember for Interviews

|Class|Purpose|
|---|---|
|Runnable|Task without return value|
|Callable|Task that returns a value|
|Future|Represents the pending result of an asynchronous task|
|FutureTask|Concrete implementation of `Future`; adapts a `Callable` into a `Runnable` and stores the result|
|CompletableFuture|Advanced asynchronous programming with chaining, composition, callbacks, and non-blocking workflows|

### The key insight

As an application developer, you'll **rarely instantiate `FutureTask` yourself**. It exists primarily as an internal building block of the Executor Framework. In day-to-day code, you'll usually use:

- `executor.submit(callable)` → for simple asynchronous tasks that return a result.
    
- `CompletableFuture` → for modern asynchronous pipelines and composing multiple async operations.
    

That's why `FutureTask` often feels unnecessary—because the framework is already using it on your behalf.



Perfect. These next three chapters are the **production engineering** part of Java Concurrency. This is where interviewers test whether you can operate thread pools in real applications, not just create them.

---

# Module 4 – Chapter 13: Thread Pool Tuning ⭐⭐⭐⭐⭐

This is one of the **most important SDE-2 interview topics**.

Creating a thread pool is easy.

```java
ExecutorService executor = Executors.newFixedThreadPool(10);
```

But...

## Question

Why 10?

Why not

```text
5

20

100

500
```

How do you decide?

That's what thread pool tuning is about.

---

# The Goal

A thread pool should have enough threads to:

- Keep CPU busy
    
- Avoid excessive context switching
    
- Avoid memory waste
    
- Maximize throughput
    

Finding this balance is tuning.

---

# CPU-bound vs I/O-bound ⭐⭐⭐⭐⭐

This is the first question every interviewer expects.

---

## CPU-bound Tasks

Examples

- Image processing
    
- Encryption
    
- Compression
    
- Mathematical calculations
    

These tasks spend almost all their time using the CPU.

Example

```java
calculatePrimeNumbers();
```

---

### Rule

Number of threads should be close to

```text
Number of CPU Cores
```

Example

Laptop

```text
8 CPU cores
```

Good thread pool

```text
8

or

9

or

10
```

Not

```text
100
```

Why?

Because only 8 threads can execute simultaneously.

The remaining 92 simply wait.

---

## What happens with 100 threads?

```text
100 Threads

↓

8 CPUs

↓

OS keeps switching

↓

Context Switching
```

Instead of doing useful work,

the CPU spends time switching threads.

Performance becomes worse.

---

# I/O-bound Tasks

Examples

- Database call
    
- REST API
    
- Kafka
    
- Redis
    
- File Reading
    

Example

```java
jdbcTemplate.query(...);
```

Most of the time

the thread is simply waiting.

```text
Thread

↓

Waiting

↓

Waiting

↓

Waiting

↓

Gets Response

↓

Works
```

During waiting,

CPU is almost idle.

---

### Therefore

We can have

```text
More Threads
```

than CPU cores.

Example

8-core machine

```text
40 Threads
```

is perfectly reasonable for I/O-heavy workloads.

---

# Famous Formula ⭐⭐⭐⭐⭐

A common guideline is

```text
Optimal Threads

=

CPU Cores

×

(1 + Wait Time / Compute Time)
```

Example

8 cores

Waiting

```text
90%
```

Working

```text
10%
```

Formula

```text
8 × (1 + 90/10)

=

8 × 10

=

80 Threads
```

This is a starting point, not a strict rule. Real systems should be measured and tuned.

---

# Choosing Queue Size

Another interview favorite.

Suppose

```text
Thread Pool

↓

Queue
```

Question

Should queue be

```text
10

100

10000
```

?

Depends.

---

## Small Queue

```text
Queue = 10
```

Benefits

- Lower latency
    
- Fail fast
    
- Better backpressure
    

Problems

- Rejections happen sooner
    

---

## Large Queue

```text
Queue = 100000
```

Benefits

- Fewer rejected tasks
    

Problems

- High memory usage
    
- Longer wait times
    
- Increased latency
    

---

# Core Pool Size

Suppose

```text
Core = 10

Maximum = 100
```

Core workers remain alive by default.

These are your permanent workers.

---

# Maximum Pool Size

Temporary workers created only during spikes.

Example

```text
Normal Traffic

↓

10 Threads

Peak Traffic

↓

40 Threads

Traffic Drops

↓

Back to 10
```

---

# Production Example

Payment Service

Traffic

```text
Normal

↓

20 requests/sec

Sale Starts

↓

500 requests/sec
```

Configuration

```text
Core = 20

Maximum = 100
```

Temporary workers help absorb spikes.

---

# Common Mistake

Many developers do

```java
Executors.newFixedThreadPool(200);
```

without measuring.

Interview answer:

> Never choose thread pool size randomly. It depends on CPU, workload, waiting time, memory, and throughput requirements.

---

# Revision

- CPU-bound → threads ≈ CPU cores
    
- I/O-bound → more threads are often beneficial
    
- Tune using measurement
    
- Queue size affects latency and memory
    
- Core threads handle steady load
    
- Maximum threads handle bursts
    

---

# Module 4 – Chapter 14: Graceful Shutdown ⭐⭐⭐⭐⭐

Suppose

```java
ExecutorService executor =
    Executors.newFixedThreadPool(5);
```

Tasks are running.

Now application exits.

Question

Should JVM immediately kill every thread?

No.

You may lose

- Transactions
    
- File writes
    
- Database updates
    

Instead

we perform a **graceful shutdown**.

---

# shutdown()

```java
executor.shutdown();
```

Meaning

```text
Stop accepting

NEW Tasks
```

But

```text
Existing Tasks

↓

Continue Running

↓

Finish Normally
```

---

Example

```java
ExecutorService executor =
        Executors.newFixedThreadPool(2);

executor.submit(() -> {

    Thread.sleep(5000);

    System.out.println("Finished");

});

executor.shutdown();
```

Output

```text
Finished
```

Task completes successfully.

---

# shutdownNow()

```java
executor.shutdownNow();
```

Behavior

```text
Stop accepting tasks

↓

Interrupt Running Threads

↓

Return Waiting Tasks
```

It **attempts** to stop running tasks by interrupting their threads. If a task ignores interruption, it may continue running.

---

# awaitTermination()

Suppose

Need to wait.

```java
executor.shutdown();

executor.awaitTermination(
        10,
        TimeUnit.SECONDS
);
```

Behavior

```text
Shutdown

↓

Wait

↓

Finished?

↓

Yes

↓

Continue
```

If timeout expires

```text
false
```

is returned.

---

# Proper Shutdown Pattern ⭐⭐⭐⭐⭐

This is the recommended pattern.

```java
executor.shutdown();

try {

    if (!executor.awaitTermination(
            10,
            TimeUnit.SECONDS)) {

        executor.shutdownNow();

    }

} catch (InterruptedException e) {

    executor.shutdownNow();

    Thread.currentThread().interrupt();

}
```

This is commonly seen in production code.

---

# Why interrupt() Again?

When catching

```java
InterruptedException
```

restore the interrupt flag.

```java
Thread.currentThread().interrupt();
```

This allows higher-level code to know that interruption was requested.

---

# Interview Questions

### Difference

|shutdown()|shutdownNow()|
|---|---|
|Stops new tasks|Stops new tasks|
|Existing tasks continue|Attempts to interrupt running tasks|
|Graceful|Immediate attempt|

---

### Does shutdown() kill threads?

No.

It only prevents new submissions.

---

# Revision

- Always call `shutdown()`.
    
- Wait with `awaitTermination()`.
    
- Use `shutdownNow()` only when necessary.
    
- Preserve the interrupt status after catching `InterruptedException`.
    

---

# Module 4 – Chapter 15: Monitoring Thread Pools ⭐⭐⭐⭐☆

Production systems need visibility.

Questions like:

- Are threads busy?
    
- Is the queue growing?
    
- Are tasks getting rejected?
    

Monitoring answers these.

---

# ThreadPoolExecutor Statistics

Instead of

```java
ExecutorService executor =
        Executors.newFixedThreadPool(5);
```

Use

```java
ThreadPoolExecutor executor =
        (ThreadPoolExecutor)
        Executors.newFixedThreadPool(5);
```

Now you can inspect internal statistics.

---

# Active Threads

```java
executor.getActiveCount();
```

Example

```text
Pool = 10

Busy = 7
```

Returns

```text
7
```

---

# Pool Size

```java
executor.getPoolSize();
```

Current worker threads.

Example

```text
Core = 10

Current = 15
```

Returns

```text
15
```

---

# Completed Tasks

```java
executor.getCompletedTaskCount();
```

Example

```text
2500
```

Useful for dashboards.

---

# Queue Size

```java
executor.getQueue().size();
```

Suppose

```text
Queue

Task

Task

Task

Task
```

Returns

```text
4
```

If this keeps increasing,

your workers cannot keep up.

---

# Largest Pool Size

```java
executor.getLargestPoolSize();
```

Shows the highest number of threads ever created simultaneously.

Great for capacity planning.

---

# Real Monitoring Example

```java
ThreadPoolExecutor executor =
        (ThreadPoolExecutor)
        Executors.newFixedThreadPool(5);

System.out.println(
        "Active : " +
        executor.getActiveCount());

System.out.println(
        "Completed : " +
        executor.getCompletedTaskCount());

System.out.println(
        "Queue : " +
        executor.getQueue().size());
```

---

# In Production

These metrics are commonly exported to monitoring systems.

Examples:

- Micrometer
    
- Prometheus
    
- Grafana
    

Typical dashboard:

```text
Active Threads      18

Queue Size           4

Completed Tasks   2,500,000

Rejected Tasks       0
```

From this, you can tell if:

- the pool is saturated,
    
- tasks are piling up,
    
- rejections are occurring,
    
- tuning is needed.
    

---

# Interview Questions

### Why monitor queue size?

A continuously growing queue often indicates the executor cannot process tasks as fast as they arrive.

---

### Why monitor active thread count?

To understand utilization and detect underutilized or overloaded pools.

---

# Revision

Monitor these metrics:

- `getActiveCount()`
    
- `getPoolSize()`
    
- `getCompletedTaskCount()`
    
- `getLargestPoolSize()`
    
- `getQueue().size()`
    

These provide the information needed to tune and troubleshoot thread pools.

---

# Module 4 Progress

Completed:

- ✅ Chapter 1 – Why Thread Pools Exist
    
- ✅ Chapter 2 – Executor Framework
    
- ✅ Chapter 3 – Executors Utility Class
    
- ✅ Chapter 4 – ThreadPoolExecutor
    
- ✅ Chapter 5 – Internal Working
    
- ✅ Chapter 6 – BlockingQueue
    
- ✅ Chapter 7 – Rejection Policies
    
- ✅ Chapter 8 – Future
    
- ✅ Chapter 9 – Callable
    
- ✅ Chapter 10 – FutureTask
    
- ✅ Chapter 11 – ScheduledExecutorService
    
- ✅ Chapter 12 – ThreadFactory
    
- ✅ Chapter 13 – Thread Pool Tuning
    
- ✅ Chapter 14 – Graceful Shutdown
    
- ✅ Chapter 15 – Monitoring Thread Pools
    

The remaining three chapters are:

1. ⭐ Common Production Mistakes
    
2. ⭐ Spring Boot `@Async`
    
3. ⭐ Complete Executor Framework Interview Revision
    

These wrap up the Executor Framework with real-world pitfalls, Spring integration, and interview-focused consolidation.



Perfect. These are the **final three chapters of Module 4**. They are highly practical and often separate someone who knows the API from someone who has operated Java applications in production.

---

# Module 4 – Chapter 16: Common Thread Pool Mistakes ⭐⭐⭐⭐⭐

Almost every production outage involving concurrency happens because of one of these mistakes.

Let's go through them one by one.

---

# Mistake 1: Creating a New Thread for Every Task ⭐⭐⭐⭐⭐

Bad

```java
public void processOrder(Order order) {
    new Thread(() -> process(order)).start();
}
```

Suppose

```text
1000 requests/sec
```

This creates

```text
1000 Threads/sec
```

Problems

- Huge memory usage
    
- Context switching
    
- Slow thread creation
    
- JVM instability
    

Instead

```java
ExecutorService executor =
        Executors.newFixedThreadPool(20);

executor.submit(() -> process(order));
```

One pool

Thousands of tasks.

---

# Mistake 2: Forgetting shutdown()

Bad

```java
ExecutorService executor =
        Executors.newFixedThreadPool(5);

executor.submit(task);

// Program exits
```

Question

Will JVM terminate?

Sometimes **No**.

Why?

Because worker threads are

```text
Non-Daemon Threads
```

JVM waits for them.

Always

```java
executor.shutdown();
```

---

# Mistake 3: Unbounded Queue ⭐⭐⭐⭐⭐

Bad

```java
Executors.newFixedThreadPool(10);
```

Remember

Internally

```text
LinkedBlockingQueue

↓

Unlimited Capacity
```

Suppose

```text
Incoming

500 Tasks/sec

Processing

100 Tasks/sec
```

Queue becomes

```text
400

800

1200

5000

50000

500000
```

Eventually

```text
OutOfMemoryError
```

Production systems often prefer a bounded queue.

Example

```java
new ArrayBlockingQueue<>(1000)
```

---

# Mistake 4: Too Many Threads

Machine

```text
8 CPU Cores
```

Developer

```java
Executors.newFixedThreadPool(500);
```

Question

Can 500 execute simultaneously?

No.

Only

```text
8
```

The rest wait.

CPU keeps switching.

Performance becomes worse.

---

# Mistake 5: Blocking Inside Thread Pool

Suppose

```java
executor.submit(() -> {

    Thread.sleep(30000);

});
```

Worker

does nothing

for

```text
30 seconds
```

If many tasks block,

pool becomes exhausted.

---

Real example

```java
executor.submit(() -> {

    restTemplate.getForObject(...);

});
```

Suppose API takes

```text
40 seconds
```

Worker waits

40 seconds.

Other requests

start waiting.

---

# Mistake 6: Ignoring Exceptions

Bad

```java
executor.execute(() -> {

    throw new RuntimeException();

});
```

Task fails.

Developer never notices.

Better

```java
Future<?> future =
        executor.submit(task);

future.get();
```

or use proper logging and uncaught exception handlers.

---

# Mistake 7: Choosing Wrong Pool Size

CPU work

```text
500 Threads
```

Waste.

Database work

```text
2 Threads
```

Too few.

Always understand the workload.

---

# Mistake 8: Never Monitoring

Production issue

```text
Application Slow
```

Developer checks

Nothing.

No metrics.

No logs.

No queue size.

No active thread count.

Impossible to diagnose.

Always monitor

```text
Active Threads

Queue Size

Completed Tasks

Rejected Tasks
```

---

# Production Checklist ⭐⭐⭐⭐⭐

Always ask:

```text
✓ Pool Size Correct?

✓ Queue Bounded?

✓ Rejection Policy?

✓ Monitoring?

✓ Shutdown?

✓ Exception Handling?
```

---

# Interview Questions

### Biggest mistake with Executors.newFixedThreadPool()?

Using the default unbounded queue without considering memory growth.

---

### Why avoid creating threads manually?

Thread creation is expensive and thread pools reuse workers efficiently.

---

# Revision

Avoid:

- New thread per request
    
- Forgetting shutdown
    
- Unlimited queues
    
- Oversized pools
    
- Blocking workers unnecessarily
    
- Ignoring exceptions
    
- No monitoring
    

---

# Module 4 – Chapter 17: Spring Boot @Async ⭐⭐⭐⭐⭐

So far we've written

```java
ExecutorService executor =
        Executors.newFixedThreadPool(5);
```

Question

Do Spring developers usually create thread pools manually?

Not often.

Spring provides

```java
@Async
```

---

# What is @Async?

Normally

```java
public void sendEmail() {

    ...
}
```

Caller waits.

```text
Caller

↓

sendEmail()

↓

Return
```

---

With

```java
@Async
```

```java
@Async
public void sendEmail() {

}
```

Flow becomes

```text
Caller

↓

Spring Thread Pool

↓

Worker Thread

↓

sendEmail()
```

Caller immediately continues.

---

# Enable Async

```java
@Configuration
@EnableAsync
public class AsyncConfig {
}
```

---

# Simple Example

```java
@Service
public class EmailService {

    @Async
    public void sendEmail() {

        System.out.println(
            Thread.currentThread().getName());

    }

}
```

Calling

```java
emailService.sendEmail();
```

returns immediately.

---

# Returning Result

Instead of

```java
void
```

Return

```java
CompletableFuture<String>
```

Example

```java
@Async
public CompletableFuture<String> loadUser() {

    return CompletableFuture.completedFuture("Alex");

}
```

Caller

```java
CompletableFuture<String> future =
        service.loadUser();
```

Notice

Spring prefers

```text
CompletableFuture
```

instead of

```text
Future
```

because it supports chaining and composition.

---

# Custom Executor ⭐⭐⭐⭐⭐

Never rely blindly on defaults.

Configuration

```java
@Bean
public Executor taskExecutor() {

    ThreadPoolTaskExecutor executor =
            new ThreadPoolTaskExecutor();

    executor.setCorePoolSize(10);

    executor.setMaxPoolSize(50);

    executor.setQueueCapacity(500);

    executor.setThreadNamePrefix(
            "payment-worker-");

    executor.initialize();

    return executor;

}
```

Spring now uses

```text
payment-worker-1

payment-worker-2
```

instead of generic names.

---

# Which Pool Does @Async Use?

If you don't configure one,

Spring uses a default async executor.

In real applications,

configure your own.

---

# Common Mistakes

## Self Invocation ⭐⭐⭐⭐⭐

Bad

```java
@Service
class PaymentService {

    @Async
    public void sendMail() {

    }

    public void process() {

        sendMail();

    }

}
```

Question

Will this be asynchronous?

No.

Reason

Spring AOP proxy is bypassed.

Calls must come

through the Spring proxy.

---

# Real Example

Checkout

```text
Save Order

↓

Return Response

↓

Send Email

↓

Generate Invoice

↓

Notify Analytics
```

Only

```text
Save Order
```

blocks the user.

Everything else

runs asynchronously.

---

# Interview Questions

### Does @Async create new Thread every time?

No.

It uses an Executor behind the scenes.

---

### Can private methods be @Async?

No.

Spring AOP cannot intercept them.

---

### Can self-invocation trigger @Async?

No.

---

# Revision

- Enable with `@EnableAsync`.
    
- Annotate methods with `@Async`.
    
- Configure a custom executor.
    
- Prefer `CompletableFuture` for return values.
    
- Beware of self-invocation.
    

---

# Module 4 – Chapter 18: Executor Framework Interview Revision ⭐⭐⭐⭐⭐

This chapter connects everything you've learned.

---

# Complete Picture

```text
                    Task
                      │
          ┌───────────┴────────────┐
          │                        │
      Runnable                Callable
          │                        │
          └───────────┬────────────┘
                      ▼
             ExecutorService
                      │
          submit() / execute()
                      │
                      ▼
           ThreadPoolExecutor
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
 Core Threads     BlockingQueue  Extra Threads
                      │
                      ▼
              Worker Threads
                      │
             Executes Task
                      │
         ┌────────────┴────────────┐
         │                         │
 execute()                    submit()
         │                         │
         ▼                         ▼
 No Result                     Future
                                    │
                                    ▼
                               FutureTask
                                    │
                                    ▼
                             Stores Result
```

---

# Decision Matrix

## Need simple background task?

```java
Runnable
```

---

## Need return value?

```java
Callable
```

---

## Need result later?

```java
Future
```

---

## Need Thread + Callable?

```java
FutureTask
```

---

## Need thread pool?

```java
ExecutorService
```

---

## Need scheduling?

```java
ScheduledExecutorService
```

---

## Need Spring async?

```java
@Async
```

---

## Need asynchronous pipelines?

```java
CompletableFuture
```

(This is our next major module.)

---

# Most Asked Interview Questions

### Difference between execute() and submit()

|execute()|submit()|
|---|---|
|Accepts `Runnable`|Accepts `Runnable` or `Callable`|
|No return value|Returns `Future`|
|Fire-and-forget|Track task and retrieve result|

---

### Difference between Runnable and Callable

|Runnable|Callable|
|---|---|
|`run()`|`call()`|
|No return|Returns value|
|No checked exceptions|Checked exceptions allowed|

---

### Difference between Future and CompletableFuture

|Future|CompletableFuture|
|---|---|
|Blocking `get()`|Supports callbacks and chaining|
|Cannot combine tasks easily|Rich composition APIs|
|Passive result holder|Active asynchronous pipeline|

---

### Difference between shutdown() and shutdownNow()

|shutdown()|shutdownNow()|
|---|---|
|Graceful|Attempts immediate interruption|
|Existing tasks continue|Running tasks are interrupted if they respond to interruption|

---

### CPU-bound vs I/O-bound

|CPU|I/O|
|---|---|
|Threads ≈ CPU cores|Usually more threads than cores|

---

# Production Best Practices

```text
✓ Use ExecutorService

✓ Bound the queue

✓ Tune the pool

✓ Monitor the pool

✓ Handle exceptions

✓ Shutdown gracefully

✓ Name your threads

✓ Use @Async in Spring

✓ Use CompletableFuture for modern async programming
```

---

# 🎉 Module 4 Completed

Congratulations! You have completed one of the most important areas of Java backend development.

## Topics Covered

- ✅ Thread Pools
    
- ✅ Executor Framework
    
- ✅ ThreadPoolExecutor
    
- ✅ BlockingQueue
    
- ✅ Rejection Policies
    
- ✅ Future
    
- ✅ Callable
    
- ✅ FutureTask
    
- ✅ ScheduledExecutorService
    
- ✅ ThreadFactory
    
- ✅ Thread Pool Tuning
    
- ✅ Graceful Shutdown
    
- ✅ Monitoring
    
- ✅ Production Mistakes
    
- ✅ Spring `@Async`
    
- ✅ Interview Revision
    

---

# What Comes Next?

I recommend the next module be a **deep dive into `CompletableFuture`**.

Unlike `Future`, `CompletableFuture` has **25+ important methods**, and interviewers often expect you to know:

- `runAsync()` vs `supplyAsync()`
    
- `thenApply()` vs `thenCompose()`
    
- `thenCombine()` vs `allOf()`
    
- `exceptionally()` vs `handle()` vs `whenComplete()`
    
- Thread execution behavior (`Async` vs non-`Async` variants)
    
- Timeouts
    
- Parallel API calls in Spring Boot
    
- Performance pitfalls and production patterns
    

It deserves a dedicated module because it's the modern foundation for asynchronous programming in Java.