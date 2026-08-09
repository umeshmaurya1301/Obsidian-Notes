---
created: 2026-08-09 18:31
tags:
  - dsa
  - dynamic-programming
  - arrays
  - memoization
source: https://leetcode.com/problems/partition-equal-subset-sum/
problem_id: "416"
difficulty: Medium
status: Solved
review_date:
---
# LT_0416 – Partition Equal Subset Sum

**Link:** [Open Problem](https://leetcode.com/problems/partition-equal-subset-sum/)

---

## 📝 Problem Description
> [!info]
> Given an integer array `nums`, return `true` if you can partition the array into **two subsets** such that the sum of the elements in both subsets is equal, or `false` otherwise.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [1,5,11,5]`
> **Output:** `true`
> **Explanation:** The array can be partitioned as `[1, 5, 5]` and `[11]`.

> [!example]
> **Input:** `nums = [1,2,3,5]`
> **Output:** `false`
> **Explanation:** The array cannot be partitioned into equal sum subsets.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 200`
> - `1 <= nums[i] <= 100`

---

## 🔍 Intuition

The "two subsets" framing is a disguise. If the array splits into two halves of equal sum, each half must total `sum / 2` — and once I've picked one half, the other is whatever's left over. So the question reduces to a **single** subset-sum decision: *is there any subset of `nums` adding up to `sum / 2`?*

That immediately buys two things. First, a free rejection: if `sum` is **odd**, no split exists, return `false` before touching the DP. Second, a classic 0/1 knapsack shape — walk the array, and at each index either **take** `nums[idx]` (subtract it from the target) or **skip** it, then OR the two branches. Each element can be used at most once, which is exactly what `idx+1` on *both* branches enforces.

Brute force explores all `2^n` subsets — at `n = 200` that's hopeless. But the state is only `(idx, target)`: how I reached a remaining target of `6` never changes whether the rest of the array can finish it. Since `target <= sum/2 <= 10⁴`, the table is at most `200 × 10⁴` cells, and the exponential collapses to a polynomial.

> 🟢 *0/1 Knapsack — Subset Sum (Take / Skip DP)*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Top-Down 2D DP (Memoization)

**Why this works:**
- **Odd-sum shortcut is provably safe:** two equal integer halves force an even total, so `sum % 2 != 0` is an immediate `false` — and it also guarantees `target = sum/2` is a clean integer for the table dimension.
- **`idx+1` on both branches makes it 0/1, not unbounded:** taking `nums[idx]` still advances the index, so no element is ever reused. (Compare `LT_0518`, where the *take* branch stays on the same index for unlimited supply.)
- **`Boolean[][]` (the boxed type) uses `null` as the "not computed" marker** — necessary here because both `true` and `false` are real answers, so no primitive sentinel value is available. An `int[][]` with `-1/0/1` would work too, at the cost of a translation layer.

**Dry Run** (`nums = [1,5,11,5]` → `sum = 22`, `target = 11`):

| call | take branch | notTake branch | result |
|------|-------------|----------------|--------|
| `dfs(0, 11)` | `dfs(1, 10)` | `dfs(1, 11)` | **true** |
| `dfs(1, 10)` | `dfs(2, 5)` | `dfs(2, 10)` | true |
| `dfs(2, 5)` | `dfs(3, -6)` → `target < 0` → false | `dfs(3, 5)` | true |
| `dfs(3, 5)` | `dfs(4, 0)` → `target == 0` → **true** | `dfs(4, 5)` → `idx >= len` → false | true |

The winning path skips `11` and takes `1 + 5 + 5 = 11` ✅ — leaving `[11]` as the other half.

```java
class Solution {
    public boolean canPartition(int[] nums) {
        int sum = 0;
        for (int n : nums) sum += n;
        if (sum%2!=0) return false;
        int target = sum/2;
        Boolean[][] dp = new Boolean[nums.length][target+1];

        boolean ans = dfs(nums, dp, 0, target);
        // System.out.println(Arrays.deepToString(dp));
        return dp[0][target];
        // return (boolean)dp[0][target];
    }

    private boolean dfs(int[] nums, Boolean[][] dp, int idx, int target) {
        if (target==0) return true;
        if (idx >= nums.length || target<0) return false;
        if (dp[idx][target]!=null) return dp[idx][target];

        boolean take = dfs(nums, dp, idx+1, target-nums[idx]);
        boolean notTake = dfs(nums, dp, idx+1, target);
        return dp[idx][target] = take || notTake;
    }
}
```

- **Time:** `O(n · sum)` — at most `200 × 10⁴` states, `O(1)` work each · **Space:** `O(n · sum)` table + `O(n)` recursion depth

---

## 🔑 Key Insights
- **"Split into two equal halves" ⇒ "find one subset summing to `sum/2`".** Recognising this rewrite is the entire problem; everything after it is boilerplate knapsack.
- **`target == 0` is checked *before* the index bound**, so a subset can succeed without consuming the rest of the array. Flipping those two lines would wrongly require the target to hit zero exactly at the last element.
- **The boxed `Boolean[][]` is a deliberate choice, not laziness** — `null` is the only free "unvisited" marker when both boolean outcomes are meaningful. This is the standard trick for memoising predicates.
- **Space can drop to `O(target)`** with the bottom-up 1D form, iterating `target` **downward** so each item is used once — the usual 0/1-knapsack rolling-array optimisation.

---

## ⚠️ Pitfalls
> [!warning]
> - **`return dp[0][target]` instead of `return ans;`** — this auto-unboxes, so it would throw `NullPointerException` if `dfs(0, target)` ever returned via the `target == 0` base case without writing the memo. It's safe *only* because `nums[i] >= 1` forces `target >= 1`; a `0` in the array under looser constraints would crash it. Returning `ans` avoids the whole hazard.
> - **No short-circuit on the `take` branch.** `take` and `notTake` are both computed into locals before the `||`, so a `true` from `take` doesn't skip the second recursion. `return dfs(take…) || dfs(notTake…);` would short-circuit — same complexity, meaningfully faster in practice.
> - **Forgetting the odd-sum guard.** Without it, `target = sum/2` truncates (e.g. `sum = 7` → `target = 3`) and the DP happily reports `true` for an array that cannot be split.

---

## ⏱️ Complexity
- **Time:** `O(n · sum)` where `sum = Σ nums[i]`
- **Space:** `O(n · sum)` for the memo, plus `O(n)` recursion stack
