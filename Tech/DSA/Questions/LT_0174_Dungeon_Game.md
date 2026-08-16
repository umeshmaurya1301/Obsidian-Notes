---
created: 2026-08-10 10:50
tags:
  - dsa
  - dynamic-programming
  - tabulation
  - grid-dp
  - matrix
source: https://leetcode.com/problems/dungeon-game/description/
problem_id: "174"
difficulty: Hard
status: Solved
review_date:
---
# LT_0174 – Dungeon Game

**Link:** [Open Problem](https://leetcode.com/problems/dungeon-game/description/)

---

## 📝 Problem Description
> [!info]
> The demons had captured the princess and imprisoned her in the bottom-right corner of a dungeon. The dungeon consists of `m x n` rooms laid out in a 2D grid. Our valiant knight was initially positioned in the top-left room and must fight his way through the dungeon to rescue the princess.
>
> The knight has an initial health point represented by a positive integer. If at any point his health point drops to `0` or below, he dies immediately.
>
> Some of the rooms are guarded by demons (negative integers), so the knight **loses** health upon entering these rooms; other rooms are either empty (`0`) or contain magic orbs that **increase** the knight's health (positive integers).
>
> To reach the princess as quickly as possible, the knight decides to move only **rightward or downward** in each step.
>
> Return the knight's **minimum initial health** so that he can rescue the princess.
>
> Note that any room can contain threats or power-ups, even the first room the knight enters and the bottom-right room where the princess is imprisoned.

---

## 🧪 Examples
> [!example]
> **Input:** `dungeon = [[-2,-3,3],[-5,-10,1],[10,30,-5]]`
> **Output:** `7`
> **Explanation:** The initial health of the knight must be at least 7 if he follows the optimal path: `RIGHT -> RIGHT -> DOWN -> DOWN`.

> [!example]
> **Input:** `dungeon = [[0]]`
> **Output:** `1`

---

## ⚠️ Constraints
> [!warning]
> - `m == dungeon.length`
> - `n == dungeon[i].length`
> - `1 <= m, n <= 200`
> - `-1000 <= dungeon[i][j] <= 1000`

---

## 🔍 Intuition

My first instinct — walk forward from `(0,0)` maximising accumulated health — is **wrong**, and understanding *why* is the entire problem. Health is not a quantity you can bank freely: a path that ends up with more total health may still have dipped to `0` somewhere in the middle and killed the knight. Two things matter at once (current health *and* the worst dip still ahead), and a forward DP can't collapse them into one number.

So I flip the direction. Define `memo[i][j]` = **the minimum health the knight must have the moment he enters room `(i,j)`** in order to survive from there to the princess. Now the state is self-contained: it only depends on what lies ahead, which is exactly what the recurrence gives me. Standing at `(i,j)`, I'll step into the cheaper of the two rooms ahead, so I need `min(memo[i+1][j], memo[i][j+1])` on arrival there; entering `(i,j)` costs me `dungeon[i][j]`, so I need `min(...) - dungeon[i][j]` before that. And since health must stay **strictly positive**, the requirement never drops below `1` — hence `max(1, ...)`.

That `max(1, ...)` is the second half of the insight: it's what stops a huge magic orb from letting the knight "carry a negative health debt" into the room. Filling backwards from the bottom-right, `memo[0][0]` is the answer.

> 🟢 *Backward Grid DP — carry the requirement, not the accumulation*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Backward Tabulation on Minimum Entry Health

**Why this works:**
- **Backwards makes the state Markovian.** "How much health do I need *from here on*" depends only on the sub-grid below-and-right of `(i,j)`. "How much health do I *have*" would depend on the whole prefix — two variables, no clean DP.
- **`max(1, ...)` enforces the survival floor at every cell**, not just at the end. It is the reason a `+1000` orb can't cancel a lethal dip that happens before it.
- **The base cell is seeded from the princess's room.** `memo[m-1][n-1] = 1 - min(0, dungeon[m-1][n-1])`, written here as an `if`: a demon there needs `|value| + 1`, anything else needs `1`.
- **The last row and last column have only one way out** (right-only / down-only respectively), so they're seeded with their own single-successor loops before the interior sweep.

**Dry Run** (`dungeon = [[-2,-3,3],[-5,-10,1],[10,30,-5]]`):

Seed the corner: `dungeon[2][2] = -5` → `memo[2][2] = 5 + 1 = 6`.

Last row (only rightward moves):

| cell | `dungeon` | successor need | `memo` |
|---|---|---|---|
| `(2,1)` | `30` | `6` | `30 >= 6` → `1` |
| `(2,0)` | `10` | `1` | `10 >= 1` → `1` |

Last column (only downward moves):

| cell | `dungeon` | successor need | `memo` |
|---|---|---|---|
| `(1,2)` | `1` | `6` | `6 - 1 = 5` |
| `(0,2)` | `3` | `5` | `5 - 3 = 2` |

Interior, sweeping up-left with `max(1, min(down, right) - dungeon)`:

| cell | `down` | `right` | `min` | `dungeon` | `memo` |
|---|---|---|---|---|---|
| `(1,1)` | `1` | `5` | `1` | `-10` | `max(1, 11) = 11` |
| `(1,0)` | `1` | `11` | `1` | `-5` | `max(1, 6) = 6` |
| `(0,1)` | `11` | `2` | `2` | `-3` | `max(1, 5) = 5` |
| `(0,0)` | `6` | `5` | `5` | `-2` | `max(1, 7) = **7**` |

Final table:
```
 7   5   2
 6  11   5
 1   1   6
```
`memo[0][0] = 7` ✅ — and tracing the smaller successor at each step reproduces `RIGHT -> RIGHT -> DOWN -> DOWN`.

```java
class Solution {
    public int calculateMinimumHP(int[][] dungeon) {
        int m = dungeon.length;
        int n = dungeon[0].length;

        int[][] memo = new int[m][n];
        int lastVal = dungeon[m-1][n-1];
        if (lastVal<0) {
            memo[m-1][n-1] = -1 * lastVal + 1;
        } else {
            memo[m-1][n-1] = 1;
        }

        for (int i=n-2; i>=0; i--) {
            if (dungeon[m-1][i] >= memo[m-1][i+1]) {
                memo[m-1][i] = 1;
            } else {
                memo[m-1][i] = memo[m-1][i+1] - dungeon[m-1][i];
            }
        }

        for (int i=m-2; i>=0; i--) {
            if (dungeon[i][n-1] >= memo[i+1][n-1]) {
                memo[i][n-1] = 1;
            } else {
                memo[i][n-1] = memo[i+1][n-1] - dungeon[i][n-1];
            }
        }

        for (int i=m-2; i>=0; i--) {
            for (int j=n-2; j>=0; j--) {
                int val = Math.min (memo[i+1][j], memo[i][j+1]);
                memo[i][j] = Math.max(1, val - dungeon[i][j]);
            }
        }

        System.out.println(Arrays.deepToString(memo));
        return memo[0][0];
    }
}
```

- **Time:** `O(m·n)` · **Space:** `O(m·n)`

---

## 🔑 Key Insights
- **Direction is the algorithm.** Forward DP fails because survival is a *path-wide minimum constraint*, not an endpoint value. Backward DP turns it into a per-cell requirement that composes.
- **`max(1, need - value)` is the whole recurrence.** `need - value` is "what I must bring so that after this room's effect I still have `need`"; `max(1, …)` clamps it because health `<= 0` is death, not debt.
- **The `if/else` in the border loops *is* `max(1, …)`.** `dungeon[..] >= memo[..]` → the room's gain fully covers the successor's requirement → `1` suffices. Recognising that collapses three code shapes into one formula.
- **A related family:** compare with [[LT_0064_Minimum_Path_Sum]] (pure additive, forward or backward both fine) — the moment a *floor constraint* enters, only backward works.

---

## ⚠️ Pitfalls
> [!warning]
> - The first border loop uses `i` as a **column** index (`dungeon[m-1][i]`) while the second uses it as a **row** index. Correct, but confusing on re-read — rename to `j` when writing it fresh.
> - Health must stay **strictly greater than 0**, so a demon of `-5` in the final room needs `6`, not `5`. Off-by-one here is the classic wrong answer.
> - Never clamp intermediate *accumulated* health to `0`; the DP tracks a requirement, and clamping it below `1` silently allows death.
> - `System.out.println(Arrays.deepToString(memo))` is left-over debug output — strip it before submitting.

---

## ⏱️ Complexity
- **Time:** `O(m·n)`
- **Space:** `O(m·n)` — reducible to `O(n)` with a single rolling row
