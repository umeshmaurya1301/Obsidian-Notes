---
created: 2026-08-30 00:00
tags:
  - dsa
  - greedy
  - heap
  - dynamic-programming
source: https://leetcode.com/problems/course-schedule-iii/
problem_id: "630"
difficulty: Hard
status: Solved
review_date:
---
# LT_0630 – Course Schedule III

**Link:** [Open Problem](https://leetcode.com/problems/course-schedule-iii/)

---

## 📝 Problem Description
> [!info]
> There are `n` different online courses numbered from `1` to `n`. You are given an array `courses` where `courses[i] = [duration_i, lastDay_i]` indicate that the `i`th course should be taken continuously for `duration_i` days and must be finished before or on `lastDay_i`.
>
> You will start on the 1st day and you cannot take two or more courses simultaneously.
>
> Return the maximum number of courses that you can take.

---

## 🧪 Examples
> [!example]
> **Input:** `courses = [[100,200],[200,1300],[1000,1250],[2000,3200]]`
> **Output:** `3`
> **Explanation:** There are totally 4 courses, but you can take 3 courses at most. First, take the 1st course, it costs 100 days so you will finish it on the 100th day, and ready to take the next course on the 101st day. Second, take the 3rd course, it costs 1000 days so you will finish it on the 1100th day, and ready to take the next course on the 1101st day. Third, take the 2nd course, it costs 200 days so you will finish it on the 1300th day. The 4th course cannot be taken now, since you will finish it on the 3300th day, which exceeds the closed date.

> [!example]
> **Input:** `courses = [[1,2]]`
> **Output:** `1`

> [!example]
> **Input:** `courses = [[3,2],[4,3]]`
> **Output:** `0`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= courses.length <= 10^4`
> - `1 <= duration_i, lastDay_i <= 10^4`

---

## 🔍 Intuition

Sorting by `lastDay` turns this into a "how many jobs fit" problem, but greedily taking every course that fits isn't safe — a short-but-late-deadline course taken early can crowd out two shorter courses that would've fit later. The fix is the classic exchange-argument trick: keep a max-heap of the durations of courses **currently accepted**. When a new course doesn't fit, check whether it's shorter than the longest course already accepted — if so, swapping it in keeps the *count* of accepted courses the same while strictly shrinking total time used, which can only help future courses fit. The DP formulation (take/skip on `(index, time-used)`, sorted by deadline) proves the same idea correct from first principles, but its state space is bounded by the largest `lastDay`, so it blows up for the given constraints — the greedy sidesteps that because it only ever needs the running total time and the current best selection, not every possible time value.

> 🟢 *Greedy Exchange Argument + Max-Heap*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Top-Down Memoized DP (Take / Skip on Sorted Courses)

**Why this works:**
- Sorting by `lastDay` first means course `i` can only ever be considered after every course with an earlier deadline has already been decided, so the recursion never needs to "go back" and reconsider an earlier course.
- State `(i, time)` fully captures the subproblem: given we're about to decide on course `i` having already spent `time` days, the best achievable count from here on is deterministic — hence it's safe to memoize.
- At each course the recursion tries both `taken` (only legal if `time + duration <= lastDay`) and `not_taken`, and keeps the max — a textbook 0/1 knapsack-style decision.

**Dry Run** (`courses = [[100,200],[200,1300],[1000,1250],[2000,3200]]`, sorted by `lastDay` → `[[100,200],[1000,1250],[200,1300],[2000,3200]]`):
```
schedule(i=0, time=0)    courses[0]=[100,200]
  taken: 0+100=100 <= 200  →  1 + schedule(1, 100)

schedule(i=1, time=100)  courses[1]=[1000,1250]
  taken: 100+1000=1100 <= 1250  →  1 + schedule(2, 1100)

schedule(i=2, time=1100) courses[2]=[200,1300]
  taken: 1100+200=1300 <= 1300  →  1 + schedule(3, 1300)

schedule(i=3, time=1300) courses[3]=[2000,3200]
  taken:     1300+2000=3300 > 3200  →  not eligible, taken=0
  not_taken: schedule(4, 1300) = 0   (i == courses.length)
  memo[3][1300] = max(0, 0) = 0

schedule(2,1100) taken-branch = 1 + 0 = 1
schedule(1,100)  taken-branch = 1 + 1 = 2
schedule(0,0)    taken-branch = 1 + 2 = 3  ✅

(the not_taken branch at every level is also explored and memoized,
 but the taken path above is the one that wins the max())
```

```java
public class Solution {
    public int scheduleCourse(int[][] courses) {
        Arrays.sort(courses, (a, b) -> a[1] - b[1]);
        Integer[][] memo = new Integer[courses.length][courses[courses.length - 1][1] + 1];
        return schedule(courses, 0, 0, memo);
    }
    public int schedule(int[][] courses, int i, int time, Integer[][] memo) {
        if (i == courses.length)
            return 0;
        if (memo[i][time] != null)
            return memo[i][time];
        int taken = 0;
        if (time + courses[i][0] <= courses[i][1])
            taken = 1 + schedule(courses, i + 1, time + courses[i][0], memo);
        int not_taken = schedule(courses, i + 1, time, memo);
        memo[i][time] = Math.max(taken, not_taken);
        return memo[i][time];
    }
}
```

- **Time:** `O(n * maxLastDay)` · **Space:** `O(n * maxLastDay)` (memo table) `+ O(n)` (recursion stack)

### ✅ Solution 2 — Greedy + Max-Heap

**Why this works:**
- Processing courses in `lastDay` order means every decision only ever has to satisfy deadlines seen so far — a course accepted now will never later be invalidated by an earlier-deadline course showing up.
- The max-heap holds the durations of currently-accepted courses; `queue.peek()` is always the single most "expensive" pick so far, i.e. the best candidate to evict if a cheaper option appears.
- Swapping the longest accepted duration for a shorter new one (`queue.peek() > c[0]`) keeps the accepted **count** unchanged while strictly reducing `time`, which can only make it easier for later, tighter-deadline courses to fit — this is the exchange argument that makes the greedy optimal.

**Dry Run** (`courses = [[100,200],[200,1300],[1000,1250],[2000,3200]]`, sorted by `lastDay` → `[[100,200],[1000,1250],[200,1300],[2000,3200]]`):
```
time=0, queue=[]

c=[100,200]:   0+100=100  <= 200   → fits.  queue=[100],        time=100
c=[1000,1250]: 100+1000=1100 <= 1250 → fits.  queue=[1000,100],  time=1100
c=[200,1300]:  1100+200=1300 <= 1300 → fits.  queue=[1000,200,100], time=1300
c=[2000,3200]: 1300+2000=3300 > 3200 → doesn't fit.
               queue.peek()=1000, not > 2000 → no swap. queue unchanged.

return queue.size() = 3  ✅
```

```java
public class Solution {
    public int scheduleCourse(int[][] courses) {
        Arrays.sort(courses, (a, b) -> a[1] - b[1]);
        PriorityQueue<Integer> queue = new PriorityQueue<>((a, b) -> b - a);
        int time = 0;
        for (int[] c: courses) {
            if (time + c[0] <= c[1]) {
                queue.offer(c[0]);
                time += c[0];
            } else if (!queue.isEmpty() && queue.peek() > c[0]) {
                time += c[0] - queue.poll();
                queue.offer(c[0]);
            }
        }
        return queue.size();
    }
}
```

- **Time:** `O(n log n)` (sort `+` up to `n` heap pushes/pops) · **Space:** `O(n)` (heap)

---

## 🔑 Key Insights
- Sorting by `lastDay` is what makes both solutions valid — the DP recursion assumes decisions are made in deadline order, and the greedy swap is only a sound trade when every future course has a deadline at least as late as the current one.
- The heap swap (`time += c[0] - queue.poll()`) is the whole trick: it never changes how many courses are accepted, only shrinks the total time spent, which is a pure win for future feasibility.
- The DP is provably correct but its `(index, time)` state space scales with `maxLastDay`, not just `n` — at the given constraints (`n, lastDay <= 10^4`) that's up to `10^8` states, so the greedy is the one to actually reach for.

---

## ⚠️ Pitfalls
> [!warning]
> - Skipping the sort, or sorting by `duration` instead of `lastDay` — both solutions are unsound on courses not ordered by deadline.
> - The fit check is `time + duration <= lastDay` (inclusive) — finishing exactly on the deadline day is allowed, so `<` would wrongly reject valid schedules.
> - In the greedy, the swap condition is strictly `queue.peek() > c[0]` — an equal-duration swap changes nothing, so there's no need (and no harm either way) to special-case it.

---

## ⏱️ Complexity
- **Time:** `O(n log n)`
- **Space:** `O(n)`
