Excellent choice. This is one of the **most important new Java 21 features** and is being asked in many SDE-2/Senior Backend interviews.

**Virtual Threads are probably the biggest change to Java concurrency since the introduction of the Executor Framework.**

---

# Module 8 - Part 1: Virtual Threads (Java 21)

## Interview Importance

⭐⭐⭐⭐⭐ **Very High (Java 21+)**

Typical interview questions:

- What are Virtual Threads?
    
- Why were they introduced?
    
- Platform Thread vs Virtual Thread?
    
- How are Virtual Threads implemented?
    
- Are they faster?
    
- When should we use them?
    
- When should we NOT use them?
    

---

# Why were Virtual Threads introduced?

Let's first understand the problem.

Suppose you have a Spring Boot application.

100,000 users call

```
GET /payment
```

Each request takes

```
500 ms
```

using a database call.

---

## Traditional Java (Platform Threads)

Normally

```
Request 1

↓

Thread 1

↓

DB Wait

↓

Response
```

Second request

```
↓

Thread 2
```

Third request

```
↓

Thread 3
```

Eventually

```
100,000 Requests

↓

100,000 Threads
```

Impossible.

Why?

Because platform threads are **expensive**.

Each thread has:

- OS thread
    
- Native stack (often around 1 MB by default)
    
- Kernel scheduling
    
- Context switching
    

---

Imagine

```
100,000 Threads

×

1 MB

=

~100 GB memory
```

Not practical.

---

# But what's the actual problem?

Look at this code.

```java
public User getUser() {

    return repository.findById(1);

}
```

What happens?

```
Thread

↓

Send SQL Query

↓

WAIT

↓

DB Responds

↓

Continue
```

The CPU is doing **nothing** while waiting.

The thread simply sits idle.

This is called an

```
I/O Bound Task
```

---

Another example

```java
String body = restTemplate.getForObject(url, String.class);
```

Timeline

```
Thread

↓

Send HTTP Request

↓

WAIT 500 ms

↓

Receive Response

↓

Continue
```

Again,

CPU is idle.

---

# The Problem

Most backend applications spend their time waiting for:

- Database
    
- Redis
    
- Kafka
    
- REST APIs
    
- File I/O
    
- Network
    

Yet an expensive OS thread is occupied during that wait.

This doesn't scale well.

---

# Traditional Solution

Many companies adopted asynchronous programming.

Example

```
CompletableFuture

Reactive Programming

Project Reactor

RxJava
```

These avoid blocking threads.

But they introduce complexity.

Example

```java
fetchUser()

.thenCompose(this::fetchOrders)

.thenCompose(this::fetchWallet)

.thenApply(...)
```

Difficult to read.

---

# Virtual Threads solve this differently

Instead of changing programming style,

Java changes the **thread implementation**.

Your code stays simple.

```java
User user = repository.findById(1);

Order order = orderRepository.findById(user.getId());

return order;
```

Still looks synchronous.

But underneath,

Java uses **Virtual Threads**.

---

# What is a Virtual Thread?

A Virtual Thread is a

> **Lightweight thread managed by the JVM instead of the Operating System.**

Platform Thread

```
Java Thread

↓

OS Thread
```

Virtual Thread

```
Java Virtual Thread

↓

JVM Scheduler

↓

Few Platform Threads

↓

Operating System
```

Notice

100,000 Virtual Threads

may use only

```
100 Platform Threads
```

---

# Analogy

Imagine a restaurant.

### Platform Threads

Each customer gets one waiter.

```
100 Customers

↓

100 Waiters
```

Expensive.

---

### Virtual Threads

```
100 Customers

↓

10 Waiters

↓

Serve whoever is ready
```

When one customer is waiting for food,

the waiter serves someone else.

Much more efficient.

---

# Platform Thread vs Virtual Thread

## Platform Thread

```
Java Thread

↓

OS Thread

↓

Kernel Scheduler
```

One Java thread always owns one OS thread.

---

## Virtual Thread

