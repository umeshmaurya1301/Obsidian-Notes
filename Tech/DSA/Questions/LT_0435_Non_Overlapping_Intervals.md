---
created: 2026-08-04 08:50
tags:
  - dsa
  - arrays
  - greedy
  - intervals
  - sorting
source: https://leetcode.com/problems/non-overlapping-intervals/
problem_id: "435"
difficulty: Medium
status: Solved
review_date:
---
# LT_0435 – Non-overlapping Intervals

**Link:** [Open Problem](https://leetcode.com/problems/non-overlapping-intervals/)

---

## 📝 Problem Description
> [!info]
> Given an array of intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the **minimum number of intervals you need to remove** to make the rest of the intervals **non-overlapping**.
>
> Note that intervals which only **touch** at a point are **non-overlapping** — e.g. `[1, 2]` and `[2, 3]` are non-overlapping.

---

## 🧪 Examples
> [!example]
> **Input:** `intervals = [[1,2],[2,3],[3,4],[1,3]]`
> **Output:** `1`
> **Explanation:** Remove `[1,3]` and the remaining intervals are non-overlapping.

> [!example]
> **Input:** `intervals = [[1,2],[1,2],[1,2]]`
> **Output:** `2`
> **Explanation:** You need to remove two `[1,2]` intervals so only one remains.

> [!example]
> **Input:** `intervals = [[1,2],[2,3]]`
> **Output:** `0`
> **Explanation:** Already non-overlapping — touching at `2` is allowed.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= intervals.length <= 10^5`
> - `intervals[i].length == 2`
> - `-5 * 10^4 <= start_i < end_i <= 5 * 10^4`

---

## 🔍 Intuition

The question asks for the **minimum removals**, but that is just the complement of a much friendlier question: **keep the maximum number of non-overlapping intervals**. If `n` intervals exist and I can keep `k`, the answer is `n - k`. This is classic **Activity Selection** in disguise.

Once I'm maximising *kept* intervals, every decision should preserve as much of the remaining timeline as possible. Given two candidate intervals I could take next, the one that **finishes earlier** is never worse — everything that fits after the later end also fits after the earlier end, plus possibly more. So I sort by **end time** and sweep left to right, greedily taking any interval whose start doesn't cut into the previously kept interval; everything else is a removal.

Brute force (try every subset, or DP over sorted intervals with binary search) is `O(n²)` or `O(n log n)` with extra machinery — the greedy gets the same answer with a single pass after sorting, and the exchange argument below is exactly what an interviewer wants to hear.

> 🟢 *Greedy — Interval Scheduling (sort by end time)*

---

## 🎯 Why "earliest end" and not "earliest start"

**Two overlapping intervals — only one can survive:**

```
A = [1,5]        1-----------5
B = [2,3]            2---3
```

Suppose `[3,4]` arrives later.

| Kept | Can `[3,4]` still fit? | Total kept |
|---|---|---|
| `A = [1,5]` | ❌ blocked until 5 | **1** |
| `B = [2,3]` | ✅ starts at 3 | **2** |

**Sorting by start actively fails:**

```
[1,100]
[2,3]
[3,4]
[4,5]
```

Sort by start → `[1,100]` comes first. Greedily keeping it kills all three others (kept = 1). Sort by end → `[2,3] [3,4] [4,5] [1,100]`, keeping 3 of 4.

> [!tip]
> **Mental model:** time is a road. `[1---80]` blocks a huge stretch; `[1--5]` blocks almost nothing. To fit the most meetings, always occupy the **smallest possible prefix** of the timeline.

---

## 🧪 Exchange Argument (the interview proof)

Suppose some optimal solution does **not** pick the earliest-ending valid interval.

- Optimal picks `X`, ending at `10`.
- The earliest-ending valid candidate is `Y`, ending at `6`.

Swap `X` → `Y`. Is the solution still valid?

**Yes.** Every interval the optimal chose after `X` starts at `≥ 10`, and `10 > 6`, so all of them still start after `Y` ends. The count is unchanged, and we finished earlier — so the swapped solution is at least as good.

> Therefore there **always exists** an optimal solution that takes the earliest-ending interval first. Apply inductively to the remainder → the greedy is optimal.

---

## 🧠 Evolution of Solutions

### ✅ Solution — Sort by End + Greedy Sweep

**Why this works:**
- Sorting by `end` means the first interval in the sorted order is always a safe greedy pick (exchange argument above).
- `prevEnd` is the finish time of the **last interval we decided to keep** — not the last interval we looked at. That distinction is the whole algorithm: on a conflict we drop the current interval and **leave `prevEnd` untouched**, because the kept one already ends earlier (sorted order guarantees it).
- Strict `<` implements the "touching is allowed" rule: `intervals[i][0] == prevEnd` is a legal chain, not an overlap.

**Dry Run** (`intervals = [[1,2],[2,3],[3,4],[1,3]]`):

After `Arrays.sort` by `end` (stable, so equal ends keep input order → `[2,3]` before `[1,3]`):

```
[1,2]  [2,3]  [1,3]  [3,4]
```

| `i` | interval | `start < prevEnd`? | action | `prevEnd` | `removed` |
|---|---|---|---|---|---|
| — | `[1,2]` | (seed) | keep | `2` | `0` |
| 1 | `[2,3]` | `2 < 2` ❌ | keep | `3` | `0` |
| 2 | `[1,3]` | `1 < 3` ✅ overlap | **remove** | `3` (unchanged) | `1` |
| 3 | `[3,4]` | `3 < 3` ❌ | keep | `4` | `1` |

**Answer = 1** ✅ (kept `[1,2] [2,3] [3,4]`, dropped `[1,3]`)

```java
class Solution {
    public int eraseOverlapIntervals(int[][] intervals) {
        Arrays.sort(intervals, (a,b) -> a[1] - b[1]);
        int removed = 0;
        int prevEnd = intervals[0][1];

        for (int i=1; i<intervals.length; i++) {
            if (intervals[i][0]  < prevEnd) {
                removed++;
            } else {
                prevEnd = intervals[i][1];
            }
        }

        return removed;
    }
}
```

---

## 🔑 Key Insights
- **Minimise removals ≡ maximise kept.** Reframing turns a "deletion" problem into standard Activity Selection.
- **`prevEnd` tracks the last *kept* interval, not the last *seen* one.** When we discard an overlapping interval we must not advance `prevEnd` — the interval we kept ends earlier, so it dominates.
- **Sorted-by-end makes discarding the current interval always correct.** If `intervals[i]` overlaps the kept one, the kept one ends at `≤ intervals[i][1]`, so keeping it is never worse. No backtracking needed.
- **`<` vs `<=` encodes the boundary rule.** Here endpoints may touch, so overlap is strictly `start < prevEnd`.

---

## ⚠️ Pitfalls
> [!warning]
> - **Sorting by start instead of end** — the single most common wrong instinct. One giant interval at the front sinks the whole answer.
> - **Advancing `prevEnd` on the removal branch** — writing `prevEnd = Math.min(prevEnd, intervals[i][1])` looks defensive but is redundant here (sorted order already guarantees `prevEnd` is the minimum); setting `prevEnd = intervals[i][1]` unconditionally is outright wrong.
> - **Using `<=` instead of `<`** — would treat `[1,2]` and `[2,3]` as overlapping and over-count removals.
> - **`(a,b) -> a[1] - b[1]` can overflow** — safe here because `|end| <= 5*10^4`, but with full `int` range this silently breaks. `Integer.compare(a[1], b[1])` is the habit worth building.
> - **`intervals[0]` on an empty array** — guaranteed non-empty by constraints (`length >= 1`), but a guard is expected if the interviewer relaxes that.

---

## ⏱️ Complexity
- **Time:** `O(n log n)` — dominated by the sort; the sweep is a single `O(n)` pass
- **Space:** `O(log n)` — sorting an object array uses TimSort, which needs auxiliary space (`O(n)` worst case); the algorithm itself is `O(1)`

---

## 🔁 Pattern Transfer

Whenever the problem says **maximum non-overlapping intervals**, **minimum removals to de-overlap**, **maximum meetings attended**, or **activity selection** — the answer is:

> **Among all intervals you can currently take, always take the one that finishes first.**

Sibling problems: `LT_0452 Minimum Number of Arrows to Burst Balloons` (same sweep, count *kept* groups instead of removals), `LT_0056 Merge Intervals` (sort by **start** — different goal: merge, not select), `LT_0253 Meeting Rooms II` (min-heap on end times).
