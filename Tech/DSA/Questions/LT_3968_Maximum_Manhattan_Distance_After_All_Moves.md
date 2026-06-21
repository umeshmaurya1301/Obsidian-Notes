---
created: 2026-06-21 00:00
tags:
  - dsa
  - math
  - greedy
  - string
source: https://leetcode.com/problems/maximum-manhattan-distance-after-all-moves/
problem_id: "3968"
difficulty: Easy
status: Solved
review_date:
---
# LT_3968 – Maximum Manhattan Distance After All Moves

**Link:** [Open Problem](https://leetcode.com/problems/maximum-manhattan-distance-after-all-moves/)

---

## 📝 Problem Description
> [!info]
> You are given a string `moves` consisting of characters `'U'`, `'D'`, `'L'`, `'R'`, and `'_'`. Starting at the origin `(0, 0)`:
> - `'U'` moves up 1 unit (y++)
> - `'D'` moves down 1 unit (y--)
> - `'L'` moves left 1 unit (x--)
> - `'R'` moves right 1 unit (x++)
> - `'_'` is a wildcard — you choose any one of the four directions
>
> Return the **maximum Manhattan distance** `|x| + |y|` achievable after performing all moves optimally.

---

## 🧪 Examples
> [!example]
> **Input:** `moves = "L_D_"`
> **Output:** `4`
> **Explanation:** Replace the two `_`s with `'D'` and `'L'` respectively. Path reaches `(-2, -2)`, giving distance `2 + 2 = 4`.

> [!example]
> **Input:** `moves = "U_R"`
> **Output:** `3`
> **Explanation:** Replace `_` with `'U'`. Path reaches `(1, 2)`, giving distance `1 + 2 = 3`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= moves.length <= 10^5`
> - `moves` consists only of `'U'`, `'D'`, `'L'`, `'R'`, `'_'`

---

## 🔍 Intuition

Manhattan distance is `|x| + |y|`, and the two axes are **completely independent** — x and y don't interact in this formula at all. So I can think of it as two separate games: an x-game and a y-game, and I just add up however far I end in each. Fixed moves set a baseline `(x, y)` via straightforward coordinate tracking. For each `'_'`, the key insight is that it is **always worth exactly +1** to the total distance: I pick whichever axis I want and push it outward (same sign as the axis is already heading), which adds 1 to `|x|` or `|y|`. Crucially, adding +1 to `|x|` and adding +1 to `|y|` are worth identical amounts in the sum, so there's no smarter axis to pick — both choices are equivalent. This means I never need to simulate how to allocate underscores: just count them and add them on top of `|x| + |y|`.

> 🟢 *Math + Greedy (Axis Independence)*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Single-Pass Coordinate Accumulation

**Why this works:**
- `|x| + |y|` from fixed moves is the unambiguous baseline — U/D/L/R each shift exactly one coordinate by ±1
- Each `_` is worth exactly +1 regardless of which axis it's assigned to, because: (a) you always assign it outward (never against the axis direction, which would cancel), and (b) `|x|` and `|y|` are symmetric contributors to the sum
- No axis-assignment decision is needed — counting underscores and adding gives the exact optimal answer in O(n) with O(1) space

**Dry Run** (`moves = "L_D_"`):

| Step | char | x  | y  | `underscore` |
|------|------|----|----|--------------|
| 0    | `'L'`  | -1 | 0  | 0            |
| 1    | `'_'`  | -1 | 0  | 1            |
| 2    | `'D'`  | -1 | -1 | 1            |
| 3    | `'_'`  | -1 | -1 | 2            |
| —    | *end*  |    |    |              |

`|x| + |y| + underscores = 1 + 1 + 2 = 4` ✓

**Bad strategy (to show why):** Send the first `_` as `'U'` instead — it adds +1 to y, but then `'D'` removes it. Net effect: 0. You wasted the wildcard by sending it against the axis's outward direction.

```java
class Solution {
    public int maxDistance(String moves) {
        int x = 0, y = 0, underscore = 0;
        
        for (char c : moves.toCharArray()) {
            switch (c) {
                case 'U': y++; break;
                case 'D': y--; break;
                case 'L': x--; break;
                case 'R': x++; break;
                case '_': underscore++; break;
            }
        }
        
        return Math.abs(x) + Math.abs(y) + underscore;
    }
}
```

---

## 🔑 Key Insights
- The x-axis and y-axis are **fully decoupled** in `|x| + |y|` — adding 1 to `|x|` and adding 1 to `|y|` contribute identical value, so there's no "smarter" axis to assign a `_` to
- A `_` pushed outward (matching the axis direction) adds +1 to distance; pushed inward (against it), it cancels a prior move and contributes −1 — always push outward
- No intermediate state tracking is needed — only the final `(x, y)` after all fixed moves matters, not the path

---

## ⚠️ Pitfalls
> [!warning]
> - Thinking you need to track axis assignment or simulate each `_` individually — you don't; the independence of axes makes every `_` unconditionally worth +1
> - Sending a `_` against the axis's current direction (e.g., picking `'U'` when `y` is net-negative) — this cancels a unit of distance instead of adding one
> - Assuming wildcards need to be balanced between axes — they don't; stacking all underscores onto one axis gives the same total as splitting them evenly

---

## ⏱️ Complexity
- **Time:** `O(n)` — single pass over the `moves` string
- **Space:** `O(1)` — three integer accumulators only
