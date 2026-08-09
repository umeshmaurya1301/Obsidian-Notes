---
created: 2026-08-09 18:31
tags:
  - dsa
  - dynamic-programming
  - arrays
  - memoization
source: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/
problem_id: "309"
difficulty: Medium
status: Solved
review_date:
---
# LT_0309 – Best Time to Buy and Sell Stock with Cooldown

**Link:** [Open Problem](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/)

---

## 📝 Problem Description
> [!info]
> You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`th day.
>
> Find the maximum profit you can achieve. You may complete **as many transactions as you like** (i.e., buy one and sell one share of the stock multiple times) with the following restrictions:
>
> - After you sell your stock, you **cannot buy stock on the next day** (i.e., cooldown one day).
>
> **Note:** You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).

---

## 🧪 Examples
> [!example]
> **Input:** `prices = [1,2,3,0,2]`
> **Output:** `3`
> **Explanation:** transactions = `[buy, sell, cooldown, buy, sell]`

> [!example]
> **Input:** `prices = [1]`
> **Output:** `0`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= prices.length <= 5000`
> - `0 <= prices[i] <= 1000`

---

## 🔍 Intuition

Transactions are unlimited, so at first glance this looks like [[LT_0122_Best_Time_to_Buy_and_Sell_Stock_II]] — but the cooldown makes churning **expensive**. Flipping daily is no longer free, because every sale burns the next day. That single rule kills the greedy and forces the take/skip DP back.

The good news is the cooldown needs **no extra state dimension**. It's purely a statement about *when the next decision happens*: after selling on day `idx`, the next day I'm allowed to act is `idx + 2`, not `idx + 1`. So the recursion keeps the same two-part state as the rest of the family — `(day, holding?)` — and encodes the whole restriction as a **jump in the index** on the sell branch.

With transactions unlimited there's no `txnLeft` dimension at all, leaving just `2n` states. Everything else is the family skeleton: buy contributes `-prices[idx]`, sell contributes `+prices[idx]`, and `canBuy` enforces "sell before you buy again".

> 🟢 *Take/Skip DP on (day, holding) — cooldown as an index jump*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Top-Down 2D DP (Memoization)

**Why this works:**
- **`idx + 2` on the sell branch *is* the cooldown.** Skipping straight past the next day makes it structurally impossible to buy on it — no flag, no third state, no extra table dimension.
- **Unlimited transactions ⇒ no `txnLeft`.** Compared with [[LT_0123_Best_Time_to_Buy_and_Sell_Stock_III]] the state drops from three dimensions to two, and the answer is read off `dp[0][1]` (day 0, free to buy).
- **The base case uses `idx >= prices.length`, not `==`** — which is exactly what makes the `idx + 2` jump safe. Selling on the last day lands on `n + 1`, and only the `>=` form catches that.

**Dry Run** (`prices = [1,2,3,0,2]`):

`f(i, 1)` = best profit from day `i` when free to buy; `f(i, 0)` = when holding.

| `idx` | `price` | `f(i,1)` free | `f(i,0)` holding | winning move at `f(i,1)` |
|-------|---------|---------------|------------------|--------------------------|
| 0 | 1 | **3** | 4 | **buy** at 1 → `f(1,0)` |
| 1 | 2 | 2 | 4 | — |
| 2 | 3 | 2 | 3 | — |
| 3 | 0 | 2 | 2 | **buy** at 0 → `f(4,0)` |
| 4 | 2 | 0 | 2 | — |

Answer `f(0,1) = 3`. The winning path: **buy at 1** (day 0) → **sell at 2** (day 1, jump to day 3, skipping day 2 as cooldown) → **buy at 0** (day 3) → **sell at 2** (day 4). Net `-1 + 2 - 0 + 2 = 3` ✅ — exactly the `[buy, sell, cooldown, buy, sell]` the problem describes.

> [!tip]
> Note `f(1,0) = 4`: holding a share on day 1 is "worth" 4 because the purchase cost was already paid by the caller. Only the `f(i,1)` column is a standalone answer.

```java
class Solution {
    public int maxProfit(int[] prices) {
        int n = prices.length;
        Integer[][] dp = new Integer[n][2];
        dfs(prices, dp, 0, 1);
        return dp[0][1];
    }

    private int dfs (int[] prices, Integer[][] dp, int idx, int canBuy) {
        if (idx>=prices.length) return 0;
        if (dp[idx][canBuy]!=null) return dp[idx][canBuy];

        int profit = 0;
        if (canBuy==1) {
            int buy = -prices[idx] + dfs (prices, dp, idx+1, 0);
            int skip = dfs (prices, dp, idx+1, 1);
            profit = Math.max (buy, skip);
        } else {
            int sell = +prices[idx] + dfs (prices, dp, idx+2, 1);
            int skip = dfs(prices, dp, idx+1, 0);
            profit = Math.max (sell, skip);
        }

        return dp[idx][canBuy] = profit;
    }
}
```

- **Time:** `O(n)` — `2n` states, `O(1)` each · **Space:** `O(n)` memo + `O(n)` recursion depth

---

## 🔑 Key Insights
- **A time-based restriction can often be encoded as an index jump rather than a new state.** That's the transferable lesson here: `idx+2` is cheaper and clearer than adding a `justSold` boolean dimension (though the three-state `hold / sold / rest` formulation is the equally valid classic alternative).
- **`>=` vs `==` in the base case is the single most fragile line.** [[LT_0714_Best_Time_to_Buy_and_Sell_Stock_with_Transaction_Fee]] can safely use `idx == prices.length` because every branch advances by exactly one; here the `+2` jump means `==` would sail past the guard and throw.
- **The cooldown is what makes the greedy invalid.** `[1,2,3]` under [[LT_0122_Best_Time_to_Buy_and_Sell_Stock_II]] earns `2` by flipping daily; here flipping costs a day, so holding through is better. That's the diagnostic for "greedy or DP?" in this family.
- Space is reducible to `O(1)` with three rolling variables (`hold`, `sold`, `rest`) — the standard follow-up.

---

## ⚠️ Pitfalls
> [!warning]
> - **`idx == prices.length` as the base case.** With the `idx+2` sell jump this misses `idx == n+1` and throws `ArrayIndexOutOfBoundsException` on any sale made on the final day. Must be `>=`.
> - **Applying the cooldown to the buy instead of the sell.** The rule is "no buying the day *after* a sale", so the jump belongs on the sell branch — putting `+2` on the buy forbids the wrong day and quietly under-reports profit.
> - **Reusing the LT_122 greedy.** Summing every upward move returns `4` on Example 1 instead of `3`, because it assumes two free flips where the cooldown only permits one.

---

## ⏱️ Complexity
- **Time:** `O(n)`
- **Space:** `O(n)` — memo plus recursion stack (reducible to `O(1)`)
