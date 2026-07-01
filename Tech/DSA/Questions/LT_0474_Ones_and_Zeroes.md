---
created: 2026-07-01 00:00
tags:
  - dsa
  - dynamic-programming
  - array
  - string
source: https://leetcode.com/problems/ones-and-zeroes/
problem_id: "474"
difficulty: Medium
status: Solved
review_date:
---
# LT_0474 – Ones and Zeroes

**Link:** [Open Problem](https://leetcode.com/problems/ones-and-zeroes/)

---

## 📝 Problem Description
> [!info]
> You are given an array of binary strings `strs` and two integers `m` and `n`.
>
> Return the size of the largest subset of `strs` such that there are **at most** `m` `0`'s and `n` `1`'s in the subset.
>
> A set `x` is a subset of a set `y` if all elements of `x` are also elements of `y`.

---

## 🧪 Examples
> [!example]
> **Input:** `strs = ["10","0001","111001","1","0"], m = 5, n = 3`
> **Output:** `4`
> **Explanation:** The largest subset with at most 5 `0`'s and 3 `1`'s is `{"10", "0001", "1", "0"}`, so the answer is `4`. Other valid but smaller subsets include `{"0001", "1"}` and `{"10", "1", "0"}`. `{"111001"}` is invalid because it contains 4 `1`'s, more than the maximum of 3.

> [!example]
> **Input:** `strs = ["10","0","1"], m = 1, n = 1`
> **Output:** `2`
> **Explanation:** The largest subset is `{"0", "1"}`, so the answer is `2`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= strs.length <= 600`
> - `1 <= strs[i].length <= 100`
> - `strs[i]` consists only of digits `'0'` and `'1'`
> - `1 <= m, n <= 100`

---

## 🔍 Intuition

Each string is an item with a cost — its own count of `0`'s and its own count of `1`'s — and I have two shared budgets, `m` zeros and `n` ones, to spend across all items I pick. That's exactly **0/1 knapsack with two weight dimensions** instead of one: every string is either taken (pay its zero-cost and one-cost, gain `+1` to the count) or skipped (pay nothing, gain nothing). Brute-force trying every subset is `O(2^len)`, hopeless for `len` up to 600, but the outcome of any future decision depends only on *how many strings are left* and *how much budget remains* — not on which specific strings were already chosen. That's the signal to memoize on `(idx, zerosRemaining, onesRemaining)`.

> 🟢 *0/1 Knapsack — Take or Skip*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Top-Down Memoization (Take/Skip DP)

**Why this works:**
- `dfs(idx, zerosRemaining, onesRemaining)` answers "how many more strings can I still select, using strings from `idx` onward, with this much budget left?" — a pure function of those three numbers, so it's safely memoizable in a 3D table.
- At each index there are only two moves — skip `strs[idx]` entirely, or take it if the budget covers its zero/one cost — and the answer is the max of the two branches.
- Guarding the "take" branch with a budget check (`zerosRemaining >= zeros && onesRemaining >= ones`) means invalid states are **never generated** in the first place, rather than being generated and then filtered out with a sentinel like `Integer.MIN_VALUE`. Cleaner, and there's no base-case-ordering trap to worry about (see Pitfalls).

**Dry Run** (`strs = ["10","0","1"], m = 1, n = 1`):

| idx | string | zeros/ones | zerosRemaining, onesRemaining | can take? | take | notTake | result |
|---|---|---|---|---|---|---|---|
| 2 | `"1"` | 0,1 | 1,1 | yes | `1 + dfs(3,1,0)=1` | `dfs(3,1,1)=0` | `max(1,0)=1` |
| 1 | `"0"` | 1,0 | 1,1 | yes | `1 + dfs(2,0,1)` → at idx 2, `zerosRemaining=0` so `"1"` still fits (costs 0 zeros) → `1+1=2` | `dfs(2,1,1)=1` | `max(2,1)=2` |
| 0 | `"10"` | 1,1 | 1,1 | yes | `1 + dfs(1,0,0)` → at idx 1 `"0"` needs 1 zero but `zerosRemaining=0` → can't take; `"1"` needs 1 one but `onesRemaining=0` → can't take → `0`; so `take=1` | `dfs(1,1,1)=2` (computed above) | `max(1,2)=2` |

Final answer at `idx=0`: `2` ✅ (matches `{"0","1"}`)

```java
class Solution {
    public int findMaxForm(String[] strs, int m, int n) {
        int len = strs.length;
        int[][][] memo = new int[len][m + 1][n + 1];
        for (int[][] row : memo)
            for (int[] col : row)
                Arrays.fill(col, -1);
        return dfs(strs, 0, m, n, memo);
    }

    private int dfs(String[] strs, int idx, int zerosRemaining, int onesRemaining, int[][][] memo) {
        if (idx == strs.length) return 0;
        if (memo[idx][zerosRemaining][onesRemaining] != -1)
            return memo[idx][zerosRemaining][onesRemaining];

        int[] count = countZerosOnes(strs[idx]);
        int zeros = count[0], ones = count[1];

        int notTake = dfs(strs, idx + 1, zerosRemaining, onesRemaining, memo);

        int take = 0;
        if (zerosRemaining >= zeros && onesRemaining >= ones) {
            take = 1 + dfs(strs, idx + 1, zerosRemaining - zeros, onesRemaining - ones, memo);
        }

        return memo[idx][zerosRemaining][onesRemaining] = Math.max(take, notTake);
    }

    private int[] countZerosOnes(String s) {
        int zeros = 0, ones = 0;
        for (char c : s.toCharArray()) {
            if (c == '0') zeros++;
            else ones++;
        }
        return new int[]{zeros, ones};
    }
}
```

---

## 🔑 Key Insights
- This is 0/1 knapsack with **two** capacity dimensions (`m` zeros, `n` ones) instead of one — the recursion shape is identical to single-capacity knapsack, just with an extra parameter threaded through.
- `dfs`'s meaning is "max strings selectable from `idx` onward" — never "how many have I selected so far." Keeping that framing straight is what makes the base cases obvious.
- Prefer guarding the take-branch with a capacity check over generating negative/invalid states and returning a sentinel (`Integer.MIN_VALUE`) — it avoids an entire class of base-case-ordering bugs.

---

## ⚠️ Pitfalls
> [!warning]
> - **If you do use a sentinel for invalid states** (`zerosRemaining < 0` → `Integer.MIN_VALUE`), the invalid-state check **must** come before the `idx == len` check. `dfs(len, -1, ...)` satisfies both conditions simultaneously — checking "finished" first wrongly returns `0`, and the caller then computes `take = 1 + 0`, silently counting an impossible selection. Checking "invalid" first correctly returns the sentinel instead.
> - Bottom-up 2D DP (`dp[z][o]`) is the standard follow-up optimization here (iterate strings, update `dp[z][o] = max(dp[z][o], 1 + dp[z-zeros][o-ones])` in reverse order of `z, o` to keep it 0/1 not unbounded) — worth revisiting to compare against this top-down version.

---

## ⏱️ Complexity
- **Time:** `O(len * m * n)` — each of the `len * (m+1) * (n+1)` states is computed once and memoized; counting zeros/ones per string adds `O(len * L)` where `L` is max string length
- **Space:** `O(len * m * n)` for the memo table, plus `O(len)` recursion depth
