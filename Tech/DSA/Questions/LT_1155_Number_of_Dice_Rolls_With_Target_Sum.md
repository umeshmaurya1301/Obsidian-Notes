---
created: 2026-08-09 18:31
tags:
  - dsa
  - dynamic-programming
  - memoization
source: https://leetcode.com/problems/number-of-dice-rolls-with-target-sum/
problem_id: "1155"
difficulty: Medium
status: Solved
review_date:
---
# LT_1155 – Number of Dice Rolls With Target Sum

**Link:** [Open Problem](https://leetcode.com/problems/number-of-dice-rolls-with-target-sum/)

---

## 📝 Problem Description
> [!info]
> You have `n` dice, and each dice has `k` faces numbered from `1` to `k`.
>
> Given three integers `n`, `k`, and `target`, return the number of possible ways (out of the `k^n` total ways) to roll the dice, so the sum of the face-up numbers equals `target`.
>
> Since the answer may be too large, return it **modulo** `10^9 + 7`.

---

## 🧪 Examples
> [!example]
> **Input:** `n = 1, k = 6, target = 3`
> **Output:** `1`
> **Explanation:** You throw one die with 6 faces. There is only one way to get a sum of 3.

> [!example]
> **Input:** `n = 2, k = 6, target = 7`
> **Output:** `6`
> **Explanation:** You throw two dice, each with 6 faces. There are 6 ways to get a sum of 7: `1+6`, `2+5`, `3+4`, `4+3`, `5+2`, `6+1`.

> [!example]
> **Input:** `n = 30, k = 30, target = 500`
> **Output:** `222616187`
> **Explanation:** The answer must be returned modulo `10^9 + 7`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= n, k <= 30`
> - `1 <= target <= 1000`

---

## 🔍 Intuition

Each die is a **decision point with `k` branches**, and rolling all `n` dice is one root-to-leaf path in a `k`-ary tree of depth `n`. Counting paths that sum to `target` is a plain "count the ways" DP: pick a face for die `idx`, subtract it from the remaining target, recurse on die `idx+1`, and add up the branch counts.

The state that matters is `(idx, remain)` — *which die am I on* and *how much target is left*. How I got to a remainder of `4` with three dice used is irrelevant to how many ways the rest can finish, so distinct paths that collapse onto the same `(idx, remain)` share an answer. That's the overlap the `n × (target+1)` memo table exploits: `k^n = 30^30` raw paths shrink to at most `30 × 1001` distinct states.

The one thing that differs from the [[LT_0322_Coin_Change]] family is that the item count is **fixed** — I must use exactly `n` dice, no more, no fewer. So the base case checks `idx == n` *and* `remain == 0` together: running out of dice with target left over is a dead branch, not a partial success.

> 🟢 *Count-the-Ways DP over (index, remaining target)*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Top-Down 2D DP (Memoization)

**Why this works:**
- **State `(idx, remain)` is sufficient:** the number of ways to finish depends only on how many dice are left and how much sum is left, never on which faces were already chosen. So the memo is legal and the table is exactly `n × (target+1)`.
- **Exactly-`n`-dice is enforced by the base case:** `idx == n && remain == 0` → `1` (a complete valid roll); `idx == n && remain != 0` → `0` (dice exhausted, target missed). There's no "stop early" branch, which is precisely what makes this different from unbounded-coin counting.
- **`newRemain >= 0` prunes overshoot** before recursing, so the memo is never indexed with a negative column — the guard doubles as the bounds check.
- **The modulo is applied at every accumulation** (`ways += tempWays; ways %= MOD;`), so `ways` can never exceed `2 × (10^9+7)` and overflow `int`.

**Dry Run** (`n = 2, k = 6, target = 7`):

`dp` has 2 rows (die 0, die 1) and 8 columns (remain 0..7).

| call | faces tried (`newRemain`) | result |
|------|---------------------------|--------|
| `dfs(1, 6)` | `1→5, 2→4, 3→3, 4→2, 5→1, 6→0` | only face `6` reaches `remain=0` at `idx=2` → `dp[1][6] = 1` |
| `dfs(1, 5)` | face `5` hits `0` | `dp[1][5] = 1` |
| `dfs(1, 4)` | face `4` hits `0` | `dp[1][4] = 1` |
| `dfs(1, 3)` | face `3` hits `0` | `dp[1][3] = 1` |
| `dfs(1, 2)` | face `2` hits `0` | `dp[1][2] = 1` |
| `dfs(1, 1)` | face `1` hits `0` | `dp[1][1] = 1` |
| `dfs(0, 7)` | `1→dp[1][6]=1`, `2→dp[1][5]=1`, `3→dp[1][4]=1`, `4→dp[1][3]=1`, `5→dp[1][2]=1`, `6→dp[1][1]=1` | `dp[0][7] = 6` |

Result: `dp[0][7] = 6` ✅ — matching `1+6, 2+5, 3+4, 4+3, 5+2, 6+1`.

```java
class Solution {
    private static final int MOD = 1000000007;

    public int numRollsToTarget(int n, int k, int target) {
        int[][] dp = new int[n][target+1];
        for (int[] a : dp) Arrays.fill(a, -1);
        dfs(k, dp, 0, target);
        System.out.println(Arrays.deepToString(dp));
        return dp[0][target];
    }

    private int dfs (int k, int[][] dp, int idx, int remain) {

        if (idx==dp.length && remain != 0) return 0;
        if (idx==dp.length && remain == 0) return 1;
        if (dp[idx][remain] != -1) return dp[idx][remain];

        int ways = 0;

        for (int i=1; i<=k; i++) {
            int newRemain = remain - i;
            // System.out.println("Calling for newRemain: "+newRemain);
            if (newRemain >= 0) {
                int tempWays = (dfs (k, dp, idx + 1, newRemain))%MOD;
                ways += tempWays;
                ways %= MOD;
            }
        }

        return dp[idx][remain] = ways;
    }
}
```

- **Time:** `O(n · target · k)` — at most `30 × 1001 × 30 ≈ 9·10⁵` operations · **Space:** `O(n · target)` table + `O(n)` recursion depth

---

## 🔑 Key Insights
- **"Exactly `n` items" vs "any number of items" is the whole difference** between this and [[LT_0322_Coin_Change]] / `LT_0518`. Here the index is a *counter that must reach `n`*, not just a pointer that may stop early — so the success test is a conjunction of both base conditions.
- **The two `idx == dp.length` lines are one decision.** They read as two base cases but really encode "a leaf counts as `1` iff the target was consumed exactly" — collapsing them to `return remain == 0 ? 1 : 0;` is equivalent and clearer.
- **Order of faces doesn't need de-duplicating.** Unlike Coin Change II, `1+6` and `6+1` *are* distinct rolls, so recursing on `idx+1` for every face (rather than restricting to non-decreasing faces) is correct by design.
- **Reachability pruning is free:** if `target > n·k` or `target < n` the answer is `0`, and the `newRemain >= 0` guard plus the exact-`n` base case produce that naturally without a special check.

---

## ⚠️ Pitfalls
> [!warning]
> - **Applying the modulo only at the return.** `ways` accumulates up to `k` sub-results, each near `10^9` — without the `ways %= MOD` inside the loop it overflows `int` after two iterations and goes negative.
> - **Returning `dp[0][target]` instead of the `dfs` result.** It works here only because `n >= 1` guarantees `dfs(0, target)` writes that slot before returning. Returning the call's value directly is safer and drops the stray `System.out.println`.
> - **Allowing a face value of `0`.** Faces are `1..k`, so the loop must start at `i = 1`; starting at `0` would let a die contribute nothing and break the exactly-`n` invariant, producing infinite recursion on `remain`.

---

## ⏱️ Complexity
- **Time:** `O(n · target · k)`
- **Space:** `O(n · target)` — memo table, plus `O(n)` recursion stack
