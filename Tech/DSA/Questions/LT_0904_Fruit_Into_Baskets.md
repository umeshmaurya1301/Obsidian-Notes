---
created: 2026-05-31 10:00
tags:
  - dsa
  - arrays
  - hash-table
  - sliding-window
source: https://leetcode.com/problems/fruit-into-baskets/
problem_id: "904"
difficulty: Medium
status: Solved
review_date:
---
# LT_0904 – Fruit Into Baskets

**Link:** [Open Problem](https://leetcode.com/problems/fruit-into-baskets/)

---

## 📝 Problem Description
> [!info]
> You are visiting a farm that has a single row of fruit trees arranged from left to right. The trees are represented by an integer array `fruits` where `fruits[i]` is the type of fruit the `i`th tree produces.
>
> You want to collect as much fruit as possible. However, the owner has some rules:
> - You only have **two baskets**, and each basket can only hold a **single type** of fruit. No limit on amount per basket.
> - Starting from any tree of your choice, you must pick exactly one fruit from every tree while moving to the right. The picked fruits must fit in one of your two baskets.
> - Once you reach a tree whose fruit doesn't fit in your two baskets, you must stop.
>
> Return the **maximum number of fruits** you can pick.

---

## 🧪 Examples
> [!example]
> **Input:** `fruits = [1,2,1]`
> **Output:** `3`
> **Explanation:** We can pick from all 3 trees.

> [!example]
> **Input:** `fruits = [0,1,2,2]`
> **Output:** `3`
> **Explanation:** We can pick from trees `[1,2,2]`. Starting at the first tree only gives `[0,1]`.

> [!example]
> **Input:** `fruits = [1,2,3,2,2]`
> **Output:** `4`
> **Explanation:** We can pick from trees `[2,3,2,2]`. Starting at the first tree only gives `[1,2]`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= fruits.length <= 10^5`
> - `0 <= fruits[i] < fruits.length`

---

## 🔍 Intuition

The two-basket rule is really just "find the longest contiguous subarray with at most 2 distinct values." A sliding window fits perfectly: expand `right` to include new fruit, shrink `left` when we exceed 2 types. A `HashMap` tracks the count of each fruit type in the current window — when a count drops to `0` we remove that type, keeping `freq.size()` as an accurate distinct-type counter.

> 🟢 *Sliding Window + Frequency Map*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Sliding Window + Frequency Map

**Why this works:**
- The window `[left, right]` always holds at most 2 distinct fruit types; the map enforces this invariant.
- Shrinking one step at a time (`left++` every inner iteration) ensures the map stays in exact sync with the actual window contents.
- Each element is added and removed at most once, giving O(n) overall.

**Dry Run** (`fruits = [0,1,2,2]`):

| `right` | `fruit` | `freq` after add | shrink? | `left` | window len | `max` |
|---------|---------|-----------------|---------|--------|------------|-------|
| 0 | 0 | `{0:1}` | No | 0 | 1 | 1 |
| 1 | 1 | `{0:1, 1:1}` | No | 0 | 2 | 2 |
| 2 | 2 | `{0:1,1:1,2:1}` | Yes → remove `fruits[0]=0` → `{1:1,2:1}`, `left=1` | 1 | 2 | 2 |
| 3 | 2 | `{1:1, 2:2}` | No | 1 | 3 | **3** |

```java
class Solution {
    public int totalFruit(int[] fruits) {
        int left = 0;
        Map<Integer, Integer> freq = new HashMap<>();
        
        int len = fruits.length;
        int right = 0;
        int max = Integer.MIN_VALUE;

        while(right < len) {
            int fruit = fruits[right];           
            freq.merge(fruit, 1, Integer::sum);

            while(freq.size() > 2) {
                int leftFruit = fruits[left];
                freq.merge(leftFruit, -1, Integer::sum);
                if (freq.get(leftFruit) == 0) {
                    freq.remove(leftFruit);
                }
                left++;
            }
            max = Math.max(max, right - left + 1);
            right++;
        }

        return max;
    }
}
```

---

## 🐛 Bug Analysis — Why `left++` Inside the `if` Is Wrong

The original inner loop had `left++` nested inside the `if (freq.get(leftFruit) == 0)` check:

```java
while(freq.size() > 2) {
    int leftFruit = fruits[left];
    freq.merge(leftFruit, -1, Integer::sum);
    if (freq.get(leftFruit) == 0) {
        freq.remove(leftFruit);
        left++;           // ← only moves when count hits 0
    }
    // if count > 0: left stays, next iteration reads the SAME position again
}
```

**What goes wrong:**
When `freq.get(leftFruit) > 0` after the decrement, `left` does not advance. The next iteration reads `fruits[left]` again — the **same index** — and decrements the same fruit's count again. This keeps looping until the count finally hits `0`, at which point `left` moves once. So a fruit that appeared 3 times in a row at positions `[0,1,2]` would decrement position `0`'s fruit count 3 times before `left` moves past position `0` — never reaching positions `1` and `2` at all.

**Why this corrupts `freq`:**
`freq` is supposed to represent the exact count of each fruit type in the live window `[left, right]`. When we decrement a count multiple times without moving `left`, the stored count becomes lower than the true count of that fruit still inside the window. The fruit at `left` is physically still in the window but `freq` no longer knows that.

**Concrete wrong-answer trace** (`fruits = [1,1,2,3,2,2]`, expected output `4`):

After adding `fruits[3]=3`, freq = `{1:2, 2:1, 3:1}`, `left=0`:
```
Inner iter 1: leftFruit = fruits[0] = 1
              freq.merge(1,-1) → {1:1, 2:1, 3:1}
              get(1) = 1 ≠ 0  →  left stays at 0   ← BUG

Inner iter 2: leftFruit = fruits[0] = 1  (same position!)
              freq.merge(1,-1) → {1:0, 2:1, 3:1}
              get(1) = 0  →  remove 1, left = 1
              freq = {2:1, 3:1}  ✓ size = 2, exit while
```

`freq` now says the window `[left=1, right=3]` contains only types `2` and `3`. But the real window is `[fruits[1], fruits[2], fruits[3]]` = `[1, 2, 3]`, which still has **3 distinct types**. The type-`1` fruit at index `1` was never actually evicted — `left` skipped right over it.

As `right` advances to `4` and `5`, the corrupted map never triggers a shrink, and the code reports a final window length of **5** (indices 1–5 = `[1,2,3,2,2]`, which contains 3 types). **Wrong answer: returns 5, should return 4.**

**The fix — always advance `left`:**
```java
while(freq.size() > 2) {
    int leftFruit = fruits[left];
    freq.merge(leftFruit, -1, Integer::sum);
    if (freq.get(leftFruit) == 0) {
        freq.remove(leftFruit);   // cleanup map entry
    }
    left++;                       // ← unconditional: one step per iteration
}
```

Every inner iteration removes **exactly one tree** from the left boundary and decrements that tree's fruit count by exactly `1`. The map stays perfectly in sync with `[left, right]` at all times.

---

## 🔑 Key Insights
- Reframe as "longest subarray with ≤ 2 distinct elements" — the basket metaphor is just flavoring.
- `freq.merge(key, delta, Integer::sum)` is a clean Java idiom for increment/decrement without null-check boilerplate.
- `freq.size()` is only a valid distinct-type counter if every `0`-count entry is removed immediately.
- The inner `while` must advance `left` **unconditionally** on every iteration — one position per step, no multi-decrement shortcuts.

---

## ⚠️ Pitfalls
> [!warning]
> - Putting `left++` inside the `if (count == 0)` block — the window boundary stops syncing with the map (see bug analysis above).
> - Forgetting to call `freq.remove()` when count hits `0` — `freq.size()` will count ghost entries and the outer window will never grow past the false limit.
> - Initializing `max = Integer.MIN_VALUE` is safe here since `fruits.length >= 1`, but `max = 0` is a cleaner default.

---

## ⏱️ Complexity
- **Time:** `O(n)` — each element enters and exits the window at most once; inner `while` has amortised `O(1)` cost per element.
- **Space:** `O(1)` — the freq map holds at most 3 entries at any point (2 valid + 1 being evicted).
