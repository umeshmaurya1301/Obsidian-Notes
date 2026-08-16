---
created: 2026-08-10 11:05
tags:
  - dsa
  - dynamic-programming
  - memoization
  - grid-dp
  - matrix
source: https://leetcode.com/problems/cherry-pickup-ii/description/
problem_id: "1463"
difficulty: Hard
status: Solved
review_date:
---
# LT_1463 – Cherry Pickup II

**Link:** [Open Problem](https://leetcode.com/problems/cherry-pickup-ii/description/)

---

## 📝 Problem Description
> [!info]
> You are given a `rows x cols` matrix `grid` representing a field of cherries where `grid[i][j]` represents the number of cherries that you can collect from the `(i, j)` cell.
>
> You have two robots that can collect cherries for you:
> - **Robot #1** is located at the top-left corner `(0, 0)`, and
> - **Robot #2** is located at the top-right corner `(0, cols - 1)`.
>
> Return the maximum number of cherries collected using both robots by following the rules below:
> - From a cell `(i, j)`, robots can move to cell `(i + 1, j - 1)`, `(i + 1, j)`, or `(i + 1, j + 1)`.
> - When any robot passes through a cell, it picks up all cherries, and the cell becomes empty.
> - When both robots stay in the same cell, only one takes the cherries.
> - Both robots cannot move outside of the grid at any moment.
> - Both robots should reach the bottom row in `grid`.

---

## 🧪 Examples
> [!example]
> **Input:** `grid = [[3,1,1],[2,5,1],[1,5,5],[2,1,1]]`
> **Output:** `24`
> **Explanation:** Cherries taken by Robot #1: `3 + 2 + 5 + 2 = 12`. Cherries taken by Robot #2: `1 + 5 + 5 + 1 = 12`. Total: `24`.

> [!example]
> **Input:** `grid = [[1,0,0,0,0,0,1],[2,0,0,0,0,3,0],[2,0,9,0,0,0,0],[0,3,0,5,4,0,0],[1,0,2,3,0,0,6]]`
> **Output:** `28`
> **Explanation:** Cherries taken by Robot #1: `1 + 9 + 5 + 2 = 17`. Cherries taken by Robot #2: `1 + 3 + 4 + 3 = 11`. Total: `28`.

---

## ⚠️ Constraints
> [!warning]
> - `rows == grid.length`
> - `cols == grid[i].length`
> - `2 <= rows, cols <= 70`
> - `0 <= grid[i][j] <= 100`

---

## 🔍 Intuition

The trap is to run one robot greedily, erase its cherries, then run the second — that's provably wrong, because robot #1 taking a fat cell can strand robot #2 in a barren column. The two paths **interact**, so they have to be optimised *together*, in one search.

The saving grace is that both robots move **exactly one row down per step**. They are always on the same row, always at the same depth. So instead of a 4-dimensional state `(r1, c1, r2, c2)`, one shared `row` plus the two columns is enough: `(row, c1, c2)` — `70 × 70 × 70 = 343k` states, trivial. From each state there are `3 × 3 = 9` joint moves, so the work per state is `O(1)`.

The "same cell counts once" rule is not a special case to bolt on later — it's just the cell value at collection time: `c1 == c2 ? grid[row][c1] : grid[row][c1] + grid[row][c2]`. And because collection happens on *entry* to a row, the recursion adds the current row's take and then asks the 9 children for the best remainder. Off-grid columns return `Integer.MIN_VALUE` so `Math.max` never picks them.

> 🟢 *Multi-Agent Grid DP — lockstep rows collapse `(r1,c1,r2,c2)` to `(row, c1, c2)`*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — 3D Memoized Simultaneous DFS on `(row, c1, c2)`

**Why this works:**
- **Lockstep is the compression.** Both robots take exactly one downward step per move, so `r1 == r2` always holds. Tracking one `row` instead of two removes a whole dimension and makes the problem tractable.
- **Optimising jointly is what sequential greedy can't do.** The 9-way branch explores every combination of the two robots' next columns, so a "sacrifice" by robot #1 that unlocks a bigger haul for robot #2 is naturally considered.
- **`Integer.MIN_VALUE` as the illegal-move marker works because `d1 = d2 = 0` is always legal.** Both robots are in range when the state is reached, so straight-down is always available and `best` is never left at `MIN_VALUE` — no overflow when `current + best` runs.
- **`Integer[][][]` (boxed) rather than `int[][][]`** lets `null` mean "not computed", which matters here because `0` is a perfectly legal answer (a grid of all zeros).

**Dry Run** (`grid = [[3,1,1],[2,5,1],[1,5,5],[2,1,1]]`, `m = 4`, `n = 3`):

Base row `row = 3` (`grid[3] = [2,1,1]`) — just the collection rule, no recursion:

| `(c1,c2)` | value | | `(c1,c2)` | value |
|---|---|---|---|---|
| `(0,0)` | `2` (same cell) | | `(1,2)` | `1+1 = 2` |
| `(0,1)` | `2+1 = 3` | | `(2,0)` | `1+2 = 3` |
| `(0,2)` | `2+1 = 3` | | `(2,1)` | `1+1 = 2` |
| `(1,0)` | `1+2 = 3` | | `(2,2)` | `1` (same cell) |
| `(1,1)` | `1` (same cell) | | | |

Row `2` (`grid[2] = [1,5,5]`) — `current + max(9 children)`:

| `(c1,c2)` | `current` | best child | `dfs` |
|---|---|---|---|
| `(0,0)` | `1` | `3` | `4` |
| `(0,1)` | `6` | `3` | `9` |
| `(0,2)` | `6` | `3` | `9` |
| `(1,0)` | `6` | `3` | `9` |
| `(1,1)` | `5` | `3` | `8` |
| `(1,2)` | `10` | `3` | **`13`** |
| `(2,1)` | `10` | `3` | `13` |
| `(2,2)` | `5` | `2` | `7` |

Row `1` (`grid[1] = [2,5,1]`):

| `(c1,c2)` | `current` | best child | `dfs` |
|---|---|---|---|
| `(0,1)` | `2+5 = 7` | `13` from `(2,1,2)` | **`20`** |
| `(0,2)` | `2+1 = 3` | `13` | `16` |
| `(1,1)` | `5` | `13` | `18` |
| `(1,2)` | `5+1 = 6` | `13` | `19` |

Row `0` — the entry state `(0, 0, 2)`: `current = grid[0][0] + grid[0][2] = 3 + 1 = 4`. Robot #1 may go to columns `{0,1}`, robot #2 to `{1,2}`:

```
max( dfs(1,0,1)=20, dfs(1,0,2)=16, dfs(1,1,1)=18, dfs(1,1,2)=19 ) = 20
answer = 4 + 20 = 24   ✅
```

Tracing the winners back gives `R1: (0,0) -> (1,0) -> (2,1) -> (3,0)` = `3+2+5+2 = 12` and `R2: (0,2) -> (1,1) -> (2,2) -> (3,2)` = `1+5+5+1 = 12`.

```java
class Solution {

    private static final int[] DIR = {-1, 0, 1};

    public int cherryPickup(int[][] grid) {

        int m = grid.length;
        int n = grid[0].length;

        Integer[][][] memo = new Integer[m][n][n];

        return dfs(grid, 0, 0, n - 1, memo);
    }

    private int dfs(int[][] grid, int row, int c1, int c2,
                    Integer[][][] memo) {

        int m = grid.length;
        int n = grid[0].length;

        if (c1 < 0 || c1 >= n || c2 < 0 || c2 >= n)
            return Integer.MIN_VALUE;

        if (row == m - 1) {
            if (c1 == c2) return grid[row][c1];
            return grid[row][c1] + grid[row][c2];
        }

        if (memo[row][c1][c2] != null) return memo[row][c1][c2];

        int current;

        if (c1 == c2)
            current = grid[row][c1];
        else
            current = grid[row][c1] + grid[row][c2];

        int best = Integer.MIN_VALUE;

        // 3 × 3 = 9 possible moves
        for (int d1 : DIR) {
            for (int d2 : DIR) {
                best = Math.max(best,dfs(grid, row + 1, c1 + d1, c2 + d2, memo) );
            }
        }

        return memo[row][c1][c2] = current + best;
    }
}
```

- **Time:** `O(m · n² · 9)` = `O(m · n²)` · **Space:** `O(m · n²)` memo + `O(m)` recursion stack

---

## 🔑 Key Insights
- **"Both agents move at the same rate" is the signal to merge their time dimensions.** Any two-agent path problem where the steps are synchronised collapses one index away — this is the same trick as the original Cherry Pickup I (where one robot's round trip is re-read as two robots walking down together).
- **Never run the two paths sequentially.** Greedy-then-erase is the single most common wrong answer; the counterexample is always "robot #1 grabs a cell that was robot #2's only bridge".
- **The overlap rule is a *collection* rule, not a *movement* rule.** Robots are allowed to share a cell; they just don't double-count it. Blocking `c1 == c2` outright is wrong.
- **Boxed `Integer[][][]` earns its keep here** — with `0` a legal answer, an `int` memo would need a separate sentinel like `-1`.

---

## ⚠️ Pitfalls
> [!warning]
> - Returning `Integer.MIN_VALUE` for out-of-bounds and then blindly doing `current + best` overflows **if `best` is ever still `MIN_VALUE`**. It's safe only because `(d1, d2) = (0, 0)` is always in range. Change the bounds logic and this becomes a real bug — prefer clamping the loop ranges over the sentinel if you're unsure.
> - The out-of-bounds check must come **before** the `row == m - 1` base case, otherwise the base case indexes `grid[row][c1]` with an illegal column.
> - Don't assume `c1 < c2` stays true. The robots *can* cross over. Some solutions exploit symmetry to halve the state space, but this one doesn't — and adding a `c1 <= c2` guard without also mapping states correctly loses answers.
> - Memo dimensions are `[m][n][n]`, not `[m][n][m]` — both robots index **columns**.

---

## ⏱️ Complexity
- **Time:** `O(m · n²)`
- **Space:** `O(m · n²)`
