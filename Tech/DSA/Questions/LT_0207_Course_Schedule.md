---
created: 2026-08-30 00:00
tags:
  - dsa
  - graph
  - topological-sort
source: https://leetcode.com/problems/course-schedule/
problem_id: "207"
difficulty: Medium
status: Solved
review_date:
---
# LT_0207 – Course Schedule

**Link:** [Open Problem](https://leetcode.com/problems/course-schedule/)

---

## 📝 Problem Description
> [!info]
> There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates that you must take course `bi` first if you want to take course `ai`.
>
> For example, the pair `[0, 1]` indicates that to take course `0` you have to first take course `1`.
>
> Return `true` if you can finish all courses. Otherwise, return `false`.

---

## 🧪 Examples
> [!example]
> **Input:** `numCourses = 2, prerequisites = [[1,0]]`
> **Output:** `true`
> **Explanation:** There are a total of 2 courses to take. To take course 1 you should have finished course 0. So it is possible.

> [!example]
> **Input:** `numCourses = 2, prerequisites = [[1,0],[0,1]]`
> **Output:** `false`
> **Explanation:** There are a total of 2 courses to take. To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= numCourses <= 2000`
> - `0 <= prerequisites.length <= 5000`
> - `prerequisites[i].length == 2`
> - `0 <= ai, bi < numCourses`
> - All the pairs `prerequisites[i]` are unique.

---

## 🔍 Intuition

This is cycle detection dressed up as a scheduling problem. Model each course as a node and each prerequisite pair `[a, b]` as a directed edge `b → a` ("finish `b`, then you can take `a`"). All courses can be finished **iff the graph has no cycle** — a cycle means a group of courses that all depend on each other, so none of them can ever be the "first" one taken. Kahn's algorithm makes this concrete: repeatedly peel off nodes with `inDegree == 0` (courses with no unmet prerequisites); if every node eventually gets peeled off, there's no cycle. The DFS approach detects the same thing directly by tracking `onPath` — if a DFS revisits a node that's still on the current recursion stack, that's a back-edge, i.e. a cycle.

> 🟢 *Topological Sort (Cycle Detection in Directed Graph)*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Kahn's Algorithm (BFS Topological Sort)

**Why this works:**
- A valid topological order exists **iff** the graph is a DAG (no cycle).
- Nodes with `inDegree == 0` have no unresolved prerequisites, so they're always safe to "take" next.
- If the graph has a cycle, every node inside that cycle will always have `inDegree > 0`, so it can never enter the queue — `topoList.size()` ends up short of `numCourses`, catching the cycle without ever explicitly looking for one.

**Dry Run** (`numCourses = 2, prerequisites = [[1,0]]`):
```
Build graph: v1=1, v2=0  →  list[0] = [1],  inDegree[1] = 1,  inDegree = [0, 1]

Seed queue with inDegree==0 nodes: queue = [0]

poll 0 → topoList = [0]
  neighbor 1: inDegree[1]-- → 0  → queue = [1]

poll 1 → topoList = [0, 1]
  no neighbors

queue empty. topoList.size() == 2 == numCourses → return true
```

```java
class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        List<List<Integer>> list = new ArrayList<>();

        for(int i=0; i<numCourses; i++) {
            list.add(new ArrayList<>());
        }

        int[] inDegree = new int[numCourses];
        for(int i=0; i<prerequisites.length; i++) {
            int[] arr = prerequisites[i];
            int v1 = arr[0];
            int v2 = arr[1];
            list.get(v2).add(v1);

            inDegree[v1]++;
        }

        Queue<Integer> queue = new LinkedList<>();
        for(int i=0; i<numCourses; i++) {
            if(inDegree[i]==0) {
                queue.add(i);
            }
        }

        List<Integer> topoList = new ArrayList<>();

        while(!queue.isEmpty()) {
            int node = queue.poll();
            topoList.add(node);

            for(int num : list.get(node)) {
                inDegree[num]--;
                if(inDegree[num]==0) {
                    queue.add(num);
                }
            }
        }

        if(topoList.size()==numCourses) return true;
        return false;

    }
}
```

- **Time:** `O(V + E)` · **Space:** `O(V + E)`

### ✅ Solution 2 — DFS Cycle Detection

**Why this works:**
- `visited[]` prevents redoing work on nodes already fully explored.
- `onPath[]` marks nodes currently on the active recursion stack — hitting a neighbor that's still `onPath` means we've looped back onto ourselves, i.e. a cycle.
- Clearing `onPath[node] = false` on backtrack is what distinguishes "already fully processed, safe" (`visited` but not `onPath`) from "currently being processed, dangerous" (`visited` and `onPath`).

**Dry Run** (`numCourses = 2, prerequisites = [[1,0]]`):
```
Build graph: list[0] = [1],  list[1] = []

i=0: not visited → hasCycle(0)
  visited[0]=true, onPath[0]=true
  neighbor 1: not visited → hasCycle(1)
    visited[1]=true, onPath[1]=true
    no neighbors
    onPath[1]=false, return false
  onPath[0]=false, return false

i=1: already visited → skip

No cycle found → return true
```

```java
class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        List<List<Integer>> list = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) {
            list.add(new ArrayList<>());
        }

        for (int[] arr : prerequisites) {
            int v1 = arr[0];
            int v2 = arr[1];
            list.get(v2).add(v1);
        }

        boolean[] visited = new boolean[numCourses];
        boolean[] onPath = new boolean[numCourses]; // to detect cycle

        for (int i = 0; i < numCourses; i++) {
            if (!visited[i]) {
                if (hasCycle(i, list, visited, onPath)) {
                    return false; // cycle detected
                }
            }
        }

        return true;
    }

    private boolean hasCycle(int node, List<List<Integer>> graph, boolean[] visited, boolean[] onPath) {
        visited[node] = true;
        onPath[node] = true;

        for (int neighbor : graph.get(node)) {
            if (!visited[neighbor]) {
                if (hasCycle(neighbor, graph, visited, onPath)) {
                    return true;
                }
            } else if (onPath[neighbor]) {
                // Cycle detected
                return true;
            }
        }

        onPath[node] = false; // backtrack
        return false;
    }
}
```

- **Time:** `O(V + E)` · **Space:** `O(V + E)` (graph) `+ O(V)` (recursion stack)

---

## 🔑 Key Insights
- "Can finish all courses" is exactly "does this directed graph have a cycle" — reframe scheduling problems as graph problems the moment you see "must do X before Y".
- Edge direction matters: `prerequisites[i] = [a, b]` means `b → a`, not `a → b`. Getting this backwards silently breaks the cycle detection.
- Kahn's `inDegree` count and DFS's `onPath` flag are two different lenses on the same fact — a node stuck with unresolved dependencies (BFS) is the same thing as a node revisited while still active on the call stack (DFS).

---

## ⚠️ Pitfalls
> [!warning]
> - Building the adjacency list with the edge direction reversed (`list.get(v1).add(v2)` instead of `list.get(v2).add(v1)`) — always double check which one is the "prerequisite" node.
> - In the DFS version, forgetting to reset `onPath[node] = false` on backtrack turns it into a plain `visited` check and produces false-positive cycles.
> - `prerequisites.length` can be `0` — both solutions must handle "every course is independently takable" correctly (they do, since disconnected nodes are trivially fine).

---

## ⏱️ Complexity
- **Time:** `O(V + E)` where `V = numCourses`, `E = prerequisites.length`
- **Space:** `O(V + E)`
