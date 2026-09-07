---
created: 2026-09-05 00:00
tags:
  - dsa
  - graph
  - bfs
  - topological-sort
  - tree
source: https://leetcode.com/problems/minimum-height-trees/
problem_id: "310"
difficulty: Medium
status: Solved
review_date:
---
# LT_0310 – Minimum Height Trees

**Link:** [Open Problem](https://leetcode.com/problems/minimum-height-trees/)

---

## 📝 Problem Description
> [!info]
> A tree is an undirected graph in which any two vertices are connected by exactly one path. In other words, any connected graph without simple cycles is a tree.
>
> Given a tree of `n` nodes labelled from `0` to `n - 1`, and an array of `n - 1` edges where `edges[i] = [ai, bi]` indicates that there is an undirected edge between the two nodes `ai` and `bi` in the tree, you can choose any node of the tree as the root. When you select a node `x` as the root, the result tree has height `h`. Among all possible rooted trees, those with minimum height (i.e. `min(h)`) are called minimum height trees (MHTs).
>
> Return a list of all MHTs' root labels. You can return the answer in any order.
>
> The height of a rooted tree is the number of edges on the longest downward path between the root and a leaf.

---

## 🧪 Examples
> [!example]
> **Input:** `n = 4, edges = [[1,0],[1,2],[1,3]]`
> **Output:** `[1]`
> **Explanation:** As shown, the height of the tree is `1` when the root is the node with label `1`, which is the only MHT.

> [!example]
> **Input:** `n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]`
> **Output:** `[3,4]`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= n <= 2 * 10^4`
> - `edges.length == n - 1`
> - `0 <= ai, bi < n`
> - `ai != bi`
> - All the pairs `(ai, bi)` are distinct.
> - The given input is guaranteed to be a tree and there will be no repeated edges.

---

## 🔍 Intuition

The height of a rooted tree is minimized when the root sits as close as possible to every other node — i.e. the root should be a **centroid** of the tree. A tree can have at most two centroids: if it had three, removing every non-centroid node would leave a triangle among them, which is a cycle — impossible in a tree. So the answer set is always size 1 or 2. Instead of rooting the tree at every node and computing height (`O(n^2)`), I can find the centroid(s) directly by repeatedly stripping away the current leaves, layer by layer, like peeling an onion. Whatever is left when 1 or 2 nodes remain is the centroid set, since those nodes are the last to be "reached" by peeling from every direction simultaneously — exactly the topological-sort-style BFS used for course-scheduling problems, but run from the leaves inward instead of from in-degree-zero nodes outward.

> 🟢 *Topological Leaf Trimming (Centroid Finding)*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Centroid via BFS Leaf Trimming

**Why this works:**
- Leaves (degree-1 nodes) can never be part of the minimum-height root set — rooting at a leaf always maximizes height, so they are safe to peel off first.
- Removing a full layer of leaves is equivalent to shrinking the diameter of the tree by 1 from both ends simultaneously — after enough layers, only the tree's geometric center(s) remain.
- The process must stop at exactly 2 remaining nodes (not 0 or 1) because trimming one node past the center can wrongly discard the true centroid when `n` is even.

**Dry Run** (`n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]`):

| Step | State |
|---|---|
| Build `adj` | `0:[3]`, `1:[3]`, `2:[3]`, `3:[0,1,2,4]`, `4:[3,5]`, `5:[4]` |
| Initial leaves | `[0, 1, 2, 5]` (degree `1`) |
| `remainingNodes` | `6 - 4 = 2` → loop condition `remainingNodes > 2` is now false after this pass |
| Trim `0` | parent `3`, `adj[3] → [1,2,4]` (size `3`, not new leaf) |
| Trim `1` | parent `3`, `adj[3] → [2,4]` (size `2`, not new leaf) |
| Trim `2` | parent `3`, `adj[3] → [4]` (size `1` → `3` becomes new leaf) |
| Trim `5` | parent `4`, `adj[4] → [3]` (size `1` → `4` becomes new leaf) |
| `newOneDegree` | `[3, 4]` → loop exits (`remainingNodes == 2`) |
| Return | `[3, 4]` ✅ matches expected output |

```java
class Solution {
    public List<Integer> findMinHeightTrees(int n, int[][] edges) {
        List<Integer> centroids = new ArrayList<>();

        if (n < 2) {
           for (int i=0; i<n; i++) {
            centroids.add(i);
           }
            return centroids;
        }

        List<List<Integer>> adj = new ArrayList<>();
        for (int i=0; i<n; i++) adj.add(new ArrayList<>());

        for (int[] edge : edges) {
            int node1 = edge[0];
            int node2 = edge[1];

            adj.get(node1).add(node2);
            adj.get(node2).add(node1);
        }

        List<Integer> leavs = new ArrayList<>();
        for (int i=0; i<n; i++) {
            if (adj.get(i).size() == 1) leavs.add(i);
        }

        int remainingNodes = n;
        while (remainingNodes > 2) {
            remainingNodes -= leavs.size();            
            List<Integer> newOneDegree = new ArrayList<>();

            for (int leaf : leavs) {
                int parentNode = adj.get(leaf).iterator().next();
                adj.get(parentNode).remove(Integer.valueOf(leaf));
                if (adj.get(parentNode).size() == 1) {
                    newOneDegree.add(parentNode);
                }
            }

            leavs = newOneDegree;
        }

        return leavs;
    }
}
```

- **Time:** `O(V + E)` — each node enters the leaf queue exactly once, and each edge is inspected `O(1)` times overall · **Space:** `O(V + E)` for the adjacency list plus the leaf queues

---

## 🔑 Key Insights
- A tree has **at most 2 centroids** — this is a hard upper bound provable by contradiction (3+ centroids would form a cycle), so the loop only ever needs to stop at `remainingNodes <= 2`.
- Peeling leaves layer by layer is structurally identical to Kahn's topological sort (BFS on degree-1/in-degree-0 nodes) — just applied to an undirected tree instead of a DAG.
- `adj.get(parentNode).remove(Integer.valueOf(leaf))` is an `O(degree)` list removal, not `O(1)` — using a `Set<Integer>` per adjacency list (or tracking degree counts instead of mutating lists) avoids this if `n` is large, though it doesn't change the asymptotic bound here since each list shrinks as nodes are removed.
- The `n < 2` edge case (single node, no edges) must be handled separately since a lone node is trivially its own MHT root and the trimming loop would never execute correctly for it.

---

## ⚠️ Pitfalls
> [!warning]
> - Forgetting the `n < 2` special case — with `n = 1` there are no edges and every node already has degree `0`, not `1`, so the "initial leaves" step would find nothing.
> - Stopping the trim loop at `remainingNodes == 0` or `1` instead of `2` — over-trimming can eliminate a valid centroid when the tree has an even diameter.
> - Using `adj.get(parentNode).remove(leaf)` (the `int` overload, which removes by **index**) instead of `remove(Integer.valueOf(leaf))` (removes by **value**) — an easy `List.remove` ambiguity bug in Java.

---

## ⏱️ Complexity
- **Time:** `O(V + E)` = `O(n)` since `E = n - 1` for a tree
- **Space:** `O(V + E)` = `O(n)` for the adjacency list and leaf queues
