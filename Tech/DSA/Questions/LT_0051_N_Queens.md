---
created: 2026-08-02 10:45
tags:
  - dsa
  - backtracking
  - recursion
  - matrix
source: https://leetcode.com/problems/n-queens/
problem_id: "51"
difficulty: Hard
status: Solved
review_date:
---
# LT_0051 – N-Queens

**Link:** [Open Problem](https://leetcode.com/problems/n-queens/)

---

## 📝 Problem Description
> [!info]
> The **n-queens** puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other.
>
> Given an integer `n`, return *all distinct solutions to the **n-queens** puzzle*. You may return the answer in **any order**.
>
> Each solution contains a distinct board configuration of the n-queens' placement, where `'Q'` and `'.'` both indicate a queen and an empty space, respectively.
>
> Recall that a queen attacks along its **row**, its **column**, and both **diagonals**.

---

## 🧪 Examples
> [!example]
> **Input:** `n = 4`
> **Output:** `[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]`
> **Explanation:** There exist two distinct solutions to the 4-queens puzzle as shown above.
>
> ```
> Solution 1          Solution 2
> . Q . .             . . Q .
> . . . Q             Q . . .
> Q . . .             . . . Q
> . . Q .             . Q . .
> ```

> [!example]
> **Input:** `n = 1`
> **Output:** `[["Q"]]`
> **Explanation:** A single queen on a `1 x 1` board attacks nothing.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= n <= 9`

---

## 🔍 Intuition

The first realisation that shrinks the problem massively: since queens attack along rows, **every row holds exactly one queen** — no more, no less. So instead of choosing `n` cells out of `n²` (astronomically many), I only choose *which column* each row's queen sits in. That turns the search into "build a permutation-like assignment row by row", and recursion becomes the natural shape: `backtrack(row)` decides row `row` and hands off row `row + 1`.

The second realisation is the one that makes it fast: the safety check shouldn't scan the board. A cell is unsafe only if its **column**, its **↘ diagonal**, or its **↙ diagonal** already contains a queen — and each of those three is identifiable by a single integer. All cells on a `↙` (anti-)diagonal share the same `row + col`; all cells on a `↘` diagonal share the same `row - col`. So three boolean arrays act as occupancy sets, and validity becomes three `O(1)` array lookups instead of an `O(n)` scan.

Brute force — generating every placement and validating it — dies immediately because it explores branches that were already doomed at row 2. Backtracking prunes the moment a conflict appears, so entire subtrees are never entered. The board itself is just a **scratch buffer**: I stamp `'Q'` on the way down, snapshot it into strings when I reach `row == n`, and erase it on the way back up so the same array is reused across the whole search.

> 🟢 *Backtracking + Constraint Sets (column & diagonal hashing)*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Backtracking with Column + Diagonal Boolean Arrays

**Why this works:**

- **One queen per row is enforced structurally.** The recursion advances `row` by exactly 1 per placement, so row conflicts are impossible *by construction* — they never even need to be checked.
- **Diagonals collapse to integers.** For a `↙` anti-diagonal, `row + col` is invariant (`(1,2)` and `(2,1)` both give `3`). For a `↘` diagonal, `row - col` is invariant (`(1,2)` and `(2,3)` both give `-1`). Since `row - col` ranges over `[-(n-1), n-1]`, adding `n` shifts it to `[1, 2n-1]` — a legal index into a `2n`-sized array.
- **Reaching `row == n` is proof of a full solution.** Every placement was validated at insert time, so no final verification pass is needed — just serialise the board.
- **Undo is exact.** Every mutation (`board`, `cols`, `diag1`, `diag2`) is reversed on the way out, so sibling branches always start from a clean state.

**Dry Run** (`n = 4`) — I'll trace to the *first* solution found:

Diagonal keys: `d1 = row + col`, `d2 = row - col + 4`

| Step | Row | Try col | Check | Action |
|---|---|---|---|---|
| 1 | 0 | 0 | free | Place `(0,0)` → `cols[0]`, `d1=0`, `d2=4` |
| 2 | 1 | 0 | `cols[0]` taken | skip |
| 3 | 1 | 1 | `d2 = 1-1+4 = 4` taken | skip *(same ↘ diagonal as `(0,0)`)* |
| 4 | 1 | 2 | free | Place `(1,2)` → `cols[2]`, `d1=3`, `d2=3` |
| 5 | 2 | 0,1,2,3 | all blocked | ❌ dead end → **undo `(1,2)`** |
| 6 | 1 | 3 | free | Place `(1,3)` → `cols[3]`, `d1=4`, `d2=2` |
| 7 | 2 | 1 | free | Place `(2,1)` → `cols[1]`, `d1=3`, `d2=5` |
| 8 | 3 | 0,1,2,3 | all blocked | ❌ dead end → **undo `(2,1)`** |
| 9 | 2 | 2,3 | blocked | ❌ dead end → **undo `(1,3)`**, then **undo `(0,0)`** |
| 10 | 0 | 1 | free | Place `(0,1)` → `cols[1]`, `d1=1`, `d2=3` |
| 11 | 1 | 0 | `d1 = 1+0 = 1` taken | skip *(same ↙ diagonal as `(0,1)`)* |
| 12 | 1 | 2 | `d2 = 1-2+4 = 3` taken | skip |
| 13 | 1 | 3 | free | Place `(1,3)` → `cols[3]`, `d1=4`, `d2=2` |
| 14 | 2 | 0 | free | Place `(2,0)` → `cols[0]`, `d1=2`, `d2=6` |
| 15 | 3 | 2 | free | Place `(3,2)` → `row` becomes `4` |
| 16 | 4 | — | `row == n` | ✅ **Record** `[".Q..","...Q","Q...","..Q."]` |

The search then unwinds and continues from `row = 0, col = 2`, eventually finding the mirrored second solution.

```java
class Solution {

    List<List<String>> result = new ArrayList<>();

    public List<List<String>> solveNQueens(int n) {

        char[][] board = new char[n][n];
        for (char[] row : board) {
            Arrays.fill(row, '.');
        }

        boolean[] cols = new boolean[n];
        boolean[] diag1 = new boolean[2 * n];
        boolean[] diag2 = new boolean[2 * n];

        backtrack(0, board, cols, diag1, diag2, n);

        return result;
    }

    private void backtrack(int row, char[][] board,
                           boolean[] cols,
                           boolean[] diag1,
                           boolean[] diag2,
                           int n) {

        if (row == n) {
            List<String> temp = new ArrayList<>();
            for (char[] r : board) {
                temp.add(new String(r));
            }
            result.add(temp);
            return;
        }

        for (int col = 0; col < n; col++) {

            int d1 = row + col;
            int d2 = row - col + n;

            if (cols[col] || diag1[d1] || diag2[d2]) {
                continue;
            }

            // Place queen
            board[row][col] = 'Q';
            cols[col] = true;
            diag1[d1] = true;
            diag2[d2] = true;

            backtrack(row + 1, board, cols, diag1, diag2, n);

            // Backtrack
            board[row][col] = '.';
            cols[col] = false;
            diag1[d1] = false;
            diag2[d2] = false;
        }
    }
}
```

---

## 🔑 Key Insights

- **Row conflicts are eliminated by design, not by checking.** Because `backtrack` moves to `row + 1` after each placement, only three of the four attack directions ever need tracking. Recognising this halves the state you carry.
- **`row + col` identifies the `↙` diagonal, `row - col` identifies the `↘` diagonal.** This is the reusable trick — it shows up again in *N-Queens II*, *Diagonal Traverse*, and matrix-diagonal-sum problems.
- **`+ n` is purely an index shift.** `row - col` can be negative; Java arrays can't be. Any offset ≥ `n - 1` works — `n` is just the convenient choice. Sizing at `2 * n` (rather than the tight `2n - 1`) buys one wasted slot to avoid off-by-one thinking.
- **`new String(r)` snapshots the row.** `board` is mutated continuously, so the copy must happen *at* the `row == n` moment. Storing `char[]` references instead would leave every recorded solution pointing at the same, later-erased board.

---

## ⚠️ Pitfalls
> [!warning]
> - **Forgetting to undo all four mutations.** Missing `cols[col] = false` (or any one of the three flags) silently poisons every sibling branch — you'll get too few solutions with no crash to point at it.
> - **Sizing `diag2` as `new boolean[n]`.** `row - col + n` can reach `2n - 1`, so an `n`-sized array throws `ArrayIndexOutOfBoundsException`. Both diagonal arrays need `2n`-ish capacity.
> - **Storing rows without copying.** `temp.add(new String(r))` is mandatory; adding the `char[]` itself (or reusing a shared `StringBuilder`) makes all solutions alias the same mutating board.
> - **Placing `cols`/`diag` as instance fields while `result` is also an instance field** is fine here, but on repeated calls (LeetCode reuses the `Solution` object in some setups) a non-reset `result` would accumulate stale answers. Local arrays passed as parameters — as done here — sidestep that.

---

## ⏱️ Complexity
- **Time:** `O(n!)` in the worst case — row `0` has `n` choices, row `1` has at most `n - 1`, and so on; pruning cuts this drastically in practice but the bound stands. Serialising each solution adds `O(n²)`, giving `O(n! · n²)` overall.
- **Space:** `O(n²)` for the `board` scratch buffer, plus `O(n)` for the recursion stack and the three constraint arrays. Output space (all solutions) is excluded from this count.

---

## 💡 Mental Model

```
Walk down the board one row at a time.
Each row must host exactly one queen — pick her column.

A column is legal if all three "already occupied" sets miss it:
    cols[col]          → someone owns this file
    diag1[row + col]   → someone owns this ↙ anti-diagonal
    diag2[row - col+n] → someone owns this ↘ diagonal

Place  → mark all three, descend.
Return → unmark all three, try the next column.
Reach row == n → the board is a valid answer; photograph it.
```

The whole trick is turning "is this square attacked?" from a board scan into **three constant-time set lookups**.
