---
created: 2026-06-29 10:00
tags:
  - dsa
  - dynamic-programming
  - array
source: https://leetcode.com/problems/coin-change/
problem_id: "322"
difficulty: Medium
status: Solved
review_date:
---
# LT_0322 – Coin Change

**Link:** [Open Problem](https://leetcode.com/problems/coin-change/)

---

## 📝 Problem Description
> [!info]
> You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.
>
> Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return `-1`.
>
> You may assume that you have an **infinite** number of each kind of coin.

---

## 🧪 Examples
> [!example]
> **Input:** `coins = [1,2,5], amount = 11`
> **Output:** `3`
> **Explanation:** `11 = 5 + 5 + 1`

> [!example]
> **Input:** `coins = [2], amount = 3`
> **Output:** `-1`

> [!example]
> **Input:** `coins = [1], amount = 0`
> **Output:** `0`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= coins.length <= 12`
> - `1 <= coins[i] <= 2^31 - 1`
> - `0 <= amount <= 10^4`

---

## 🔍 Intuition

To find the minimum coins for `amount`, think top-down: "pick one coin now, solve the remainder recursively." For each denomination, subtract it from the current amount and recurse — the answer is `1 + min(results)` over all valid coin choices. Without memoization this is exponential because the same sub-amount gets recomputed across many call paths (e.g., reaching amount `6` from both `11→5→6` and `11→9→6`). By caching `dp[amount]` on first solve, every sub-amount is computed exactly once. `Integer.MAX_VALUE` serves as the "unreachable" sentinel, but we must guard against overflow before adding `1` to it.

> 🟢 *Top-Down DP (Memoization / DFS)*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Top-Down DP (Memoization)

**Why this works:**
- Optimal substructure: `minCoins(n) = 1 + min(minCoins(n - coin))` over all coins — recurse, cache, done.
- Three dp states: `-1` = unvisited, `Integer.MAX_VALUE` = unreachable, finite positive = solved. The `dp[amount] != -1` check correctly skips both solved and confirmed-unreachable amounts.
- The `res != Integer.MAX_VALUE` guard prevents `MAX_VALUE + 1` integer overflow before the `Math.min` comparison.

**Dry Run** (`coins = [1,2,5], amount = 6`):

| dfs call | winning coin | dp filled |
|----------|-------------|-----------|
| dfs(0) | base case | 0 |
| dfs(1) | coin=1 → dfs(0)=0 | dp[1]=1 |
| dfs(2) | coin=2 → dfs(0)=0 | dp[2]=1 |
| dfs(3) | coin=1 → dp[2]=1; coin=2 → dp[1]=1 | dp[3]=2 |
| dfs(4) | coin=2 → dp[2]=1 | dp[4]=2 |
| dfs(5) | coin=5 → dfs(0)=0 | dp[5]=1 |
| dfs(6) | coin=5 → dp[1]=1; coin=1 → dp[5]=1 | dp[6]=2 |

Result: `dp[6] = 2` → coins `5 + 1` ✅

```java
class Solution {
    public int coinChange(int[] coins, int amount) {
        if (amount==0) return 0;
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, -1);
        int ans = dfs(coins, amount, dp);
        System.out.println(Arrays.toString(dp));
        return dp[amount] == Integer.MAX_VALUE ? -1 : dp[amount];
        // return ans == Integer.MAX_VALUE ? -1 : ans;
    }

    private int dfs(int[] coins, int amount, int[] dp) {

        if (amount == 0) return 0;
        if (amount < 0) return Integer.MAX_VALUE;
        if (dp[amount] != -1) return dp[amount];

        int minCoins = Integer.MAX_VALUE;
        for (int coin : coins) {
            int res = dfs(coins, amount - coin, dp);
            if(res!=Integer.MAX_VALUE) {minCoins = Math.min(minCoins, res+1);}
        }

        return dp[amount] = minCoins;
    }

}
```

---

## ❓ Sentinel Design: `Integer.MAX_VALUE` vs `amount + 1`

> [!info]
> Both represent "infinity" but handle the `+1` hazard differently.

| Sentinel | Overflow risk on `+1`? | Guard needed? | Used in |
|----------|----------------------|--------------|---------|
| `Integer.MAX_VALUE` | ✅ Yes — overflows to negative | `if (res != MAX_VALUE)` | Top-Down |
| `amount + 1` | ❌ No — always ≤ `10^4 + 1` | None | Bottom-Up |

The top-down solution uses `Integer.MAX_VALUE` and guards it explicitly. The bottom-up alternative uses `amount + 1` instead, sidestepping overflow entirely — cleaner in practice.

---

## 📊 Approach Comparison

| Approach | Time | Space | Interview Preference |
|---|---|---|---|
| Brute Force | Exponential | `O(amount)` | ❌ |
| **Memoization (Top-Down)** | **`O(amount × n)`** | **`O(amount)`** + stack | ⭐ Natural to derive |
| Bottom-Up DP | `O(amount × n)` | `O(amount)` | ⭐ Best (no stack overhead) |
| BFS | `O(amount × n)` | `O(amount)` | Rarely used |

> [!tip]
> Top-down memoization is easier to derive from the recurrence intuitively. Bottom-up converts the same recurrence to iterative with no call-stack risk — preferred in interviews.

---

## 🔑 Key Insights
- Three dp states: `-1` = unvisited, `MAX_VALUE` = unreachable, finite positive = solved — never conflate them.
- `Integer.MAX_VALUE` as sentinel requires an explicit `res != Integer.MAX_VALUE` guard before `res + 1` to avoid overflow.
- Memoization ensures each sub-amount is visited exactly once → same `O(amount × n)` complexity as bottom-up.
- Infinite coin supply means no "used" flag is needed — just recurse on `amount - coin` freely.

---

## ⚠️ Pitfalls
> [!warning]
> - Missing the `res != Integer.MAX_VALUE` guard — `MAX_VALUE + 1` overflows to `Integer.MIN_VALUE`, corrupting every subsequent `min()` comparison.
> - Confusing the three dp states: initialising to `0` or treating `-1` as "zero coins needed" breaks the cache lookup.
> - The early `if (amount == 0) return 0` in `coinChange()` is a convenience guard — without it, `dfs` still handles it correctly via its own base case.

---

## ⏱️ Complexity
- **Time:** `O(amount × coins.length)` — each of the `amount` sub-problems is solved once, trying all `n` coins.
- **Space:** `O(amount)` — the `dp` array plus `O(amount)` recursion stack depth in the worst case.
