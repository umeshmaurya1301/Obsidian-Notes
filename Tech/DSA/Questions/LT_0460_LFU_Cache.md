---
created: 2026-08-16 12:00
tags:
  - dsa
  - design
  - hash-table
  - linked-list
  - doubly-linked-list
source: https://leetcode.com/problems/lfu-cache/
problem_id: "460"
difficulty: Hard
status: Solved
review_date:
---
# LT_0460 – LFU Cache

**Link:** [Open Problem](https://leetcode.com/problems/lfu-cache/)

---

## 📝 Problem Description
> [!info]
> Design and implement a data structure for a Least Frequently Used (LFU) cache.
>
> Implement the `LFUCache` class:
> - `LFUCache(int capacity)` Initializes the object with the capacity of the data structure.
> - `int get(int key)` Gets the value of the key if the key exists in the cache. Otherwise, returns `-1`.
> - `void put(int key, int value)` Update the value of the key if present, or inserts the key if not already present. When the cache reaches its capacity, it should invalidate and remove the least frequently used key before inserting a new item. For this problem, when there is a tie (i.e., two or more keys with the same frequency), the least recently used key would be invalidated.
>
> To determine the least frequently used key, a use counter is maintained for each key in the cache. The key with the smallest use counter is the least frequently used key.
>
> When a key is first inserted into the cache, its use counter is set to `1` (due to the `put` operation). The use counter for a key in the cache is incremented every time `get` or `put` is called on it.
>
> The functions `get` and `put` must each run in `O(1)` average time complexity.

---

## 🧪 Examples
> [!example]
> **Input:**
> ```
> ["LFUCache", "put", "put", "get", "put", "get", "get", "put", "get", "get", "get"]
> [[2], [1, 1], [2, 2], [1], [3, 3], [2], [3], [4, 4], [1], [3], [4]]
> ```
> **Output:** `[null, null, null, 1, null, -1, 3, null, -1, 3, 4]`
> **Explanation:**
> - `lfu = LFUCache(2)`
> - `put(1, 1)` → `cnt(1) = 1`
> - `put(2, 2)` → `cnt(2) = 1, cnt(1) = 1`
> - `get(1)` → returns `1`; `cnt(1) = 2`
> - `put(3, 3)` → `2` is the LFU key (`cnt(2) = 1` is smallest), evict it
> - `get(2)` → returns `-1` (not found)
> - `get(3)` → returns `3`; `cnt(3) = 2`
> - `put(4, 4)` → `cnt(1) = cnt(3) = 2`, tie broken by recency: `1` is LRU, evict it
> - `get(1)` → returns `-1` (not found)
> - `get(3)` → returns `3`
> - `get(4)` → returns `4`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= capacity <= 10^4`
> - `0 <= key <= 10^5`
> - `0 <= value <= 10^9`
> - At most `2 * 10^5` calls will be made to `get` and `put`.

---

## 🔍 Intuition

The `O(1)` requirement for both `get` and `put` rules out scanning for the minimum frequency on every eviction — that's the whole design problem. The fix is to never store "one big ordered structure," but a **HashMap of frequency → doubly linked list**: every key with use-count `f` lives in bucket `f`'s list, and within a bucket the list is kept in recency order (most-recently-used at the head) so a tie on frequency is broken by simply evicting from the tail. A second `HashMap<key, Node>` gives `O(1)` lookup straight to a key's node, and each node knows its own list via its `freq` field, so "bump this key's frequency" is just: remove it from bucket `freq`, increment `freq`, insert it at the head of bucket `freq+1`.

The subtle part is tracking `minFreq` without a scan. It only needs to move in two situations: a brand-new key is inserted (which always starts at frequency `1`, so `minFreq` resets to `1` unconditionally), or a key gets bumped out of what was *currently* the minimum-frequency bucket, and that bucket becomes empty as a result. The second case is easy to get backwards — emptying *any* bucket does **not** mean the global minimum changed, only emptying the bucket that *was* the minimum does. That's why the check is `oldFreq == minFreq && oldList.size == 0`, not just `oldList.size == 0`: the first half asks "was this even the bucket that mattered?", the second half asks "did it just run out?" — both must hold before `minFreq++`.

> 🟢 *Bucket by the Cheap Key, Track the Frontier Instead of Scanning*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — HashMap of Frequency Buckets (Doubly Linked Lists) + minFreq Pointer

**Why this works:**
- `cache: Map<key, Node>` gives `O(1)` access to any key's node; `freqMap: Map<freq, DoublyLinkedList>` groups nodes by use-count, and each bucket's list is MRU-first so eviction within a tie is always "remove the tail" — `O(1)`.
- `updateFrequency` is the single operation both `get` (on a hit) and `put` (on an existing key) funnel through: unlink the node from its old frequency bucket, bump `freq`, relink at the head of the new bucket.
- `minFreq` is maintained incrementally rather than recomputed: it's forced to `1` whenever a new key is inserted (a fresh key's bucket-1 list is now non-empty, and nothing can have a lower count than a brand-new key), and it's incremented only when the bucket it currently points at goes empty because a node just left it.
- Sentinel `head`/`tail` nodes in `DoublyLinkedList` remove all null-checks from `addFirst`/`remove`/`removeLast`, keeping every list operation `O(1)` with no edge cases.

**Dry Run** (`capacity = 2`, ops from Example 1):

| Call | Effect | `freqMap` after | `minFreq` |
|---|---|---|---|
| `put(1,1)` | new key, freq 1 | `1 -> [1]` | `1` |
| `put(2,2)` | new key, freq 1 | `1 -> [2,1]` | `1` |
| `get(1)` → `1` | bucket 1 emptied of `1` but still has `2`, so `oldFreq(1)==minFreq(1)` but `oldList.size!=0` → no bump; `1` moves to freq 2 | `1 -> [2]`, `2 -> [1]` | `1` |
| `put(3,3)` | capacity full; evict tail of `freqMap.get(minFreq=1)` → `2`; insert `3` at freq 1 | `1 -> [3]`, `2 -> [1]` | `1` |
| `get(2)` → `-1` | not in cache | unchanged | `1` |
| `get(3)` → `3` | bucket 1 empties completely (`oldFreq(1)==minFreq(1) && size==0`) → `minFreq++` | `2 -> [3,1]` | `2` |
| `put(4,4)` | capacity full; evict tail of `freqMap.get(minFreq=2)` → `1` (LRU tiebreak); insert `4` at freq 1, reset `minFreq=1` | `1 -> [4]`, `2 -> [3]` | `1` |
| `get(1)` → `-1` | not in cache | unchanged | `1` |
| `get(3)` → `3` | bucket 1 (`[4]`) unaffected, bucket 2 loses `3` but `oldFreq(2) != minFreq(1)` → no bump | `1 -> [4]`, `2 -> [3]` (new freq 3 bucket) | `1` |
| `get(4)` → `4` | bucket 1 empties → `minFreq++` | `2 -> [4]`, `3 -> [3]` | `2` |

```java
class LFUCache {

    private final int capacity;;
    private int size;
    private int minFreq;

    private final Map<Integer, Node> cache;
    private final Map<Integer, DoublyLinkedList> freqMap;

    public LFUCache(int capacity) {
        this.capacity = capacity;
        this.size = 0;
        this.minFreq = 0;

        cache = new HashMap<>();
        freqMap = new HashMap<>();    
    }
    
    public int get(int key) {
        Node node = cache.get(key);
        if (node == null) return -1;
        updateFrequency(node);
        return node.value;
    }
    
    public void put(int key, int value) {
        if (capacity == 0) return;

        if (cache.containsKey(key)) {
            Node node = cache.get(key);
            node.value = value;
            updateFrequency(node);
            return;
        }

        if (size == capacity) {
            DoublyLinkedList minFreqList = freqMap.get(minFreq);
            Node nodeToRemove = minFreqList.removeLast();
            cache.remove(nodeToRemove.key);
            size--;
        }

        Node newNode = new Node (key, value, 1);
        cache.put(key, newNode);
        DoublyLinkedList list = freqMap.computeIfAbsent(1, k-> new DoublyLinkedList());

        list.addFirst(newNode);
        minFreq = 1;
        size++;
    }

    private void updateFrequency(Node node) {
        int oldFreq = node.freq;
        DoublyLinkedList oldList = freqMap.get(oldFreq);
        oldList.remove(node);
        if (oldFreq == minFreq && oldList.size == 0) {
            minFreq++;
        }

        node.freq++;

        DoublyLinkedList newList = freqMap.computeIfAbsent(node.freq, k -> new DoublyLinkedList());
        newList.addFirst(node);
    }

    static class DoublyLinkedList {
        Node head;
        Node tail;
        int size;

        DoublyLinkedList () {
            this.head = new Node(-1,-1, 0);
            this.tail = new Node(-1, -1, 0);
            this.size = 0;

            head.next = tail;
            tail.prev = head;
        }

        void addFirst(Node node) {
            node.next = head.next;
            node.prev = head;

            head.next.prev = node;
            head.next = node;

            size++;
        }

        void remove (Node node) {
            node.prev.next = node.next;
            node.next.prev = node.prev;

            size--;
        }

        Node removeLast () {
            if (size == 0) return null;
            Node node = tail.prev;
            remove(node);
            return node;
        }

    }

    static class Node {
        int key;
        int value;
        int freq;

        Node next;
        Node prev;

        Node (int key, int value, int freq) {
            this.key = key;
            this.value = value;
            this.freq = freq;
        }
    }
}
```

- **Time:** `get` and `put` both `O(1)` amortized · **Space:** `O(capacity)`

---

## 🔑 Key Insights
- Splitting storage by frequency into a `Map<freq, DoublyLinkedList>` turns "find the least-frequently-used key" into "look up bucket `minFreq`" — no scan, because the bucket itself is the answer.
- Within a frequency bucket, keeping the list MRU-first (`addFirst` on every touch) makes the LRU tiebreak free: the tail of the current bucket is always the correct eviction target.
- `minFreq` only ever needs to *decrease conceptually* on insert (reset to `1`, since a fresh key can't have a lower true minimum) and *increase* when the bucket it's currently pointing at empties out — it never needs to jump forward by scanning, and it never decreases except via that insert reset.
- `get` (on a hit) and `put` (on an existing key) are the same underlying event — "this key was used" — so routing both through one `updateFrequency` method keeps the frequency-bump/relink logic in exactly one place.

---

## ⚠️ Pitfalls
> [!warning]
> - The classic bug: writing `if (oldList.size == 0) minFreq++;` without also checking `oldFreq == minFreq`. Emptying a *non-minimum* bucket must not move `minFreq` — only emptying the bucket that was currently the minimum can.
> - Forgetting to reset `minFreq = 1` inside `put` when inserting a brand-new key — after an eviction the previous `minFreq` could be stale/too high, but a freshly inserted key always starts at frequency `1`, which is now the true minimum.
> - `capacity == 0` must make `put` a no-op (never insert, since there's no room to evict into) — worth a dedicated early return rather than relying on the eviction branch to handle it.
> - Sentinel `head`/`tail` nodes exist purely to remove null-checks from list surgery; they must never be handed back from `removeLast()` as if they were real cached entries (guarded here by checking `size == 0` first).

---

## ⏱️ Complexity
- **Time:** `O(1)` amortized per `get` / `put`
- **Space:** `O(capacity)`
