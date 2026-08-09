---
created: 2026-08-08 23:02
tags:
  - dsa
  - array
  - dynamic-programming
  - greedy
source: https://leetcode.com/problems/wiggle-subsequence/
problem_id: "376"
difficulty: Medium
status: Solved
review_date:
---
# LT_0376 – Wiggle Subsequence

**Link:** [Open Problem](https://leetcode.com/problems/wiggle-subsequence/)

---

## 📝 Problem Description
> [!info]
> A **wiggle sequence** is a sequence where the differences between successive numbers strictly alternate between positive and negative. The first difference (if one exists) may be either positive or negative. A sequence with one element and a sequence with two non-equal elements are trivially wiggle sequences.
>
> - For example, `[1, 7, 4, 9, 2, 5]` is a **wiggle sequence** because the differences `(6, -3, 5, -7, 3)` alternate between positive and negative.
> - In contrast, `[1, 4, 7, 2, 5]` and `[1, 7, 4, 5, 5]` are not wiggle sequences. The first is not because its first two differences are positive, and the second is not because its last difference is zero.
>
> A **subsequence** is obtained by deleting some elements (possibly zero) from the original sequence, leaving the remaining elements in their original order.
>
> Given an integer array `nums`, return *the length of the longest **wiggle subsequence** of* `nums`.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [1,7,4,9,2,5]`
> **Output:** `6`
> **Explanation:** The entire sequence is a wiggle sequence with differences `(6, -3, 5, -7, 3)`.

> [!example]
> **Input:** `nums = [1,17,5,10,13,15,10,5,16,8]`
> **Output:** `7`
> **Explanation:** There are several subsequences that achieve this length. One is `[1, 17, 10, 13, 10, 16, 8]` with differences `(16, -7, 3, -3, 6, -8)`.

> [!example]
> **Input:** `nums = [1,2,3,4,5,6,7,8,9]`
> **Output:** `2`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 1000`
> - `0 <= nums[i] <= 1000`
> - *Follow up:* could you solve this in `O(n)` time?

---

## 🔍 Intuition

The trap here is reading "subsequence" and reaching for the `O(n²)` LIS machinery — but a wiggle only cares about the **sign of the last step**, not the value I'm sitting on, so the state is just `(index, direction I need next)`. Two directions × `n` indices = `2n` states, which collapses the whole thing to linear. The deeper insight is that inside a monotone run (say `4 → 9 → 12`), only the **extreme** endpoint can ever be worth keeping — swapping any interior element for the peak never shortens the answer — so I don't need to compare against the previously *picked* element at all, just against `nums[i-1]`. That's why both solutions get away with looking one step back. Once I see that, the DP is really just counting direction flips, and I can throw away the table entirely: sweep left to right, and every time the sign of `nums[i] - nums[i-1]` differs from the last sign I committed to, that's one more term in the wiggle. Flat steps (`currDiff == 0`) are simply ignored, because they neither extend nor break the alternation.

> 🟢 *DP on (index, direction) → Greedy Direction-Flip Counting*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — State Machine DP (Memoized DFS on `(idx, isUp)`)

**Why this works:**
- The only thing that matters about the past is **which direction the next step must go**, so state is `(idx, isUp)` — `isUp == 0` means "I still need an up-move next", `isUp == 1` means "I need a down-move next". That's `2n` states, each resolved in `O(1)`.
- At each index the choice is forced, not branched: if `nums[idx]` provides the required direction versus `nums[idx-1]`, take it (`1 + dfs(idx+1, flipped)`); otherwise skip it and keep waiting for the same direction (`dfs(idx+1, isUp)`).
- `idx == 0` is treated as always-takeable in both modes, which is why `wiggleMaxLength` seeds **two** roots — `dfs(0,0)` and `dfs(0,1)` — and takes the max. The best wiggle may start by going up or by going down, and only one of those is optimal.

**Dry Run** (`nums = [1,7,4,9,2,5]`):

Branch A — `dfs(0, 0)` (start expecting an up-move):

| Call | Check | Action | Returns |
|---|---|---|---|
| `dfs(0,0)` | `idx == 0` | take → `1 + dfs(1,1)` | `5` |
| `dfs(1,1)` | `7 < 1`? ✗ | skip → `dfs(2,1)` | `4` |
| `dfs(2,1)` | `4 < 7`? ✓ | take → `1 + dfs(3,0)` | `4` |
| `dfs(3,0)` | `9 > 4`? ✓ | take → `1 + dfs(4,1)` | `3` |
| `dfs(4,1)` | `2 < 9`? ✓ | take → `1 + dfs(5,0)` | `2` |
| `dfs(5,0)` | `5 > 2`? ✓ | take → `1 + dfs(6,·)` | `1` |
| `dfs(6,·)` | `idx == len` | base case | `0` |

→ `dfs(0,0) = 5`

Branch B — `dfs(0, 1)` (start expecting a down-move):

| Call | Check | Action | Returns |
|---|---|---|---|
| `dfs(0,1)` | `idx == 0` | take → `1 + dfs(1,0)` | `6` |
| `dfs(1,0)` | `7 > 1`? ✓ | take → `1 + dfs(2,1)` | `5` |
| `dfs(2,1)` | *memo hit* | — | `4` |

→ `dfs(0,1) = 6`

`Math.max(5, 6) = 6` ✅ — note Branch B reuses the memoized `dfs(2,1)` computed in Branch A.

```java
class Solution {
    public int wiggleMaxLength(int[] nums) {
        int len = nums.length;
        int[][] dp = new int[len][2];
        for (int[] a : dp)
            Arrays.fill(a, -1);

        int val1 = dfs(nums, dp, 0, 0);
        int val2 = dfs(nums, dp, 0, 1);
        return Math.max(val1, val2);
    }

    private int dfs(int[] nums, int[][] dp, int idx, int isUp) {
        int len = nums.length;
        if (idx == len)
            return 0;

        if (dp[idx][isUp] != -1)
            return dp[idx][isUp];

        int val = 0;
        if (isUp == 0) {
            if (idx == 0 || nums[idx] > nums[idx - 1]) {
                val = 1 + dfs(nums, dp, idx + 1, 1);
            } else {
                val = dfs(nums, dp, idx + 1, 0);
            }
        }

        if (isUp == 1) {
            if (idx == 0 || nums[idx] < nums[idx - 1]) {
                val = 1 + dfs(nums, dp, idx + 1, 0);
            } else {
                val = dfs(nums, dp, idx + 1, 1);
            }
        }

        return dp[idx][isUp] = val;
    }

}
```

- **Time:** `O(n)` · **Space:** `O(n)` (`2n` memo table + up to `O(n)` recursion stack)

### ✅ Solution 2 — Greedy: Count Direction Flips

**Why this works:**
- `prevDiff` remembers only the sign of the **last committed** step. A new element is worth taking exactly when `currDiff` flips that sign — `(prevDiff <= 0 && currDiff > 0)` or `(prevDiff >= 0 && currDiff < 0)`.
- `prevDiff` is updated **only inside the `if`**. That's the whole trick: while walking a monotone run, the non-flipping steps are silently dropped and `prevDiff` keeps pointing at the last real turn, so the run contributes exactly one element (its extreme endpoint).
- The `<=` / `>=` on `prevDiff` handles both the seed (`prevDiff = 0`, so the very first non-zero difference always counts) and plateaus (`currDiff == 0` satisfies neither branch and is skipped) with no special-casing.
- `count = 1` seeds the first element, which is always part of some wiggle — this also makes the `n == 1` case fall out for free.

**Dry Run** (`nums = [1,7,4,9,2,5]`):

| `i` | `nums[i]` | `currDiff` | `prevDiff` (before) | Flip? | `count` | `prevDiff` (after) |
|---|---|---|---|---|---|---|
| — | — | — | — | — | `1` | `0` |
| `1` | `7` | `+6` | `0` | ✓ (`<=0 → +`) | `2` | `6` |
| `2` | `4` | `-3` | `6` | ✓ (`>=0 → -`) | `3` | `-3` |
| `3` | `9` | `+5` | `-3` | ✓ | `4` | `5` |
| `4` | `2` | `-7` | `5` | ✓ | `5` | `-7` |
| `5` | `5` | `+3` | `-7` | ✓ | `6` | `3` |

→ returns `6` ✅

(On `[1,2,3,4,5,6,7,8,9]` only `i = 1` flips — every later `currDiff` is positive while `prevDiff` is already positive — so `count` stays at `2`.)

```java
class Solution {
    public int wiggleMaxLength(int[] nums) {
        int len = nums.length;
        int count = 1;
        int prevDiff = 0;

        for (int i=1; i<len; i++) {
            
            int currDiff = nums[i] - nums[i-1];

            if ( ( prevDiff <= 0 && currDiff > 0 ) || ( prevDiff >= 0 && currDiff < 0) ) {
                count++;
                prevDiff = currDiff;
            }
        }

        return count;
    }
}
```

- **Time:** `O(n)` · **Space:** `O(1)`

---

## 🔑 Key Insights
- **The state is a direction, not a value.** Unlike LIS, I never need to know *which* element I last picked — only whether the next step must rise or fall. That's what kills the `O(n²)` pairwise comparison.
- **Monotone runs collapse to their endpoint.** Replacing any interior element of a rising run with the run's peak keeps the wiggle valid and leaves more room for the next fall, so greedily keeping the extreme is safe. This is the exchange argument that justifies Solution 2.
- **Comparing against `nums[i-1]` is enough** — a subtle point, since intuitively you'd compare against the last *picked* element. It works precisely because of the collapse above: within a run the two comparisons agree in sign.
- **`prevDiff = 0` is a dual-purpose sentinel** — it satisfies both `<= 0` and `>= 0`, so the first non-zero difference is accepted regardless of its direction, mirroring the DP's two-root `Math.max(dfs(0,0), dfs(0,1))`.

---

## ⚠️ Pitfalls
> [!warning]
> - **Updating `prevDiff` unconditionally** (outside the `if`) breaks it: `[1,2,3]` would then read as two flips instead of one, since `prevDiff` would track every step rather than only committed turns.
> - **Forgetting the second DP root.** Running only `dfs(0, 0)` returns `5` on Example 1 instead of `6` — the optimal wiggle here starts with a *down*-expectation at index `0`. You must take `Math.max` over both.
> - **Mishandling equal adjacent values.** `currDiff == 0` must be skipped entirely; using `<` / `>` where `<=` / `>=` belongs (or vice versa) makes `[1,7,4,5,5]`-style plateaus count as a wiggle step.
> - **`count = 0` instead of `1`.** The first element is always free; seeding at `0` under-counts every answer by one and breaks the single-element case.

---

## ⏱️ Complexity
- **Time:** `O(n)`
- **Space:** `O(1)`