```
Virtual Thread A

Virtual Thread B

Virtual Thread C

↓

JVM Scheduler

↓

Platform Thread 1

Platform Thread 2

↓

Operating System
```

Virtual threads are **multiplexed** onto a small number of platform threads.

---

# Creating Virtual Threads

Java 21

Simplest way

```java
Thread.startVirtualThread(() -> {

    System.out.println("Hello");

});
```

Done.

No executors needed.

---

Another way

```java
Thread.Builder builder =
        Thread.ofVirtual();

builder.start(() -> {

    System.out.println("Running");

});
```

---

Using an Executor

```java
ExecutorService executor =

Executors.newVirtualThreadPerTaskExecutor();

executor.submit(() -> {

    processPayment();

});
```

Very common in enterprise applications.

---

# Example

```java
public class Demo {

    public static void main(String[] args) {

        Thread.startVirtualThread(() -> {

            System.out.println(

                Thread.currentThread()

            );

        });

    }

}
```

Output

```
VirtualThread[#21]/runnable
```

Notice

Not

```
Thread-0
```

---

# How do Virtual Threads work internally?

Suppose

```java
repository.findById();
```

takes

```
2 seconds
```

Timeline

```
Virtual Thread

↓

Calls Database

↓

BLOCKS
```

Old Java

```
Platform Thread

↓

Wait 2 seconds
```

Platform thread is wasted.

---

With Virtual Threads

```
Virtual Thread

↓

Waiting for Database

↓

JVM unmounts it

↓

Platform Thread becomes free

↓

Runs another Virtual Thread
```

When the database replies

```
Virtual Thread

↓

Mounted again

↓

Continue Execution
```

This **mount/unmount** behavior is the key innovation.

---

# Mounting and Unmounting

Imagine

```
Platform Thread 1
```

currently executes

```
Virtual Thread A
```

Database call begins.

```
VT A

↓

Waiting
```

Instead of wasting the platform thread,

the JVM does

```
Unmount VT A

↓

Platform Thread free

↓

Run VT B
```

Later

Database responds.

```
Mount VT A again

↓

Continue
```

Huge scalability improvement.

---

# How many Virtual Threads?

You can create

```
Millions
```

depending on available memory.

Unlike platform threads,

they have much smaller footprints because their stacks grow on demand and are managed by the JVM.

---

# Performance Example

Traditional

```
10,000 Requests

↓

Need thousands of threads

↓

Large memory usage

↓

Heavy context switching
```

Virtual Threads

```
10,000 Virtual Threads

↓

Few hundred Platform Threads

↓

Lower memory

↓

Less context switching
```

---

# Are Virtual Threads faster?

Interview trick.

Most people answer

```
Yes
```

Wrong.

Correct answer:

> **Virtual Threads do not make your code execute faster. They improve scalability.**

Example

Database query

```
3 seconds
```

Platform Thread

```
3 sec
```

Virtual Thread

```
3 sec
```

Same.

The database is still the bottleneck.

What improves is the ability to handle many concurrent requests without needing thousands of OS threads.

---

# When should you use Virtual Threads?

Excellent for

- REST APIs
    
- Database calls
    
- HTTP clients
    
- Kafka consumers (I/O-heavy processing)
    
- File I/O
    
- Network operations
    
- Microservices
    

Basically

```
I/O Bound
```

workloads.

---

# When should you NOT use Virtual Threads?

Suppose

```java
while(true){

    calculatePrimeNumbers();

}
```

CPU is always busy.

No waiting.

Virtual threads cannot help.

Better to use a fixed-size thread pool.

These are

```
CPU Bound
```

tasks.

---

# Pinning (Very Important Interview Topic)

Virtual threads can temporarily lose their scalability advantage if they become **pinned**.

Pinned means:

```
Virtual Thread

↓

Cannot unmount

↓

Keeps Platform Thread occupied
```

Common causes:

```java
synchronized(lock) {

    blockingCall();

}
```

or certain native/JNI operations.

