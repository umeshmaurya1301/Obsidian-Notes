---
created: 2026-08-16 12:00
tags:
  - dsa
  - design
  - stack
  - hash-table
source: https://leetcode.com/problems/maximum-frequency-stack/
problem_id: "895"
difficulty: Hard
status: Solved
review_date:
---
# LT_0895 – Maximum Frequency Stack

**Link:** [Open Problem](https://leetcode.com/problems/maximum-frequency-stack/)

---

## 📝 Problem Description
> [!info]
> Design a stack-like data structure to push elements to the stack and pop the most frequent element from the stack.
>
> Implement the `FreqStack` class:
> - `FreqStack()` constructs an empty frequency stack.
> - `void push(int val)` pushes an integer `val` onto the top of the stack.
> - `int pop()` removes and returns the most frequent element in the stack.
>
> If there is a tie for the most frequent element, the element closest to the stack's top is removed and returned.

---

## 🧪 Examples
> [!example]
> **Input:**
> ```
> ["FreqStack","push","push","push","push","push","push","pop","pop","pop","pop"]
> [[],[5],[7],[5],[7],[4],[5],[],[],[],[]]
> ```
> **Output:** `[null,null,null,null,null,null,null,5,7,5,4]`
> **Explanation:** After six `push` operations, the stack contains `[5,7,5,7,4,5]` from bottom to top.
> - `pop()` → `5` (most frequent, count 3)
> - `pop()` → `7` (tied with `5` at count 2, but `7` is nearest the top)
> - `pop()` → `5`
> - `pop()` → `4`

---

## ⚠️ Constraints
> [!warning]
> - Calls to `push(int val)` will be such that `0 <= val <= 10^9`.
> - The total number of `push` calls will not exceed `10^4` in a single test case; the total number of `pop` calls will not exceed `10^4` in a single test case; the total number of `push` and `pop` calls will not exceed `1.5 * 10^5` across all test cases.
> - It is guaranteed that `pop()` won't be called if the stack has zero elements.

---

## 🔍 Intuition

The naive read is "track `value -> frequency`, and on `pop` scan for the max" — but that's `O(n)` per pop, and the problem wants `O(1)`-ish. The fix is the same move as LFU Cache, mirrored: instead of only storing `value -> frequency`, also store the inverse, `frequency -> stack of values` (`freqStack`), plus a running `maxFreq`. A `pop` never searches — it goes straight to `freqStack.get(maxFreq)` and pops its top.

The elegant part is that tie-breaking ("most frequent, and among ties the one closest to the top") falls out for free. Every value that reaches frequency `f` gets pushed onto bucket `f`'s stack at the moment it gets there — so within a bucket, later arrivals sit above earlier ones purely because that's how `Stack.push` works. Popping bucket `maxFreq`'s top is therefore automatically "the most recent value to reach the current max frequency," with zero extra bookkeeping for recency. `maxFreq` itself only ever needs to move by exactly one bucket at a time: it rises by construction on every `push` (`Math.max(maxFreq, f)`, and a bucket can't reach frequency `f` before frequency `f-1`), and it falls by exactly one when a `pop` empties the bucket it's currently pointing at — never further, since the bucket below can't be empty (it fed the one above).

> 🟢 *Bucket by the Cheap Key, Track the Frontier Instead of Scanning*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — HashMap of Frequency Buckets (Stacks) + maxFreq Pointer

**Why this works:**
- `freqMap: Map<val, freq>` tracks each value's current count in `O(1)`; `freqStack: Map<freq, Stack<Integer>>` groups values by that count, so "who currently has the highest frequency" is just `freqStack.get(maxFreq)` — no scan.
- Recency-among-ties is free: within a frequency bucket, a value is pushed onto that bucket's stack only when it *reaches* that frequency, so the stack's natural top-to-bottom order already encodes "most recently reached this frequency" — exactly the tiebreak the problem asks for.
- `maxFreq` is maintained incrementally, never recomputed: `push` can only ever raise it by one (`Math.max(maxFreq, f)`), and `pop` can only ever lower it by one, and only when the bucket it currently points at goes empty — the bucket one below is guaranteed non-empty since it's what fed the value now being removed.

**Dry Run** (`push(5) push(7) push(5) push(7) push(4) push(5)`, then four `pop()`s):

