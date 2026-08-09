---
created: 2026-08-09 18:31
tags:
  - dsa
  - dynamic-programming
  - grid-dp
  - memoization
source: https://leetcode.com/problems/minimum-path-sum/
problem_id: "64"
difficulty: Medium
status: Solved
review_date:
---
# LT_0064 – Minimum Path Sum

**Link:** [Open Problem](https://leetcode.com/problems/minimum-path-sum/)

---

## 📝 Problem Description
> [!info]
> Given a `m x n` grid filled with **non-negative** numbers, find a path from **top left** to **bottom right**, which minimizes the sum of all numbers along its path.
>
> **Note:** You can only move either **down** or **right** at any point in time.

---

## 🧪 Examples
> [!example]
> **Input:** `grid = [[1,3,1],[1,5,1],[4,2,1]]`
> **Output:** `7`
> **Explanation:** Because the path `1 → 3 → 1 → 1 → 1` minimizes the sum.

> [!example]
> **Input:** `grid = [[1,2,3],[4,5,6]]`
> **Output:** `12`

---

## ⚠️ Constraints
> [!warning]
> - `m == grid.length`
> - `n == grid[i].length`
> - `1 <= m, n <= 200`
> - `0 <= grid[i][j] <= 200`

---

## 🔍 Intuition

Same grid, same two moves as [[LT_0062_Unique_Paths]] — but the accumulator changes from **count** to **min**. Instead of `paths(r,c) = right + down`, it's `cost(r,c) = grid[r][c] + min(right, down)`: whatever I do from here, I'm paying for this cell, and then I take the cheaper of the two ways onward.

The optimal-substructure argument is the standard one: the cheapest route from `(r,c)` to the corner must begin with either a right or a down step, and its remainder must itself be the cheapest route from wherever that step lands. If it weren't, swapping in the cheaper remainder would give a better total — contradiction. So caching per cell is legal, and there are only `m × n` cells.

The implementation detail worth pausing on is the **out-of-bounds sentinel**. Since we're minimising, falling off the grid has to look infinitely expensive rather than free — hence `Integer.MAX_VALUE`. That's what makes `Math.min` naturally reject illegal moves, but it's also the line that would overflow if both directions were ever off-grid at once.

> 🟢 *Grid DP — Minimise Path Cost (Right / Down)*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Top-Down DP (Memoization)

**Why this works:**
- **Optimal substructure holds:** the best route through `(row, col)` is `grid[row][col]` plus the best of the two sub-routes, and those sub-routes don't depend on how `(row, col)` was reached. That's what licenses the per-cell memo.
- **`Integer.MAX_VALUE` for out-of-bounds makes `Math.min` do the filtering.** An illegal direction can never win the comparison, so there's no need for explicit bounds branching around each recursive call.
- **The destination base case writes the memo** (`return dp[row][col] = grid[row][col];`) rather than returning bare — so `dp` ends up fully populated, and the caller's `return dp[0][0]` is safe.

**Dry Run** (`grid = [[1,3,1],[1,5,1],[4,2,1]]`):

Filling from the destination backwards, `dp[r][c]` = cheapest cost from `(r,c)` to the corner (inclusive):

| | `col 0` | `col 1` | `col 2` |
|---|---|---|---|
| **row 0** | **7** | 6 | 3 |
| **row 1** | 8 | 7 | 2 |
| **row 2** | 7 | 3 | 1 |

- `(2,2)`: destination → `1`
- `(2,1)`: `2 + min(right = 1, down = ∞)` = **3**
- `(2,0)`: `4 + min(right = 3, down = ∞)` = **7**
- `(1,2)`: `1 + min(right = ∞, down = 1)` = **2**
- `(1,1)`: `5 + min(right = 2, down = 3)` = **7**
- `(1,0)`: `1 + min(right = 7, down = 7)` = **8**
- `(0,2)`: `1 + min(right = ∞, down = 2)` = **3**
- `(0,1)`: `3 + min(right = 3, down = 7)` = **6**
- `(0,0)`: `1 + min(right = 6, down = 8)` = **7** ✅

Tracing the winning choices gives `1 → 3 → 1 → 1 → 1`, exactly the path in the explanation.

```java
class Solution {
    public int minPathSum(int[][] grid) {
        int n = grid.length;
        int m = grid[0].length;

        int[][] dp = new int[n][m];
        for (int[] a : dp) Arrays.fill(a, -1);
        dfs(grid, dp, 0, 0);
        // System.out.println(Arrays.deepToString(dp));
        // for (int[] a : dp) {
        //     System.out.println(Arrays.toString(a));
        // }
        return dp[0][0];
    }

    private int dfs (int[][] grid, int[][] dp, int row, int col) {
        int n = grid.length;
        int m = grid[0].length;

        if (row>=n || col>=m) return Integer.MAX_VALUE;
        if (row==n-1 && col==m-1) return dp[row][col] = grid[row][col];
        if (dp[row][col]!=-1) return dp[row][col];

        int val = grid[row][col];
        int right =  dfs (grid, dp, row, col+1);
        int down =  dfs (grid, dp, row+1, col);
        return dp[row][col] = Math.min (right, down) + val;
    }
}
```

- **Time:** `O(m · n)` · **Space:** `O(m · n)` table + `O(m + n)` recursion depth

---

## 🔑 Key Insights
- **Counting vs. minimising is a one-symbol change.** `+` becomes `min(…) + cost`, and the out-of-bounds return flips from `0` (the additive identity) to `+∞` (the min identity). Recognising that these grid problems are one template with a swappable accumulator is the whole point of doing 62/63/64 together.
- **`Math.min(MAX, MAX) + val` would overflow — but can't happen here.** Every in-bounds non-destination cell has at least one in-bounds neighbour on the way to the corner, so at least one of `right`/`down` is always finite. The pattern is still fragile; `Integer.MAX_VALUE / 2` is the usual defensive sentinel.
- **The bounds check must come first.** It precedes the destination check, so an out-of-range `(row, col)` never indexes `grid` or `dp` — reordering those two lines throws.
- **Watch the variable naming:** this solution uses `n` for rows and `m` for columns, the reverse of the problem statement's `m x n`. Harmless internally, but easy to trip over when adapting the code.

---

## ⚠️ Pitfalls
> [!warning]
> - **Using `0` as the out-of-bounds sentinel.** In a *counting* problem `0` is right; in a *minimising* one it makes walking off the grid free, and the answer collapses to the first cell's value.
> - **Forgetting that the destination cell's own value counts.** The base case returns `grid[row][col]`, not `0` — the path sum includes both endpoints.
> - **Assuming greedy "always step to the smaller neighbour" works.** It doesn't: a cheap immediate step can lead into an expensive region. Example 1's first move to `3` (over `1`) is exactly that trap — the greedy takes `1 → 1 → 4 …` and loses.

---

## ⏱️ Complexity
- **Time:** `O(m · n)`
- **Space:** `O(m · n)` — memo table, plus `O(m + n)` recursion stack (reducible to `O(n)` with a rolling row)
