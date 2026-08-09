---
created: 2026-08-09 18:31
tags:
  - dsa
  - arrays
  - greedy
  - dynamic-programming
source: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/
problem_id: "122"
difficulty: Medium
status: Solved
review_date:
---
# LT_0122 – Best Time to Buy and Sell Stock II

**Link:** [Open Problem](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/)

---

## 📝 Problem Description
> [!info]
> You are given an integer array `prices` where `prices[i]` is the price of a given stock on the `i`th day.
>
> On each day, you may decide to buy and/or sell the stock. You can only hold **at most one** share of the stock at any time. However, you can sell and buy the stock multiple times on the same day, ensuring you never hold more than one share.
>
> Find and return the **maximum profit** you can achieve.

---

## 🧪 Examples
> [!example]
> **Input:** `prices = [7,1,5,3,6,4]`
> **Output:** `7`
> **Explanation:** Buy on day 2 (price = 1) and sell on day 3 (price = 5), profit = `5-1 = 4`. Then buy on day 4 (price = 3) and sell on day 5 (price = 6), profit = `6-3 = 3`. Total profit is `4 + 3 = 7`.

> [!example]
> **Input:** `prices = [1,2,3,4,5]`
> **Output:** `4`
> **Explanation:** Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = `5-1 = 4`. Total profit is `4`.

> [!example]
> **Input:** `prices = [7,6,4,3,1]`
> **Output:** `0`
> **Explanation:** There is no way to make a positive profit, so we never buy the stock to achieve the maximum profit of `0`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= prices.length <= 3 * 10^4`
> - `0 <= prices[i] <= 10^4`

---

## 🔍 Intuition

Unlimited transactions with no fee and no cooldown is the *degenerate* member of the stock family — and the reason is a telescoping identity. Holding from day `i` to day `j` earns `prices[j] - prices[i]`, which is exactly the same as the sum of every consecutive daily change in between: `(p[i+1]-p[i]) + (p[i+2]-p[i+1]) + … + (p[j]-p[j-1])`.

So *any* long hold can be decomposed into a chain of one-day holds with no loss of profit. And since I'm free to buy and sell every single day, I can just **collect every upward daily move and skip every downward one** — there's no penalty for churning, so there's never a reason to sit through a decline.

That turns the whole DP (state: day × holding-or-not) into a single greedy pass summing `max(0, p[i] - p[i-1])`. The DP would work and give the same answer, but the greedy is `O(1)` space and one line of logic. The moment a fee ([[LT_0714_Best_Time_to_Buy_and_Sell_Stock_with_Transaction_Fee]]) or a cooldown ([[LT_0309_Best_Time_to_Buy_and_Sell_Stock_with_Cooldown]]) is added, the churn stops being free and this trick breaks — that's the line worth remembering.

> 🟢 *Greedy — Sum of Positive Consecutive Differences*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Greedy (Sum Every Upward Move)

**Why this works:**
- **Telescoping makes long holds and daily flips equivalent:** `p[j] - p[i] = Σ (p[t] - p[t-1])` over `t = i+1..j`. So the greedy never *loses* profit relative to holding.
- **Skipping declines is never worse:** dropping a negative term from that sum strictly increases the total, and there's no cost to re-entering the next day. So the greedy's total is an upper bound that is also achievable.
- **The all-declining case falls out for free:** no `if` ever fires, `profit` stays `0`, which is the correct "never buy" answer.

**Dry Run** (`prices = [7,1,5,3,6,4]`):

| `i` | `prices[i-1] → prices[i]` | rising? | `profit` |
|-----|---------------------------|---------|----------|
| 1 | `7 → 1` | ❌ | 0 |
| 2 | `1 → 5` | ✅ `+4` | 4 |
| 3 | `5 → 3` | ❌ | 4 |
| 4 | `3 → 6` | ✅ `+3` | **7** |
| 5 | `6 → 4` | ❌ | 7 |

Result: `7` ✅ — the same `4 + 3` the explanation describes, arrived at without ever tracking a buy price.

For `[1,2,3,4,5]` the greedy collects `1+1+1+1 = 4`, which is exactly the single hold `5 - 1` — telescoping in action.

```java
class Solution {
    public int maxProfit(int[] prices) {
        int profit = 0;

        for (int i = 1; i < prices.length; i++) {
            // Buy yesterday and sell today if profitable
            if (prices[i] > prices[i - 1]) {
                profit += prices[i] - prices[i - 1];
            }
        }

        return profit;
    }
}
```

- **Time:** `O(n)` — one pass · **Space:** `O(1)` — a single accumulator

---

## 🔑 Key Insights
- **The greedy is only valid because churning is free.** Add a per-transaction fee and `[1,2,3]` should be one trade, not two — the greedy would pay the fee twice. That single fact is what separates this from the other four problems in the family.
- **This is the `k = ∞` case of [[LT_0188_Best_Time_to_Buy_and_Sell_Stock_IV]].** It's also the standard shortcut inside that problem: when `k >= n/2` you can't be transaction-limited, so fall through to this `O(n)` greedy instead of building a `k`-deep table.
- **Contrast with [[LT_0121_Best_Time_to_Buy_and_Sell_Stock]]** (one transaction): there you must track the running minimum, because you only get one shot. Here every local rise is independently harvestable.
- The equivalent DP is `hold = max(hold, free - p[i])`, `free = max(free, hold + p[i])` — worth being able to write, since it's the form that generalises to fee and cooldown.

---

## ⚠️ Pitfalls
> [!warning]
> - **Reaching for the "buy low, sell high" single-transaction logic.** Tracking `minPrice` and one best spread solves LT_121, not this — it would return `5` instead of `7` on Example 1.
> - **Starting the loop at `i = 0`.** `prices[i-1]` underflows the array. The comparison is inherently between neighbours, so the scan starts at index `1`.
> - **Assuming this greedy transfers to the fee/cooldown variants.** It doesn't — those need the two-state DP, because a "free" daily flip is no longer free.

---

## ⏱️ Complexity
- **Time:** `O(n)`
- **Space:** `O(1)`