| Call | `freqMap` after | `freqStack` after | `maxFreq` | returns |
|---|---|---|---|---|
| `push(5)` | `5:1` | `1 -> [5]` | `1` | — |
| `push(7)` | `5:1, 7:1` | `1 -> [5,7]` | `1` | — |
| `push(5)` | `5:2, 7:1` | `1 -> [5,7]`, `2 -> [5]` | `2` | — |
| `push(7)` | `5:2, 7:2` | `1 -> [5,7]`, `2 -> [5,7]` | `2` | — |
| `push(4)` | `5:2, 7:2, 4:1` | `1 -> [5,7,4]`, `2 -> [5,7]` | `2` | — |
| `push(5)` | `5:3, 7:2, 4:1` | `1 -> [5,7,4]`, `2 -> [5,7]`, `3 -> [5]` | `3` | — |
| `pop()` | bucket 3 pops `5`, `5:2`; bucket 3 empty → `maxFreq--` | `3 -> []` | `2` | `5` |
| `pop()` | bucket 2 pops top `7`, `7:1` | `2 -> [5]` | `2` | `7` |
| `pop()` | bucket 2 pops `5`, `5:1`; bucket 2 empty → `maxFreq--` | `2 -> []` | `1` | `5` |
| `pop()` | bucket 1 pops top `4`, `4:0` | `1 -> [5,7]` | `1` | `4` |

```java
class FreqStack {
    
    int maxFreq;
    Map<Integer, Integer> freqMap = new HashMap<>();
    Map<Integer, Stack<Integer>> freqStack = new HashMap<>();

    public FreqStack() {
        freqMap = new HashMap<>();
        freqStack = new HashMap<>();
        maxFreq = 0;
    }
    
    public void push(int val) {
        int f = freqMap.getOrDefault(val, 0) + 1;
        freqMap.put(val, f);
        maxFreq = Math.max(maxFreq, f);
        freqStack.computeIfAbsent(f, k -> new Stack()).push(val);
    }
    
    public int pop() {
        int val = freqStack.get(maxFreq).pop();
        freqMap.put(val, freqMap.get(val)-1);
        if(freqStack.get(maxFreq).isEmpty()) maxFreq--;
        return val;
    }
}
```

- **Time:** `push` and `pop` both `O(1)` amortized · **Space:** `O(n)` where `n` is the number of elements pushed

---

## 🔑 Key Insights
- Storing the inverse mapping (`frequency -> bucket of values`) alongside the forward one (`value -> frequency`) is the same trick as LFU Cache — it turns "find the extreme by frequency" from a scan into a direct lookup by a tracked pointer (`maxFreq` here, `minFreq` there).
- Using a plain `Stack` (not a queue or a doubly linked list) per bucket is enough, because within one bucket only "top" and "push" are ever needed — there's no eviction from the middle or the bottom, unlike LFU Cache's need for arbitrary removal.
- `maxFreq` moves by at most one bucket per operation in either direction: `push` can raise a value's frequency by exactly one step, and popping the current max bucket empty can only reveal the bucket immediately below (which is guaranteed non-empty, since every value in a higher bucket passed through the one below it first).
- This is structurally the mirror image of LFU Cache's `minFreq` + `Map<freq, DoublyLinkedList>` — same bucket-by-frequency idea, opposite extreme, and a simpler per-bucket structure since nothing needs `O(1)` arbitrary-position removal.

---

## ⚠️ Pitfalls
> [!warning]
> - Forgetting that `maxFreq` only decreases when the bucket it currently points at (not just *some* bucket) becomes empty — but unlike LFU Cache's `minFreq` check, this one is actually simpler here: since `pop` always pops from `freqStack.get(maxFreq)` itself, there's no risk of checking the wrong bucket the way LFU Cache's `updateFrequency` can.
> - `maxFreq` must never be reset or recomputed by scanning — always adjust it by exactly one step (`Math.max` on push, `maxFreq--` on emptied pop) to keep both operations `O(1)`.
> - Decrementing `freqMap.get(val)` on `pop` without also touching `freqStack` would be wrong — the popped value must be physically removed from its old bucket's stack (which `Stack.pop()` already does) so it isn't found there again.

---

## ⏱️ Complexity
- **Time:** `O(1)` amortized per `push` / `pop`
- **Space:** `O(n)`
