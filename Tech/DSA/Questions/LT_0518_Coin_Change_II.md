---
created: 2026-06-29 10:00
tags:
  - dsa
  - dynamic-programming
  - array
source: https://leetcode.com/problems/coin-change-ii/description/
problem_id: "518"
difficulty: Medium
status: Solved
review_date:
---
# LT_0518 – Coin Change II

**Link:** [Open Problem](https://leetcode.com/problems/coin-change-ii/description/)

---

## 📝 Problem Description
> [!info]
> You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.
>
> Return the number of combinations that make up that amount. If that amount of money cannot be made up by any combination of the coins, return `0`.
>
> You may assume that you have an **infinite** number of each kind of coin.
>
> The answer is **guaranteed** to fit into a signed 32-bit integer.

---

## 🧪 Examples
> [!example]
> **Input:** `amount = 5, coins = [1,2,5]`
> **Output:** `4`
> **Explanation:** there are four ways to make up the amount:
> `5=5` | `5=2+2+1` | `5=2+1+1+1` | `5=1+1+1+1+1`

> [!example]
> **Input:** `amount = 3, coins = [2]`
> **Output:** `0`
> **Explanation:** the amount `3` cannot be made up with only coin `2`.

> [!example]
> **Input:** `amount = 10, coins = [10]`
> **Output:** `1`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= coins.length <= 300`
> - `1 <= coins[i] <= 5000`
> - All values of `coins` are **unique**.
> - `0 <= amount <= 5000`

---

## 🔍 Intuition

This problem asks for *combinations* — `[1,2]` and `[2,1]` are the same, so we must not double-count. The trick is to constrain choices to a fixed coin order using an index `idx`: at each state `(idx, amount)` we either **take** `coins[idx]` (stay at same `idx` since coins are unlimited) or **not take** it (advance to `idx+1`). This ordering ensures each combination is explored in exactly one canonical path. The 2D memoization table `dp[idx][amount]` caches the count of valid combinations reachable from each state so no subproblem is recomputed. `amount < 0` simply returns `0` — a dead end contributes zero combinations, no sentinel needed.

> 🟢 *Top-Down 2D DP (Unbounded Knapsack — Combination Count)*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Top-Down 2D DP (Memoization)

**Why this works:**
- State `(idx, amount)` = "ways to make `amount` using only coins from index `idx` onwards" — advancing `idx` only on the *not-take* path fixes coin ordering and eliminates permutation duplicates.
- "Take" recurses at the **same** `idx` (unbounded supply); "not take" moves to `idx+1`. Together they cover every valid combination without repetition.
- `amount < 0` returns `0` directly — no sentinel needed since we're counting, not minimising. This removes all guard boilerplate from the previous version.

**Dry Run** (`coins = [1,2,5], amount = 5`):

Fill order is depth-first; the final cached dp table looks like:

| idx (coin) | amt=0 | amt=1 | amt=2 | amt=3 | amt=4 | amt=5 |
|-----------|-------|-------|-------|-------|-------|-------|
| 2 (5) | 1 | 0 | 0 | 0 | 0 | 1 |
| 1 (2) | 1 | 0 | 1 | 0 | 1 | 1 |
| 0 (1) | 1 | 1 | 2 | 2 | 3 | **4** |

Key traces for row `idx=0` (coin=1):
- `dfs(0,5)` = take→`dfs(0,4)=3` + notTake→`dfs(1,5)=1` = **4** ✅
- `dfs(0,4)` = take→`dfs(0,3)=2` + notTake→`dfs(1,4)=1` = 3
- `dfs(0,3)` = take→`dfs(0,2)=2` + notTake→`dfs(1,3)=0` = 2
- `dfs(0,2)` = take→`dfs(0,1)=1` + notTake→`dfs(1,2)=1` = 2
- `dfs(0,1)` = take→`dfs(0,0)=1` + notTake→`dfs(1,1)=0` = 1

```java
class Solution {
    public int change(int amount, int[] coins) {
        int[][] dp = new int[coins.length][amount+1];
        for(int [] a : dp) Arrays.fill(a, -1);
        return dfs(coins, dp, amount, 0);
    }

    private int dfs(int[] coins, int[][] dp, int amount, int idx) {
        if (amount==0) return 1;
        if (amount < 0) return 0;
        if (dp[idx][amount]!=-1) return dp[idx][amount];

        int tempCount = dfs(coins, dp, amount-coins[idx], idx);
        if (idx+1<coins.length) tempCount += dfs(coins, dp, amount, idx+1);
        return dp[idx][amount] = tempCount;
    }
}
```

---

## 🔑 Key Insights
- `idx` in the state is the combination-dedup mechanism — it enforces a left-to-right coin order so `[1,2]` and `[2,1]` collapse to the same path.
- "Take stays at `idx`" = unbounded use; "not-take advances `idx`" = moves on permanently — this is the unbounded knapsack decision at every node.
- When `idx+1 >= coins.length` the not-take branch is skipped entirely — there are no more coins to fall back on, so only repeated takes of the current coin can still reach the target.
- `dp[idx][amount] = 0` for amounts that become positive but are unreachable (e.g., `dp[2][3]` with coin=5 — can never hit 3 by taking 5s).

---

## ⚠️ Pitfalls
> [!warning]
> - **Not advancing `idx` on not-take** — causes infinite recursion since the state never changes.
> - **Using 1D dp** directly like Coin Change I counts *permutations*, not combinations — `[1,2]` and `[2,1]` are both counted, inflating the result.
> - **Skipping the `idx+1 < coins.length` guard** on not-take — leads to an array-out-of-bounds on `dp[idx+1]` when at the last coin.
> - **Using `Integer.MAX_VALUE` for `amount < 0`** — tempting carry-over from Coin Change I, but for a counting problem it just adds guard boilerplate. Returning `0` is cleaner and correct: a negative remainder contributes zero combinations.

---

## 📊 Coin Change I vs II — Key Differences

| | Coin Change I | Coin Change II |
|---|---|---|
| Goal | Minimum coins | Count combinations |
| Base case (amount=0) | `return 0` | `return 1` |
| dp state | 1D `dp[amount]` | 2D `dp[idx][amount]` |
| "Infinity" sentinel | `Integer.MAX_VALUE` | `0` (no sentinel needed) |
| Why 2D needed? | Not needed — order irrelevant for min | Needed — `idx` prevents permutation double-count |
| Out-of-coins case | No coins left → amount unreachable | Handled by `idx+1 >= length` guard |

---

## ⏱️ Complexity
- **Time:** `O(coins.length × amount)` — each `(idx, amount)` state is computed exactly once.
- **Space:** `O(coins.length × amount)` — the 2D `dp` table; recursion stack depth is `O(coins.length + amount)`.