Because the JVM cannot safely move the virtual thread while it's in that critical section, the platform thread remains occupied.

Better approach:

```java
ReentrantLock lock = new ReentrantLock();

lock.lock();

try {

    blockingCall();

} finally {

    lock.unlock();

}
```

`ReentrantLock` is generally friendlier to virtual threads because the JVM has more flexibility around parking and scheduling.

---

# Real Spring Boot Example

Imagine

```
GET /dashboard
```

Workflow

```
Database

↓

Redis

↓

Recommendation Service

↓

Payment Service
```

Every step waits on I/O.

Virtual threads allow each request to be written in a straightforward blocking style while scaling to many concurrent requests because waiting virtual threads don't permanently occupy platform threads.

---

# Platform Thread vs Virtual Thread

|Platform Thread|Virtual Thread|
|---|---|
|Managed by OS|Managed by JVM|
|Expensive|Lightweight|
|One Java thread ↔ One OS thread|Many virtual threads share platform threads|
|Higher memory usage|Much lower memory usage|
|Good for CPU-bound work|Excellent for I/O-bound work|
|Limited in number|Can create very large numbers|

---

# Frequently Asked Interview Questions

## 1. Are Virtual Threads asynchronous?

**No.**

Your code is still written in a synchronous, sequential style.

The concurrency improvement comes from the JVM's scheduler, not from callbacks or reactive programming.

---

## 2. Do Virtual Threads replace `CompletableFuture`?

**Not completely.**

- Virtual Threads simplify many blocking I/O workflows.
    
- `CompletableFuture` is still valuable when you need to compose multiple independent tasks, run work in parallel, or build asynchronous pipelines.
    

For example, aggregating results from three independent services is still a great fit for `CompletableFuture.thenCombine()` or `allOf()`.

---

## 3. Do Virtual Threads replace Thread Pools?

For many **I/O-bound request-per-task** workloads, yes—you can often use:

```java
Executors.newVirtualThreadPerTaskExecutor();
```

instead of a fixed thread pool.

For **CPU-bound** work, a bounded platform-thread pool is still the better choice.

---

## 4. Are Virtual Threads daemon threads?

No. They behave like normal threads in terms of lifecycle, but they're scheduled differently by the JVM.

---

# SDE-2 Interview Cheat Sheet

If the interviewer asks:

> **What problem do Virtual Threads solve?**

A strong answer is:

> Traditional Java uses one OS thread per Java thread, which becomes expensive when many threads spend most of their time blocked on I/O. Virtual Threads are lightweight JVM-managed threads that can be unmounted while waiting and later remounted onto a platform thread. This allows applications to handle a much larger number of concurrent I/O-bound tasks without requiring thousands of operating-system threads. They improve scalability, not the execution speed of individual operations.


Excellent question. The answer is:

> **No, not at the repository level.** You don't make `findById()` use a virtual thread. Instead, you run the **entire request (or task)** on a virtual thread. Then `findById()` automatically executes on that virtual thread.

Let's understand how it works.

---

# Traditional Spring Boot

Suppose you have:

```java
@RestController
public class UserController {

    @GetMapping("/user/{id}")
    public User getUser(@PathVariable Long id) {

        return userRepository.findById(id)
                .orElseThrow();
    }
}
```

Normally:

```text
HTTP Request

↓

Tomcat Worker Thread (Platform Thread)

↓

Controller

↓

Service

↓

Repository

↓

Database

↓

Response
```

When `findById()` sends the SQL query,

```text
Thread

↓

Waiting for DB

↓

Blocked
```

The Tomcat thread remains occupied.

---

# With Virtual Threads

The flow becomes:

```text
HTTP Request

↓

Virtual Thread

↓

Controller

↓

Service

↓

Repository.findById()

↓

Database

↓

Response
```

When the JDBC driver performs a blocking database operation:

```text
Virtual Thread

↓

Waiting for DB
```

The JVM can **park (unmount)** the virtual thread.

