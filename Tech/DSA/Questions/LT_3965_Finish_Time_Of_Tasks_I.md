---
created: 2026-06-21 00:00
tags:
  - dsa
  - tree
  - dfs
  - recursion
source: https://leetcode.com/problems/finish-time-of-tasks-i/
problem_id: "3965"
difficulty: Medium
status: Solved
review_date:
---
# LT_3965 – Finish Time Of Tasks I

**Link:** [Open Problem](https://leetcode.com/problems/finish-time-of-tasks-i/)

---

## 📝 Problem Description
> [!info]
> You manage `n` tasks (numbered `0` to `n-1`) organized as a **tree rooted at task 0**. The array `edges` of length `n-1` defines parent-child relationships where `edges[i] = [u, v]` means task `u` is the parent of task `v`. Each task has a `baseTime[i]` representing its base completion duration.
>
> The **finish time** is defined recursively:
> - **Leaf task:** `finishTime = baseTime[i]`
> - **Non-leaf task:** Let `earliest` = min finish time among children, `latest` = max finish time among children.
>   - `ownDuration = (latest - earliest) + baseTime[i]`
>   - `finishTime = latest + ownDuration`
>
> Return the finish time of the root task `0`.

---

## 🧪 Examples
> [!example]
> **Input:** `n = 3, edges = [[0,1],[1,2]], baseTime = [9,5,3]`
> **Output:** `17`
> **Explanation:** Task 2 (leaf) → 3. Task 1 (one child, finish=3) → `ownDuration=(3-3)+5=5`, finish=8. Task 0 → `ownDuration=(8-8)+9=9`, finish=17.

> [!example]
> **Input:** `n = 3, edges = [[0,1],[0,2]], baseTime = [4,7,6]`
> **Output:** `12`
> **Explanation:** Task 1 (leaf) → 7. Task 2 (leaf) → 6. Task 0: `earliest=6, latest=7`, `ownDuration=(7-6)+4=5`, finish=12.

> [!example]
> **Input:** `n = 4, edges = [[0,1],[0,2],[2,3]], baseTime = [5,8,2,1]`
> **Output:** `18`
> **Explanation:** Task 3→1, Task 1→8, Task 2→3, Task 0: `earliest=3, latest=8`, `ownDuration=(8-3)+5=10`, finish=18.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= n <= 10^5`
> - `edges.length == n - 1`
> - Tree structure is valid (connected, acyclic)
> - `1 <= baseTime[i] <= 10^5`

---

## 🔍 Intuition

Each task's finish time depends entirely on its children's finish times — a textbook **post-order DFS**. I build a parent→child adjacency list from the edges, then DFS from the root. At a leaf, the answer is just `baseTime[node]` (no dependencies). At an internal node, I can't start my own work until every child has finished, so I'm forced to wait until `latest` anyway. But between when the *earliest* child finishes and when the *latest* child finishes, the node is sitting idle — that idle gap `(latest - earliest)` inflates the node's effective duration on top of its `baseTime`. The finish time is then `latest + ownDuration`, and this propagates naturally up the tree through the recursion.

> 🟢 *Post-order DFS on Tree*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Recursive Post-order DFS

**Why this works:**
- Post-order DFS ensures all children are resolved before a parent is computed — matches the dependency direction exactly
- The `(latest - earliest)` term captures the idle wait at a node between when its first and last child complete; this overhead is correctly baked into `ownDuration`
- When a node has only one child: `earliest == latest`, so `ownDuration = baseTime[node]` and `finishTime = latest + baseTime[node]` — the single-child case degenerates cleanly into "chain addition"

**Dry Run** (`n=4, edges=[[0,1],[0,2],[2,3]], baseTime=[5,8,2,1]`):

Tree structure:
```
      0 (base=5)
     / \
    1   2 (base=2)
 (b=8)  |
        3 (base=1)
```

| DFS call | Children finish times | earliest | latest | ownDuration | return |
|----------|-----------------------|----------|--------|-------------|--------|
| `dfs(3)` | leaf                  | —        | —      | —           | **1**  |
| `dfs(1)` | leaf                  | —        | —      | —           | **8**  |
| `dfs(2)` | [1]                   | 1        | 1      | (1-1)+2 = 2 | **3**  |
| `dfs(0)` | [8, 3]                | 3        | 8      | (8-3)+5 = 10| **18** |

Return **18** ✓

```java
class Solution {
    private List<List<Integer>> children;
    private int[] baseTime;

    public long finishTime(int n, int[][] edges, int[] baseTime) {
        this.baseTime = baseTime;
        children = new ArrayList<>();
        for (int i = 0; i < n; i++) children.add(new ArrayList<>());
        for (int[] e : edges) {
            children.get(e[0]).add(e[1]); // parent -> child
        }
  
        return dfs(0);
    }

    private long dfs(int node) {

        List<Integer> kids = children.get(node);
        if (kids.isEmpty()) {
            return baseTime[node]; // leaf case
        }
    
        long earliest = Long.MAX_VALUE, latest = Long.MIN_VALUE;
        for (int child : kids) {
            long childFinish = dfs(child);
            earliest = Math.min(earliest, childFinish);
            latest = Math.max(latest, childFinish);
        }
        long ownDuration = (latest - earliest) + baseTime[node];
        return latest + ownDuration;
    }
}
```

---

## 🔑 Key Insights
- `finishTime = latest + ownDuration = 2*latest - earliest + baseTime[node]` algebraically, but the split form `latest + (latest - earliest + baseTime)` is clearer: "wait till slowest child, then add own effective duration"
- The "idle wait" `(latest - earliest)` is not wasted from the problem's perspective — it's the unavoidable overhead of having children that finish at different times
- Single-child nodes behave like a simple chain: `earliest == latest` → `ownDuration = baseTime[node]` → `finishTime = childFinish + baseTime[node]`

---

## ⚠️ Pitfalls
> [!warning]
> - Using `int` instead of `long` for finish times — with `n` up to `10^5` and `baseTime[i]` up to `10^5`, a long chain can produce finish times up to `~10^10`, overflowing `int`
> - Building the adjacency list with `child → parent` direction — DFS from root 0 requires `parent → child` edges
> - Missing the leaf base case — without it, `earliest = Long.MAX_VALUE` and `latest = Long.MIN_VALUE` enter arithmetic and silently produce garbage results

---

## ⏱️ Complexity
- **Time:** `O(n)` — each node visited exactly once in the DFS
- **Space:** `O(n)` — adjacency list size `O(n)` + recursion stack `O(n)` in worst case (degenerate chain tree)
