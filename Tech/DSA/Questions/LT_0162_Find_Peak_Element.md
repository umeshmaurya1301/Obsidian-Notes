---
created: 2026-08-02 11:30
tags:
  - dsa
  - binary-search
  - arrays
source: https://leetcode.com/problems/find-peak-element/
problem_id: "162"
difficulty: Medium
status: Solved
review_date:
---
# LT_0162 – Find Peak Element

**Link:** [Open Problem](https://leetcode.com/problems/find-peak-element/)

---

## 📝 Problem Description
> [!info]
> A peak element is an element that is **strictly greater** than its neighbors.
>
> Given a **0-indexed** integer array `nums`, find a peak element, and return its index. If the array contains multiple peaks, return the index to **any of the peaks**.
>
> You may imagine that `nums[-1] = nums[n] = -∞`. In other words, an element is always considered to be strictly greater than a neighbor that is outside the array.
>
> You must write an algorithm that runs in `O(log n)` time.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [1,2,3,1]`
> **Output:** `2`
> **Explanation:** `3` is a peak element and your function should return the index number `2`.

> [!example]
> **Input:** `nums = [1,2,1,3,5,6,4]`
> **Output:** `5`
> **Explanation:** Your function can return either index number `1` where the peak element is `2`, or index number `5` where the peak element is `6`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 1000`
> - `-2^31 <= nums[i] <= 2^31 - 1`
> - `nums[i] != nums[i + 1]` for all valid `i`

---

## 🔍 Intuition

The thing that confused me at first: binary search normally needs a *sorted* array, and this array is arbitrary. But sortedness was never the real requirement — what binary search actually needs is a way to **discard half the range with certainty**. Here that guarantee comes from slope, not order.

Look at `nums[mid]` versus `nums[mid + 1]`. If `nums[mid] > nums[mid + 1]`, I'm on a **descending** slope, so walking left from `mid` either keeps rising or turns over — and since `nums[-1] = -∞`, it *must* eventually turn over. A peak is guaranteed somewhere in `[lo..mid]`, and `mid` itself might be it, so `hi = mid` (not `mid - 1`). Symmetrically, if `nums[mid] < nums[mid + 1]` I'm **ascending**, and since `nums[n] = -∞` the rise must break somewhere to the right, so a peak exists in `[mid+1..hi]` and I set `lo = mid + 1`.

The `-∞` sentinels are what make this airtight — they guarantee a peak always exists in whichever half I keep, so I never chase an empty answer. The two neighbours are also guaranteed unequal by the constraints, so there's no flat-plateau case to break the slope test. A linear scan for "greater than both neighbours" would be `O(n)`; this is the same idea, but I let the slope direction throw away half the array each step.

> 🟢 *Binary Search on Slope / Peak Finding*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Binary Search on the Slope Direction

**Why this works:**

- **The half I keep always contains a peak.** Going uphill (`nums[mid] < nums[mid+1]`) means the right side starts with a rise and ends at `-∞`, so it must peak somewhere. Going downhill means the left side starts at `-∞` and ends high at `mid`, so it peaked somewhere too. The invariant "current window contains at least one peak" holds at every step.
- **`while (lo < hi)` with `hi = mid` is the right template.** The loop ends when the window collapses to a single index, and that index *is* a peak — no final verification needed. Using `lo <= hi` here would loop forever, since `hi = mid` doesn't shrink when `lo == hi`.
- **`mid + 1` can never overflow the array.** Because `lo < hi` is the loop condition, `mid = lo + (hi - lo) / 2` always lands strictly below `hi`, so `mid + 1 <= hi <= len - 1`. The access is safe without an explicit bounds check.
- **Only one comparison is needed per step.** I never check `nums[mid] > nums[mid - 1]`. Comparing against the right neighbour alone fully determines which half to keep — that's what keeps the branch logic this small.

**Dry Run** (`nums = [1,2,3,1]`):

| Iter | `lo` | `hi` | `mid` | `nums[mid]` | `nums[mid+1]` | Slope | Action |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 3 | 1 | `2` | `3` | `2 < 3` → uphill ↗ | peak is to the right → `lo = 2` |
| 2 | 2 | 3 | 2 | `3` | `1` | `3 > 1` → downhill ↘ | `mid` may be the peak → `hi = 2` |
| — | 2 | 2 | — | — | — | `lo == hi` → exit | **return `2`** ✅ |

Second trace on the multi-peak case — `nums = [1,2,1,3,5,6,4]`:

| Iter | `lo` | `hi` | `mid` | `nums[mid]` | `nums[mid+1]` | Slope | Action |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | `3` | `5` | uphill ↗ | `lo = 4` |
| 2 | 4 | 6 | 5 | `6` | `4` | downhill ↘ | `hi = 5` |
| 3 | 4 | 5 | 4 | `5` | `6` | uphill ↗ | `lo = 5` |
| — | 5 | 5 | — | — | — | exit | **return `5`** ✅ |

Index `1` is also a valid peak here — the algorithm converged on `5` instead, and the problem explicitly accepts any peak.

```java
class Solution {
    public int findPeakElement(int[] nums) {
        int len = nums.length;
        int lo = 0;
        int hi = len-1;

        while (lo < hi) {
            int mid = lo + (hi-lo)/2;
            int val = nums[mid];
            // 1 2 1
            if ( nums[mid] > nums[mid+1]) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
            
        }

        return lo;
    }
}
```

> [!tip]
> `int val = nums[mid];` is left over from a previous draft — the comparison uses `nums[mid]` directly, so `val` is never read. Harmless, but worth deleting if you re-type this in an interview; an unused local invites "why is that there?" questions.

---

## 🔑 Key Insights

- **Binary search doesn't require sorted input — it requires a reliable discard rule.** That's the transferable lesson. Any property that lets you rule out half the range works: slope here, a feasibility predicate in *Koko Eating Bananas* / *Ship Packages*, a sorted-half check in *Search in Rotated Sorted Array*.
- **The `-∞` boundary convention is doing real work.** It's what guarantees a peak always exists, so "keep searching this half" never dead-ends. Without it (i.e. if array ends counted as non-peaks) the whole argument collapses.
- **`hi = mid` vs `hi = mid - 1` is the crux.** When descending, `mid` itself is still a peak candidate — it's greater than its right neighbour and might beat its left one too. Excluding it can discard the only peak.
- **The answer is `lo`, and `lo == hi` at exit** — returning either works. The loop is a *convergence* pattern, not a *search-and-return-early* pattern; there's no `return mid` inside.

---

## ⚠️ Pitfalls
> [!warning]
> - **Writing `while (lo <= hi)` with `hi = mid`.** When `lo == hi`, `mid == lo`, and `hi = mid` leaves the window unchanged → infinite loop. The `hi = mid` branch *requires* the strict `lo < hi` condition.
> - **Using `hi = mid - 1` on the downhill branch.** That throws away `mid`, which is the peak in a case like `[1,2,1]`: `mid = 1` is the answer, and `hi = 0` loses it, returning `0`.
> - **Adding a bounds guard for `mid + 1` "just in case".** Not needed, and if you write it as `if (mid + 1 < len && ...)` the else-branch silently fires at the boundary and can push `lo` past the peak. Trust the `lo < hi` invariant instead.
> - **Trying to find the *global* maximum.** The problem only asks for *a* local peak. Chasing the global max forces `O(n)` and misses the point of the question.

---

## ⏱️ Complexity
- **Time:** `O(log n)` — the window halves on every iteration, with one comparison per step
- **Space:** `O(1)` — iterative, only `lo`, `hi`, `mid` held

---

## 💡 Mental Model

```
Stand at mid and look one step to the right.

  nums[mid] < nums[mid+1]   → you're walking uphill
                            → the climb must end somewhere right (array ends at -∞)
                            → lo = mid + 1

  nums[mid] > nums[mid+1]   → you're walking downhill
                            → you already passed a summit, or you're on it
                            → hi = mid   (keep mid — it might BE the peak)

Window shrinks to one index. That index is a peak.
```

Walk uphill and you cannot help but hit a summit — the edges are cliffs down to `-∞`.
