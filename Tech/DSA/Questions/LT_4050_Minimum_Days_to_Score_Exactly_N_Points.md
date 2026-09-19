---
created: 2026-09-13 00:00
tags:
  - dsa
  - dynamic-programming
  - math
source: https://leetcode.com/problems/minimum-days-to-score-exactly-n-points/description/
problem_id: "4050"
difficulty: Medium
status: Solved
review_date:
---
# LT_4050 – Minimum Days to Score Exactly N Points

**Link:** [Open Problem](https://leetcode.com/problems/minimum-days-to-score-exactly-n-points/description/)

---

## 📝 Problem Description
> [!info]
> You are given an integer `n` representing a target score.
>
> Your score starts at `0`, and each day you either earn points or skip.
>
> Points are earned during a streak. On the first day of a streak you earn `1` point, on the second day `2` points, on the third day `3` points, and so on. Skipping a day earns nothing and resets the streak, so the next time you earn points, you start from `1` again.
>
> Return the minimum number of days, including any skipped days, needed to reach a score of exactly `n`.

---

## 🧪 Examples
> [!example]
> **Input:** `n = 2`
> **Output:** `3`
> **Explanation:** Day 1: earn 1 point (score 1). Day 2: skip (earning would add 2 and overshoot). Day 3: streak reset, earn 1 point — score is exactly 2 in 3 days.

> [!example]
> **Input:** `n = 9`
> **Output:** `6`
> **Explanation:** Days 1-3: earn 1, 2, 3 (score 6). Day 4: skip. Days 5-6: earn 1, 2 — score is exactly 9 in 6 days.

> [!example]
> **Input:** `n = 12`
> **Output:** `7`
> **Explanation:** Days 1-3: earn 1, 2, 3 (score 6). Day 4: skip. Days 5-7: earn 1, 2, 3 — score is exactly 12 in 7 days.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= n <= 10^5`

---

## 🔍 Intuition

A streak of length `k` always earns the same triangular total `k*(k+1)/2`, no matter which days it sits on — so I don't need to simulate day-by-day at all, only decide **which streak lengths to chain together** to hit `n` exactly. Every streak except the very last one must be followed by one skip day to reset the counter before the next streak can start again at `1`. That turns the problem into a coin-change / unbounded-knapsack: each "coin" is a streak of length `k`, worth `k*(k+1)/2` points at a cost of `k+1` days (`k` earning days + `1` reset day), and I want the minimum-cost way to make exactly `n` points. Since `k*(k+1)/2 <= n` bounds `k` to roughly `O(sqrt(n))`, there are only `O(sqrt(n))` distinct "coins" to consider, keeping the DP cheap. The final `-1` correction exists because the DP always prices in a trailing reset day after the *last* streak too, which is never actually taken.

> 🟢 *Unbounded Knapsack / Coin Change on precomputed triangular "coins"*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Precomputed Streak Costs + Unbounded Knapsack DP

**Why this works:**
- Any streak of length `k` is a reusable "block" worth `k*(k+1)/2` points for `k+1` days (the streak itself plus the mandatory reset day before the next one can begin).
- Since only `points <= n` matters, `k` is bounded by roughly `sqrt(2n)`, so precomputing all valid `(points, cost)` pairs up front is cheap — `O(sqrt(n))` of them.
- `dp[i]` = minimum days to reach exactly `i` points, built bottom-up by trying to end on each streak "coin"; this is the standard unbounded-knapsack recurrence since the same streak length can be reused any number of times (interspersed with other lengths).
- Because `dp[i]` always counts a reset day after every streak including the last, and the actual last streak doesn't need to reset, subtracting `1` at the end corrects the overcount.

**Dry Run** (`n = 9`):

Precomputed streaks (`points`, `cost`): `[1,2]`, `[3,3]`, `[6,4]` (next one, `k=4` → `points=10 > 9`, stops).

| `i` | best transition | `dp[i]` |
|---|---|---|
| 0 | base case | 0 |
| 1 | `dp[0]+2` | 2 |
| 2 | `dp[1]+2` | 4 |
| 3 | `dp[0]+3` | 3 |
| 4 | `dp[1]+3` or `dp[3]+2` | 5 |
| 5 | `dp[2]+3` | 7 |
| 6 | `dp[0]+4` | 4 |
| 7 | `dp[1]+4` or `dp[6]+2` | 6 |
| 8 | `dp[2]+4` or `dp[6]+2`... | 8 |
| 9 | `dp[6]+3` or `dp[3]+4` | 7 |

`dp[9] = 7`, answer = `dp[9] - 1 = 6` ✅ (matches Example 2).

```java
class Solution {
    public int minimumDays(int n) {
        List<int[]> streaks = new ArrayList<>();
        for (int k = 1;; k++) {
            int points = k * (k + 1) / 2;
            if (points > n) break;
            streaks.add(new int[] {points, k + 1});
        }

        int[] dp = new int[n + 1];
        Arrays.fill(dp, Integer.MAX_VALUE);
        dp[0] = 0;

        for (int i = 1; i <= n; i++) {
            for (int[] streak : streaks) {
                int points = streak[0], cost = streak[1];
                if (points <= i && dp[i - points] != Integer.MAX_VALUE) {
                    dp[i] = Math.min(dp[i], dp[i - points] + cost);
                }
            }
        }

        return dp[n] - 1;
    }
}
```

- **Time:** `O(n * sqrt(n))` (`n` DP states, each scanning `O(sqrt(n))` streaks) · **Space:** `O(n)` for `dp`, `O(sqrt(n))` for `streaks`

---

## 🔑 Key Insights
- The streak's internal day-by-day earning order never matters for the total — only its length `k` and its triangular total `k*(k+1)/2` matter, so the problem reduces to picking a multiset of streak lengths.
- Modeling each streak as costing `k+1` days (bundling in a forced reset) turns an otherwise awkward "streaks separated by skips" structure into a clean unbounded-knapsack coin set.
- `k` is bounded by `sqrt(2n)` because triangular numbers grow quadratically — this keeps the number of "coins" small even though `n` itself can be `10^5`.
- The `-1` at the end is a bookkeeping fix, not part of the core DP logic — easy to forget and easy to verify against a tiny example like `n = 2`.

---

## ⚠️ Pitfalls
> [!warning]
> - Forgetting the trailing `-1` correction gives an answer that's exactly one day too high, since every streak (including the last) gets charged a reset day in the DP.
> - Off-by-one in the streak loop: the break condition must be `points > n` (strictly greater), otherwise a streak whose points exactly equal `n` gets silently dropped.
> - Initializing `dp` with `0` instead of a sentinel (`Integer.MAX_VALUE`) would let unreachable states masquerade as reachable with cost `0`, corrupting every subsequent transition.

---

## ⏱️ Complexity
- **Time:** `O(n * sqrt(n))`
- **Space:** `O(n)`
