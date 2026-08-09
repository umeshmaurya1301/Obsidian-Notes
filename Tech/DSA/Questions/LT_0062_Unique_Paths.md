---
created: 2026-08-09 18:31
tags:
  - dsa
  - dynamic-programming
  - grid-dp
  - memoization
source: https://leetcode.com/problems/unique-paths/
problem_id: "62"
difficulty: Medium
status: Solved
review_date:
---
# LT_0062 – Unique Paths

**Link:** [Open Problem](https://leetcode.com/problems/unique-paths/)

---

## 📝 Problem Description
> [!info]
> There is a robot on an `m x n` grid. The robot is initially located at the **top-left** corner (i.e., `grid[0][0]`). The robot tries to move to the **bottom-right** corner (i.e., `grid[m-1][n-1]`). The robot can only move either **down** or **right** at any point in time.
>
> Given the two integers `m` and `n`, return the number of possible unique paths that the robot can take to reach the bottom-right corner.
>
> The test cases are generated so that the answer will be less than or equal to `2 * 10^9`.

---

## 🧪 Examples
> [!example]
> **Input:** `m = 3, n = 7`
> **Output:** `28`

> [!example]
> **Input:** `m = 3, n = 2`
> **Output:** `3`
> **Explanation:** From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
> 1. `Right -> Down -> Down`
> 2. `Down -> Down -> Right`
> 3. `Down -> Right -> Down`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= m, n <= 100`

---

## 🔍 Intuition

Standing on any cell, the number of ways to finish is completely determined by that cell's coordinates — the route taken to arrive is irrelevant. That's the whole problem: `paths(r, c) = paths(r, c+1) + paths(r+1, c)`, because every path from `(r,c)` starts with exactly one of the two legal moves, and those two sets are disjoint.

The base cases fall out of the geometry. Reaching the destination is one complete path (`return 1`); walking off the grid is zero. Everything else is the sum of the cell to the right and the cell below.

Raw recursion re-derives the same cell over and over — the number of distinct routes *to* a cell is itself exponential, so the tree blows up while there are only `m × n ≤ 10⁴` distinct questions. Caching turns it linear in the grid size. Both solutions below do exactly that; they differ only in **direction of travel**: memoization asks top-down and fills lazily, tabulation seeds the last row/column with `1` and fills backwards from the destination.

> 🟢 *Grid DP — Count Paths (Right + Down)*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Top-Down DP (Memoization)

**Why this works:**
- **The recurrence is a clean disjoint sum:** every path from `(row, col)` begins with either a right step or a down step and never both, so adding the two sub-counts double-counts nothing and misses nothing.
- **Out-of-bounds returns `0`, destination returns `1`** — the two base cases together mean "a path only counts if it actually lands on the target", so illegal overshoots contribute nothing.
- **`dp[row][col] != -1` collapses the exponential tree** to at most `m × n` real computations; `-1` is a safe sentinel because a genuine path count is always `>= 0`.

**Dry Run** (`m = 3, n = 2`):

Cells fill lazily from `(0,0)` but settle to:

| | `col 0` | `col 1` |
|---|---|---|
| **row 0** | **3** | 1 |
| **row 1** | 2 | 1 |
| **row 2** | 1 | *(destination)* |

- `(2,0)`: right → `(2,1)` = 1 (destination), down → off-grid = 0 → **1**
- `(1,1)`: right → off-grid = 0, down → `(2,1)` = 1 → **1**
- `(1,0)`: right → `(1,1)` = 1, down → `(2,0)` = 1 → **2**
- `(0,1)`: right → off-grid = 0, down → `(1,1)` = 1 → **1**
- `(0,0)`: right → `(0,1)` = 1, down → `(1,0)` = 2 → **3** ✅

Matching the three routes listed in the problem.

```java
class Solution {
    public int uniquePaths(int m, int n) {
        int[][] dp = new int[m][n];
        for(int[] a : dp) Arrays.fill(a, -1);
        return function(m,n,0,0,dp);
    }

    private int function(int m, int n, int row, int col, int[][] dp) {
        if(row==m-1 && col==n-1) return 1;
        if(row>=m || col>=n) return 0;
        if(dp[row][col]!=-1) return dp[row][col];
        return dp[row][col] = function(m,n,row,col+1,dp) + function(m,n,row+1,col,dp);
    }
}
```

- **Time:** `O(m · n)` · **Space:** `O(m · n)` table + `O(m + n)` recursion depth

### ✅ Solution 2 — Bottom-Up DP (Tabulation)

**Why this works:**
- **The last row and last column are all `1` by inspection:** from anywhere on the bottom row the only legal move is right, so there's exactly one path; same going down the rightmost column. Seeding those turns the base cases into data instead of branches.
- **Filling from `(m-2, n-2)` upward-left** guarantees both `dp[row+1][col]` and `dp[row][col+1]` are already final when `dp[row][col]` is computed — the dependency order is the reverse of the movement order.
- **No recursion, so no stack** — same `O(m·n)` work, but it can't overflow, which matters if the grid bound ever grows.

**Dry Run** (`m = 3, n = 2`):

Seeding — last column `dp[0][1] = dp[1][1] = dp[2][1] = 1`, last row `dp[2][0] = dp[2][1] = 1`:

| | `col 0` | `col 1` |
|---|---|---|
| **row 0** | ? | 1 |
| **row 1** | ? | 1 |
| **row 2** | 1 | 1 |

Then the fill loop (`row = 1 → 0`, `col = 0`):
- `dp[1][0] = dp[2][0] + dp[1][1] = 1 + 1 = 2`
- `dp[0][0] = dp[1][0] + dp[0][1] = 2 + 1 = **3**` ✅

```java
class Solution {
    public int uniquePaths(int m, int n) {
        int[][] dp = new int[m][n];

        // Step 1: Base Case - fill last row and last column with 1
        for (int i = 0; i < m; i++) dp[i][n - 1] = 1;  // last column
        for (int j = 0; j < n; j++) dp[m - 1][j] = 1;  // last row

        // Step 2: Fill from bottom-right to top-left
        for (int row = m - 2; row >= 0; row--) {
            for (int col = n - 2; col >= 0; col--) {
                dp[row][col] = dp[row + 1][col] + dp[row][col + 1];
            }
        }

        return dp[0][0]; // Start from top-left
    }
}
```

- **Time:** `O(m · n)` · **Space:** `O(m · n)`, reducible to `O(n)` with a single rolling row

---

## 🔑 Key Insights
- **The path count is a binomial coefficient.** Every route is a fixed sequence of `m-1` downs and `n-1` rights, so the answer is `C(m+n-2, m-1)` — computable in `O(min(m,n))` time and `O(1)` space. That's the real optimal answer, and the expected follow-up.
- **The `1`-seeded last row/column is the same fact stated as data.** Tabulation's seeding step and memoization's `return 1` at the destination are two encodings of "there's exactly one way to travel in a straight line".
- **`int` is just barely enough.** With `m = n = 100` the true count is astronomically larger than `int`, which is why the problem *promises* the answer is `<= 2 × 10⁹` (`Integer.MAX_VALUE ≈ 2.147 × 10⁹`). Without that guarantee this would need `long`.
- **The memoized version never writes `dp[m-1][n-1]`** — the destination check returns before the memo write, so that cell stays `-1` forever. Harmless (it's `O(1)` to re-derive), but it's why the printed table has a hole in the corner.

---

## ⚠️ Pitfalls
> [!warning]
> - **Checking bounds before the destination.** Both base cases must be ordered destination-first as written; the reverse order is fine here only because `(m-1, n-1)` is in bounds — but in [[LT_0063_Unique_Paths_II]] the ordering interacts with the obstacle check and genuinely matters.
> - **Filling the tabulation in the wrong direction.** Iterating `row = 0 → m-1` reads `dp[row+1][col]` before it's computed and returns garbage. Dependencies point down-right, so the fill must go up-left.
> - **Initialising the memo to `0` instead of `-1`.** `0` is a legitimate answer (off-grid), so it can't double as "unvisited" — every cell would be treated as already solved.

---

## ⏱️ Complexity
- **Time:** `O(m · n)`
- **Space:** `O(m · n)` — the DP table (`O(n)` with a rolling row; `O(1)` via the binomial formula)