```text
Virtual Thread parked

↓

Platform Thread released

↓

Runs another Virtual Thread
```

When the database responds:

```text
Platform Thread

↓

Resumes (mounts) Virtual Thread

↓

Continue execution
```

Notice that **your repository code did not change at all**.

---

# So do I change `findById()`?

No.

You still write:

```java
User user = userRepository.findById(id)
        .orElseThrow();
```

Exactly the same.

The repository has **no idea** whether it's running on:

- a platform thread, or
    
- a virtual thread.
    

It simply runs on the current thread.

---

# What actually changes?

Instead of:

```text
Request

↓

Platform Thread
```

you configure Spring Boot so that:

```text
Request

↓

Virtual Thread
```

Everything underneath inherits that thread.

```
Controller

↓

Service

↓

Repository

↓

JDBC

↓

Database
```

All execute on the same virtual thread.

---

# How do we enable Virtual Threads in Spring Boot?

If you're using **Spring Boot 3.2+** with **Java 21+**, it's surprisingly easy.

Just add:

```properties
spring.threads.virtual.enabled=true
```

to your `application.properties`.

That's it.

Spring Boot configures the embedded web server (Tomcat/Jetty, etc.) to handle incoming requests using virtual threads.

Now every HTTP request gets its own virtual thread.

---

# Do I need `@Async`?

Not for normal request processing.

Example:

```java
@GetMapping("/user")
public User getUser() {

    return userRepository.findById(1L)
            .orElseThrow();
}
```

This already runs on a virtual thread (if virtual threads are enabled).

No `@Async` required.

---

# What if I create my own Executor?

Then **you** choose whether to use virtual threads.

Platform thread executor:

```java
ExecutorService executor =
        Executors.newFixedThreadPool(10);
```

Virtual thread executor:

```java
ExecutorService executor =
        Executors.newVirtualThreadPerTaskExecutor();
```

If you submit work to the second executor, that work runs on virtual threads.

---

# Important Point About JDBC

You might wonder:

> **JDBC is blocking. Doesn't that defeat the purpose?**

Actually, **Virtual Threads were designed for blocking APIs like JDBC.**

Example:

```java
userRepository.findById(1L);
```

The JDBC driver blocks while waiting for the database.

With platform threads:

```text
Platform Thread

↓

Blocked for 2 seconds
```

With virtual threads:

```text
Virtual Thread

↓

Blocked

↓

JVM parks it

↓

Platform Thread reused
```

So **you keep the simple blocking programming model**, but gain much better scalability.

---

# What if I'm using Hibernate/JPA?

Same answer.

```java
userRepository.findById(id);
```

Internally:

```text
Repository

↓

Hibernate

↓

JDBC

↓

Database
```

Nothing changes in your code.

The entire call stack simply runs on a virtual thread.

---

# Interview Question

**Q: Do I need to change my repository code to use Virtual Threads?**

**Answer:**

No. Repository methods like `findById()` remain unchanged. Virtual Threads are enabled at the thread or server level. Once a request is executing on a virtual thread, all downstream code—including controllers, services, repositories, Hibernate, and JDBC—runs on that same virtual thread automatically. The benefit is that when the code blocks on I/O, the JVM can park the virtual thread and free the underlying platform thread for other work.

---

## One important caveat

Virtual Threads **don't make the database faster**.

Suppose:

```text
Database query = 2 seconds
```

With a platform thread:

```text
Thread blocked for 2 seconds
```

With a virtual thread:

```text
Virtual Thread waits for 2 seconds
```

The query still takes **2 seconds**.

The advantage is that while one virtual thread is waiting, the underlying platform thread can execute other virtual threads, allowing your application to handle many more concurrent requests efficiently.


Great. The next topic is another major Java 21 feature that is closely related to Virtual Threads.

# Module 8 - Part 2: Structured Concurrency

**Interview Importance:** ⭐⭐⭐⭐☆ (Increasingly important for Java 21+)

Typical interview questions:

- What is Structured Concurrency?
    
- Why was it introduced?
    
