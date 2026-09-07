---
created: 2026-09-06 00:00
tags:
  - dsa
  - graph
  - shortest-path
  - dijkstra
  - heap-priority-queue
source: https://leetcode.com/problems/network-delay-time/
problem_id: "743"
difficulty: Medium
status: Solved
review_date:
---
# LT_0743 – Network Delay Time

**Link:** [Open Problem](https://leetcode.com/problems/network-delay-time/)

---

## 📝 Problem Description
> [!info]
> You are given a network of `n` nodes, labeled from `1` to `n`. You are also given `times`, a list of travel times as directed edges `times[i] = (ui, vi, wi)`, where `ui` is the source node, `vi` is the target node, and `wi` is the time it takes for a signal to travel from source to target.
>
> We will send a signal from a given node `k`. Return the minimum time it takes for all the `n` nodes to receive the signal. If it is impossible for all the `n` nodes to receive the signal, return `-1`.

---

## 🧪 Examples
> [!example]
> **Input:** `times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2`
> **Output:** `2`

> [!example]
> **Input:** `times = [[1,2,1]], n = 2, k = 1`
> **Output:** `1`

> [!example]
> **Input:** `times = [[1,2,1]], n = 2, k = 2`
> **Output:** `-1`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= k <= n <= 100`
> - `1 <= times.length <= 6000`
> - `times[i].length == 3`
> - `1 <= ui, vi <= n`
> - `ui != vi`
> - `0 <= wi <= 100`
> - All the pairs `(ui, vi)` are unique (no multiple edges)

---

## 🔍 Intuition

This is single-source shortest path on a directed, non-negatively-weighted graph — the textbook setup for Dijkstra's algorithm. The signal from `k` doesn't broadcast to every node simultaneously; it fans out along the cheapest known paths, and "time for all nodes to receive it" is just "the shortest distance to the *farthest* node." So the algorithm is: run Dijkstra from `k` to get `dist[]` to every other node, then the answer is `max(dist[])` — unless some node is unreachable, in which case it stays at infinity and the answer is `-1`. A min-heap keyed by current tentative distance guarantees that whenever a node is popped for the first time, that popped distance is already its true shortest distance (since all edge weights are `>= 0`, nothing cheaper can arrive later) — that's the core invariant that makes greedy relaxation valid here.

> 🟢 *Dijkstra's Algorithm — Single-Source Shortest Path*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Dijkstra (Lazy-Deletion Min-Heap)

**Why this works:**
- A `PriorityQueue` ordered by current tentative time always pops the globally-cheapest frontier node next, so relaxations happen in non-decreasing order of finalized distance — the correctness condition Dijkstra relies on for non-negative weights.
- `timesArr[]` doubles as both the "best distance so far" table and an implicit visited check: a node is only ever pushed to the queue again if a strictly shorter path to it was just found (`newTime < timesArr[nextNode]`), so stale/worse paths never get relaxed further.
- Taking `max` over `timesArr[1..n]` at the end directly answers "when has the *last* node received the signal," and any leftover `Integer.MAX_VALUE` means that node was never reached, so the answer is `-1`.

**Dry Run** (`times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2`):

| Step | Popped `(node, time)` | Relaxations | `timesArr[1..4]` |
|---|---|---|---|
| init | — | `timesArr[2] = 0`, queue = `{(2,0)}` | `[INF, INF, 0, INF]` |
| 1 | `(2, 0)` | `1`: `0+1=1 < INF` → push `(1,1)`; `3`: `0+1=1 < INF` → push `(3,1)` | `[1, INF, 0, 1]`... → `[1, 0, 1, INF]` (1-indexed: `timesArr[1]=1, timesArr[3]=1`) |
| 2 | `(1, 1)` | node `1` has no outgoing edges — nothing to relax | unchanged |
| 3 | `(3, 1)` | `4`: `1+1=2 < INF` → push `(4,2)` | `timesArr[4] = 2` |
| 4 | `(4, 2)` | node `4` has no outgoing edges — nothing to relax | unchanged |
| end | queue empty | `max(timesArr[1..4]) = max(1, 0, 1, 2) = 2` | **`2`** ✅ |

```java
class Solution {
    public int networkDelayTime(int[][] times, int n, int k) {
        List<List<int[]>> graph = new ArrayList<>();
        for (int i = 0; i <= n; i++) {
            graph.add(new ArrayList<>());
        }

        Set<Integer> nodesToConsider = new HashSet<>();
        for (int[] time : times) {
            graph.get(time[0]).add(new int[]{time[1], time[2]});
            nodesToConsider.add(time[0]);
            nodesToConsider.add(time[1]);
        }

        Queue<int[]> queue = new PriorityQueue<>((a,b) -> a[1]-b[1]);
        queue.add(new int[]{k,0});
        int[] timesArr = new int[n+1];
        Arrays.fill(timesArr, Integer.MAX_VALUE);
        timesArr[k] = 0;

        int ans = 0;   
        while(!queue.isEmpty()) {
            int[] a = queue.poll();
            int node = a[0]; // 2
            int time = a[1]; // 0

    
            for(int[] arr : graph.get(node)) {
                int nextNode = arr[0];
                int nextTime = arr[1];

                int newTime = time + nextTime;
                if(newTime<timesArr[nextNode]) {
                    timesArr[nextNode] = newTime;                                        
                    queue.add(new int[]{nextNode, newTime});                    
                }
            }            
        }

         
        for(int i=1; i<=n; i++) {
            int num = timesArr[i];
            if(num==Integer.MAX_VALUE) return -1;
            ans = Math.max(num, ans);
        }

        return ans;
    }
}
```

- **Time:** `O(E log E)` — with lazy deletion (no "already finalized, skip" check on pop), a node can be re-pushed up to once per incoming edge, so the heap holds up to `O(E)` entries, each `push`/`poll` costing `O(log E)` · **Space:** `O(V + E)` for the adjacency list plus `O(E)` for the heap in the worst case

---

## 🔑 Key Insights
- Non-negative weights are what let a min-heap greedily finalize distances in pop order — this exact approach breaks (needs Bellman-Ford) if any `wi` could be negative.
- The relaxation guard `newTime < timesArr[nextNode]` is doing double duty: it's both the standard Dijkstra relaxation check *and* the only thing preventing infinite re-processing of a node.
- `nodesToConsider` is built but never actually used to check reachability — the code instead relies on `timesArr[i] == Integer.MAX_VALUE` for nodes `1..n`, which is correct and simpler, but the unused set is dead code worth deleting.

---

## ⚠️ Pitfalls
> [!warning]
> - No `if (time > timesArr[node]) continue;` guard after popping means stale queue entries (superseded by a shorter path found later) still get fully re-relaxed — correct, but wasteful; a proper "skip if already finalized" check tightens this to closer to `O(E log V)`.
> - Forgetting the graph is **directed** — building an undirected adjacency list would let the signal "flow backward" and silently produce wrong (usually smaller) answers.
> - Off-by-one on the loop bound when scanning for unreached nodes: it must be `i <= n` (1-indexed nodes), not `i < n`, or node `n` never gets checked.

---

## ⏱️ Complexity
- **Time:** `O(E log E)`
- **Space:** `O(V + E)`
