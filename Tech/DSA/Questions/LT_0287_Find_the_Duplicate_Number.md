---
created: 2026-08-16 12:00
tags:
  - dsa
  - array
  - binary-search
  - pigeonhole-principle
  - linked-list
  - floyd-cycle-detection
source: https://leetcode.com/problems/find-the-duplicate-number/
problem_id: "287"
difficulty: Medium
status: Solved
review_date:
---
# LT_0287 – Find the Duplicate Number

**Link:** [Open Problem](https://leetcode.com/problems/find-the-duplicate-number/)

---

## 📝 Problem Description
> [!info]
> Given an array of integers `nums` containing `n + 1` integers where each integer is in the range `[1, n]` inclusive.
>
> There is only one repeated number in `nums`, return this repeated number.
>
> You must solve the problem **without modifying** the array `nums` and using only **constant extra space**.
>
> **Follow up:**
> - How can we prove that at least one duplicate number must exist in `nums`?
> - Can you solve the problem in linear runtime complexity?

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [1,3,4,2,2]`
> **Output:** `2`

> [!example]
> **Input:** `nums = [3,1,3,4,2]`
> **Output:** `3`

> [!example]
> **Input:** `nums = [3,3,3,3,3]`
> **Output:** `3`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= n <= 10^5`
> - `nums.length == n + 1`
> - `1 <= nums[i] <= n`
> - All the integers in `nums` appear only once except for precisely one integer which appears two or more times.

---

## 🔍 Intuition

The "no modification, `O(1)` space" constraint kills sorting and hash-set approaches, and the trap is thinking the binary search here searches **array positions** — it doesn't, it searches the **value range** `[1, n]`. For any candidate split point `mid`, the sub-range `[1, mid]` can hold at most `mid` distinct values. Count how many elements of `nums` actually satisfy `num <= mid`; by the pigeonhole principle, if that count exceeds `mid`, more numbers were crammed into `[1, mid]` than it has room for, so the duplicate must live in `[1, mid]`. If the count is `<= mid`, that half is "full but not overflowing," so the duplicate must be in `(mid, n]` instead.

This is a "find the first value where a property holds" binary search, so it must use `hi = mid` (not `mid - 1`) whenever the overflow condition is true — `mid` itself could be the duplicate, and `mid - 1` would discard it. The loop keeps halving the range until `lo == hi`, and that single remaining value is provably the duplicate, because it's the only value left in a range that's been repeatedly shown to contain more numbers than room.

A sharper reading treats the array itself as a linked list: index `i` pointing to value `nums[i]` is exactly a `next` pointer, so walking `0 -> nums[0] -> nums[nums[0]] -> ...` traces a path through an implicit list. Since there are `n+1` indices but only `n` possible values, two different indices must eventually point at the same value — the pigeonhole principle again, but this time it forces a **cycle** rather than an overflow count. The duplicate value is exactly the node where two incoming paths first merge, which is precisely the cycle's entrance — the same quantity Floyd's Tortoise-and-Hare algorithm (`Linked List Cycle II`) finds, in `O(n)` time and `O(1)` space, without ever touching the array.

> 🟢 *Binary Search the Answer Space via Pigeonhole Counting — or See the Array as a Linked List and Hunt the Cycle*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Binary Search on the Value Range

**Why this works:**
- Searching `[1, n]` by value (not by array index) turns "find the duplicate" into "find the smallest `mid` where `count(nums[i] <= mid) > mid`" — a monotonic predicate, which is exactly what binary search needs.
- The count itself never modifies `nums` and uses no extra data structure — a single `O(n)` linear scan per binary-search step, satisfying both the no-modification and `O(1)`-space constraints.
- `hi = mid` (never `mid - 1`) is required because the overflow condition `count > mid` means the duplicate is somewhere in `[lo, mid]` **including `mid`** — shrinking past it would throw away a valid answer.

**Dry Run** (`nums = [1,3,4,2,2]`, `n = 4`):

| `lo` | `hi` | `mid` | `count(nums[i] <= mid)` | `count > mid`? | action |
|---|---|---|---|---|---|
| `0` | `3` (idx) | `1` | `nums≤2`: `1,2,2 → 3` | `3 > 2` → true | `hi = mid = 1` (value-space `hi=2`) |
| `0` | `1` | `0` | `nums≤1`: `1 → 1` | `1 > 1` → false | `lo = mid+1 = 1` |

`lo == hi == 1` (0-indexed loop bound) → returns `2` (the duplicate). *(Note: the code below runs `lo`/`hi` over array indices `0..len-1`, which line up 1:1 with values `1..n` since `n = len - 1`; the walkthrough above tracks the equivalent value-range logic described in the intuition.)*

```java
class Solution {
    public int findDuplicate(int[] nums) {
        int len = nums.length;
        int lo = 0;
        int hi = len-1;

        while (lo < hi) {
            int mid = lo + (hi-lo)/2;
            int count = 0;
            for (int num : nums) {
                if (num<=mid) count++;
            }

            if (count > mid) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }

        return lo;
    }
}
```

- **Time:** `O(n log n)` — `log n` binary-search steps, each doing an `O(n)` count · **Space:** `O(1)`

### ✅ Solution 2 — Floyd's Cycle Detection (Tortoise and Hare)

**Why this works:**
- Treating index `i` as a node and `nums[i]` as its `next` pointer turns the array into an implicit linked list; since there are `n+1` indices funneling into only `n` possible values, two indices must point to the same value, which forces the "list" to loop back on itself into a cycle rather than terminate.
- The duplicate value is exactly the index where two incoming paths first collide — i.e. the cycle's entrance — because that's the only node with in-degree `≥ 2` in this implicit graph, and it's reached by walking `nums[...]` from more than one starting index.
- This is structurally identical to `Linked List Cycle II`: Phase 1 finds *some* point inside the cycle by running a slow pointer (`+1` step) and a fast pointer (`+2` steps) until they collide; Phase 2 resets one pointer to the start and advances both one step at a time — they provably meet exactly at the cycle entrance, by the standard `a = c - b` distance argument.
- No array modification and `O(1)` extra space, since only two integer pointers (`slow`, `fast`) are used — strictly better than Solution 1's `O(n log n)`.

**Dry Run** (`nums = [1,3,4,2,2]`, treating `i -> nums[i]` as pointers: `0->1->3->2->4->2->...`):

*Phase 1 — find a meeting point inside the cycle:*

| step | `slow = nums[slow]` | `fast = nums[nums[fast]]` |
|---|---|---|
| init | `1` | `1` |
| 1 | `nums[1] = 3` | `nums[nums[1]] = nums[3] = 2` |
| 2 | `nums[3] = 2` | `nums[nums[2]] = nums[4] = 2` — **`slow == fast == 2`**, stop |

*Phase 2 — reset `slow` to the start, advance both one step at a time until they meet:*

| step | `slow` | `fast` |
|---|---|---|
| init | `nums[0] = 1` | `2` (from Phase 1) |
| 1 | `nums[1] = 3` | `nums[2] = 4` |
| 2 | `nums[3] = 2` | `nums[4] = 2` — **meet at `2`**, stop |

Returns `2` — the duplicate, and the cycle's entrance. ✅

```java
public int findDuplicate(int[] nums) {

    int slow = nums[0];
    int fast = nums[0];

    do {
        slow = nums[slow];
        fast = nums[nums[fast]];
    } while (slow != fast);

    slow = nums[0];

    while (slow != fast) {
        slow = nums[slow];
        fast = nums[fast];
    }

    return slow;
}
```

- **Time:** `O(n)` · **Space:** `O(1)`

---

## 🔑 Key Insights
- This binary search operates on the **answer's value range**, not array indices — the search question is "which half of `[1, n]` must contain the duplicate?", never "is `nums[mid]` the answer?".
- The pigeonhole principle makes the predicate monotonic: once `count(nums[i] <= mid) > mid` becomes true for some `mid`, it stays true for every larger `mid` too, since the count only grows — that monotonicity is what makes binary search valid here.
- `lo` and `hi` are guaranteed equal at loop termination (`while (lo < hi)` only exits when they meet), so `return lo` and `return hi` are interchangeable — the choice is just convention from the "find first true" pattern.
- `hi = mid` vs `hi = mid - 1` is the single most important line: since `mid` can itself be the duplicate, only `hi = mid` preserves it as a still-reachable candidate.
- Reframing `index -> nums[index]` as a linked-list `next` pointer is the same pigeonhole idea as Solution 1, aimed at a different target: instead of forcing an *overflow count*, it forces a *cycle*, because `n+1` indices can't injectively map into only `n` values without two paths colliding.
- The cycle's entrance is provably the duplicate — not just "some node in the cycle" — because it's the unique node reached by two distinct incoming paths (the duplicate value is written to the array at two different indices, both of which point into it).
- Phase 1's meeting point is *not* the entrance in general — only Phase 2 (reset one pointer to the start, advance both one step at a time) is guaranteed to land exactly on the entrance, by the classic `distance(start→entrance) = c - distance(entrance→meeting)` argument from Floyd's algorithm.

---

## ⚠️ Pitfalls
> [!warning]
> - Writing `hi = mid - 1` instead of `hi = mid` on the overflow branch — this silently discards `mid` as a candidate even when it's the actual duplicate, breaking correctness.
> - Reaching for a `HashSet` or sorting to detect the duplicate — both violate the problem's explicit "no modification, `O(1)` extra space" constraint, even though they're the obvious first instinct.
> - Assuming the binary search narrows down an **index** into `nums` — it narrows down a **value** in `[1, n]`; the count comparison (`num <= mid`) is comparing element *values*, not positions.
> - Off-by-one on the count check: the condition is strictly `count > mid` (overflow), not `count >= mid` — `count == mid` means that sub-range is exactly full with no forced collision yet.
> - In the cycle-detection solution, returning the **Phase 1 meeting point** instead of running Phase 2 — the meeting point is guaranteed to be *somewhere* in the cycle, not necessarily the entrance/duplicate itself.
> - Starting `fast` two steps behind `slow` (or starting both from index `0`'s value inconsistently) breaks the `a = c - b` distance proof; both pointers must start from the exact same node (`nums[0]`) in Phase 1, and Phase 2's reset pointer must start from the true beginning (`nums[0]`), not from wherever Phase 1 left off.

---

## ⏱️ Complexity
- **Time:** `O(n)` — Solution 2 (Floyd's Cycle Detection) is the optimal approach; Solution 1 (Binary Search) runs in `O(n log n)`
- **Space:** `O(1)`