- How is it different from `CompletableFuture`?
    
- What problem does it solve?
    
- When should I use it?
    

---

# Why was Structured Concurrency introduced?

Let's start with a real backend example.

Suppose your Dashboard API needs data from three services.

```
User Service

Order Service

Wallet Service
```

Without concurrency:

```
Fetch User (500ms)

↓

Fetch Orders (600ms)

↓

Fetch Wallet (400ms)

Total = 1500ms
```

Too slow.

Naturally, we run them in parallel.

---

## Traditional CompletableFuture Solution

```java
CompletableFuture<User> user =
        CompletableFuture.supplyAsync(this::fetchUser);

CompletableFuture<List<Order>> orders =
        CompletableFuture.supplyAsync(this::fetchOrders);

CompletableFuture<Wallet> wallet =
        CompletableFuture.supplyAsync(this::fetchWallet);

CompletableFuture.allOf(user, orders, wallet).join();

return new Dashboard(
        user.join(),
        orders.join(),
        wallet.join());
```

Works perfectly.

But what happens if

```
Order Service
```

fails?

Questions arise:

- Should the other tasks continue?
    
- Who cancels them?
    
- Who waits for them?
    
- What if one hangs forever?
    
- What if the parent request is cancelled?
    

Managing all this quickly becomes complicated.

---

# The Core Problem

Imagine your API request creates three child tasks.

```
HTTP Request

      │

      ▼

 Parent Task

 ┌────┼────┐

 ▼    ▼    ▼

User Orders Wallet
```

Now suppose:

```
Orders

↓

Throws Exception
```

Should

```
User

Wallet
```

continue?

With `CompletableFuture`, **you must decide and implement this yourself**.

There is no automatic parent-child relationship.

---

# What is Structured Concurrency?

Structured Concurrency introduces the idea that:

> **Child tasks belong to a parent task.**

When the parent finishes,

all children must also finish.

Just like method calls.

---

Think of normal Java methods.

```java
public void process() {

    step1();

    step2();

    step3();
}
```

When

```
process()
```

returns,

you know

```
step1

step2

step3
```

have completed.

No loose threads remain.

Structured Concurrency brings the same discipline to concurrent tasks.

---

# Parent-Child Relationship

Instead of

```
Independent Tasks
```

we now have

```
Parent

├── Child 1

├── Child 2

└── Child 3
```

The parent owns the children.

If the parent exits,

the children cannot continue running in the background.

This makes concurrent code much easier to reason about.

---

# Introducing StructuredTaskScope

Java 21 (Preview)

Main class:

```java
StructuredTaskScope
```

Think of it as

```
ExecutorService

+

Automatic Task Management
```

---

# Basic Example

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {

    Subtask<User> user =
            scope.fork(this::fetchUser);

    Subtask<List<Order>> orders =
            scope.fork(this::fetchOrders);

    Subtask<Wallet> wallet =
            scope.fork(this::fetchWallet);

    scope.join();

    return new Dashboard(
            user.get(),
            orders.get(),
            wallet.get());
}
```

Notice

No `CompletableFuture`.

No `allOf()`.

No manual executor.

Everything belongs to one scope.

---

# What does `fork()` do?

```java
scope.fork(this::fetchUser);
```

means

```
Start Child Task

↓

Execute Concurrently

↓

Attach to Parent Scope
```

Unlike `CompletableFuture`, the task cannot "escape" the scope.

---

# What does `join()` do?

```
Parent

↓

Wait

↓

All Child Tasks Finish

↓

Continue
```

Very similar to

```
CompletableFuture.allOf()
```

But the scope also manages task lifetime.

---

# ShutdownOnFailure

One of the biggest benefits.

Suppose

```
User

Orders

Wallet
```

run concurrently.

Timeline

```
User

Running

Orders

Exception

Wallet

Running
```

With

```java
StructuredTaskScope.ShutdownOnFailure
```

this happens automatically:

```
Orders Failed

↓

Cancel User

↓

Cancel Wallet

