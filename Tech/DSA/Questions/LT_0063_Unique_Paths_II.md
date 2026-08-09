---
created: 2026-08-09 18:31
tags:
  - dsa
  - dynamic-programming
  - grid-dp
  - memoization
source: https://leetcode.com/problems/unique-paths-ii/
problem_id: "63"
difficulty: Medium
status: Solved
review_date:
---
# LT_0063 – Unique Paths II

**Link:** [Open Problem](https://leetcode.com/problems/unique-paths-ii/)

---

## 📝 Problem Description
> [!info]
> You are given an `m x n` integer array `grid`. There is a robot initially located at the **top-left** corner (i.e., `grid[0][0]`). The robot tries to move to the **bottom-right** corner (i.e., `grid[m-1][n-1]`). The robot can only move either **down** or **right** at any point in time.
>
> An obstacle and space are marked as `1` or `0` respectively in `grid`. A path that the robot takes **cannot include** any square that is an obstacle.
>
> Return the number of possible unique paths that the robot can take to reach the bottom-right corner.
>
> The testcases are generated so that the answer will be less than or equal to `2 * 10^9`.

---

## 🧪 Examples
> [!example]
> **Input:** `obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]`
> **Output:** `2`
> **Explanation:** There is one obstacle in the middle of the 3x3 grid above. There are two ways to reach the bottom-right corner:
> 1. `Right -> Right -> Down -> Down`
> 2. `Down -> Down -> Right -> Right`

> [!example]
> **Input:** `obstacleGrid = [[0,1],[0,0]]`
> **Output:** `1`

---

## ⚠️ Constraints
> [!warning]
> - `m == obstacleGrid.length`
> - `n == obstacleGrid[i].length`
> - `1 <= m, n <= 100`
> - `obstacleGrid[i][j]` is `0` or `1`.

---

## 🔍 Intuition

Structurally this is [[LT_0062_Unique_Paths]] with one extra base case. The recurrence is untouched — `paths(r,c) = paths(r,c+1) + paths(r+1,c)` — because an obstacle doesn't change *how* paths compose, it only changes which cells are legal to stand on.

So the obstacle is just a **third way to return `0`**, sitting alongside "walked off the grid". A blocked cell contributes nothing to whoever asked about it, and since counts are summed, contributing `0` is exactly the right way to say "no route passes through here". No special propagation logic is needed; the zeros flow outward on their own.

The only genuine thinking is about **where the obstacle test goes relative to the other base cases**, because the destination and the start are both special. The solution handles the destination with an early return in the caller and the start naturally inside the recursion — but get that ordering wrong and a blocked destination reports `1` path.

> 🟢 *Grid DP — Count Paths with Blocked Cells*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Top-Down DP (Memoization) with Obstacle Check

**Why this works:**
- **An obstacle returning `0` is semantically identical to going out of bounds** — both mean "no valid path continues from here". Because the recurrence *sums* its two children, a `0` child silently removes that whole branch from the count.
- **A blocked destination is caught up front.** `if (obstacleGrid[m-1][n-1] == 1) return 0;` runs before any recursion, which is necessary because the recursive base case `row == m-1 && col == n-1` returns `1` *without* consulting the grid.
- **A blocked start is handled naturally.** `function(0,0)` isn't the destination (except on a `1x1` grid, already covered by the caller's guard), so it falls through to the obstacle check and returns `0`.

**Dry Run** (`obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]`):

The settled counts, with the obstacle at `(1,1)`:

| | `col 0` | `col 1` | `col 2` |
|---|---|---|---|
| **row 0** | **2** | 1 | 1 |
| **row 1** | 1 | 🚧 `0` | 1 |
| **row 2** | 1 | 1 | *(destination)* |

- `(2,1)`: right → destination = 1, down → off-grid = 0 → **1**
- `(2,0)`: right → `(2,1)` = 1, down → off-grid = 0 → **1**
- `(1,2)`: right → off-grid = 0, down → destination = 1 → **1**
- `(1,1)`: **obstacle** → **0**
- `(1,0)`: right → `(1,1)` = 0, down → `(2,0)` = 1 → **1**
- `(0,1)`: right → `(0,2)` = 1, down → `(1,1)` = 0 → **1**
- `(0,0)`: right → `(0,1)` = 1, down → `(1,0)` = 1 → **2** ✅

Exactly the two routes the problem lists — the obstacle zeroed out every path through the centre.

```java
class Solution {
    public int uniquePathsWithObstacles(int[][] obstacleGrid) {
        int m = obstacleGrid.length;
        int n = obstacleGrid[0].length;

        if(obstacleGrid[m-1][n-1]==1) return 0;

        int[][] dp = new int[m][n];
        for(int[] a : dp) Arrays.fill(a, -1);
        return function(obstacleGrid,0, 0, dp);
    }

    private int function(int[][] obstacleGrid, int row, int col, int[][] dp) {
        int m = obstacleGrid.length;
        int n = obstacleGrid[0].length;

        if (row == m - 1 && col == n - 1) return 1;
        if (row >= m || col >= n) return 0;
        if (dp[row][col] != -1) return dp[row][col];
        if(obstacleGrid[row][col]==1) return 0;

        return dp[row][col] = function(obstacleGrid, row, col + 1, dp) + function(obstacleGrid, row + 1, col, dp);
    }
}
```

- **Time:** `O(m · n)` · **Space:** `O(m · n)` table + `O(m + n)` recursion depth

---

## 🔑 Key Insights
- **The obstacle needs no propagation logic.** Because the recurrence adds its children, a single `return 0` at a blocked cell automatically erases every path routed through it — no flood fill, no "unreachable" marking.
- **The blocked-destination guard in the caller is load-bearing**, not defensive padding. The recursive base case returns `1` on coordinate match alone, so without that guard a grid ending in `1` would report paths that don't exist.
- **Obstacle cells are never memoized** — the `return 0` fires after the memo lookup but skips the write, so those cells stay `-1` and re-run the `O(1)` check on every visit. Correct, just mildly redundant; moving the obstacle test above the memo lookup would make that explicit.
- **The binomial shortcut from [[LT_0062_Unique_Paths]] dies here.** `C(m+n-2, m-1)` counts unrestricted routes; with arbitrary blocked cells there's no closed form, so the DP is genuinely necessary.

---

## ⚠️ Pitfalls
> [!warning]
> - **Checking the destination before the obstacle without the caller's guard.** A `1` in the bottom-right corner then returns `1` instead of `0` — the single most common wrong answer on this problem.
> - **Forgetting the start can be blocked.** `obstacleGrid[0][0] == 1` must yield `0`. It works here via the fall-through, but a solution that seeds `dp[0][0] = 1` up front (the usual bottom-up shape) has to special-case it explicitly.
> - **Initialising the memo to `0`.** `0` is a real answer for blocked and off-grid cells, so it can't also mean "unvisited" — hence the `-1` fill.

---

## ⏱️ Complexity
- **Time:** `O(m · n)`
- **Space:** `O(m · n)` — memo table, plus `O(m + n)` recursion stack
