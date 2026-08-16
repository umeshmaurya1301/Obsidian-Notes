---
created: 2026-08-10 12:05
tags:
  - dsa
  - dynamic-programming
  - hashing
  - subsequence
source: https://leetcode.com/problems/longest-arithmetic-subsequence/description/
problem_id: "1027"
difficulty: Medium
status: Solved
review_date:
---
# LT_1027 – Longest Arithmetic Subsequence

**Link:** [Open Problem](https://leetcode.com/problems/longest-arithmetic-subsequence/description/)

---

## 📝 Problem Description
> [!info]
> Given an array `nums` of integers, return the length of the longest **arithmetic subsequence** in `nums`.
>
> A subsequence of an array is a list `nums[i1], nums[i2], ..., nums[ik]` with `0 <= i1 < i2 < ... < ik <= nums.length - 1`. A sequence `seq` is arithmetic if `seq[i + 1] - seq[i]` are all the same value (for `0 <= i < seq.length - 1`).

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [3,6,9,12]`
> **Output:** `4`
> **Explanation:** The whole array is an arithmetic sequence with a common difference of 3.

> [!example]
> **Input:** `nums = [9,4,7,2,10]`
> **Output:** `3`
> **Explanation:** The longest arithmetic subsequence is `[4,7,10]`.

> [!example]
> **Input:** `nums = [20,1,15,3,10,5,8]`
> **Output:** `4`
> **Explanation:** The longest arithmetic subsequence is `[20,15,10,5]`.

---

## ⚠️ Constraints
> [!warning]
> - `2 <= nums.length <= 1000`
> - `0 <= nums[i] <= 500`

---

## 🔍 Intuition

Plain LIS-style DP fails here because `dp[i]` isn't a single number — an arithmetic chain ending at `i` is only extendable if the **common difference matches**, so index `i` may sit at the end of many different chains, one per difference. The state has to be `(index, difference)`, not just `index`.

The difference can be anything in `[-500, 500]` (and in general is unbounded), so instead of a second array dimension I keep `dp[i]` as a **HashMap from difference → chain length ending at `i` with that difference**. Then the classic `O(n²)` double loop works: for every pair `j < i`, compute `diff = nums[i] - nums[j]` and glue `i` onto whatever chain `j` already had for that same `diff`.

The one line that carries all the weight is `dp[j].getOrDefault(diff, 1)`. If `j` has never seen this difference, `j` alone is a chain of length **1**, so appending `i` makes **2** — every pair of elements is trivially arithmetic. That default is why `ans` can safely start at `2` and why no explicit "seed every pair" pass is needed.

> 🟢 *DP with a hashed second dimension — `(index, common difference) → length`*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — `HashMap` per Index, Keyed by Common Difference

**Why this works:**
- **`dp[i][diff]` is the right state.** "Longest arithmetic subsequence ending at `i` whose step is `diff`" is extendable in exactly one way — by a later `k` with `nums[k] - nums[i] == diff` — which is precisely what the outer loop does.
- **`getOrDefault(diff, 1)` seeds pairs implicitly.** A single element is a length-1 arithmetic sequence for *every* difference, so the base case doesn't need materialising — it's produced on demand.
- **The `max` in the `put`** guards against a difference that can be reached at `i` from several `j`s; keep the longest.
- **`ans = 2` initially** is correct because `nums.length >= 2` is guaranteed, so an answer of at least 2 always exists.

**Dry Run** (`nums = [9,4,7,2,10]`):

| `i` | `j` | `diff` | `dp[j].getOrDefault(diff,1)` | write | `ans` |
|---|---|---|---|---|---|
| 1 (`4`) | 0 (`9`) | `-5` | `1` | `dp[1][-5] = 2` | `2` |
| 2 (`7`) | 0 (`9`) | `-2` | `1` | `dp[2][-2] = 2` | `2` |
| 2 (`7`) | 1 (`4`) | `3` | `1` | `dp[2][3] = 2` | `2` |
| 3 (`2`) | 0 (`9`) | `-7` | `1` | `dp[3][-7] = 2` | `2` |
| 3 (`2`) | 1 (`4`) | `-2` | `1` (`dp[1]` has no `-2`) | `dp[3][-2] = 2` | `2` |
| 3 (`2`) | 2 (`7`) | `-5` | `1` (`dp[2]` has no `-5`) | `dp[3][-5] = 2` | `2` |
| 4 (`10`) | 0 (`9`) | `1` | `1` | `dp[4][1] = 2` | `2` |
| 4 (`10`) | 1 (`4`) | `6` | `1` | `dp[4][6] = 2` | `2` |
| 4 (`10`) | 2 (`7`) | `3` | **`2`** (`dp[2][3]`) | `dp[4][3] = 3` | **`3`** |
| 4 (`10`) | 3 (`2`) | `8` | `1` | `dp[4][8] = 2` | `3` |

Answer `3` ✅ — the chain `4 → 7 → 10` built through `dp[2][3] = 2` being extended at `i = 4`.

Note row 5: `dp[1]` has `-5` but not `-2`, so the lookup correctly falls back to `1` instead of accidentally reusing the wrong chain. That's the whole reason the difference must be part of the key.

```java
class Solution {
    public int longestArithSeqLength(int[] nums) {
        int len = nums.length;
        Map<Integer, Integer>[] dp = new HashMap[len];
        for (int i = 0; i < len; i++) {
            dp[i] = new HashMap<>();
        }
        int ans = 2;

        for (int i=1; i<len; i++) {

            for (int j=0; j<i; j++) {
                int diff = nums[i] - nums[j];
                int prevLength = dp[j].getOrDefault(diff, 1);
                dp[i].put(diff,  Math.max(dp[i].getOrDefault(diff, 0), prevLength + 1)  );
                ans = Math.max ( ans, dp[i].get(diff));
            }
        }

        return ans;

    }
}
```

- **Time:** `O(n²)` (each of the `n²/2` pairs does `O(1)` hash work) · **Space:** `O(n²)` — each `dp[i]` can hold up to `i` distinct differences

---

## 🔑 Key Insights
- **When "extendable" depends on more than position, widen the state.** LIS needs only `dp[i]`; arithmetic needs `dp[i][diff]`. The moment a chain carries a *property* forward, that property joins the state.
- **`HashMap` beats a 2D array when the second dimension is sparse or unbounded.** Here `nums[i] <= 500` means `diff ∈ [-500, 500]`, so `int[n][1001]` with an offset would also work and be faster in practice — but the map version generalises to unbounded values and is what you'd write first.
- **The `1` in `getOrDefault(diff, 1)` is the base case in disguise.** Using `0` there would return one less than the true length everywhere.
- Contrast with [[LT_0300_Longest_Increasing_Subsequence]]: LIS gets an `O(n log n)` patience-sorting speedup; arithmetic subsequence does **not** — `O(n²)` is the accepted bound, and `n <= 1000` confirms it.

---

## ⚠️ Pitfalls
> [!warning]
> - `Map<Integer, Integer>[] dp = new HashMap[len];` is an unchecked generic array creation — it compiles with a warning. Cleaner alternatives are `List<Map<Integer,Integer>>` or the `int[n][1001]` offset array.
> - Don't initialise `ans = 0` or `1` unless you also handle short arrays; here `2` is safe *only* because the constraints guarantee `nums.length >= 2`.
> - `dp[i].getOrDefault(diff, 0)` (the inner one) uses `0`, while `dp[j].getOrDefault(diff, 1)` uses `1` — they mean different things ("nothing written at `i` yet" vs "`j` alone is a chain of 1"). Swapping them is a subtle off-by-one.
> - Arithmetic subsequences of length 1 or 2 are always valid, so the answer is never less than 2 — a return of `1` means a bug.

---

## ⏱️ Complexity
- **Time:** `O(n²)`
- **Space:** `O(n²)`
