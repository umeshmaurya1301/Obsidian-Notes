---
created: 2026-08-10 10:35
tags:
  - dsa
  - dynamic-programming
  - memoization
  - grid-dp
  - matrix
source: https://leetcode.com/problems/maximal-square/description/
problem_id: "221"
difficulty: Medium
status: Solved
review_date:
---
# LT_0221 – Maximal Square

**Link:** [Open Problem](https://leetcode.com/problems/maximal-square/description/)

---

## 📝 Problem Description
> [!info]
> Given an `m x n` binary matrix filled with `0`'s and `1`'s, find the largest **square** containing only `1`'s and return its **area**.

---

## 🧪 Examples
> [!example]
> **Input:** `matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]`
> **Output:** `4`
> **Explanation:** The largest all-`1` square is the `2 x 2` block at rows 1–2, columns 2–3.

> [!example]
> **Input:** `matrix = [["0","1"],["1","0"]]`
> **Output:** `1`

> [!example]
> **Input:** `matrix = [["0"]]`
> **Output:** `0`

---

## ⚠️ Constraints
> [!warning]
> - `m == matrix.length`
> - `n == matrix[i].length`
> - `1 <= m, n <= 300`
> - `matrix[i][j]` is `'0'` or `'1'`

---

## 🔍 Intuition

The naive move is to try every cell as a corner and expand the square outward, checking all `k²` cells each time — `O(m·n·min(m,n)³)`, hopeless at 300×300. The unlock is realising a square is **recursively defined**: a `k × k` square of 1's anchored at `(r,c)` exists *iff* `(r,c)` is a `1` **and** three overlapping `(k-1) × (k-1)` squares exist — one to the right, one below, and one diagonally down-right.

So define `f(r,c)` = the side length of the biggest all-1 square whose **top-left corner** is `(r,c)`. Then `f(r,c) = 1 + min(f(r,c+1), f(r+1,c+1), f(r+1,c))` when the cell is `1`, and `0` when it's `0`. The `min` is the key: the square can only be as large as its *weakest* of the three sub-squares, because all three must be present simultaneously to tile the bigger square. Off-grid returns `0`, which naturally caps squares at the border.

That gives one number per cell — `O(m·n)` states, each `O(1)` work. The final answer is `max(f(r,c))²` over the whole memo, since the problem asks for area, not side.

> 🟢 *Grid DP — square side length via `1 + min` of three overlapping neighbours*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Memoized Square Side from the Top-Left Corner

**Why this works:**
- **The `min` of three neighbours is exactly the "all three must fit" condition.** If the right neighbour supports a side-3 square but the one below only supports side-1, then `(r,c)` can only support side-2 — anything larger would poke into the gap that limited the neighbour.
- **Every cell is computed once.** The driver loop visits all `(i,j)` and the memo check short-circuits everything the recursion already resolved, so the whole thing is linear in the number of cells despite looking like a triple-branch DFS.
- **Off-grid → `0` handles the borders for free.** A `1` on the last row or last column has at least one neighbour returning `0`, so it caps at side `1` — correct, since no bigger square fits.

**Dry Run** (`matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]`):

Filling the memo bottom-up (the recursion resolves it in this dependency order). `-` marks a `'0'` cell:

| row | matrix | memo (side lengths) | notes |
|---|---|---|---|
| 3 | `1 0 0 1 0` | `1 0 0 1 0` | last row — every `1` caps at `1` |
| 2 | `1 1 1 1 1` | `1 1 1 1 1` | each is blocked by a `0` below or diagonally |
| 1 | `1 0 1 1 1` | `1 0 2 2 1` | `(1,3)`: right=`1`, diag=`1`, down=`1` → `1 + 1 = 2` |
| 0 | `1 0 1 0 0` | `1 0 1 0 0` | `(0,2)`: right is `'0'` → `1 + 0 = 1` |

Walking `(1,2)` in detail:
```
matrix[1][2] = '1'
  right = f(1,3) = 2
  diag  = f(2,3) = 1
  down  = f(2,2) = 1
  min   = 1  ->  memo[1][2] = 2
```

Max side over the whole memo = `2` → answer `2 * 2 = 4` ✅
The winning square is rows 1–2, columns 2–3.

```java
class Solution {
    private static final int[][] DIR = new int[][]{{0,1},{1,1},{1,0} };

    public int maximalSquare(char[][] matrix) {
        int m = matrix.length;
        int n = matrix[0].length;

        int[][] memo = new int[m][n];
        for (int[] a : memo) Arrays.fill(a, -1);

        for (int i=0; i<m; i++) {
            for (int j=0; j<n; j++) {
                function(matrix, memo, i, j);
            }
        }

        int max = 0;
        System.out.println(Arrays.deepToString(memo));
        for (int[] a : memo) {
            for (int d : a) {
                max = Math.max (max, d*d);
            }
        }

        return max;
    }

    private int function (char[][] matrix, int[][] memo, int row, int col) {
        if (row>=matrix.length || col>=matrix[0].length) return 0;
        if (matrix[row][col]=='0') return memo[row][col] = 0;
        if (memo[row][col] != -1) return memo[row][col];

        int min = Integer.MAX_VALUE;
        for (int[] dir : DIR) {
            int newRow = row + dir[0];
            int newCol = col + dir[1];
            min = Math.min (min, function(matrix, memo, newRow, newCol));
        }
        return memo[row][col] = min==Integer.MAX_VALUE ? 0 : min + 1;
    }
}
```

- **Time:** `O(m·n)` · **Space:** `O(m·n)` memo + `O(m + n)` recursion stack

---

## 🔑 Key Insights
- **`min`, not `max`.** Every instinct says "take the biggest neighbour", but a square is only as big as its most constrained sub-square. `min` is the whole algorithm.
- **Two mirror formulations exist.** The textbook version anchors on the **bottom-right** corner and looks *up / up-left / left*; this one anchors on the **top-left** and looks *right / down-right / down*. Identical logic, opposite sweep direction — know both so an interviewer's phrasing doesn't throw you.
- **Side vs. area.** The DP computes side lengths; the answer squares them. Forgetting `d*d` is the single most common way to lose this problem.
- **Only three neighbours, not four.** The fourth diagonal isn't needed — with `right`, `down`, and `down-right` all present, the interior is fully covered.

---

## ⚠️ Pitfalls
> [!warning]
> - `matrix[i][j]` is a **`char`**, not an `int`. Compare against `'0'` / `'1'`, never `0` / `1` — the latter compiles (char widens to int) and silently always fails.
> - The `min == Integer.MAX_VALUE ? 0 : min + 1` guard is **dead code**: `DIR` always has three entries, so `min` is always overwritten. Harmless, but don't mistake it for a needed base case.
> - The `'0'` check sits *before* the memo hit, so a `'0'` cell re-runs its (trivial) branch on every visit. Correct and `O(1)`, but if you move the memo check above it you must make sure `-1` can never be a legitimate stored value.
> - `System.out.println(Arrays.deepToString(memo))` is left-over debug output — remove it before submitting or it slows the run and clutters stdout.

---

## ⏱️ Complexity
- **Time:** `O(m·n)`
- **Space:** `O(m·n)`
