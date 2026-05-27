---
created: 2026-05-27 00:00
tags:
  - dsa
  - hash-table
  - linked-list
  - design
  - doubly-linked-list
source: https://leetcode.com/problems/lru-cache/
problem_id: "146"
difficulty: Medium
status: Solved
review_date:
---
# LT_0146 – LRU Cache

**Link:** [Open Problem](https://leetcode.com/problems/lru-cache/)

---

## 📝 Problem Description
> [!info]
> Design a data structure that follows the constraints of a **Least Recently Used (LRU) cache**.
>
> Implement the `LRUCache` class:
> - `LRUCache(int capacity)` — initialise the cache with positive size `capacity`.
> - `int get(int key)` — return the value of `key` if it exists, otherwise return `-1`.
> - `void put(int key, int value)` — update the value if `key` exists; otherwise insert the pair. If the cache exceeds `capacity`, evict the **least recently used** key.
>
> Both `get` and `put` must run in **O(1) average time complexity**.

---

## 🧪 Examples
> [!example]
> **Input:**
> ```
> ["LRUCache","put","put","get","put","get","put","get","get","get"]
> [[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]
> ```
> **Output:** `[null, null, null, 1, null, -1, null, -1, 3, 4]`
>
> **Explanation:**
> ```
> LRUCache(2)  → cache: {}
> put(1, 1)    → cache: {1=1}
> put(2, 2)    → cache: {1=1, 2=2}
> get(1)       → 1        (1 promoted to MRU; cache: {2=2, 1=1})
> put(3, 3)    → evicts 2 (LRU); cache: {1=1, 3=3}
> get(2)       → -1       (evicted)
> put(4, 4)    → evicts 1 (LRU); cache: {3=3, 4=4}
> get(1)       → -1       (evicted)
> get(3)       → 3
> get(4)       → 4
> ```

---

## ⚠️ Constraints
> [!warning]
> - `1 <= capacity <= 3000`
> - `0 <= key <= 10^4`
> - `0 <= value <= 10^5`
> - At most `10^4` calls will be made to `get` and `put`.

---

## 🔍 Intuition

The two O(1) requirements point directly to two data structures working together: a `HashMap` for O(1) key → node lookup, and a **Doubly Linked List (DLL)** for O(1) insertion and removal of arbitrary nodes. A singly linked list can't remove in O(1) because you can't reach the predecessor without traversal — the `prev` pointer is essential. The list is ordered by recency: the **most recently used (MRU)** node lives right after a dummy `head`, and the **least recently used (LRU)** lives right before a dummy `tail`. Every `get` and `put` moves the touched node to the MRU position via `remove` + `insert`; eviction always pulls from `tail.prev`. The sentinel head/tail nodes eliminate null-checks for every edge case — there is no concept of an "empty" list from the operation's perspective.

> 🟢 *HashMap + Doubly Linked List (Sentinel Pattern)*

---

## 🧠 Evolution of Solutions

### ✅ Solution — HashMap + Doubly Linked List

**Why this works:**
- `HashMap<key, Node>` gives O(1) node lookup; the DLL gives O(1) remove/insert since each `Node` holds `prev` and `next` directly — no traversal needed.
- The list maintains recency order implicitly: `insert` always places a node at `head.next` (MRU slot), so `tail.prev` is always the LRU candidate ready for eviction.
- Sentinel `head` and `tail` mean `remove()` and `insert()` always have valid neighbours — no `if (list is empty)` or `if (node is first/last)` branches anywhere.

> [!info] **Sentinel head / tail — why dummy nodes?**
> Without sentinels, `insert` into an empty list and `remove` of the only element both require special-case code (check if `prev == null`, check if `next == null`, update `head`/`tail` pointers). With sentinels, real nodes always sit *between* `head` and `tail`, so `node.prev` and `node.next` are guaranteed non-null for any real node. Both helper methods become branchless four-pointer swaps.

> [!info] **Why `Node` must store `key`?**
> When the cache overflows, we evict `tail.prev` and must also remove it from the `HashMap`. The HashMap call is `map.remove(lru.key)`. If `Node` only stored `value`, eviction would be impossible without a reverse lookup. Always store the `key` in the node.

**Pointer mechanics of `remove(node)`:**

Before (`head ↔ A ↔ node ↔ B ↔ tail`):
```
A.next → node    node.prev → A
B.prev → node    node.next → B
```
After:
```
A.next → B       B.prev → A
node.next → null  node.prev → null   (cleaned up for safety)
```

**Pointer mechanics of `insert(node)` at head:**

Before (`head ↔ A ↔ ... ↔ tail`), inserting `node`:
```
Step 1: nextNode = head.next        (save A)
Step 2: head.next = node
Step 3: node.next = nextNode (A)
Step 4: node.prev = head
Step 5: nextNode.prev = node        (A.prev now → node)
```
Result: `head ↔ node ↔ A ↔ ... ↔ tail`

**Full operation dry run** (capacity = 2):

| Operation | List (MRU→LRU) | Map keys | Return |
|-----------|----------------|----------|--------|
| `LRUCache(2)` | `head ↔ tail` | {} | — |
| `put(1,1)` | `head ↔ [1] ↔ tail` | {1} | — |
| `put(2,2)` | `head ↔ [2] ↔ [1] ↔ tail` | {1,2} | — |
| `get(1)` | `head ↔ [1] ↔ [2] ↔ tail` | {1,2} | 1 |
| `put(3,3)` → evict LRU=2 | `head ↔ [3] ↔ [1] ↔ tail` | {1,3} | — |
| `get(2)` | unchanged | {1,3} | **-1** |
| `put(4,4)` → evict LRU=1 | `head ↔ [4] ↔ [3] ↔ tail` | {3,4} | — |
| `get(1)` | unchanged | {3,4} | **-1** |
| `get(3)` | `head ↔ [3] ↔ [4] ↔ tail` | {3,4} | 3 |
| `get(4)` | `head ↔ [4] ↔ [3] ↔ tail` | {3,4} | 4 |

Output: `[null, null, null, 1, null, -1, null, -1, 3, 4]` ✅

```java
class LRUCache {

    static class Node {
        int key;
        int value;
        Node prev;
        Node next;
        Node(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }

    Node head;
    Node tail;
    int capacity;
    Map<Integer, Node> map;

    public LRUCache(int capacity) {
        this.capacity = capacity;
        map = new HashMap<>(capacity);

        head = new Node(0,0);
        tail = new Node(0,0);
        head.next = tail;
        tail.prev = head;
    }
    
    public int get(int key) {
        if(!map.containsKey(key)) return -1;
        Node node = map.get(key);
        remove(node);
        insert(node);
        return node.value;
    }
    
    public void put(int key, int value) {
        if(map.containsKey(key)) {
            Node oldNode = map.get(key);
            remove(oldNode);
        }

        Node newNode = new Node(key, value);
        insert(newNode);
        map.put(key, newNode);

        if(map.size() > capacity) {
            Node lru = tail.prev;
            remove(lru);
            map.remove(lru.key);
        }

    }

    public void remove(Node node) {
        // Head <-> A <-> B <-> C <-> Tail
        Node prevNode = node.prev;
        Node nextNode = node.next;

        if(prevNode!=null) prevNode.next = nextNode;
        if(nextNode!=null) nextNode.prev = prevNode;

        node.next = null;
        node.prev = null;
    }

    public void insert(Node node) {
        // Head <-> A <-> B <-> C <-> Tail
        Node nextNode = head.next;
        
        head.next = node;

        node.next = nextNode;
        node.prev = head;

        nextNode.prev = node;
    }
}

/**
 * Your LRUCache object will be instantiated and called as such:
 * LRUCache obj = new LRUCache(capacity);
 * int param_1 = obj.get(key);
 * obj.put(key,value);
 */
```

---

## 🔑 Key Insights
- O(1) remove requires `prev` — you can't unlink a node in O(1) from a singly linked list; the doubly linked list is non-negotiable here.
- `remove` + `insert` is the atomic "move to front" operation — both `get` and `put` (on existing keys) share this exact two-step pattern.
- In `put`, insert the new node *before* checking capacity overflow — after insertion the list naturally has `capacity + 1` nodes, so `tail.prev` is exactly the right LRU candidate to evict.
- The `null` checks in `remove()` (`if(prevNode!=null)`) are defensive but technically unnecessary with sentinels — real nodes always have non-null neighbours. Harmless, but worth knowing so you don't add them in fresh code.

---

## ⚠️ Pitfalls
> [!warning]
> - Forgetting to store `key` in `Node` — eviction calls `map.remove(lru.key)`; without the key in the node this is impossible.
> - Evicting before inserting in `put` — insert first, then evict, so the size check and `tail.prev` are always correct.
> - Using a singly linked list — removal of an arbitrary node requires the predecessor; without `prev` you can't do it in O(1).
> - Not cleaning `node.next` / `node.prev` to `null` in `remove` — stale pointers won't break correctness here (nodes are immediately reinserted or discarded), but it's a bad habit that can cause subtle bugs in other DLL problems.

---

## ⏱️ Complexity
- **Time:** `O(1)` per `get` and `put` — one `HashMap` lookup + two O(1) pointer-swap operations.
- **Space:** `O(capacity)` — at most `capacity` nodes in the DLL plus `capacity` entries in the `HashMap`.