↓

Throw Exception
```

No manual cancellation code.

---

# Compare with CompletableFuture

Without Structured Concurrency

```
User

Orders

Wallet

↓

Orders fails

↓

User keeps running

Wallet keeps running
```

Waste of resources.

---

With Structured Concurrency

```
User

Orders

Wallet

↓

Orders fails

↓

Everything cancelled
```

Cleaner.

---

# ShutdownOnSuccess

Another useful scope.

Suppose you have

```
Server A

Server B

Server C
```

Need

```
First successful response
```

Use

```java
StructuredTaskScope.ShutdownOnSuccess<String>
```

Execution

```
A Running

B Running

C Running

↓

B Succeeds

↓

Cancel A

↓

Cancel C

↓

Return B
```

Very similar to

```
CompletableFuture.anyOf()
```

but with automatic cancellation.

---

# Parent Cancellation

Imagine the client disconnects.

```
HTTP Request

↓

Cancelled
```

With Structured Concurrency

```
Parent Cancelled

↓

Cancel Every Child
```

With raw `CompletableFuture`

You often need to implement this propagation yourself.

---

# Exception Handling

Suppose

```
User Service

↓

Exception
```

With `ShutdownOnFailure`

```
Exception

↓

Cancel Remaining Tasks

↓

Propagate Error
```

No extra code.

---

# Relationship with Virtual Threads

These two features were designed to work together.

Usually

```
One HTTP Request

↓

One Virtual Thread

↓

StructuredTaskScope

↓

Many Child Virtual Threads
```

Each child is lightweight.

If one fails,

the scope handles cleanup automatically.

---

# Real Spring Boot Example

Suppose

```
GET /dashboard
```

Needs

```
Profile

Orders

Wallet

Coupons
```

Implementation

```
Virtual Thread

↓

StructuredTaskScope

├── Profile

├── Orders

├── Wallet

└── Coupons

↓

Join

↓

Return Dashboard
```

Simple synchronous code.

High concurrency.

Automatic cancellation.

---

# Structured Concurrency vs CompletableFuture

|CompletableFuture|Structured Concurrency|
|---|---|
|Independent tasks|Parent-child tasks|
|Manual cancellation|Automatic cancellation|
|Easy to leak background work|Scope guarantees cleanup|
|Callback chaining|Sequential style|
|Great for async pipelines|Great for request-scoped parallel work|

---

# When should you use Structured Concurrency?

Excellent for

- Dashboard aggregation
    
- Calling multiple microservices
    
- Parallel database queries
    
- Request-scoped parallel work
    
- API composition
    

---

# When is CompletableFuture still better?

Suppose

```
Task A

↓

Task B depends on A

↓

Task C depends on B
```

or

```
Task

↓

thenCompose()

↓

thenApply()

↓

exceptionally()
```

Complex asynchronous pipelines are still a natural fit for `CompletableFuture`.

---

# Virtual Threads vs Structured Concurrency

This is a favorite interview question.

### Virtual Threads answer

They solve

```
How tasks are executed.
```

They provide lightweight threads.

---

### Structured Concurrency answer

It solves

```
How concurrent tasks are organized and managed.
```

It provides parent-child relationships, cancellation, and scoped lifetimes.

---

# Virtual Threads + Structured Concurrency

Together

```
HTTP Request

↓

Virtual Thread (Parent)

↓

StructuredTaskScope

├── Virtual Thread 1

├── Virtual Thread 2

├── Virtual Thread 3

↓

Join

↓

