---
created: 2026-05-28 00:00
tags:
  - dsa
  - array
  - greedy
  - dynamic-programming
source: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/
problem_id: "121"
difficulty: Easy
status: Solved
review_date:
---
# LT_0121 – Best Time to Buy and Sell Stock

**Link:** [Open Problem](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/)

---

## 📝 Problem Description
> [!info]
> You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`th day.
>
> You want to maximize your profit by choosing **a single day** to buy one stock and choosing a **different day in the future** to sell that stock.
>
> Return the *maximum profit* you can achieve from this transaction. If you cannot achieve any profit, return `0`.

---

## 🧪 Examples
> [!example]
> **Input:** `prices = [7, 1, 5, 3, 6, 4]`
> **Output:** `5`
> **Explanation:** Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6 − 1 = 5. Buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

> [!example]
> **Input:** `prices = [7, 6, 4, 3, 1]`
> **Output:** `0`
> **Explanation:** In this case, no transactions are done and the max profit = 0.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= prices.length <= 10^5`
> - `0 <= prices[i] <= 10^4`

---

## 🔍 Intuition

At every price, the best possible profit is `currentPrice - lowestPriceSoFar`. So if I track the running minimum as I scan left to right, I can compute the best sell profit at each point without looking ahead. I don't need DP or a second pass — the greedy insight is that I always want to buy at the cheapest price seen before now. I update `min` first (would I buy today?), then check if selling today beats my best profit. This single-pass greedy is O(n) and needs only two variables.

> 🟢 *Greedy — Single Pass, Track Minimum*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Greedy One Pass (Track Min Price)

**Why this works:**
- The minimum price seen so far is always the ideal buy day for any future sell — no look-ahead needed.
- Updating `min` before computing `num - min` ensures we never sell before we buy (same-day gives profit 0, which is fine).
- `max` accumulates the best profit seen at any sell point, so the answer is naturally the global maximum.

**Dry Run** (`prices = [7, 1, 5, 3, 6, 4]`):

| Step | `num` | `min` | `num - min` | `max` |
|------|-------|-------|-------------|-------|
| 1    | 7     | 7     | 0           | 0     |
| 2    | 1     | 1     | 0           | 0     |
| 3    | 5     | 1     | 4           | 4     |
| 4    | 3     | 1     | 2           | 4     |
| 5    | 6     | 1     | **5**       | **5** |
| 6    | 4     | 1     | 3           | 5     |

Return: `5` ✓

```java
class Solution {
    public int maxProfit(int[] prices) {
        int min = Integer.MAX_VALUE;
        int max = Integer.MIN_VALUE;

        for(int num:prices) {
            if(num<min) {
                min = num;
            }
            max = Math.max(max, num-min);
        }

        return max;
    }
}
```

---

## 🔑 Key Insights
- Update `min` **before** computing `num - min` so the same-day buy-sell (profit 0) is handled correctly and you never compute a negative "future" profit.
- Initialising `max = Integer.MIN_VALUE` still works: on the very first iteration `min` is set to `num`, making `num - min = 0`, which overwrites `MIN_VALUE` immediately.
- This is essentially a simplified DP: `maxProfit[i] = max(maxProfit[i-1], prices[i] - minPrice[i-1])`, collapsed to two variables.
- A strictly decreasing array always yields profit 0 — the running minimum chases the price down, keeping `num - min = 0` every step.

---

## ⚠️ Pitfalls
> [!warning]
> - Forgetting to update `min` **before** computing profit — doing it after means you use yesterday's min, which skips the same-day 0-profit base case and can return `Integer.MIN_VALUE` for a length-1 array.
> - Returning a raw negative number when all prices decrease — handled here because `num - min` is always ≥ 0 after `min` is updated first.
> - Using a brute-force O(n²) double loop when the greedy O(n) pass is sufficient for this single-transaction variant.

---

## ⏱️ Complexity
- **Time:** `O(n)` — single pass through `prices`
- **Space:** `O(1)` — only `min` and `max` variables
