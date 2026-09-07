---
created: 2026-09-05 00:00
tags:
  - dsa
  - dynamic-programming
  - dfs
  - matrix
  - memoization
source: https://leetcode.com/problems/number-of-increasing-paths-in-a-grid/
problem_id: "2328"
difficulty: Hard
status: Solved
review_date:
---
# LT_2328 – Number of Increasing Paths in a Grid

**Link:** [Open Problem](https://leetcode.com/problems/number-of-increasing-paths-in-a-grid/)

---

## 📝 Problem Description
> [!info]
> You are given an `m x n` integer matrix `grid`, where you can move from a cell to any adjacent cell in all 4 directions.
>
> Return the number of strictly increasing paths in the grid such that you can start from any cell and end at any cell. Since the answer may be very large, return it modulo `10^9 + 7`.
>
> Two paths are considered different if they do not have exactly the same sequence of visited cells.

---

## 🧪 Examples
> [!example]
> **Input:** `grid = [[1,1],[3,4]]`
> **Output:** `8`
> **Explanation:** The strictly increasing paths are:
> - Paths with length `1`: `[1]`, `[1]`, `[3]`, `[4]`.
> - Paths with length `2`: `[1 -> 3]`, `[1 -> 4]`, `[3 -> 4]`.
> - Paths with length `3`: `[1 -> 3 -> 4]`.
>
> The total number of paths is `4 + 3 + 1 = 8`.

> [!example]
> **Input:** `grid = [[1],[2]]`
> **Output:** `3`
> **Explanation:** The strictly increasing paths are:
> - Paths with length `1`: `[1]`, `[2]`.
> - Paths with length `2`: `[1 -> 2]`.
>
> The total number of paths is `2 + 1 = 3`.

---

## ⚠️ Constraints
> [!warning]
> - `m == grid.length`
> - `n == grid[i].length`
> - `1 <= m, n <= 1000`
> - `1 <= m * n <= 10^5`
> - `1 <= grid[i][j] <= 10^5`

---

## 🔍 Intuition

The "strictly increasing" constraint is the whole trick: it turns an undirected 4-directional grid into an implicit DAG, since a move is only ever legal from a smaller value to a larger one — there is no way to revisit a cell, so no cycle can ever form. That means I never need a `visited` set the way a normal grid DFS would; the natural recursion terminates on its own, and results can be safely memoized without worrying about re-entering an in-progress path. Define `dp[i][j]` = number of strictly increasing paths that *start* at `(i, j)` (including the trivial length-1 path of just itself). Then `dp[i][j] = 1 + sum(dp[neighbor] for every neighbor with a strictly greater value)`, and the answer is simply the sum of `dp[i][j]` over every cell, since every increasing path is counted exactly once — from its own unique starting cell. This is top-down DP on a DAG dressed up as grid DFS.

> 🟢 *DFS + Memoization on an Implicit DAG*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — DFS + Memoization (Top-Down DP on DAG)

**Why this works:**
- Strictly increasing values guarantee the recursion graph is acyclic, so memoizing `dp[i][j]` is safe with no explicit cycle/visited check needed.
- `dp[i][j]` counts every path *starting* at `(i, j)`; since every path has exactly one starting cell, summing `dp[i][j]` across the whole grid double-counts nothing and misses nothing.
- `dp` doubles as both cache and "computed" flag — since every valid `dp[i][j]` is `>= 1` (the trivial single-cell path), `0` unambiguously means "not yet computed."

**Dry Run** (`grid = [[1,1],[3,4]]`, cells visited in row-major order, directions = right, down, left, up):

| Call | Value | Increasing neighbors | Result |
|---|---|---|---|
| `dfs(1,1)` (value `4`) | `4` | none (right/down out of bounds, left `3` and up `1` both `<= 4`) | `dp[1][1] = 1` |
| `dfs(1,0)` (value `3`) | `3` | right `(1,1)=4 > 3` → `+dfs(1,1)=1` | `dp[1][0] = 1 + 1 = 2` |
| `dfs(0,0)` (value `1`) | `1` | down `(1,0)=3 > 1` → `+dfs(1,0)=2` | `dp[0][0] = 1 + 2 = 3` |
| `dfs(0,1)` (value `1`) | `1` | down `(1,1)=4 > 1` → `+dfs(1,1)=1` (cached) | `dp[0][1] = 1 + 1 = 2` |
| `totalCount` | — | `dp[0][0] + dp[0][1] + dp[1][0] + dp[1][1]` | `3 + 2 + 2 + 1 = 8` ✅ |

```java
class Solution {
    private final int[][] DIR = { { 0, 1 }, { 1, 0 }, { 0, -1 }, { -1, 0 } };
    private int m, n;
    private final int MOD = 1000_000_007;

    public int countPaths(int[][] matrix) {
        if (matrix == null || matrix.length == 0)
            return 0;

        m = matrix.length;
        n = matrix[0].length;
        int[][] dp = new int[m][n];

        int totalCount = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                totalCount += dfs(matrix, dp, i, j);
                totalCount = totalCount % MOD;
            }
        }

        return totalCount;
    }

    private int dfs (int[][] matrix, int[][] dp, int i, int j) {
        if (dp[i][j] != 0) return dp[i][j];
        int count = 1;

        for (int[] d : DIR) {
            int newRow = i + d[0];
            int newCol = j + d[1];

            if (isWithInBoundary(newRow, newCol) && matrix[newRow][newCol] > matrix[i][j]) {
                count += dfs (matrix, dp, newRow, newCol);
                count = count % MOD;
            }
        }

        return dp[i][j] = count;

    }

    private boolean isWithInBoundary(int x, int y) {
        return x >= 0 && x < m && y >= 0 && y < n;
    }
}
```

- **Time:** `O(m * n)` — each cell's `dfs` body runs exactly once thanks to memoization, and each run does `O(1)` work (4 neighbor checks) · **Space:** `O(m * n)` for `dp`, plus `O(m * n)` worst-case recursion stack depth for a long strictly-increasing chain

---

## 🔑 Key Insights
- The strictly-increasing move rule is what removes the need for a `visited` array — it's a grid problem that's secretly a DAG longest-path-count problem.
- `dp[i][j]` is a "paths starting here" count, not "paths ending here" or "paths through here" — get this backwards and the summation at the end double-counts or misses paths.
- Take the modulo at *every* accumulation step (`count = count % MOD` inside `dfs`, and `totalCount = totalCount % MOD` in the loop) since intermediate sums can otherwise overflow before the final mod is applied.

---

## ⚠️ Pitfalls
> [!warning]
> - Relying on `dp[i][j] == 0` as the "unvisited" sentinel only works because every real answer is `>= 1` (the trivial single-cell path) — this trick breaks if the base case were ever allowed to be `0`.
> - Using `>=` instead of `>` when comparing neighbor values silently turns "strictly increasing" into "non-decreasing," inflating the count.
> - Skipping the modulo on the recursive `count` accumulation (only applying it at the top-level `totalCount`) can let `int` overflow before that final mod ever runs.

---

## ⏱️ Complexity
- **Time:** `O(m * n)`
- **Space:** `O(m * n)`
