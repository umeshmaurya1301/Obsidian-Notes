---
created: 2026-06-26 10:00
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

I want to find the minimum coins needed for every sub-amount from `0` up to `amount`. Define `dp[i]` as the minimum number of coins to make exactly amount `i`.

Starting from `dp[0] = 0`, for each sub-amount I try every coin — if `currAmount >= coin`, then `dp[currAmount]` can be improved as `dp[currAmount - coin] + 1` (use that coin once, solve the remainder). Everything else is initialized to `amount + 1` as a safe "infinity" sentinel — since the maximum valid answer is at most `amount` (all 1-coins), anything that stays at `amount + 1` after all processing was unreachable. This avoids the integer overflow that `Integer.MAX_VALUE + 1` would cause.

> 🟢 *Bottom-Up DP (Unbounded Knapsack)*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Bottom-Up DP

**Why this works:**
- `dp[i]` builds on already-solved sub-problems: to make amount `i` using coin `c`, we need `dp[i - c] + 1` coins.
- Iterating amounts (outer) × coins (inner) covers all possibilities — each coin is available infinitely (unbounded).
- The `amount + 1` sentinel is safely larger than any valid answer and never overflows on `+1`.

**Dry Run** (`coins = [1,2,5], amount = 11`):

Initial state (∞ = `amount + 1` = 12):

| Amount | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|--------|---|---|---|---|---|---|---|---|---|---|----|----|
| dp     | 0 | ∞ | ∞ | ∞ | ∞ | ∞ | ∞ | ∞ | ∞ | ∞ | ∞  | ∞  |

After processing all amounts:

| Amount | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|--------|---|---|---|---|---|---|---|---|---|---|----|----|
| dp     | 0 | 1 | 1 | 2 | 2 | 1 | 2 | 2 | 3 | 3 | 2  | 3  |

`dp[11] = 3` → Answer: `5 + 5 + 1` ✅

```java
class Solution {
    public int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];

        Arrays.fill(dp, amount + 1);
        dp[0] = 0;

        for (int currAmount = 1; currAmount <= amount; currAmount++) {
            for (int coin : coins) {
                if (currAmount >= coin) {
                    dp[currAmount] = Math.min(
                        dp[currAmount],
                        dp[currAmount - coin] + 1
                    );
                }
            }
        }

        return dp[amount] == amount + 1 ? -1 : dp[amount];
    }
}
```

---

## ❓ Why `amount + 1` and Not `Integer.MAX_VALUE`?

This is the most common follow-up for this problem.

> [!info]
> **`dp[i]` = minimum coins to make amount `i`.** Initially unknown → represent as "infinity".

**Why not `0`?**
`dp[7] = 0` would falsely mean "0 coins needed for amount 7."

**Why not `Integer.MAX_VALUE`?**
The transition does `dp[currAmount - coin] + 1`. If `dp[curr - coin] == Integer.MAX_VALUE`, then `Integer.MAX_VALUE + 1` overflows to a **negative number** in Java — silently corrupting every future `min()` comparison.

**Why `amount + 1` works:**
Every coin has value ≥ 1, so any valid solution uses **at most `amount` coins** (worst case: all 1-coins). Therefore `amount + 1 > any valid answer`. It safely represents ∞ without overflow.

```
coins = [1], amount = 5
→ worst case: dp[5] = 5  (five 1-coins)
→ sentinel = 6  (always strictly larger ✅)
```

At the end, `dp[amount] == amount + 1` means: nobody updated this value → amount is unreachable → return `-1`.

---

## 📊 Approach Comparison

| Approach | Time | Space | Interview Preference |
|---|---|---|---|
| Brute Force | Exponential | `O(amount)` | ❌ |
| Memoization (Top-Down) | `O(amount × n)` | `O(amount)` + stack | ✅ Good |
| **Bottom-Up DP** | **`O(amount × n)`** | **`O(amount)`** | ⭐ Best |
| BFS | `O(amount × n)` | `O(amount)` | Rarely used |

> [!tip]
> Learn memoization first to build the recurrence intuitively, then convert to bottom-up. The bottom-up solution is the memoized recurrence evaluated iteratively — same complexity, no stack overhead.

---

## 🔑 Key Insights
- `amount + 1` as the ∞ sentinel avoids `Integer.MAX_VALUE` overflow on `+1`
- Outer loop over amounts, inner loop over coins — this is **unbounded knapsack** (each coin usable infinitely)
- `dp[currAmount - coin] + 1` means: "use this coin once, then solve the remaining sub-problem"
- Final check `dp[amount] == amount + 1` cleanly detects unreachable amounts

---

## ⚠️ Pitfalls
> [!warning]
> - Using `Integer.MAX_VALUE` as sentinel — overflows on `+1` and corrupts `min()` comparisons
> - Missing the `currAmount >= coin` guard — leads to negative array index access
> - Returning `0` for impossible amounts instead of `-1`

---

## ⏱️ Complexity
- **Time:** `O(amount × coins.length)` — for each of the `amount` sub-problems, we try every coin
- **Space:** `O(amount)` — the `dp` array only