Return Response
```

This is the modern Java concurrency model envisioned by Project Loom.

---

# Interview Questions

### 1. Is Structured Concurrency a replacement for `CompletableFuture`?

No.

- Use **Structured Concurrency** for request-scoped parallel work with related child tasks.
    
- Use **CompletableFuture** for asynchronous composition, pipelines, and APIs that naturally expose futures.
    

---

### 2. Why is it called "Structured"?

Because concurrent tasks follow a clear lexical scope, just like method calls. Child tasks cannot outlive the scope in which they were created.

---

### 3. Does Structured Concurrency require Virtual Threads?

No.

It works with platform threads too.

However, it is **most effective when combined with Virtual Threads**, because creating many child tasks becomes inexpensive.

---

# SDE-2 Cheat Sheet

If an interviewer asks:

> **What is Structured Concurrency?**

A strong answer is:

> Structured Concurrency is a Java concurrency model introduced with Project Loom that organizes concurrent tasks into a parent-child hierarchy. Child tasks are created within a scope, and the parent waits for them to finish before exiting. It provides automatic cancellation, exception propagation, and lifecycle management, making concurrent code easier to understand and less error-prone than managing independent `CompletableFuture`s. It pairs naturally with Virtual Threads for highly scalable, request-oriented applications.


The final topic in **Modern Java Concurrency** is:

# Module 8 - Part 3: Scoped Values (Java 21)

**Interview Importance:** ⭐⭐⭐⭐☆ (Growing, especially for Java 21+)

This is the **replacement for many ThreadLocal use cases** in the Virtual Thread era.

---

## Why do we need Scoped Values?

To understand Scoped Values, we first need to understand the problem with `ThreadLocal`.

Suppose in a Spring Boot application:

```text
HTTP Request

↓

Controller

↓

Service

↓

Repository
```

Every layer needs the current user's information.

Without passing it around:

```java
service.doWork(userId);
```

↓

```java
repository.save(userId);
```

↓

```java
audit(userId);
```

You'd have to pass `userId` through every method.

Instead, people used:

```java
ThreadLocal<User> currentUser = new ThreadLocal<>();
```

---

### Example

```java
public class Context {

    static ThreadLocal<String> user =
            new ThreadLocal<>();

}
```

Controller

```java
Context.user.set("Umesh");
```

Service

```java
String name = Context.user.get();
```

Repository

```java
String name = Context.user.get();
```

No need to pass parameters.

---

## Why is ThreadLocal a Problem?

### 1. Memory Leaks

Suppose you're using a thread pool.

```
Thread Pool

Thread-1

↓

Request A

↓

ThreadLocal = Umesh
```

Request finishes.

The thread is **reused**.

```
Thread-1

↓

Request B
```

If you forgot:

```java
threadLocal.remove();
```

Request B may accidentally see Request A's data.

This is a classic source of bugs.

---

### 2. Mutable State

```java
threadLocal.set("Alice");
threadLocal.set("Bob");
threadLocal.set("Charlie");
```

Any code can modify it.

Hard to reason about.

---

### 3. Virtual Threads

With millions of virtual threads,

`ThreadLocal` becomes less attractive because:

- Every thread carries its own mutable state.
    
- Context propagation becomes more complicated.
    
- Mutable per-thread state doesn't fit well with the structured, immutable style encouraged by Project Loom.
    

---

# Enter Scoped Values

A Scoped Value is:

> **An immutable value that is available only within a specific execution scope.**

Think of it as

```
ThreadLocal

+

Immutable

+

Automatic cleanup

+

Works naturally with Virtual Threads
```

---

# Creating a Scoped Value

```java
static final ScopedValue<String> USER =
        ScopedValue.newInstance();
```

Notice

No

```java
set()
```

No

```java
remove()
```

---

# Binding a Value

```java
ScopedValue.where(USER, "Umesh")
           .run(() -> {

               process();

           });
```

Inside

```java
process();
```

You can access

```java
USER.get();
```

---

Example

```java
static final ScopedValue<String> USER =
        ScopedValue.newInstance();

public static void main(String[] args) {

    ScopedValue.where(USER, "Umesh")
               .run(() -> {

                   System.out.println(USER.get());

               });

}
```

Output

```
Umesh
```

---

# Scope Ends Automatically

```
ScopedValue.where(USER, "Umesh")
           .run(() -> {

               process();

           });

