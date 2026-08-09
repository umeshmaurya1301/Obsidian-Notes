---
created: 2026-08-09 18:31
tags:
  - dsa
  - dynamic-programming
  - math
  - memoization
source: https://leetcode.com/problems/perfect-squares/
problem_id: "279"
difficulty: Medium
status: Solved
review_date:
---
# LT_0279 – Perfect Squares

**Link:** [Open Problem](https://leetcode.com/problems/perfect-squares/)

---

## 📝 Problem Description
> [!info]
> Given an integer `n`, return the **least** number of perfect square numbers that sum to `n`.
>
> A **perfect square** is an integer that is the square of an integer; in other words, it is the product of some integer with itself. For example, `1`, `4`, `9`, and `16` are perfect squares while `3` and `11` are not.

---

## 🧪 Examples
> [!example]
> **Input:** `n = 12`
> **Output:** `3`
> **Explanation:** `12 = 4 + 4 + 4`.

> [!example]
> **Input:** `n = 13`
> **Output:** `2`
> **Explanation:** `13 = 4 + 9`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= n <= 10^4`

---

## 🔍 Intuition

This is [[LT_0322_Coin_Change]] wearing a different hat: the "coins" are the perfect squares `1, 4, 9, 16, …` up to `n`, supply is unlimited, and I want the **fewest** of them summing to `n`. Once I see that, the recurrence writes itself — `minSquares(n) = 1 + min(minSquares(n - i²))` over every `i` with `i² ≤ n`.

The state is a single integer (the remaining amount), because how I got to a remainder never changes how cheaply I can finish it. Different orderings of the same squares collapse onto the same remainder, which is exactly the overlap that makes memoisation worth it: without it the recursion tree branches `√n` ways at every level and blows up exponentially.

The one thing that differs from Coin Change is that **the coin list isn't given — it's generated on the fly** by `i*i <= n` inside the loop, which also means the branching factor shrinks as the remainder does. And unlike Coin Change, no `-1` case exists: `1` is always a perfect square, so every `n` is reachable and the answer is always finite.

> 🟢 *Unbounded Knapsack / Coin Change (Min Count) — Top-Down DP*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Top-Down DP (Memoization)

**Why this works:**
- **Optimal substructure:** subtracting one square `i²` leaves an independent subproblem `n - i²`, so `dp[n] = 1 + min(dp[n - i²])` is correct — the best way to finish a remainder is the same no matter which squares preceded it.
- **`i*i <= n` guards the recursion**, so the recursive call always gets a non-negative argument. That makes the `if (n<0) return 0;` line **unreachable** in practice — harmless here, but it would be a genuine bug if the guard were ever loosened, since returning `0` for a negative remainder would report a bogus valid split.
- **No unreachable sentinel needed.** `i = 1` is always available (`1² = 1 ≤ n`), so `ans` is always overwritten with a finite value before it's stored — unlike Coin Change, `Integer.MAX_VALUE` can never survive into `dp`, and there's no `MAX_VALUE + 1` overflow risk.

**Dry Run** (`n = 12`):

The recursion goes depth-first from `12`, but the settled table reads cleanly bottom-up:

| `n` | squares tried (`1+dp[n-i²]`) | `dp[n]` |
|-----|------------------------------|---------|
| 1 | `1+dp[0]=1` | 1 |
| 2 | `1+dp[1]=2` | 2 |
| 3 | `1+dp[2]=3` | 3 |
| 4 | `1+dp[3]=4`, `1+dp[0]=1` | **1** |
| 7 | `1+dp[6]=4`, `1+dp[3]=4` | 4 |
| 8 | `1+dp[7]=5`, `1+dp[4]=2` | **2** |
| 11 | `1+dp[10]=3`, `1+dp[7]=5`, `1+dp[2]=3` | 3 |
| 12 | `1+dp[11]=4`, `1+dp[8]=3`, `1+dp[3]=4` | **3** |

`dp[12] = 3` → `4 + 4 + 4` ✅

```java
class Solution {
    public int numSquares(int n) {
        int[] dp = new int[n+1];
        Arrays.fill(dp, -1);
        dfs(n, dp);
        return dp[n];
    }

    private int dfs(int n, int[] dp) {
        if (n==0) return 0;
        if (n<0) return 0;
        if (dp[n] != -1) return dp[n];

        int ans = Integer.MAX_VALUE;
        for (int i=1; i*i<=n; i++) {
            ans = Math.min(ans, 1 + dfs(n-i*i, dp));
        }

        return dp[n] = ans;
    }
}
```

- **Time:** `O(n√n)` — `n` distinct states, each looping over `√n` candidate squares · **Space:** `O(n)` — dp array plus `O(n)` worst-case recursion depth (the all-`1`s chain)

---

## 🔑 Key Insights
- **Recognise the shape, not the story.** "Fewest items from an unlimited pool summing to a target" is Coin Change every time — [[LT_0322_Coin_Change]], `LT_0518`, and this problem share one recurrence and differ only in where the item list comes from.
- **The item list is derived, not given.** `i*i <= n` regenerates the usable squares per call, so the branching factor is `√n` and naturally shrinks as the remainder does.
- **`-1` can never be the answer here.** Because `1 = 1²`, the worst case is `n` ones — which also means `dp[n] <= n` always, and (by Lagrange's four-square theorem) actually `dp[n] <= 4` for every `n`. That's the basis of the `O(√n)` math solution, though it's not what this DP does.
- `dp[0]` is never written — the `n == 0` base case returns before the memo lookup, so the slot stays `-1` and is simply never read.

---

## ⚠️ Pitfalls
> [!warning]
> - **Returning `dp[n]` without calling `dfs` first.** `numSquares` relies on the side effect of `dfs(n, dp)` filling the slot; returning the `dfs` result directly is clearer and equivalent.
> - **Looping `i` up to `n` instead of `i*i <= n`.** Costs a factor of `√n` for nothing, and `i*i` overflows `int` for large `i` if written as `i <= Math.sqrt(n)` carelessly.
> - **Copy-pasting the `if (n<0) return 0;` guard into Coin Change.** There, negative remainders *are* reachable and must return an unreachable sentinel — returning `0` would claim a valid zero-coin split.

---

## ⏱️ Complexity
- **Time:** `O(n√n)`
- **Space:** `O(n)` — memo array + recursion stack
