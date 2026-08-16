---
created: 2026-08-10 10:20
tags:
  - dsa
  - dynamic-programming
  - memoization
  - grid-dp
source: https://leetcode.com/problems/triangle/description/
problem_id: "120"
difficulty: Medium
status: Solved
review_date:
---
# LT_0120 – Triangle

**Link:** [Open Problem](https://leetcode.com/problems/triangle/description/)

---

## 📝 Problem Description
> [!info]
> Given a `triangle` array, return the **minimum path sum from top to bottom**.
>
> For each step, you may move to an adjacent number of the row below. More formally, if you are on index `i` on the current row, you may move to either index `i` or index `i + 1` on the next row.

---

## 🧪 Examples
> [!example]
> **Input:** `triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]`
> **Output:** `11`
> **Explanation:** The triangle looks like
> ```
>    2
>   3 4
>  6 5 7
> 4 1 8 3
> ```
> The minimum path sum from top to bottom is `2 + 3 + 5 + 1 = 11`.

> [!example]
> **Input:** `triangle = [[-10]]`
> **Output:** `-10`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= triangle.length <= 200`
> - `triangle[0].length == 1`
> - `triangle[i].length == triangle[i - 1].length + 1`
> - `-10^4 <= triangle[i][j] <= 10^4`

---

## 🔍 Intuition

This is [[LT_0064_Minimum_Path_Sum]] wearing a different shape. The grid isn't rectangular, but the recursion is identical: standing at `(i, j)`, the cheapest way down is `triangle[i][j]` plus the cheaper of the two cells I'm allowed to step onto — `(i+1, j)` (straight down) and `(i+1, j+1)` (down-right). The only real content is the adjacency rule: from index `i` you may only go to `i` or `i+1`, never `i-1`, because row `i+1` is one wider and is *left-aligned* under row `i`.

Brute force is `2^n` paths, but there are only `n(n+1)/2` distinct `(row, col)` states and every path funnels through them — massive overlap. Memoizing on `(i, j)` collapses it to `O(n²)`. Notice there is **no explicit out-of-bounds check**: the base case `i == size - 1` fires on the last row, and `j` can never exceed `i` because it only ever grows by 1 when the row does. The recursion is bounds-safe by construction.

> 🟢 *Top-Down DP on a Triangular Grid — min-path recursion with `(down, down-right)` transitions*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Top-Down Memoization on `(row, col)`

**Why this works:**
- `dfs(i, j)` is a clean subproblem — "cheapest cost to walk from `(i,j)` to *any* cell in the bottom row" — and it depends only on the row below, never on how I arrived. That independence from history is what makes memoization legal.
- The `Integer.MAX_VALUE` fill doubles as the "not computed yet" sentinel. It's safe here because a real answer is at most `200 × 10^4 = 2 × 10^6` in magnitude, nowhere near `MAX_VALUE`. (`-1` would have been *unsafe* — path sums can legitimately be negative.)
- Each `(i, j)` is computed once and reused by both parents that can reach it, so the total work is the number of states: `1 + 2 + … + n = O(n²)`.

**Dry Run** (`triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]`, `n = 4`):

Row 3 is the base case — it returns the cell value directly:

| cell | `dfs` | value |
|---|---|---|
| `(3,0)` | base | `4` |
| `(3,1)` | base | `1` |
| `(3,2)` | base | `8` |
| `(3,3)` | base | `3` |

Row 2 — `triangle[2][j] + min(down, diag)`:

| cell | `down` | `diag` | `memo` |
|---|---|---|---|
| `(2,0)` | `4` | `1` | `6 + 1 = 7` |
| `(2,1)` | `1` | `8` | `5 + 1 = 6` |
| `(2,2)` | `8` | `3` | `7 + 3 = 10` |

Row 1:

| cell | `down` | `diag` | `memo` |
|---|---|---|---|
| `(1,0)` | `7` | `6` | `3 + 6 = 9` |
| `(1,1)` | `6` | `10` | `4 + 6 = 10` |

Row 0: `(0,0)` → `down = 9`, `diag = 10` → `2 + 9 = 11` ✅

The winning path is `2 → 3 → 5 → 1`.

```java
class Solution {
    public int minimumTotal(List<List<Integer>> triangle) {
        int[][] memo = new int[triangle.size()][triangle.size()];
        for (int[] row : memo) Arrays.fill(row, Integer.MAX_VALUE);
        return dfs(triangle, 0, 0, memo);
    }

    private int dfs(List<List<Integer>> triangle, int i, int j, int[][] memo) {
        if (i == triangle.size() - 1) return triangle.get(i).get(j);
        if (memo[i][j] != Integer.MAX_VALUE) return memo[i][j];

        int down = dfs(triangle, i + 1, j, memo);
        int diag = dfs(triangle, i + 1, j + 1, memo);

        memo[i][j] = triangle.get(i).get(j) + Math.min(down, diag);
        return memo[i][j];
    }
}
```

- **Time:** `O(n²)` · **Space:** `O(n²)` memo + `O(n)` recursion stack

---

## 🔑 Key Insights
- **Left-aligned rows are the whole trick.** Because row `i+1` extends row `i` on the *right*, the legal moves are `j` and `j+1` — a "down / down-right" pair, not the "down / diagonal-either-way" you'd get from a centred triangle drawing.
- **`j <= i` is an invariant, not a check.** Starting at `(0,0)` with `j` incrementing only alongside `i`, `j` can never run off the end of a row — which is why the code has a single base case and no bounds guard.
- **Sentinel choice matters when values can be negative.** `-1` is the usual "unvisited" marker in grid DP, but here `-10^4` cells make `-1` a plausible real answer. `Integer.MAX_VALUE` is the correct pick.
- The memo is allocated `n × n` (square) even though only the lower triangle is used — `O(n²)` either way, so it's a fine simplification.

---

## ⚠️ Pitfalls
> [!warning]
> - Allocating `memo` as `new int[n][triangle.get(i).size()]` per row is tempting but `n × n` is simpler and same asymptotically — just don't index `memo[i][j]` with `j > i`.
> - Using `0` as the unvisited sentinel silently breaks on triangles containing `0` cells; using `-1` breaks on negative cells. Pick a sentinel outside the achievable range.
> - The recursion returns the answer from `dfs(...)`, not from `memo[0][0]`. Reading `memo[0][0]` also works here, but only because the root is always written before returning — don't assume that pattern holds when a base case short-circuits the root (a 1-row triangle returns `triangle.get(0).get(0)` **without** touching `memo`).

---

## ⏱️ Complexity
- **Time:** `O(n²)`
- **Space:** `O(n²)`
