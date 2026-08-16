---
created: 2026-08-16 12:00
tags:
  - dsa
  - matrix
  - heap
  - priority-queue
  - bfs
source: https://leetcode.com/problems/trapping-rain-water-ii/
problem_id: "407"
difficulty: Hard
status: Solved
review_date:
---
# LT_0407 – Trapping Rain Water II

**Link:** [Open Problem](https://leetcode.com/problems/trapping-rain-water-ii/)

---

## 📝 Problem Description
> [!info]
> Given an `m x n` integer matrix `heightMap` representing the height of each unit cell in a 2D elevation map, return the volume of water it can trap after raining.

---

## 🧪 Examples
> [!example]
> **Input:** `heightMap = [[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]]`
> **Output:** `4`
> **Explanation:** After the rain, water is trapped between the blocks. There are two small ponds — 1 and 3 units trapped. Total volume trapped is 4.

> [!example]
> **Input:** `heightMap = [[3,3,3,3,3],[3,2,2,2,3],[3,2,1,2,3],[3,2,2,2,3],[3,3,3,3,3]]`
> **Output:** `10`

---

## ⚠️ Constraints
> [!warning]
> - `m == heightMap.length`
> - `n == heightMap[i].length`
> - `1 <= m, n <= 200`
> - `0 <= heightMap[i][j] <= 2 * 10^4`

---

## 🔍 Intuition

The 1D "Trapping Rain Water" trick (water level at a cell = `min(maxLeft, maxRight)`) doesn't generalize directly to 2D, because there's no single "left" and "right" anymore — water can be blocked by *any* surrounding wall, in any direction. The fix is to flip the direction of reasoning: instead of asking "what walls surround this cell," start from the **outer boundary** (which can never hold water — it always drains off the edge of the grid) and flood inward, always expanding through the *currently lowest known wall* first. That's exactly what a min-heap gives you: push every boundary cell in, and repeatedly pop the globally smallest height, because that's the weakest point the water could escape through, and everything reachable from it is bounded by at least that height.

As the flood expands, `maxValue` tracks the highest wall height seen *so far along the current expansion frontier* — effectively "the water level being maintained while walking inward." For each newly visited neighbor, if its ground is lower than `maxValue`, water sits on it up to that level (`maxValue - currentHeight`); if it's taller, it becomes part of the new boundary instead, and no water is trapped there. Critically, once a cell is processed, its *effective* height going forward is `max(currentHeight, maxValue)` — because a low cell that just got flooded now behaves like a wall of height `maxValue` for everything beyond it, not its original ground height. This is a min-heap variant of Dijkstra: expanding the smallest known "barrier" first guarantees that by the time a cell is popped, `maxValue` is the true minimum possible water ceiling for it — never revisited, never recomputed.

> 🟢 *Flood from the Boundary Inward via Min-Heap (Dijkstra-style Water Level)*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Min-Heap BFS from the Boundary

**Why this works:**
- The boundary can never trap water (it always has an escape route off the grid edge), so it's the only safe, correct starting frontier — everything else must be reasoned about relative to it.
- Always popping the **smallest** height from the heap first (not just any order) guarantees that when a cell is processed, every path that could have offered a *lower* ceiling has already been considered — so `maxValue` at that point is provably the true trapped-water level for that cell, matching Dijkstra's greedy-relaxation guarantee.
- Pushing `Math.max(currentHeight, maxValue)` — not the cell's raw height — propagates the *effective* wall height outward: once a low cell is flooded, it behaves as a wall of height `maxValue` to everything beyond it, so the water level can never incorrectly "drop" as the flood spreads inward.

**Dry Run** (small `3x3` corner of Example 2's pattern, `[[3,3,3],[3,2,2],[3,2,1]]` conceptually — tracing the outer-ring-then-inward expansion):

| popped `(h,i,j)` | `maxValue` | neighbor checked | `currentHeight < maxValue`? | water added | pushed as |
|---|---|---|---|---|---|
| boundary cells (all `3`s) seeded first, `maxValue` starts at `3` after first pop | `3` | inner `2` at `(1,1)` | `2 < 3` → yes | `+1` | `Entry(max(2,3)=3, 1,1)` |
| `(3,1,1)` popped next | `3` | inner `1` at `(2,2)` | `1 < 3` → yes | `+2` | `Entry(max(1,3)=3, 2,2)` |

Total for this pocket: `1 + 2 = 3` — matches the "small pond" pattern the real Example 2 grid produces around its center (full grid gives `10` across all four interior cells).

```java
class Solution {
    private class Entry {
        int h, i, j;

        Entry(int h, int i, int j) {
            this.h = h;
            this.i = i;
            this.j = j;
        }
    }

    public int trapRainWater(int[][] heightMap) {
        int rows = heightMap.length;
        int cols = heightMap[0].length;
        PriorityQueue<Entry> queue = new PriorityQueue<>((a, b) -> a.h - b.h);
        boolean[][] visited = new boolean[rows][cols];
        int[][] directions = {
            {0, -1}, {0, 1}, {-1, 0}, {1, 0}
        };

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (isOnBoundary(i, j, rows, cols)) {
                    queue.offer(new Entry(heightMap[i][j], i, j));
                    visited[i][j] = true;
                }
            }
        }

        int maxValue = 0;
        int trapWater = 0;

        while (!queue.isEmpty()) {
            Entry entry = queue.poll();
            maxValue = Math.max(maxValue, entry.h);

            for (int[] dir : directions) {
                int newX = entry.i + dir[0];
                int newY = entry.j + dir[1];

                if (isValid(newX, newY, rows, cols) && !visited[newX][newY]) {
                    visited[newX][newY] = true;
                    int currentHeight = heightMap[newX][newY];
                    if (currentHeight < maxValue) {
                        trapWater += (maxValue - currentHeight);
                    } 

                    queue.offer(new Entry(Math.max(currentHeight, maxValue), newX, newY));
                }
            }
        }

        return trapWater;
    }

    private boolean isValid(int x, int y, int rows, int cols) {
        return x >= 0 && y >= 0 && x < rows && y < cols;
    }

    private boolean isOnBoundary(int i, int j, int rows, int cols) {
        return i == 0 || j == 0 || i == rows - 1 || j == cols - 1;
    }
}
```

- **Time:** `O(m * n * log(m * n))` — every cell is pushed/popped from the heap once, each heap operation costs `O(log(m*n))` · **Space:** `O(m * n)` for the heap, `visited` array, and boundary seeding

---

## 🔑 Key Insights
- The boundary is the only starting frontier that's *provably* free of trapped water — every interior cell's water level must be derived relative to it, never assumed independently.
- Popping the heap's minimum first (not BFS in insertion order, not DFS) is what makes this correct: it's a min-heap variant of Dijkstra, where "distance" is replaced by "the lowest wall height encountered on the way in."
- The condition is strictly `currentHeight < maxValue` (not `>`) — water only sits where the ground is *lower* than the current flood level; a taller cell simply raises the frontier's effective wall height instead.
- Pushing `Math.max(currentHeight, maxValue)` instead of the raw `currentHeight` is the line that makes the whole algorithm correct — it encodes "this cell, once flooded, now acts as a wall at the water's level" for every future neighbor exploration.
- An equivalent, arguably clearer formulation skips the global `maxValue` entirely and instead carries the boundary level directly on each popped entry: `water += Math.max(0, entry.h - neighborHeight)`, then pushes `Math.max(entry.h, neighborHeight)` — same idea, no shared mutable state.

---

## ⚠️ Pitfalls
> [!warning]
> - Using `currentHeight > maxValue` instead of `< maxValue` — water can never sit on a cell *taller* than the current flood level; that branch should instead just raise the effective wall height via the `Math.max` push, not add water.
> - Pushing the neighbor's raw `currentHeight` instead of `Math.max(currentHeight, maxValue)` — this "forgets" that a flooded low cell now behaves as a wall, and lets later cells incorrectly see a lower boundary than actually exists.
> - Trying to reuse the 1D two-pointer trick (`maxLeft`/`maxRight`) directly — 2D has no single left/right axis; water can be blocked from any of 4 directions, which is exactly why this needs a boundary-inward heap expansion instead.
> - Forgetting to mark boundary cells `visited` *before* the main loop — without it, the algorithm could revisit and double-count boundary cells once expansion reaches them from the interior side.

---

## ⏱️ Complexity
- **Time:** `O(m * n * log(m * n))`
- **Space:** `O(m * n)`
