---
created: 2026-08-02 17:31
tags:
  - dsa
  - backtracking
  - recursion
  - matrix
  - hash-table
source: https://leetcode.com/problems/sudoku-solver/
problem_id: "37"
difficulty: Hard
status: Solved
review_date:
---
# LT_0037 – Sudoku Solver

**Link:** [Open Problem](https://leetcode.com/problems/sudoku-solver/)

> Companion problem: [[LT_0036_Valid_Sudoku]] — same constraint rules, but only *checking* instead of *filling*.

---

## 📝 Problem Description
> [!info]
> Write a program to solve a Sudoku puzzle by filling the empty cells.
>
> A sudoku solution must satisfy **all of the following rules**:
>
> 1. Each of the digits `1-9` must occur exactly once in each **row**.
> 2. Each of the digits `1-9` must occur exactly once in each **column**.
> 3. Each of the digits `1-9` must occur exactly once in each of the nine `3x3` sub-boxes of the grid.
>
> The `'.'` character indicates empty cells.
>
> Modify the board **in place** — there is no return value.

---

## 🧪 Examples
> [!example]
> **Input:**
> ```
> board =
> [["5","3",".",".","7",".",".",".","."]
> ,["6",".",".","1","9","5",".",".","."]
> ,[".","9","8",".",".",".",".","6","."]
> ,["8",".",".",".","6",".",".",".","3"]
> ,["4",".",".","8",".","3",".",".","1"]
> ,["7",".",".",".","2",".",".",".","6"]
> ,[".","6",".",".",".",".","2","8","."]
> ,[".",".",".","4","1","9",".",".","5"]
> ,[".",".",".",".","8",".",".","7","9"]]
> ```
> **Output:**
> ```
> [["5","3","4","6","7","8","9","1","2"]
> ,["6","7","2","1","9","5","3","4","8"]
> ,["1","9","8","3","4","2","5","6","7"]
> ,["8","5","9","7","6","1","4","2","3"]
> ,["4","2","6","8","5","3","7","9","1"]
> ,["7","1","3","9","2","4","8","5","6"]
> ,["9","6","1","5","3","7","2","8","4"]
> ,["2","8","7","4","1","9","6","3","5"]
> ,["3","4","5","2","8","6","1","7","9"]]
> ```
> **Explanation:** The only valid solution for the given board.

---

## ⚠️ Constraints
> [!warning]
> - `board.length == 9`
> - `board[i].length == 9`
> - `board[i][j]` is a digit or `'.'`
> - It is **guaranteed** that the input board has only one solution

---

## 🔍 Intuition

There's no clever formula here — Sudoku is a **constraint satisfaction** problem, and the honest answer is *try digits and undo the ones that don't work*. That's backtracking. The structure I need is: find the first empty cell, try each of `'1'..'9'` in it, and for every digit that doesn't immediately violate a rule, **commit it and recurse**. If the recursive call reports success, the board is solved and I propagate `true` all the way up. If it fails, I **erase the digit** (`board[i][j] = '.'`) and try the next one.

The two lines that carry the whole algorithm are `if (solver(board)) return true;` and `board[i][j] = '.';`. The first says *"my guess led to a complete solution — stop, don't touch anything."* The second says *"my guess led to a dead end — pretend I never made it."* Skipping the erase is the classic bug: the board gets polluted with abandoned guesses and every later `isValid` lies to you.

The `return false` after the digit loop is the other subtle piece. If I've reached an empty cell and **none** of `1-9` works, this branch is unsolvable — I must return `false` immediately rather than continuing the scan, because there's no point examining later cells when this one can't be filled at all. And the `return true` at the very bottom is reached only when both loops complete without finding a single `'.'` — meaning the board is full, and since we only ever placed valid digits, full ⇒ solved.

Compared to [[LT_0036_Valid_Sudoku]], the difference is direction: LC 36 checks a *given* board in one pass; LC 37 *searches* the space of boards, using an LC-36-style check as its pruning test at every step.

> 🟢 *Backtracking / DFS over Cell Assignments with Constraint Pruning*

---

## 🔁 The `box → cells` Formula — Derived From Scratch

The `isValid` helper needs to scan all 9 cells of one box using a single loop variable. That's this pair of lines:

```java
int boxRow = 3 * (row / 3) + k / 3;
int boxCol = 3 * (col / 3) + k % 3;
```

It looks cryptic, but it's more intuitive than it seems once you stop reading the code and just think about the box.

### Step 1 — Suppose we're validating cell `(4, 5)`

```
      0 1 2 | 3 4 5 | 6 7 8
      ---------------------
0           |       |
1           |       |
2           |       |
      ---------------------
3           | X X X |
4           | X ? X |
5           | X X X |
      ---------------------
6           |       |
7           |       |
8           |       |
```

It belongs to the **centre box**.

### Step 2 — Find the top-left corner of that box

The box spans rows `3,4,5` and columns `3,4,5`, so its corner is `(3,3)`. How do we compute that?

```java
startRow = (row / 3) * 3;   // 4/3 = 1  ->  1*3 = 3
startCol = (col / 3) * 3;   // 5/3 = 1  ->  1*3 = 3
```

> `/3` snaps down to *which block of three* you're in; `*3` converts that block number back into an actual row/column index. `(row/3)*3` is "round `row` down to the nearest multiple of 3."

### Step 3 — Visit every cell in the box with one loop variable

We want these 9 coordinates:

```
(3,3) (3,4) (3,5)
(4,3) (4,4) (4,5)
(5,3) (5,4) (5,5)
```

Can one variable `k = 0..8` generate all of them? Yes.

### Step 4 — Arrange `k` as a 3×3 grid

Forget Sudoku for a second and just stare at this:

```
    k             k/3            k%3
  0 1 2          0 0 0          0 1 2
  3 4 5          1 1 1          0 1 2
  6 7 8          2 2 2          0 1 2
                    ↑              ↑
             row offsets    column offsets
```

- `k/3` is constant across each row → that's exactly the **row offset**.
- `k%3` cycles `0,1,2` across each row → that's exactly the **column offset**.

### Step 5 — Add the offsets to the corner

| k | k/3 | k%3 | Row | Col | Cell |
| - | --- | --- | --- | --- | ----- |
| 0 | 0   | 0   | 3+0 | 3+0 | (3,3) |
| 1 | 0   | 1   | 3+0 | 3+1 | (3,4) |
| 2 | 0   | 2   | 3+0 | 3+2 | (3,5) |
| 3 | 1   | 0   | 3+1 | 3+0 | (4,3) |
| 4 | 1   | 1   | 3+1 | 3+1 | (4,4) |
| 5 | 1   | 2   | 3+1 | 3+2 | (4,5) |
| 6 | 2   | 0   | 3+2 | 3+0 | (5,3) |
| 7 | 2   | 1   | 3+2 | 3+1 | (5,4) |
| 8 | 2   | 2   | 3+2 | 3+2 | (5,5) |

Exactly the 9 cells we wanted. Substituting `startRow = (row/3)*3` and `startCol = (col/3)*3` gives the formula:

```java
int boxRow = (row / 3) * 3 + k / 3;
int boxCol = (col / 3) * 3 + k % 3;
```

> [!tip]
> **The key intuition isn't about Sudoku.** It's about using a single number to walk a 3×3 grid. Whenever you see `for (int k = 0; k < 9; k++)` over a box, read `k` as this mini-grid:
> ```
> 0 1 2
> 3 4 5
> 6 7 8
> ```
> `k / 3` = which row of the mini-grid, `k % 3` = which column. The same trick shows up all over matrix problems, not just Sudoku.

> [!info]
> **Don't confuse this with the LC 36 formula.** They answer opposite questions:
> - **cell → box** (`[[LT_0036_Valid_Sudoku]]`): `boxIndex = (row/3)*3 + (col/3)` — *"which of the 9 boxes am I in?"*
> - **box → cells** (here): `r = (row/3)*3 + k/3`, `c = (col/3)*3 + k%3` — *"walk all 9 cells of my box."*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Backtracking with On-Demand Validation

**Why this works:**
- **The invariant is that the board is always legal.** We only ever write a digit that `isValid` approved, so at any point in the recursion the partially filled board contains no rule violations. That means "board is full" and "board is solved" are the same condition — which is why the bottom `return true` needs no extra checking.
- **Every guess is fully reversible.** `board[i][j] = k` then `board[i][j] = '.'` on failure means the board is restored to exactly its prior state before trying the next digit. Backtracking is only correct if the undo is complete.
- **Failure propagates correctly.** `return false` inside the empty-cell branch prunes the entire subtree rooted at that guess — the caller then erases *its* digit and moves on. This is what makes the search finite instead of wandering.
- **`isValid` is the pruning function.** Without it, this would be brute-force over `9^m` boards with a validity check only at the end. Checking *before* placing kills most branches at depth 1–2, which is what makes a Hard-labelled exponential search finish in milliseconds.

**Dry Run** (Example 1 — the very first empty cell):

Scan order finds the first `'.'` at **`(0, 2)`**. What are its legal candidates?

```
row 0    = 5 3 . . 7 . . . .     ->  blocks 5, 3, 7
col 2    = . . 8 . . . . . .     ->  blocks 8
box 0    = 5 3 .                 ->  blocks 5, 3, 6, 9, 8
           6 . .
           . 9 8

candidates = {1..9} - {3,5,6,7,8,9} = {1, 2, 4}
```

Now watch `isValid(board, 0, 2, '1')` use the box formula:

```
row = 0, col = 2
boxRow = 3*(0/3) + k/3 = 0 + k/3
boxCol = 3*(2/3) + k%3 = 0 + k%3

k = 0..8  ->  (0,0)(0,1)(0,2)(1,0)(1,1)(1,2)(2,0)(2,1)(2,2)   ← exactly box 0 ✅
```

The backtracking trace at this cell:

| Attempt | Action | Outcome |
|---|---|---|
| `k = '1'` | `isValid` ✅ → place `1` at `(0,2)`, recurse | subtree explores deeply, eventually hits a cell with **no legal digit** → `false` bubbles up → **erase**, `board[0][2] = '.'` |
| `k = '2'` | `isValid` ✅ → place `2` at `(0,2)`, recurse | same story — dead end → **erase** |
| `k = '3'` | `isValid` ❌ (row 0 already has `3`) | skipped without recursing — pruned instantly |
| `k = '4'` | `isValid` ✅ → place `4` at `(0,2)`, recurse | subtree succeeds → `solver` returns `true` → **`4` stays**, and every frame above returns `true` without erasing ✅ |
| `k='5'..'9'` | never reached | we already returned `true` |

And indeed the final answer has `board[0][2] == '4'`.

The next frame down starts its own scan from `(0,0)`, skips filled cells, and lands on `(0,3)` — repeating the same process until the two loops complete without finding a `'.'`, at which point the deepest frame hits `return true` and the whole stack unwinds successfully.

```java
class Solution {
    public void solveSudoku(char[][] board) {
        solver(board);
    }

    private boolean solver(char[][] board) {
        for(int i=0; i<board.length; i++) {
            for(int j=0; j<board[0].length; j++) {
                char ch = board[i][j];
                if(ch=='.') {
                    
                    for(char k='1'; k<='9'; k++) {
                        if(isValid(board, i, j, k)) {
                            board[i][j] = k;
                            
                            if(solver(board)) {
                                return true;
                            }
                            board[i][j] = '.';
                        }    
                    }
                    return false;
                }
            }
        }

        return true;
    }

    private boolean isValid(char[][] board, int row, int col, char val) {
        for(int k=0; k<9; k++) {
            if(board[k][col]==val) return false;
            if(board[row][k]==val) return false;

            int boxIdxRow = 3 * (row/3) + k/3;
            int boxColIdx = 3 * (col/3) + k%3;
            if(board[boxIdxRow][boxColIdx]==val) return false;
        }
        return true;
    }
}
```

---

### ⚡ Optimisation Worth Mentioning in an Interview

Two costs are being paid repeatedly, and both are worth naming even if you don't write the code:

**1. The scan restarts from `(0,0)` on every recursive call.**
Each `solver()` invocation re-walks up to 81 cells just to find the next `'.'`. Passing a linear position `pos = 0..80` instead makes the descent `O(1)`:

```java
private boolean solver(char[][] board, int pos) {
    if (pos == 81) return true;                 // filled every cell
    int i = pos / 9, j = pos % 9;               // 1D -> 2D  (see LT_0036)
    if (board[i][j] != '.') return solver(board, pos + 1);

    for (char k = '1'; k <= '9'; k++) {
        if (isValid(board, i, j, k)) {
            board[i][j] = k;
            if (solver(board, pos + 1)) return true;
            board[i][j] = '.';
        }
    }
    return false;
}
```

**2. `isValid` re-derives constraints by scanning 27 cells every call.**
Carrying the three `boolean[9][9]` grids from [[LT_0036_Valid_Sudoku]] (`rowUsed`, `colUsed`, `boxUsed`) turns the check into three array reads — `O(1)` instead of `O(9)`. Place = set three flags to `true`; backtrack = set them back to `false`. Same backtracking skeleton, ~10× less work per node.

> [!tip]
> The genuinely big win is **Most Constrained Variable** (MRV): instead of taking the *first* empty cell, pick the empty cell with the **fewest legal candidates**. Failing fast near the root prunes enormously more of the tree than any constant-factor tweak. Good thing to mention out loud — usually not worth coding under interview time pressure.

---

## 🔑 Key Insights
- **The undo is the algorithm.** `board[i][j] = '.'` after a failed recursion is what separates backtracking from brute force. Everything else is bookkeeping.
- **`return true` short-circuits the erase.** When the recursive call succeeds we return *immediately*, so the digit is never undone — that's how the solution survives the unwind. This only works because the problem guarantees a unique solution; we don't need to keep searching.
- **`return false` must sit inside the empty-cell branch**, after the digit loop — not after the outer loops. It means *"this cell is unfillable, so this whole branch is dead."*
- **Reaching the bottom `return true` means every cell is filled**, and since every write passed `isValid`, full ⇒ valid ⇒ solved. No final verification pass is needed.
- **`k/3` and `k%3` decompose one index into a `(row, col)` pair** for any 3-column grid. The same `/width` and `%width` pair converts a 1D index back to 2D anywhere — see [[LT_0036_Valid_Sudoku]] for the derivation.
- **The single `for(k=0..8)` loop in `isValid` does triple duty** — column scan, row scan, and box scan share one counter. Compact, and no correctness cost since the three checks are independent.

---

## ⚠️ Pitfalls
> [!warning]
> - **Forgetting `board[i][j] = '.'` on failure.** The single most common bug. Abandoned guesses stay on the board, poison every later `isValid`, and the solver either returns a wrong board or fails on a solvable puzzle.
> - **Erasing after a *successful* recursion.** If you write `solver(board); board[i][j] = '.';` without the `if (...) return true;` guard, you unwind the solution you just found and end up with an empty board.
> - **Putting `return false` after the outer loops instead of inside the `'.'` branch.** Then a cell with no legal digit doesn't abort — the scan continues to later cells and the search explodes (or silently returns `true` on an unfinished board).
> - **`isValid` scans the target cell itself** — `(row,col)` appears in all three sweeps. It's harmless *only because* the cell is `'.'` when we call it, and `'.'` never equals a digit. If you ever refactor to call `isValid` after placing, it will always return `false`.
> - **Returning a new board.** The signature is `void` — the grader reads the mutated input array. Building a copy and returning it scores zero.
> - **Assuming `isValid` alone is enough.** A digit passing all three rules right now can still lead to a dead end 20 cells later. The pruning is necessary but not sufficient — the recursion is what actually finds the answer.

---

## ⏱️ Complexity
- **Time:** `O(9^m)` worst case, where `m` is the number of empty cells — each empty cell branches up to 9 ways. With this code's per-node cost that's `O(9^m · 81 · 9)` (board rescan × `isValid`). Since the board is fixed at `9x9`, this is technically bounded by a constant, and pruning makes real inputs finish almost instantly.
- **Space:** `O(m)` — recursion depth is at most 81 stack frames (one per empty cell). The board is mutated in place, and `isValid` uses `O(1)` extra space.

---

## 💡 Mental Model

```
Walk the board until you hit a blank.

For each digit 1..9:
    Does it break a row / column / box rule right now?
        Yes -> skip it, don't even recurse.       (prune)
        No  -> write it down and walk deeper.     (guess)
                Deeper call says SOLVED?  -> freeze it, return SOLVED.
                Deeper call says STUCK?   -> rub it out, try next digit.

Tried all 9 and none worked?  -> this branch is impossible, report STUCK.
Never found a blank at all?   -> the board is full and legal -> SOLVED.
```

The board is a **single shared mutable state** that the recursion writes to on the way down and cleans up on the way back — pencil marks you erase when the path dead-ends.
