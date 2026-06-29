---
created: 2026-06-27 10:00
tags:
  - dsa
  - array
  - sliding-window
  - ordered-set
source: https://leetcode.com/problems/contains-duplicate-iii/description/
problem_id: "220"
difficulty: Hard
status: Solved
review_date:
---
# LT_0220 – Contains Duplicate III

**Link:** [Open Problem](https://leetcode.com/problems/contains-duplicate-iii/description/)

---

## 📝 Problem Description
> [!info]
> Given an integer array `nums` and two integers `indexDiff` and `valueDiff`, return `true` if there exist two indices `i` and `j` such that:
> - `i != j`
> - `abs(i - j) <= indexDiff`
> - `abs(nums[i] - nums[j]) <= valueDiff`
>
> Return `false` otherwise.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [1,2,3,1], indexDiff = 3, valueDiff = 0`
> **Output:** `true`
> **Explanation:** We can choose `i = 0`, `j = 3`. `|0 - 3| = 3 <= 3` and `|1 - 1| = 0 <= 0`.

> [!example]
> **Input:** `nums = [1,5,9,1,5,9], indexDiff = 2, valueDiff = 3`
> **Output:** `false`
> **Explanation:** No pair of indices satisfies both conditions simultaneously.

---

## ⚠️ Constraints
> [!warning]
> - `2 <= nums.length <= 10^5`
> - `-10^9 <= nums[i] <= 10^9`
> - `1 <= indexDiff <= nums.length`
> - `0 <= valueDiff <= 10^9`

---

## 🔍 Intuition

`|curr - nums[j]| <= valueDiff` is a distance condition — it means `nums[j]` must lie within `valueDiff` of `curr` on the number line, i.e., inside the interval `[curr - valueDiff, curr + valueDiff]`. This converts the absolute-value check into a plain range query: "does my current window contain any element in this interval?" A `TreeSet` is the right tool — its `ceiling(x)` method finds the smallest element ≥ `x` in O(log k) time, so I ask for `ceiling(curr - valueDiff)` and check whether the result is ≤ `curr + valueDiff`. One call, one check, done. The sliding window of size `indexDiff` handles the index constraint by evicting the element at `i - indexDiff` each step.

> 🟢 *Sliding Window + Ordered Set (TreeSet)*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Sliding Window + TreeSet

**Why this works:**
- `|a - b| <= k` ↔ `b ∈ [a - k, a + k]`, converting the value condition into a range membership query.
- `TreeSet` keeps the window sorted; `ceiling(curr - valueDiff)` finds the smallest candidate in O(log k) — if it is ≤ `curr + valueDiff`, a valid pair exists.
- Removing `nums[i - indexDiff]` at each step ensures the set always holds exactly the last `indexDiff` elements, satisfying the index constraint automatically.

**Dry Run** (`nums = [1,2,3,1], indexDiff = 3, valueDiff = 0`):

| i | curr | Window (before add) | Query range | `ceiling` result | Found? |
|---|------|---------------------|-------------|------------------|--------|
| 0 | 1    | {}                  | [1, 1]      | null             | No     |
| 1 | 2    | {1}                 | [2, 2]      | null             | No     |
| 2 | 3    | {1, 2}              | [3, 3]      | null             | No     |
| 3 | 1    | {1, 2, 3}           | [1, 1]      | 1 ≤ 1            | ✅ Yes |

```java
class Solution {
    public boolean containsNearbyAlmostDuplicate(int[] nums, int indexDiff, int valueDiff) {
        TreeSet<Long> set = new TreeSet<>();

        for(int i=0; i<nums.length; i++) {
            long curr = nums[i];
            Long candidate = set.ceiling(curr-valueDiff);
            if(candidate!=null && candidate <= curr+valueDiff) return true;
            set.add(curr);
            if(i>=indexDiff) {
                set.remove( (long)nums[i-indexDiff] );
            }
        }

        return false;
    }
}
```

---

## 🔑 Key Insights
- `|a - b| <= k` ↔ `a - k <= b <= a + k` — always convert absolute-value distance conditions into intervals before reaching for a data structure.
- `ceiling(curr - valueDiff)` is the single O(log k) call that answers the full range query; one candidate is enough because `TreeSet` is sorted.
- Use `long` throughout — `curr + valueDiff` can exceed `Integer.MAX_VALUE` when both values approach 10^9.
- Evict at `i >= indexDiff` (not `i > indexDiff`) — at step `i`, index `i - indexDiff` is just outside the allowed window of `indexDiff`.

---

## ⚠️ Pitfalls
> [!warning]
> - **Integer overflow:** `curr + valueDiff` overflows `int` for large inputs — always cast to `long` before arithmetic.
> - **Off-by-one on eviction:** Remove when `i >= indexDiff`, not `i > indexDiff`; the window covers indices `[i - indexDiff, i - 1]`.
> - **Check before add:** Query the set before inserting `curr`; inserting first lets `curr` match itself and always returns `true` for `valueDiff >= 0`.

---

## ⏱️ Complexity
- **Time:** `O(n log k)` — `n` iterations, each with O(log k) TreeSet operations where `k = indexDiff`.
- **Space:** `O(k)` — the TreeSet holds at most `indexDiff + 1` elements at any time.
