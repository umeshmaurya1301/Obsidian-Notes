---
created: 2026-08-09 18:31
tags:
  - dsa
  - dynamic-programming
  - arrays
  - memoization
source: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/
problem_id: "714"
difficulty: Medium
status: Solved
review_date:
---
# LT_0714 – Best Time to Buy and Sell Stock with Transaction Fee

**Link:** [Open Problem](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/)

---

## 📝 Problem Description
> [!info]
> You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`th day, and an integer `fee` representing a transaction fee.
>
> Find the maximum profit you can achieve. You may complete **as many transactions as you like**, but you need to pay the transaction fee for each transaction.
>
> **Note:**
> - You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).
> - The transaction fee is only charged **once** for each stock purchase and sale.

---

## 🧪 Examples
> [!example]
> **Input:** `prices = [1,3,2,8,4,9], fee = 2`
> **Output:** `8`
> **Explanation:** The maximum profit can be achieved by:
> - Buying at `prices[0] = 1`
> - Selling at `prices[3] = 8`
> - Buying at `prices[4] = 4`
> - Selling at `prices[5] = 9`
>
> The total profit is `((8 - 1) - 2) + ((9 - 4) - 2) = 8`.

> [!example]
> **Input:** `prices = [1,3,7,5,10,3], fee = 3`
> **Output:** `6`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= prices.length <= 5 * 10^4`
> - `1 <= prices[i] < 5 * 10^4`
> - `0 <= fee < 5 * 10^4`

---

## 🔍 Intuition

Same setup as [[LT_0122_Best_Time_to_Buy_and_Sell_Stock_II]] — unlimited transactions — but the fee makes churning cost money. The greedy there worked because a long hold and a chain of daily flips earn identically; with a fee, the chain pays `fee` per link while the hold pays it once. So the two stop being equivalent, and I'm back to genuinely deciding *whether each rise is worth a round trip*.

That decision is take/skip, so it's the family DP with state `(day, holding?)`. No `txnLeft` dimension is needed since transactions are unlimited, which leaves just `2n` states.

The fee itself is a **one-line change** to the sell branch: `+prices[idx] - fee`. Charging it on the sell (rather than the buy) matters for a subtle reason — an unmatched buy at the end of the array should cost nothing, and only fee-on-sell gives that for free. Example 1 shows the payoff: holding `1 → 8` through the dip at `2` beats flipping, because a flip would cost an extra `fee = 2`.

> 🟢 *Take/Skip DP on (day, holding) — fee charged on sell*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Top-Down 2D DP (Memoization)

**Why this works:**
- **`- fee` on the sell branch charges each completed round trip exactly once**, matching "the fee is only charged once for each purchase and sale". A buy that is never sold never triggers it, which is exactly right — and is why fee-on-sell is cleaner than fee-on-buy.
- **`canBuy` enforces one share at a time**, so every fee corresponds to a real matched pair; there's no path where two fees are charged for one holding.
- **`idx == prices.length` is a safe base case here** because every branch advances by exactly one day — unlike [[LT_0309_Best_Time_to_Buy_and_Sell_Stock_with_Cooldown]], where the `idx+2` jump forces a `>=` guard.

**Dry Run** (`prices = [1,3,2,8,4,9], fee = 2`):

`f(i,1)` = best profit from day `i` when free to buy; `f(i,0)` = when holding.

| `idx` | `price` | `f(i,1)` free | `f(i,0)` holding | winning move at `f(i,1)` |
|-------|---------|---------------|------------------|--------------------------|
| 0 | 1 | **8** | 9 | **buy** at 1 → `f(1,0)` |
| 1 | 3 | 7 | 9 | — |
| 2 | 2 | 7 | 9 | — |
| 3 | 8 | 3 | 9 | — |
| 4 | 4 | 3 | 7 | **buy** at 4 → `f(5,0)` |
| 5 | 9 | 0 | 7 | — |

Answer `f(0,1) = 8`. The winning path: **buy at 1** → skip days 1–2 (selling at 3 would net `3-1-2 = 0`, and the dip at 2 is not worth exiting for) → **sell at 8** on day 3 → **buy at 4** on day 4 → **sell at 9** on day 5. Net `(8-1-2) + (9-4-2) = 5 + 3 = 8` ✅

> [!tip]
> Compare with the fee-free greedy: `[1,3,2,8,4,9]` has rises `+2, +6, +5 = 13`. Three round trips would cost `3 × 2 = 6`, netting `7` — worse than the two-trip answer of `8`. That gap *is* the reason the greedy fails here.

```java
class Solution {
    public int maxProfit(int[] prices, int fee) {
        int n = prices.length;
        Integer[][] dp = new Integer[n][2];
        dfs(prices, fee, dp, 0, 1);
        return dp[0][1];
    }

    private int dfs (int[] prices, int fee, Integer[][] dp, int idx, int canBuy) {
        if (idx==prices.length) return 0;
        if (dp[idx][canBuy]!=null) return dp[idx][canBuy];

        int profit = 0;
        if (canBuy==1) {
            int buy = -prices[idx] + dfs (prices, fee, dp, idx+1, 0);
            int skip = dfs (prices, fee, dp, idx+1, 1);
            profit = Math.max(buy, skip);
        } else {
            int sell = +prices[idx] + dfs (prices, fee, dp, idx + 1, 1) - fee;
            int skip = dfs (prices, fee, dp, idx + 1, 0);
            profit = Math.max (sell, skip);
        }

        return dp[idx][canBuy] = profit;
    }
}
```

- **Time:** `O(n)` — `2n` states, `O(1)` each · **Space:** `O(n)` memo + `O(n)` recursion depth

---

## 🔑 Key Insights
- **The fee is what forbids the greedy.** Its only job is to make a merge of two adjacent trades strictly better than keeping them separate whenever the intervening dip is smaller than the fee. Knowing *why* the greedy breaks is more valuable than the code.
- **Charge on sell, not on buy.** Both conventions give the same answer when every buy is matched, but fee-on-sell avoids penalising a dangling buy at the end of the array and reads more naturally against the problem's wording.
- **This is [[LT_0309_Best_Time_to_Buy_and_Sell_Stock_with_Cooldown]] with the `idx+2` swapped for `- fee`** — the same two-state skeleton, one different line. Seeing them as one solution with a parameter is the point of doing the family together.
- Space collapses to `O(1)` with two rolling variables: `free = max(free, hold + p[i] - fee)`, `hold = max(hold, free - p[i])`. At `n = 5·10⁴` the recursive version is fine, but the iterative one avoids the deep stack.

---

## ⚠️ Pitfalls
> [!warning]
> - **Charging the fee on both buy and sell.** Double-counts every trade and halves the answer on fee-heavy inputs. It's one fee per *round trip*.
> - **Copying the `idx >= prices.length` habit from the cooldown version** — harmless, but the reverse mistake matters: using `==` in LT_309 throws. Keep track of which variant jumps indices.
> - **Assuming more transactions is always better.** With `fee = 3` and rises of `2`, taking the trade *loses* money — the `skip` branch has to be a real option, which is exactly what the `Math.max` provides.

---

## ⏱️ Complexity
- **Time:** `O(n)`
- **Space:** `O(n)` — memo plus recursion stack (reducible to `O(1)`)
