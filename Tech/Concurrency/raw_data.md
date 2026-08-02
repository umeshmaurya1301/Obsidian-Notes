Yes, I understand exactly what you want.

You **don't** want examples that already introduce race conditions, synchronization, locks, or advanced concurrency.

You want to first build an intuition for:

* What is a `Thread`?
* What is a `Runnable`?
* What does `start()` actually do?
* What happens if we call `run()` directly?
* Why do we even need `Runnable` if `Thread` already exists?
* What mistakes beginners make with `Thread` and `Runnable`.

That's actually the right order.

---

# Learning Roadmap

## Example 1 — Normal Java Program (No Threads)

Understand that everything runs on the **main thread**.

```java
public class Main {

    public static void main(String[] args) {

        System.out.println("Step 1");
        System.out.println("Step 2");
        System.out.println("Step 3");
    }
}
```

Question:

* How many threads are running?
* Answer: Only the `main` thread.

---

# Example 2 — Extending Thread

```java
class MyThread extends Thread {

    @Override
    public void run() {
        System.out.println("Child Thread");
    }
}

public class Main {

    public static void main(String[] args) {

        MyThread t = new MyThread();

        t.start();

        System.out.println("Main Thread");
    }
}
```

Learn:

* `run()` contains the task.
* `start()` creates a **new thread**.
* JVM eventually calls `run()` on that new thread.

---

# Example 3 — What `start()` Actually Does

```java
class MyThread extends Thread {

    @Override
    public void run() {

        System.out.println(
                Thread.currentThread().getName());
    }
}

public class Main {

    public static void main(String[] args) {

        MyThread t = new MyThread();

        t.start();

        System.out.println(
                Thread.currentThread().getName());
    }
}
```

Possible Output

```
main
Thread-0
```

Question:
Who executed `run()`?

Answer:
`Thread-0`

---

# Example 4 — Calling `run()` Directly

```java
class MyThread extends Thread {

    @Override
    public void run() {

        System.out.println(
                Thread.currentThread().getName());
    }
}

public class Main {

    public static void main(String[] args) {

        MyThread t = new MyThread();

        t.run();
    }
}
```

Output

```
main
```

Notice:

No new thread was created.

`run()` became just another normal method call.

---

# Example 5 — `run()` vs `start()`

```java
class MyThread extends Thread {

    @Override
    public void run() {

        System.out.println(
                "Running on "
                + Thread.currentThread().getName());
    }
}

public class Main {

    public static void main(String[] args) {

        MyThread t = new MyThread();

        // t.run();

        t.start();
    }
}
```

Output if using `run()`

```
Running on main
```

Output if using `start()`

```
Running on Thread-0
```

This is probably **the most asked interview question**.

---

# Example 6 — Calling `start()` Twice

```java
class MyThread extends Thread {

    @Override
    public void run() {

        System.out.println("Running...");
    }
}

public class Main {

    public static void main(String[] args) {

        MyThread t = new MyThread();

        t.start();

        t.start();
    }
}
```

Output

```
Running...

Exception in thread "main"

java.lang.IllegalThreadStateException
```

Question:
Why?

Answer:

A `Thread` object represents one execution.

Once started, it cannot be started again.

Create a new `Thread` object instead.

---

# Example 7 — Runnable

```java
class MyTask implements Runnable {

    @Override
    public void run() {

        System.out.println("Task Executing");
    }
}

public class Main {

    public static void main(String[] args) {

        Runnable task = new MyTask();

        Thread t = new Thread(task);

        t.start();
    }
}
```

Learn:

`Runnable` only defines **what work should be done**.

`Thread` decides **where that work runs**.

---

# Example 8 — Calling Runnable's `run()` Directly

```java
class MyTask implements Runnable {

    @Override
    public void run() {

        System.out.println(
                Thread.currentThread().getName());
    }
}

public class Main {

    public static void main(String[] args) {

        Runnable task = new MyTask();

        task.run();
    }
}
```

Output

```
main
```

Again,

No thread was created.

---

# Example 9 — Runnable with Thread

```java
class MyTask implements Runnable {

    @Override
    public void run() {

        System.out.println(
                Thread.currentThread().getName());
    }
}

public class Main {

    public static void main(String[] args) {

        Runnable task = new MyTask();

        Thread t = new Thread(task);

        t.start();
    }
}
```

Output

```
Thread-0
```

---

# Example 10 — One Runnable, Multiple Threads

```java
class MyTask implements Runnable {

    @Override
    public void run() {

        System.out.println(
                Thread.currentThread().getName()
                + " is executing the task");
    }
}

public class Main {

    public static void main(String[] args) {

        Runnable task = new MyTask();

        Thread t1 = new Thread(task, "Payment");
        Thread t2 = new Thread(task, "Settlement");

        t1.start();
        t2.start();
    }
}
```

Possible Output

```
Payment is executing the task
Settlement is executing the task
```

This shows that the **same task** (`Runnable`) can be executed by multiple threads.

---

# Example 11 — A Common Beginner Mistake

```java
Runnable task = new MyTask();

Thread t = new Thread(task);

task.run();
```

Question:

Did we create a new thread?

No.

Output

```
main
```

Why?

Because we called `run()` ourselves.

---

# Example 12 — Another Common Mistake

```java
Runnable task = new MyTask();

Thread t = new Thread(task);

// Forgot to call start()
```

Output

```
Nothing happens.
```

Reason:

Creating a `Thread` object does **not** start execution. The thread begins only when `start()` is invoked.

---

# Before Moving to Synchronization, You Should Clearly Understand

You should be able to answer these confidently:

1. What is a `Thread` object?
2. What is a `Runnable` object?
3. Why does `start()` create a new thread but `run()` doesn't?
4. Why can `start()` be called only once?
5. Can I call `run()` directly? (Yes, but it's just a normal method call.)
6. Why is `Runnable` preferred over extending `Thread`?
7. Can multiple `Thread` objects execute the same `Runnable` instance? (Yes.)

Once these concepts are clear, the next natural step is to see **what goes wrong when multiple threads access the same data**, which leads into synchronization and related concurrency topics.
