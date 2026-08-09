---
created: 2026-08-09 18:31
tags:
  - dsa
  - dynamic-programming
  - arrays
  - memoization
source: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/
problem_id: "188"
difficulty: Hard
status: Solved
review_date:
---
# LT_0188 – Best Time to Buy and Sell Stock IV

**Link:** [Open Problem](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/)

---

## 📝 Problem Description
> [!info]
> You are given an integer array `prices` where `prices[i]` is the price of a given stock on the `i`th day, and an integer `k`.
>
> Find the maximum profit you can achieve. You may complete **at most `k` transactions**: i.e. you may buy at most `k` times and sell at most `k` times.
>
> **Note:** You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).

---

## 🧪 Examples
> [!example]
> **Input:** `k = 2, prices = [2,4,1]`
> **Output:** `2`
> **Explanation:** Buy on day 1 (price = 2) and sell on day 2 (price = 4), profit = `4-2 = 2`.

> [!example]
> **Input:** `k = 2, prices = [3,2,6,5,0,3]`
> **Output:** `7`
> **Explanation:** Buy on day 2 (price = 2) and sell on day 3 (price = 6), profit = `6-2 = 4`. Then buy on day 5 (price = 0) and sell on day 6 (price = 3), profit = `3-0 = 3`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= k <= 100`
> - `1 <= prices.length <= 1000`
> - `0 <= prices[i] <= 1000`

---

## 🔍 Intuition

This is [[LT_0123_Best_Time_to_Buy_and_Sell_Stock_III]] with the `2` pulled out into a parameter — literally the same recursion, the same three-part state, and the same buy-as-`-price` / sell-as-`+price` accounting. Once I've written the `at most two` version, the generalisation is a change to one array dimension and one initial argument.

The state stays `(day, holding?, transactions left)`, because those three facts fully determine what's still achievable: past trades only matter through the profit already banked, and `canBuy` is what encodes "you must sell before buying again". The table is `n × 2 × k`, so with `n = 1000` and `k = 100` that's `2 × 10⁵` states — comfortably fast at `O(1)` work each.

The one genuinely new idea `k` brings is a **degeneracy check**: a completed transaction needs at least two distinct days, so more than `n/2` transactions can never all be used. Once `k >= n/2` the cap stops binding and the problem *is* [[LT_0122_Best_Time_to_Buy_and_Sell_Stock_II]] — solvable by the `O(n)`/`O(1)` greedy. The solution below doesn't take that shortcut (it doesn't need to at these constraints), but it's the first thing an interviewer will ask about.

> 🟢 *Take/Skip DP on (day, holding, transactions left) — generalised `k`*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Top-Down 3D DP (Memoization)

**Why this works:**
- **`txnLeft` is 0-indexed against a `k`-wide dimension.** The initial call passes `k-1`, so the legal values are `k-1 … 0` — exactly `k` transactions — and the `txnLeft < 0` base case is what closes the budget.
- **The decrement lands on the sell**, so a transaction is only spent once the round trip completes. A buy that never sells simply never costs anything (and never earns anything either, since the `-price` stays unmatched and loses to `skip`).
- **`canBuy` structurally forbids overlapping trades** — from a holding state the only options are *sell* or *skip*, so no path can hold two shares.

**Dry Run** (`k = 2, prices = [3,2,6,5,0,3]`):

`txnLeft` runs over `{1, 0}`. The settled memo, `f(i, canBuy, t)`:

| `idx` | `price` | `f(i,1,0)` | `f(i,0,0)` | `f(i,1,1)` | `f(i,0,1)` |
|-------|---------|------------|------------|------------|------------|
| 0 | 3 | 4 | 6 | **7** | 9 |
| 1 | 2 | 4 | 6 | 7 | 9 |
| 2 | 6 | 3 | 6 | 3 | 9 |
| 3 | 5 | 3 | 5 | 3 | 8 |
| 4 | 0 | 3 | 3 | 3 | 3 |
| 5 | 3 | 0 | 3 | 0 | 3 |

Answer is `f(0,1,1) = 7`. Tracing the winning branch: skip day 0 → **buy at 2** (day 1) → **sell at 6** (day 2, spends txn 1) → skip day 3 → **buy at 0** (day 4) → **sell at 3** (day 5, spends txn 0). Net `-2 + 6 - 0 + 3 = 7` ✅

```java
class Solution {
    public int maxProfit(int k, int[] prices) {
        int n = prices.length;
        Integer[][][] dp = new Integer[n][2][k];
        dfs (prices, dp, 0, 1, k-1);
        return dp[0][1][k-1];
    }

    private int dfs (int[] prices, Integer[][][] dp, int idx, int canBuy, int txnLeft) {
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

- **Time:** `O(n · k)` — `2nk` states, `O(1)` each · **Space:** `O(n · k)` memo + `O(n)` recursion depth

---

## 🔑 Key Insights
- **`k >= n/2` ⇒ the cap is non-binding.** Each transaction consumes at least two days, so beyond `n/2` transactions the limit can never be reached — short-circuit to the [[LT_0122_Best_Time_to_Buy_and_Sell_Stock_II]] greedy for `O(n)` time and `O(1)` space. This is the expected follow-up when `k` is allowed to be large.
- **The `txnLeft < 0` guard must precede the memo lookup**, since the sell branch passes `txnLeft-1` and legitimately reaches `-1`. Reordering those two lines turns a correct solution into an `ArrayIndexOutOfBoundsException`.
- **Off-by-one lives in the third dimension.** `new Integer[n][2][k]` with an initial `k-1` is a 0-indexed budget; writing `[k+1]` with an initial `k` is the other common convention. Both work — mixing them doesn't.
- **One skeleton, five problems.** [[LT_0121_Best_Time_to_Buy_and_Sell_Stock]] is `k=1`, [[LT_0123_Best_Time_to_Buy_and_Sell_Stock_III]] is `k=2`, [[LT_0122_Best_Time_to_Buy_and_Sell_Stock_II]] is `k=∞`, and the fee/cooldown variants change exactly one line of the sell branch.

---

## ⚠️ Pitfalls
> [!warning]
> - **`new Integer[n][2][k]` when `k` could be `0`.** The constraints here guarantee `k >= 1`, but a `k = 0` input would make the third dimension empty and `dp[0][1][-1]` fail immediately. Guard it if the constraint ever loosens.
> - **Skipping the `k >= n/2` shortcut on large `k`.** With this problem's `k <= 100` and `n <= 1000` the plain table is fine, but on a variant with `k = 10⁹` the `O(n·k)` allocation is fatal.
> - **Recursion depth.** One frame per day means `n = 1000` is safe here, but the same code applied to LT_123's `n = 10⁵` can overflow the stack — prefer the bottom-up form when `n` is large.

---

## ⏱️ Complexity
- **Time:** `O(n · k)`
- **Space:** `O(n · k)` — memo table, plus `O(n)` recursion stack
