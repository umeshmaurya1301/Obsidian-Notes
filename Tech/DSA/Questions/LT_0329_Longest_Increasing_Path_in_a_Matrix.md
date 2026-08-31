---
created: 2026-08-30 00:00
tags:
  - dsa
  - graph
  - dynamic-programming
  - dfs
source: https://leetcode.com/problems/longest-increasing-path-in-a-matrix/
problem_id: "329"
difficulty: Hard
status: Solved
review_date:
---
# LT_0329 – Longest Increasing Path in a Matrix

**Link:** [Open Problem](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/)

---

## 📝 Problem Description
> [!info]
> Given an `m x n` integers `matrix`, return the length of the longest increasing path in `matrix`.
>
> From each cell, you can either move in four directions: left, right, up, or down. You may not move diagonally or move outside the boundary (i.e., wrap-around is not allowed).

---

## 🧪 Examples
> [!example]
> **Input:** `matrix = [[9,9,4],[6,6,8],[2,1,1]]`
> **Output:** `4`
> **Explanation:** The longest increasing path is `[1, 2, 6, 9]`.

> [!example]
> **Input:** `matrix = [[3,4,5],[3,2,6],[2,2,1]]`
> **Output:** `4`
> **Explanation:** The longest increasing path is `[3, 4, 5, 6]`. Moving diagonally is not allowed.

> [!example]
> **Input:** `matrix = [[1]]`
> **Output:** `1`

---

## ⚠️ Constraints
> [!warning]
> - `m == matrix.length`
> - `n == matrix[i].length`
> - `1 <= m, n <= 200`
> - `0 <= matrix[i][j] <= 2^31 - 1`

---

## 🔍 Intuition

Every cell is the start of some increasing path, so brute-force DFS from all `m*n` cells re-explores the same sub-paths over and over — the naive recursion is exponential. The fix is memoization: `dp[i][j]` caches "the longest increasing path *starting* at `(i, j)`", computed once and reused by every predecessor that also reaches `(i, j)`. What makes this DFS safe to memoize without a separate `visited`/on-stack cycle guard (unlike ordinary graph DFS) is that every move must go to a strictly greater value — the reachability graph induced by "increasing" edges is automatically a DAG, so there's no way to revisit a cell mid-recursion. The outer double loop just tries every cell as a candidate starting point and keeps the global max, since the true longest path could start anywhere in the grid.

> 🟢 *DFS + Memoization on an Implicit DAG*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — DFS + Memoization

**Why this works:**
- `matrix[x][y] > matrix[i][j]` as the move condition guarantees the recursion graph has no cycles, so `dp[i][j] != 0` alone is a safe "already solved" check — no extra recursion-stack tracking needed.
- `dp[i][j]` memoizes the longest increasing path starting at `(i, j)`, so once any predecessor computes it, every other predecessor that also reaches `(i, j)` gets it in `O(1)`.
- Trying every cell as a starting point in the outer loop and taking the max is necessary because the globally longest increasing path isn't known to start at any particular cell in advance.

**Dry Run** (`matrix = [[9,9,4],[6,6,8],[2,1,1]]`, tracing the winning path `1 → 2 → 6 → 9`):
```
dfs(2,1) value=1
  right (2,2)=1  not > 1        → skip
  left  (2,0)=2  > 1            → dfs(2,0)
    up (1,0)=6  > 2             → dfs(1,0)
      up (0,0)=9  > 6           → dfs(0,0)
        right (0,1)=9  not > 9  → skip
        down  (1,0)=6  not > 9  → skip
        dp[0][0] = 1
      candidate = 1 + dp[0][0] = 2 → dp[1][0] = 2
    candidate = 1 + dp[1][0] = 3 → dp[2][0] = 3
  up (1,1)=6  > 1                → dfs(1,1)
    right (1,2)=8  > 6           → dfs(1,2) = 1  → candidate 2
    up    (0,1)=9  > 6           → dfs(0,1) = 1  → candidate 2
    dp[1][1] = 2
  candidates for dfs(2,1): left → 1+dp[2][0]=4,  up → 1+dp[1][1]=3
  dp[2][1] = max(4, 3) = 4  ✅
```

```java
class Solution {
    private int[][] dirs = { { 0, 1 }, { 1, 0 }, { 0, -1 }, { -1, 0 } };
    private int m, n;

    public int longestIncreasingPath(int[][] matrix) {
        if (matrix == null || matrix.length == 0)
            return 0;

        m = matrix.length;
        n = matrix[0].length;
        int[][] dp = new int[m][n];
        int maxLen = 0;

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                maxLen = Math.max(maxLen, dfs(matrix, i, j, dp));
            }
        }

        return maxLen;
    }

    private int dfs(int[][] matrix, int i, int j, int[][] dp) {
        if (dp[i][j] != 0)
            return dp[i][j];

        int max = 1;
        for (int[] dir : dirs) {
            int x = i + dir[0];
            int y = j + dir[1];

            if (x >= 0 && x < m && y >= 0 && y < n &&
                    matrix[x][y] > matrix[i][j]) {
                max = Math.max(max, 1 + dfs(matrix, x, y, dp));
            }
        }

        dp[i][j] = max;
        return max;
    }
}
```

- **Time:** `O(m * n)` · **Space:** `O(m * n)` (dp table `+` recursion stack, worst case `O(m * n)` on a fully snaking increasing path)

---

## 🔑 Key Insights
- The "strictly greater" move condition is what makes the grid's reachability graph acyclic — that's the only reason a plain `dp[i][j] != 0` check is enough, with no `onPath`/`visited` array like `LT_0207`'s DFS cycle detection needed.
- `dp[i][j]` is "longest path *starting* here", not "longest path *through* here" — that distinction is why the outer loop must scan every cell rather than starting only from local minima or matrix corners.
- Memoization is what collapses the exponential re-exploration: many cells have multiple valid predecessors, and without caching each shared sub-path gets recomputed once per predecessor.

---

## ⚠️ Pitfalls
> [!warning]
> - `dp[i][j] != 0` as the memo sentinel only works because a valid path length is always `>= 1` here — it would silently break on a problem where `0` is itself a legitimate memoized result.
> - The move condition must be strict (`matrix[x][y] > matrix[i][j]`, not `>=`) — treating equal-valued neighbors as "increasing" reintroduces cycles and breaks the whole no-visited-array argument.
> - It's tempting to add a separate `visited` array out of habit from other grid-DFS problems — here it's redundant (and would be wrong, since a cell can legitimately be entered from multiple different DFS calls) precisely because the strictly-increasing condition already rules out revisits.

---

## ⏱️ Complexity
- **Time:** `O(m * n)`
- **Space:** `O(m * n)`