Outside
```

Now

```java
USER.get();
```

throws an exception because the value is **no longer bound**.

No cleanup required.

---

# Immutability

Unlike ThreadLocal

```java
threadLocal.set("Alice");

threadLocal.set("Bob");
```

Scoped Values

```java
ScopedValue.where(USER, "Umesh")
```

Cannot be modified.

Once bound,

the value stays the same for that scope.

This makes concurrent code safer.

---

# Scope Hierarchy

Suppose

```
Parent Scope

↓

USER = Umesh
```

Child method

```java
process();
```

can read

```
USER.get()
```

because it inherits the binding.

---

# Real Spring Boot Example

Suppose

```
HTTP Request

↓

Authentication Filter

↓

Controller

↓

Service

↓

Repository
```

Authentication

```java
ScopedValue.where(USER, authenticatedUser)
```

Everything inside that request can access

```java
USER.get();
```

No parameter passing.

No ThreadLocal.

Automatic cleanup.

---

# Scoped Values + Virtual Threads

Suppose

```
Request

↓

Virtual Thread

↓

ScopedValue

↓

Controller

↓

Service

↓

Repository
```

The context naturally follows the execution.

No manual propagation.

---

# Scoped Values + Structured Concurrency

Even better.

```
Parent Scope

USER = Umesh

↓

StructuredTaskScope

├── Child 1

├── Child 2

└── Child 3
```

All child tasks automatically inherit the scoped value.

Each child can call

```java
USER.get();
```

No copying.

No extra code.

---

# ThreadLocal vs ScopedValue

|ThreadLocal|ScopedValue|
|---|---|
|Mutable|Immutable|
|Manual cleanup|Automatic cleanup|
|Can leak|Scope-bound|
|`set()` / `remove()`|`where(...).run()`|
|Better for legacy code|Better for Virtual Threads|

---

# When should you use Scoped Values?

Excellent for:

- Current authenticated user
    
- Correlation ID
    
- Request ID
    
- Tenant ID
    
- Locale
    
- Trace ID
    

Basically,

**read-only request context**.

---

# When NOT to use Scoped Values?

Don't use them for:

- Counters
    
- Mutable caches
    
- Session state that changes
    
- Frequently updated values
    

They're designed for **immutable contextual data**, not shared mutable state.

---

# Modern Java Concurrency Stack

```
Virtual Threads
        │
        ▼
Run millions of lightweight tasks

        │
        ▼
Structured Concurrency
        │
Manage related concurrent tasks

        │
        ▼
Scoped Values
        │
Share immutable request context safely
```

These three features together form the foundation of **Project Loom**.

---

# Interview Questions

### 1. Why were Scoped Values introduced?

To provide a safer, immutable, and scope-bound alternative to many `ThreadLocal` use cases, especially for Virtual Threads.

---

### 2. Do Scoped Values replace ThreadLocal completely?

No.

- Use **Scoped Values** for immutable context (user ID, trace ID, tenant ID).
    
- Keep `ThreadLocal` for cases that genuinely require mutable per-thread state, though those cases are becoming less common.
    

---

### 3. Can child tasks access Scoped Values?

Yes.

Child tasks created within the scope inherit the binding automatically, which works especially well with Structured Concurrency.

---

# Complete Java Concurrency Roadmap ✅

You've now covered the major Java concurrency topics expected for a modern Java/Spring Boot SDE-2 interview:

1. **Thread Basics**
    
2. **Synchronization**
    
3. **Locks (`ReentrantLock`, `ReadWriteLock`, `StampedLock`)**
    
4. **Thread Communication (`wait`, `notify`, `Condition`)**
    
5. **Atomic Classes & CAS**
    
6. **Concurrent Collections**
    
7. **Executor Framework & `CompletableFuture`**
    
8. **Modern Java Concurrency**
    
    - ✅ Virtual Threads
        
    - ✅ Structured Concurrency
        
    - ✅ Scoped Values
        

At this point, you're well prepared for the concurrency questions commonly asked in Java 17/21 backend interviews at companies using modern Spring Boot and Project Loom.











