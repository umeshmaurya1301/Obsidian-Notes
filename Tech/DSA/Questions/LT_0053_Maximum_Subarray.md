---
created: 2026-08-09 18:31
tags:
  - dsa
  - arrays
  - dynamic-programming
  - kadane
source: https://leetcode.com/problems/maximum-subarray/
problem_id: "53"
difficulty: Medium
status: Solved
review_date:
---
# LT_0053 – Maximum Subarray

**Link:** [Open Problem](https://leetcode.com/problems/maximum-subarray/)

---

## 📝 Problem Description
> [!info]
> Given an integer array `nums`, find the subarray with the largest sum, and return its sum.
>
> **Follow up:** If you have figured out the `O(n)` solution, try coding another solution using the divide and conquer approach, which is more subtle.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [-2,1,-3,4,-1,2,1,-5,4]`
> **Output:** `6`
> **Explanation:** The subarray `[4,-1,2,1]` has the largest sum `6`.

> [!example]
> **Input:** `nums = [1]`
> **Output:** `1`
> **Explanation:** The subarray `[1]` has the largest sum `1`.

> [!example]
> **Input:** `nums = [5,4,-1,7,8]`
> **Output:** `23`
> **Explanation:** The subarray `[5,4,-1,7,8]` has the largest sum `23`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 10^5`
> - `-10^4 <= nums[i] <= 10^4`

---

## 🔍 Intuition

The naive read is "try every subarray" — `O(n²)` pairs, each summed in `O(n)`. At `n = 10⁵` that's dead on arrival, and caching the sums doesn't help because each `(i, j)` pair is only ever asked about once.

The insight that kills it is to stop thinking about *pairs* and think about **one question per index**: what is the best subarray sum that *ends exactly at `i`*? That has a one-line answer — either extend the best subarray ending at `i-1`, or start fresh at `nums[i]`. Whichever is bigger. The global answer is then the max over all those per-index bests, so a single left-to-right sweep suffices.

The implementation below expresses "start fresh" as **resetting a running sum to `0` the moment it goes negative** — because a negative prefix can only ever hurt whatever follows it, so dragging it along is strictly worse than dropping it. The subtle part is *ordering*: the answer must be recorded **before** the reset, otherwise an all-negative array would return `0` (an empty subarray), which the problem doesn't allow.

> 🟢 *Kadane's Algorithm — Running Sum with Negative Reset*

---

## 🧠 Evolution of Solutions

### ❌ Solution 1 — Brute Force Over All Subarrays (TLE)

**Why it's bad:** it enumerates all `O(n²)` `(i, j)` pairs and re-sums each range from scratch in `O(n)` — `O(n³)` overall, plus an `O(n²)` table that never returns a single cache hit. At `n = 10⁵` the table alone is `10¹⁰` ints, so it fails on memory before it even gets to time out.

**Why the memo does nothing:** the driver loop visits every `(i, j)` exactly once, so `dp[i][j] != MAX` is never true when the pair is reached. The stored sums are written and never read — the same dead-memo shape as in [[LT_0647_Palindromic_Substrings]]. A real `O(n²)` version would reuse `sum(i, j-1)` to get `sum(i, j)` in `O(1)`, which this does not do.

**Dry Run** (`nums = [-2,1,-3,4,-1,2,1,-5,4]`): pairs `(0,0) = -2`, `(0,1) = -1`, `(0,2) = -4`, … eventually `(3,6) = 4-1+2+1 = 6`, which is the max. Correct answer, `45` separate range-sum loops to get there for just `n = 9`.

```java
class Solution {

    private static final int MAX = Integer.MAX_VALUE;

    public int maxSubArray(int[] nums) {
        int n = nums.length;
        int[][] dp = new int[n][n];
        for (int[] a : dp) Arrays.fill(a, MAX);
        int max = Integer.MIN_VALUE;

        for (int i=0; i<n; i++) {
            for (int j=i; j<n; j++) {
                int subArrSum = dfs (i, j, nums, dp);
                if (subArrSum > max) {
                    max = subArrSum;
                }
            }
        }

        return max;
    }

    private int dfs (int i, int j, int[] nums, int[][] dp) {
        if (dp[i][j] != MAX) return dp[i][j];
        int sum = 0;
        for (int idx = i; idx<=j; idx++) sum += nums[idx];
        return dp[i][j] = sum;
    }
}
```

- **Time:** `O(n³)` · **Space:** `O(n²)` — **TLE / MLE** on the real constraints

### ✅ Solution 2 — Kadane's Algorithm

**Why this works:**
- **`sum` is always "the best subarray sum ending here".** Adding `nums[i]` extends the current run; the `sum < 0` reset abandons it, because any prefix with a negative total makes every extension worse than restarting.
- **`max` is updated before the reset**, so the value that gets recorded is a *real* subarray sum including `nums[i]`. This is what makes all-negative inputs work: `[-3]` records `-3` and only *then* clears `sum`.
- **`max` starts at `Integer.MIN_VALUE`, not `0`.** Seeding with `0` would implicitly allow the empty subarray and return `0` for `[-1,-2]`, whose correct answer is `-1`.

**Dry Run** (`nums = [-2,1,-3,4,-1,2,1,-5,4]`):

| `n` | `sum += n` | `max` | reset? |
|-----|-----------|-------|--------|
| -2 | -2 | -2 | ✅ `sum → 0` |
| 1 | 1 | 1 | — |
| -3 | -2 | 1 | ✅ `sum → 0` |
| 4 | 4 | 4 | — |
| -1 | 3 | 4 | — |
| 2 | 5 | 5 | — |
| 1 | 6 | **6** | — |
| -5 | 1 | 6 | — |
| 4 | 5 | 6 | — |

Result: `6` ✅ — the window that produced it is `[4,-1,2,1]`.

```java
class Solution {
    public int maxSubArray(int[] nums) {
        int max = Integer.MIN_VALUE;
        int sum = 0;
        for(int n : nums) {
            sum += n;
            max = Math.max(sum, max);
            if(sum<0) {
                sum=0;
            }
        }
        return max;
    }
}
```

- **Time:** `O(n)` — one pass · **Space:** `O(1)` — two ints

---

## 🔑 Key Insights
- **Reframe "all subarrays" as "best subarray ending at each index".** That single change turns an `O(n²)` search space into `n` independent `O(1)` decisions — the same move that powers [[LT_152_Maximum_Product_SubArray]], which needs *two* running values because a negative can flip min into max.
- **The reset is the DP recurrence in disguise.** `sum = max(nums[i], sum + nums[i])` is the textbook form; `if (sum < 0) sum = 0;` after the update is exactly equivalent, just written without the `Math.max`.
- **Update-then-reset ordering is the whole correctness argument** for all-negative arrays. Swap the two lines and `[-1,-2,-3]` returns `0`.
- **A memo only helps when states repeat.** Solution 1's table is proof by counterexample: `O(n²)` cells, `O(n²)` distinct lookups, zero hits — allocation without benefit.

---

## ⚠️ Pitfalls
> [!warning]
> - **Initialising `max = 0`.** Returns `0` on all-negative input instead of the largest (least negative) element. The problem requires a non-empty subarray.
> - **Resetting before recording.** `if (sum < 0) sum = 0;` placed *above* the `max` update silently drops every negative candidate and breaks the same all-negative case.
> - **Reaching for the `O(n²)` table at all.** With `n = 10⁵` an `n × n` `int[][]` is ~40 GB — the brute force here fails on memory long before time, which is worth saying out loud in an interview rather than just "it's too slow".

---

## ⏱️ Complexity
- **Time:** `O(n)` — single pass (Solution 2)
- **Space:** `O(1)` — two scalars, no auxiliary structures
