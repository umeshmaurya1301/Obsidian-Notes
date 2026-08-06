---
created: 2026-08-02 17:15
tags:
  - dsa
  - arrays
  - hash-table
  - matrix
source: https://leetcode.com/problems/valid-sudoku/
problem_id: "36"
difficulty: Medium
status: Solved
review_date:
---
# LT_0036 – Valid Sudoku

**Link:** [Open Problem](https://leetcode.com/problems/valid-sudoku/)

---

## 📝 Problem Description
> [!info]
> Determine if a `9 x 9` Sudoku board is **valid**. Only the filled cells need to be validated according to the following rules:
>
> 1. Each row must contain the digits `1-9` without repetition.
> 2. Each column must contain the digits `1-9` without repetition.
> 3. Each of the nine `3 x 3` sub-boxes of the grid must contain the digits `1-9` without repetition.
>
> **Note:**
> - A Sudoku board (partially filled) could be valid but is **not necessarily solvable**.
> - Only the filled cells need to be validated according to the mentioned rules.

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
> **Output:** `true`

> [!example]
> **Input:**
> ```
> board =
> [["8","3",".",".","7",".",".",".","."]
> ,["6",".",".","1","9","5",".",".","."]
> ,[".","9","8",".",".",".",".","6","."]
> ,["8",".",".",".","6",".",".",".","3"]
> ,["4",".",".","8",".","3",".",".","1"]
> ,["7",".",".",".","2",".",".",".","6"]
> ,[".","6",".",".",".",".","2","8","."]
> ,[".",".",".","4","1","9",".",".","5"]
> ,[".",".",".",".","8",".",".","7","9"]]
> ```
> **Output:** `false`
> **Explanation:** Same as Example 1, except with the `5` in the top-left corner modified to `8`. Since there are **two 8's** in the top-left `3x3` sub-box, it is invalid.

---

## ⚠️ Constraints
> [!warning]
> - `board.length == 9`
> - `board[i].length == 9`
> - `board[i][j]` is a digit `1-9` or `'.'`
> - Only the filled cells need to be validated

---

## 🔍 Intuition

The naive instinct is to write three separate passes — one scanning rows, one scanning columns, one scanning each `3x3` box — but that's three traversals of the same 81 cells doing structurally identical work. The realisation that collapses it into **one pass** is that every cell participates in exactly **three constraint groups** simultaneously: its row, its column, and its box. So while standing on a single cell I can ask all three questions at once, and if any of them already contains this digit, the board is invalid immediately.

The second realisation is that I don't need `HashSet`s at all. The value domain is fixed and tiny — digits `1-9`, so 9 possible values across 9 rows / 9 columns / 9 boxes. That's exactly a `boolean[9][9]` per constraint type, giving me `O(1)` lookup with zero hashing overhead and no object allocation. `rowCheck[i][val]` answers *"has row `i` already seen digit `val`?"* in a single array read.

The only non-trivial part is mapping a `(i, j)` cell to its box number, which is `3 * (i/3) + j/3` — the standard 2D→1D flattening applied to the `3x3` grid of boxes rather than the `9x9` grid of cells. That derivation is worth internalising, so it gets its own section below.

> 🟢 *Single-Pass Constraint Tracking with Fixed-Size Boolean Grids*

---

## 📐 The Box Index Formula — Derived, Not Memorised

This is **the** hardest part of Sudoku problems for most people. The trick is to stop memorising the formula and instead understand **how the 3×3 boxes are laid out**.

### Visualise the board

```
Rows
      0 1 2 | 3 4 5 | 6 7 8
      ---------------------
0     A A A | B B B | C C C
1     A A A | B B B | C C C
2     A A A | B B B | C C C
      ---------------------
3     D D D | E E E | F F F
4     D D D | E E E | F F F
5     D D D | E E E | F F F
      ---------------------
6     G G G | H H H | I I I
7     G G G | H H H | I I I
8     G G G | H H H | I I I
```

There are **9 boxes**. Let's number them:

```
0 1 2
3 4 5
6 7 8
```

So we want: `(row, col)` → **which box?**

### Step 1 — Which box-row?

Rows are grouped into:

```
0 1 2  ->  box row 0
3 4 5  ->  box row 1
6 7 8  ->  box row 2
```

That's just integer division by `3`:

```
row = 1  ->  1/3 = 0
row = 4  ->  4/3 = 1
row = 8  ->  8/3 = 2
```

So `boxRow = row / 3`.

### Step 2 — Which box-column?

Identically:

```
0 1 2  ->  box column 0
3 4 5  ->  box column 1
6 7 8  ->  box column 2
```

So `boxCol = col / 3`.  (e.g. `col = 5` → `5/3 = 1`)

### Step 3 — Flatten `(boxRow, boxCol)` into one number

We have a coordinate in a **3×3 grid of boxes** and we want a single index `0..8`. That's the classic 2D→1D conversion:

```
index = row * numberOfColumns + col
```

Here there are **3 box-columns**, so:

```
boxIndex = boxRow * 3 + boxCol
```

Substituting `boxRow = row/3` and `boxCol = col/3`:

```java
boxIndex = 3 * (row/3) + (col/3);
```

### Sanity checks

| Cell | `row/3` | `col/3` | `boxIndex` | ✔ |
|---|---|---|---|---|
| `(4,7)` | `1` | `2` | `1*3 + 2 = 5` | ✅ |
| `(8,0)` | `2` | `0` | `2*3 + 0 = 6` | ✅ |
| `(2,5)` | `0` | `1` | `0*3 + 1 = 1` | ✅ |

---

## 🔄 Why `index = row * numColumns + col` Works At All

Worth deriving once, because it shows up everywhere: 2D arrays, matrices, images, game boards.

Take a `3 x 4` matrix:

```text
      Col
      0  1  2  3
Row  ----------------
0    A  B  C  D
1    E  F  G  H
2    I  J  K  L
```

Stored in a **1D array** it becomes:

```text
Index   0 1 2 3 4 5 6 7 8 9 10 11
Value   A B C D E F G H I J K  L
```

- **Row 0:** `A→0, B→1, C→2, D→3` — `index = column`, because no rows come before it.
- **Row 1:** starts at index `4`, because row 0 already occupied `1 × 4 = 4` slots. So `F = 4 + 1 = 5`.
- **Row 2:** starts at index `8`, because two full rows came before: `2 × 4 = 8`. So `L = 8 + 3 = 11`.

**The pattern:** every row contributes `numberOfColumns` elements, so before row `r` there are `r × numberOfColumns` elements. Then move `col` steps into the row:

```java
index = row * numberOfColumns + col;
```

> [!tip]
> **Mental model.** Imagine reading a book left-to-right, top-to-bottom. To reach `K` you first skip 2 full rows (`2 × 4 = 8`), then move `2` columns in → index `10`.
>
> Whenever you see `row * something + col`, ask: *"How many complete rows do I skip before reaching my target row?"* The answer is always `rows skipped × number of columns`.

And the inverse — 1D index back to 2D — is the same identity read backwards:

```java
row = index / numberOfColumns;   // which row am I in
col = index % numberOfColumns;   // how far into that row
```

**Sudoku is just this formula applied to the 3×3 grid of boxes** instead of the 9×9 grid of cells — which is why `numberOfColumns` is `3`, not `9`.

---

## 🔁 The *Other* Formula — `box → cells`

A closely related formula shows up in the **Sudoku Solver** variant, and confuses almost everyone because it looks similar but does the opposite job:

```java
int boxIdxRow = 3 * (row/3) + k/3;
int boxColIdx = 3 * (col/3) + k%3;
```

Here you're **not** finding a box number — you're iterating over **all 9 cells inside a box**.

Say `(row, col) = (4, 5)`, which lies in the centre box. That box starts at:

```
startRow = 3 * (row/3) = 3 * 1 = 3
startCol = 3 * (col/3) = 3 * 1 = 3
```

To visit all 9 cells with a single loop variable `k = 0..8`, arrange `k` as a 3×3 grid:

```
k          k/3            k%3
0 1 2      0 0 0          0 1 2
3 4 5      1 1 1          0 1 2
6 7 8      2 2 2          0 1 2
           ↑ row offset   ↑ col offset
```

So `actualRow = startRow + k/3` and `actualCol = startCol + k%3`, generating exactly:

| k | row | col |
| - | --- | --- |
| 0 | 3   | 3   |
| 1 | 3   | 4   |
| 2 | 3   | 5   |
| 3 | 4   | 3   |
| 4 | 4   | 4   |
| 5 | 4   | 5   |
| 6 | 5   | 3   |
| 7 | 5   | 4   |
| 8 | 5   | 5   |

> [!tip]
> **Remember them as two separate transformations:**
> - **cell → box** — compress the `9x9` board into a `3x3` grid: `boxIndex = (row/3) * 3 + (col/3)`
> - **box → cells** — find the top-left corner, then add offsets: `r = 3*(row/3) + k/3`, `c = 3*(col/3) + k%3`
>
> Derive them, don't memorise them.

---

## 🧠 Evolution of Solutions

### ✅ Solution — Single Pass with Three Boolean Grids

**Why this works:**
- **Every cell belongs to exactly one row, one column, one box.** Validating all three at the moment we visit the cell means one traversal instead of three, and lets us bail out on the very first duplicate.
- **The value domain is fixed** (`1-9`), so `boolean[9][9]` is a perfect hash — `O(1)` lookup, no hashing, no boxing, no `HashSet` allocation. This is strictly faster than the `HashSet<String>` approach that encodes keys like `"5@row3"`.
- **Marking after checking is the correct order.** We check all three grids *before* setting any of them, so a cell never conflicts with itself.
- `'.'` cells are skipped entirely — the problem only asks about filled cells, and a partially filled board can be valid without being solvable.

**Dry Run** (Example 1, first few filled cells):

`val = ch - '1'` maps `'1'→0 ... '9'→8`, so digit `d` lives at index `d-1`.

| `(i,j)` | `ch` | `val` | `boxIndex` = `3*(i/3)+j/3` | Checks | Action |
|---|---|---|---|---|---|
| `(0,0)` | `5` | `4` | `3*0 + 0 = 0` | `rowCheck[0][4]`, `colCheck[4][0]`, `boxCheck[0][4]` → all `false` | mark all three |
| `(0,1)` | `3` | `2` | `3*0 + 0 = 0` | all `false` | mark |
| `(0,2)` | `.` | — | — | — | `continue` |
| `(0,4)` | `7` | `6` | `3*0 + 1 = 1` | all `false` | mark |
| `(1,0)` | `6` | `5` | `3*0 + 0 = 0` | `boxCheck[0][5]` = `false` (box 0 so far holds only `5,3,6`) | mark |
| `(1,3)` | `1` | `0` | `3*0 + 1 = 1` | all `false` | mark |
| `(1,5)` | `5` | `4` | `3*0 + 1 = 1` | `rowCheck[1][4]`=`false`, `colCheck[4][5]`=`false`, `boxCheck[1][4]`=`false` | mark — note `colCheck[4][0]` *is* set from `(0,0)`, but that's column `0`, not `5` ✅ |
| `(2,1)` | `9` | `8` | `3*0 + 0 = 0` | all `false` | mark |

…continues through all 81 cells with no conflict → **returns `true`** ✅

**Example 2 — where it short-circuits:**

```
(0,0) = '8'  ->  val = 7, boxIndex = 0  ->  boxCheck[0][7] = true
...
(2,2) = '8'  ->  val = 7, boxIndex = 3*(2/3) + 2/3 = 0
                 rowCheck[2][7] = false   (different row)
                 colCheck[7][2] = false   (different column)
                 boxCheck[0][7] = TRUE    ← 💥 same box, same digit
                 return false
```

```java
class Solution {
    public boolean isValidSudoku(char[][] board) {
        boolean[][] rowCheck = new boolean[9][9];
        boolean[][] colCheck = new boolean[9][9];
        boolean[][] boxCheck = new boolean[9][9];

        for(int i=0; i<board.length; i++) {
            for(int j=0; j<board[0].length; j++) {
                char ch = board[i][j];
                if(ch=='.') continue;

                int val = ch - '1';
                int boxIndex = 3 * (i/3) + j/3;

                if(rowCheck[i][val] || colCheck[val][j] || boxCheck[boxIndex][val]) {
                    return false;                                        
                }
                rowCheck[i][val]  = true;
                colCheck[val][j] = true;
                boxCheck[boxIndex][val] = true;
            }
        }

        return true;
    }
}
```

---

## 🔑 Key Insights
- **One cell, three constraints.** The whole optimisation is recognising that row / column / box checks can share a single traversal instead of needing three.
- **Fixed domain → array beats hash.** With only 9 values, `boolean[9][9]` is a perfect hash function. No `HashSet<String>` key-building (`"5@row3"`), no hashing cost, no allocation — same `O(1)` semantics, far lower constants.
- **`ch - '1'` not `ch - '0'`.** Subtracting `'1'` maps `'1'..'9'` into `0..8`, using all 9 slots. Subtracting `'0'` would give `1..9` and require a `boolean[9][10]`.
- **`boxIndex = 3 * (i/3) + j/3`** is `row * numColumns + col` applied to the 3×3 grid of *boxes*. Integer division truncates, which is exactly the "which group of 3 am I in" answer we want.
- **Check-then-mark ordering** is what prevents a cell from flagging itself as a duplicate.

---

## ⚠️ Pitfalls
> [!warning]
> - **`colCheck` is indexed `[val][j]`, not `[j][val]`** — the opposite convention from `rowCheck[i][val]`. It's still correct (a `9x9` boolean grid works either way as long as you're consistent), but the asymmetry is easy to misread later. `rowCheck[i][val]` = *"row `i` has digit `val`"*; `colCheck[val][j]` = *"digit `val` appears in column `j`"*.
> - **Marking before checking** — if you set `rowCheck[i][val] = true` before the `if`, every filled cell instantly reports a conflict with itself and the method always returns `false`.
> - **Forgetting to skip `'.'`** — `'.' - '1'` is `-3`, which throws `ArrayIndexOutOfBoundsException`. The `continue` must come first.
> - **Assuming valid ⇒ solvable.** The problem only asks for *no current violations*. A board can pass every rule here and still have no solution — don't over-engineer.

---

## ⏱️ Complexity
- **Time:** `O(1)` — the board is always `9x9`, so exactly 81 cells with `O(1)` work each. Stated generally for an `n x n` board it's `O(n²)`, i.e. linear in input size.
- **Space:** `O(1)` — three fixed `9x9` boolean grids = 243 booleans, independent of input.

---

## 💡 Mental Model

```
Stand on a cell. It sits at the intersection of 3 constraint groups:

        column j
           │
  row i ───┼───   and lives inside box  3*(i/3) + j/3
           │
        [3x3 box]

Ask all three "have you seen this digit?" in one breath.
Any "yes" -> invalid, stop immediately.
All "no"  -> record the digit in all three, move on.
```

Three `boolean[9][9]` grids are just three lookup tables — one per constraint type — where the first index selects *which* row / column / box, and the second selects *which digit*.
