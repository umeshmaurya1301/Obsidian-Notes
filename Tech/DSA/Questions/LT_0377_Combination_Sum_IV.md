---
created: 2026-06-29 10:00
tags:
  - dsa
  - dynamic-programming
  - array
source: https://leetcode.com/problems/combination-sum-iv/description/
problem_id: "377"
difficulty: Medium
status: Solved
review_date:
---
# LT_0377 – Combination Sum IV

**Link:** [Open Problem](https://leetcode.com/problems/combination-sum-iv/description/)

---

## 📝 Problem Description
> [!info]
> Given an array of **distinct** integers `nums` and a target integer `target`, return the number of possible combinations that add up to `target`.
>
> The test cases are generated so that the answer can fit in a **32-bit integer**.
>
> **Note:** Different sequences are counted as different combinations — order matters.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [1,2,3], target = 4`
> **Output:** `7`
> **Explanation:**
> `(1,1,1,1)` | `(1,1,2)` | `(1,2,1)` | `(1,3)` | `(2,1,1)` | `(2,2)` | `(3,1)`

> [!example]
> **Input:** `nums = [9], target = 3`
> **Output:** `0`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 200`
> - `1 <= nums[i] <= 1000`
> - All the elements of `nums` are **unique**.
> - `1 <= target <= 1000`

---

## 🔍 Intuition

Since order matters (`[1,2,1]` and `[2,1,1]` are different), we're counting *permutations*, not combinations. This means for each remaining `target`, we're free to pick *any* number from `nums` — there's no coin-ordering constraint to enforce. So the state is just `dp[target]` = "number of ordered sequences summing to `target`", no index dimension needed. The recurrence is simply: try every number, recurse on `target - num`, sum up the results. This is the mirror image of Coin Change II — 1D dp with a full loop over all nums at each step counts permutations; 2D dp with an index parameter counts combinations.

> 🟢 *Top-Down DP (Memoization) — Permutation Count*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Top-Down 1D DP (Memoization)

**Why this works:**
- At each `target`, any element from `nums` can be chosen next — no ordering restriction → 1D dp state suffices.
- `dp[t] = Σ dp[t - num]` for all `num ∈ nums` counts every distinct ordered path to `t`, which is exactly what we want.
- `target < 0` returns `0` (dead end); `target == 0` returns `1` (one valid sequence found).

**Dry Run** (`nums = [1,2,3], target = 4`):

| target | nums tried | dp[target] |
|--------|-----------|------------|
| 0 | base | 1 |
| 1 | 1→dp[0]=1; 2→dp[-1]=0; 3→dp[-2]=0 | 1 |
| 2 | 1→dp[1]=1; 2→dp[0]=1; 3→dp[-1]=0 | 2 |
| 3 | 1→dp[2]=2; 2→dp[1]=1; 3→dp[0]=1 | 4 |
| 4 | 1→dp[3]=4; 2→dp[2]=2; 3→dp[1]=1 | **7** |

`dp[4] = 7` ✅

```java
class Solution {
    public int combinationSum4(int[] nums, int target) {
        int[] dp = new int[target+1];
        Arrays.fill(dp, -1);
        dfs(nums, dp, target);
        return dp[target];
    }

    private int dfs(int[] nums, int[] dp, int target) {
        if (target==0) return 1;
        if (target < 0) return 0;
        if (dp[target]!=-1) return dp[target];
        
        int ways = 0;
        for (int num : nums) {
            ways += dfs(nums, dp, target-num);
        }
        
        return dp[target] = ways;
    }
}
```

---

## 🧩 The 1D vs 2D DP Design Rule

This trio of problems reveals a single design principle:

| Problem | Counting what? | dp dimensions | Loop structure |
|---------|---------------|--------------|----------------|
| Coin Change I (#322) | Min coins | 1D `dp[amount]` | `min` over all coins |
| Coin Change II (#518) | Combinations (order ✗) | 2D `dp[idx][amount]` | take / not-take per coin |
| **Combination Sum IV (#377)** | **Permutations (order ✓)** | **1D `dp[target]`** | **loop all nums per target** |

> [!info]
> **The deciding question:** does order matter?
> - **No** (combinations) → need `idx` to fix coin order → 2D dp
> - **Yes** (permutations) → restart from all nums every step → 1D dp

---

## 🔑 Key Insights
- The absence of an `idx` parameter is the intentional design choice — it lets every num be reconsidered at every level, which is exactly what permutation counting requires.
- `dp[t] = Σ dp[t - num]` is essentially asking: "how many sequences have `num` as their first element, summed over all possible first elements?"
- The same 1D recurrence with `min` instead of `+` gives Coin Change I — same structure, different aggregation operator.
- Memoization collapses all paths that reach the same `target` remainder into one cached value, giving O(target × n) instead of exponential.

---

## ⚠️ Pitfalls
> [!warning]
> - **Adding an `idx` parameter** — would constrain coin ordering and count combinations instead of permutations (i.e., accidentally solves Coin Change II).
> - **Skipping the `target < 0` guard** — `target - num` can go negative when `num > target`; without the guard this causes infinite recursion or array out-of-bounds.
> - **Overflow during accumulation** — `ways` accumulates many recursive results; although the final answer fits in 32 bits, intermediate sums can overflow if constraints were larger. Safe here per problem guarantee.

---

## ⏱️ Complexity
- **Time:** `O(target × nums.length)` — each of the `target` subproblems tries all `n` numbers once (memoized).
- **Space:** `O(target)` — the `dp` array plus `O(target)` recursion stack depth in the worst case.
