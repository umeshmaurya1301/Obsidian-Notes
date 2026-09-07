---
created: 2026-09-06 00:00
tags:
  - dsa
  - graph
  - dfs
  - backtracking
source: https://leetcode.com/problems/all-paths-from-source-to-target/
problem_id: "797"
difficulty: Medium
status: Solved
review_date:
---
# LT_0797 – All Paths From Source to Target

**Link:** [Open Problem](https://leetcode.com/problems/all-paths-from-source-to-target/)

---

## 📝 Problem Description
> [!info]
> Given a directed acyclic graph (DAG) of `n` nodes labeled from `0` to `n - 1`, find all possible paths from node `0` to node `n - 1` and return them in any order.
>
> The graph is given as follows: `graph[i]` is a list of all nodes you can visit from node `i` (i.e., there is a directed edge from node `i` to node `graph[i][j]`).

---

## 🧪 Examples
> [!example]
> **Input:** `graph = [[1,2],[3],[3],[]]`
> **Output:** `[[0,1,3],[0,2,3]]`
> **Explanation:** There are two paths: `0 -> 1 -> 3` and `0 -> 2 -> 3`.

> [!example]
> **Input:** `graph = [[4,3,1],[3,2,4],[3],[4],[]]`
> **Output:** `[[0,4],[0,3,4],[0,1,3,4],[0,1,2,3,4],[0,1,4]]`

---

## ⚠️ Constraints
> [!warning]
> - `n == graph.length`
> - `2 <= n <= 15`
> - `0 <= graph[i][j] < n`
> - `graph[i][j] != i` (no self-loops)
> - All the elements of `graph[i]` are unique
> - The input graph is guaranteed to be a DAG

---

## 🔍 Intuition

This is plain path-enumeration DFS with backtracking, made simpler than the usual grid/graph traversal because the input is *guaranteed* to be a DAG — no cycles means no `visited` set is ever needed, since the recursion can never loop back on itself. The trick is just to treat `path` as a single mutable buffer: append the current node before recursing, and remove it right after returning, so every recursive branch sees a clean prefix to build on. Whenever the current node equals `n - 1` (the target), the buffer *is* a complete valid path, so a defensive copy gets pushed into the answer — copying is essential since `path` keeps getting mutated as the DFS backtracks through other branches. Because a DAG can fan out and rejoin (see Example 2, where multiple paths reach node `4` via different routes), the number of valid paths can blow up combinatorially, which is exactly why this is inherently exponential rather than something a shortest-path algorithm could shortcut.

> 🟢 *DFS + Backtracking on a DAG*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — DFS + Backtracking

**Why this works:**
- No cycles are possible (guaranteed DAG), so plain DFS recursion always terminates — no `visited` array needed to guard against infinite loops.
- `path` is shared, mutated in place, and restored via `path.remove(path.size() - 1)` after each recursive call, so backtracking correctly re-uses the buffer across sibling branches instead of allocating a new list per branch.
- The base case `node == adj.size() - 1` fires exactly when the just-appended node is the target, at which point `new ArrayList<>(path)` snapshots the current path before it gets mutated further.

**Dry Run** (`graph = [[1,2],[3],[3],[]]`):

| Call | `path` before | Action | `path` after / result |
|---|---|---|---|
| `dfs(0)` | `[0]` | loop `n=1`: `path.add(1)` | `[0,1]` |
| `dfs(1)` | `[0,1]` | loop `n=3`: `path.add(3)` | `[0,1,3]` |
| `dfs(3)` | `[0,1,3]` | `node==3==adj.size()-1` → save | `ans = [[0,1,3]]`, then backtrack: `path.remove()` → `[0,1]` |
| back in `dfs(1)` | `[0,1]` | loop ends → backtrack | `path.remove()` → `[0]` |
| back in `dfs(0)` | `[0]` | loop `n=2`: `path.add(2)` | `[0,2]` |
| `dfs(2)` | `[0,2]` | loop `n=3`: `path.add(3)` | `[0,2,3]` |
| `dfs(3)` | `[0,2,3]` | `node==3` → save | `ans = [[0,1,3],[0,2,3]]`, backtrack → `[0,2]` → `[0]` |

```java
class Solution {
    public List<List<Integer>> allPathsSourceTarget(int[][] graph) {
        int len = graph.length;
        List<List<Integer>> adj = new ArrayList<>();
        for (int i=0; i<len; i++) adj.add(new ArrayList<>());

        for (int i=0; i<len; i++) {
            int[] a = graph[i];
            for (int n : a) adj.get(i).add(n);
        }

        List<List<Integer>> ans = new ArrayList<>();
        List<Integer> path = new ArrayList<>();
        path.add(0);
        dfs (ans, adj, path, 0);
        return ans;
    }

    private void dfs (List<List<Integer>> ans, List<List<Integer>> adj, List<Integer> path, int node) {
        if (node==adj.size()-1) {
            ans.add(new ArrayList<>(path));
            return;
        }

        for (int n : adj.get(node)) {
            path.add(n);
            dfs(ans, adj, path, n);
            path.remove(path.size() - 1);
        }
    }
}
```

- **Time:** `O(2^n * n)` — in the worst-case fan-out DAG, the number of source-to-target paths is exponential in `n`, and each found path costs `O(n)` to copy into `ans` · **Space:** `O(2^n * n)` for the output, plus `O(n)` recursion depth / `path` buffer

---

## 🔑 Key Insights
- `graph[i]` *is already* the adjacency list — building a separate `adj` copy first is redundant work; recursing directly on `graph[node]` would skip that `O(V + E)` copy entirely.
- The "no cycles" guarantee is what makes this problem tractable without a `visited` set — it's the reason a DAG-path-enumeration problem is easier than the general graph version.
- `ans.add(new ArrayList<>(path))` must be a copy, not `ans.add(path)` — since `path` is the same mutable list reused across the whole DFS, storing a live reference would leave every saved path pointing at whatever `path` ends up containing after the DFS finishes (effectively all empty or partial).

---

## ⚠️ Pitfalls
> [!warning]
> - Skipping `path.remove(path.size() - 1)` after the recursive call breaks backtracking — later sibling branches would silently inherit nodes from an unrelated earlier branch.
> - Forgetting the defensive copy at the base case (`new ArrayList<>(path)`) means every entry in `ans` aliases the same list, corrupting all previously saved paths as `path` keeps mutating.
> - Assuming this scales linearly: with `n` up to `15`, a densely-connected DAG can still produce up to `2^13` paths, so this only stays fast because the constraint caps `n` deliberately low.

---

## ⏱️ Complexity
- **Time:** `O(2^n * n)`
- **Space:** `O(2^n * n)`
