---
created: 2026-08-09 18:31
tags:
  - dsa
  - dynamic-programming
  - arrays
  - memoization
source: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/
problem_id: "123"
difficulty: Hard
status: Solved
review_date:
---
# LT_0123 – Best Time to Buy and Sell Stock III

**Link:** [Open Problem](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/)

---

## 📝 Problem Description
> [!info]
> You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`th day.
>
> Find the maximum profit you can achieve. You may complete **at most two transactions**.
>
> **Note:** You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).

---

## 🧪 Examples
> [!example]
> **Input:** `prices = [3,3,5,0,0,3,1,4]`
> **Output:** `6`
> **Explanation:** Buy on day 4 (price = 0) and sell on day 6 (price = 3), profit = `3-0 = 3`. Then buy on day 7 (price = 1) and sell on day 8 (price = 4), profit = `4-1 = 3`.

> [!example]
> **Input:** `prices = [1,2,3,4,5]`
> **Output:** `4`
> **Explanation:** Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = `5-1 = 4`. Note that you cannot buy on day 1, buy on day 2 and sell them later, as you are engaging multiple transactions at the same time. You must sell before buying again.

> [!example]
> **Input:** `prices = [7,6,4,3,1]`
> **Output:** `0`
> **Explanation:** In this case, no transaction is done, i.e. max profit = `0`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= prices.length <= 10^5`
> - `0 <= prices[i] <= 10^5`

---

## 🔍 Intuition

The greedy from [[LT_0122_Best_Time_to_Buy_and_Sell_Stock_II]] dies the moment transactions become a scarce resource — with only two allowed, I can't just harvest every rise, I have to choose *which* two runs are worth spending a transaction on. That choice is a classic take/skip decision, so it's DP.

The state needs three things: **which day** I'm on, **whether I'm holding a share** (that's the "must sell before you buy again" rule, encoded as `canBuy`), and **how many transactions are left**. Everything else about the past — which days I traded, what I paid — is already baked into the accumulated profit, so `(idx, canBuy, txnLeft)` is a complete state.

The elegant part is how profit is accumulated: a buy contributes `-prices[idx]` and a sell contributes `+prices[idx]`, so the recursion never needs to remember the purchase price — the arithmetic carries it. `2 × n × 2` states, `O(1)` work each, so the whole thing is linear despite looking exponential.

> 🟢 *Take/Skip DP on (day, holding, transactions left)*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Top-Down 3D DP (Memoization)

**Why this works:**
- **`canBuy` enforces the no-overlap rule structurally.** When `canBuy == 1` the only moves are *buy* or *skip*; when `canBuy == 0` they're *sell* or *skip*. There's no reachable path that buys twice in a row, so the "sell before you buy again" constraint needs no separate check.
- **Buy/sell as `-price` / `+price` removes the need to store a buy price.** The net of a matched pair telescopes to `sell - buy` automatically, which is what keeps the state 3-dimensional instead of 4.
- **`txnLeft` is decremented on the *sell*, not the buy** — so a transaction is only "spent" once it's complete. Combined with `txnLeft < 0 → 0` as a base case, this caps the count at exactly two.
- **`txnLeft` is 0-indexed:** the initial call passes `1`, meaning *two* transactions (`1` then `0`), which is why the array's third dimension is size `2`.

**Dry Run** (`prices = [3,3,5,0,0,3,1,4]`):

Reading the settled memo, where `f(i, canBuy, t)` is the best profit from day `i` onward:

| `idx` | `price` | `f(i,1,0)` 1 txn, free | `f(i,0,0)` 1 txn, holding | `f(i,1,1)` 2 txn, free | `f(i,0,1)` 2 txn, holding |
|-------|---------|------|------|------|------|
| 0 | 3 | 4 | 5 | **6** | 9 |
| 1 | 3 | 4 | 5 | 6 | 9 |
| 2 | 5 | 4 | 5 | 6 | 9 |
| 3 | 0 | 4 | 4 | 6 | 6 |
| 4 | 0 | 4 | 4 | 6 | 6 |
| 5 | 3 | 3 | 4 | 3 | 6 |
| 6 | 1 | 3 | 4 | 3 | 4 |
| 7 | 4 | 0 | 4 | 0 | 4 |

The answer is `f(0,1,1) = 6`. Following the winning branch: skip until day 3, **buy at 0** → `f(4,0,1) = 6`, **sell at 3** on day 5 → `f(6,1,0) = 3`, **buy at 1** on day 6, **sell at 4** on day 7. Total `3 + 3 = 6` ✅

> [!tip]
> The `canBuy == 0` columns look inflated (e.g. `f(0,0,1) = 9`) because they represent "I already own a share, for free" — the purchase cost was subtracted by whoever bought it. Only the `canBuy == 1` column is a real answer.

```java
class Solution {
    public int maxProfit(int[] prices) {
        int n = prices.length;
        Integer[][][] dp = new Integer[n][2][2];
        dfs (prices, dp, 0, 1, 1);
        // System.out.println(Arrays.deepToString(dp));
        return dp[0][1][1];
    }

    private int dfs (int[] prices, Integer[][][] dp, int idx, int canBuy, int txnLeft) {
        // System.out.println("idx: "+idx);
        // System.out.println("canBuy: "+canBuy);
        // System.out.println("txnLeft: "+txnLeft);
        if (txnLeft<0 ||  idx==prices.length) return 0;
        if (dp[idx][canBuy][txnLeft]!=null) return dp[idx][canBuy][txnLeft];

        int profit = 0;
        if (canBuy == 1) {
            int buy = -prices[idx] + dfs (prices, dp, idx+1, 0, txnLeft);
            int skip = dfs (prices, dp, idx+1, 1, txnLeft);
            profit = Math.max (buy, skip);
        } else {
            int sell = +prices[idx] + dfs (prices, dp, idx+1, 1, txnLeft-1);
            int skip = dfs(prices, dp, idx+1, 0, txnLeft);
            profit = Math.max(sell, skip);
        }

        return dp[idx][canBuy][txnLeft] = profit;
    }
}
```

- **Time:** `O(n · 2 · 2) = O(n)` — `4n` states, `O(1)` each · **Space:** `O(n)` memo + `O(n)` recursion depth

---

## 🔑 Key Insights
- **`txnLeft < 0` must be checked *before* indexing the memo.** The sell branch calls with `txnLeft-1`, which reaches `-1`; without that guard as the first line, `dp[idx][canBuy][-1]` throws. The ordering of the two base conditions is load-bearing.
- **This exact code is [[LT_0188_Best_Time_to_Buy_and_Sell_Stock_IV]] with the `2` hard-coded.** Generalising is a one-character change to the array dimension plus passing `k-1` — worth internalising as *one* solution, not two.
- **The whole stock family is the same skeleton**, differing only in one line: unlimited + free ([[LT_0122_Best_Time_to_Buy_and_Sell_Stock_II]]) collapses to greedy; a fee subtracts on sell ([[LT_0714_Best_Time_to_Buy_and_Sell_Stock_with_Transaction_Fee]]); a cooldown jumps `idx+2` on sell ([[LT_0309_Best_Time_to_Buy_and_Sell_Stock_with_Cooldown]]).
- **`Integer[][][]` (boxed) uses `null` as "unvisited"** — necessary because `0` is a legitimate profit, so no primitive sentinel is safe here.
- Space drops to `O(1)` in the bottom-up form: only four rolling variables (`buy1, sell1, buy2, sell2`) are ever needed, which is the interview-preferred `O(n)`/`O(1)` answer.

---

## ⚠️ Pitfalls
> [!warning]
> - **Decrementing `txnLeft` on the buy instead of the sell.** Both count transactions, but mixing conventions (decrement on buy *and* base-case at `txnLeft < 0`) silently allows or forbids one extra trade. Pick one and stay consistent.
> - **`return dp[0][1][1]` rather than the `dfs` return value.** It's safe here only because `n >= 1` guarantees the slot is written; returning the call result directly is both clearer and immune to the empty-array edge case.
> - **Recursion depth at `n = 10⁵`.** The top-down version recurses one level per day and can blow the default JVM stack on the largest inputs — the iterative/rolling-variable version avoids this entirely.

---

## ⏱️ Complexity
- **Time:** `O(n)` — `4n` distinct states
- **Space:** `O(n)` — memo table plus recursion stack (reducible to `O(1)` bottom-up)
