---
created: 2026-05-18 00:00
tags:
  - Arrays
  - SlidingWindow
  - TreeSet
  - OrderedSet
  - BinarySearch
source: https://leetcode.com/problems/contains-duplicate-iii/
problem_id: "220"
difficulty: Hard
status: Completed
review_date:
---
# LT_0220 – Contains Duplicate III

**Link:** [Open Problem](https://leetcode.com/problems/contains-duplicate-iii/)

---

## 📝 Problem Description
> [!info]
> Given an integer array `nums` and two integers `indexDiff` and `valueDiff`, return `true` if there exist two indices `i` and `j` such that:
>
> - `i != j`
> - `|i - j| <= indexDiff`
> - `|nums[i] - nums[j]| <= valueDiff`
>
> Return `false` otherwise.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [1,2,3,1]`, `indexDiff = 3`, `valueDiff = 0`
> **Output:** `true`
> **Explanation:** `nums[0]` and `nums[3]` are equal and their index difference is `3`.

> [!example]
> **Input:** `nums = [1,5,9,1,5,9]`, `indexDiff = 2`, `valueDiff = 3`
> **Output:** `false`
> **Explanation:** No valid pair satisfies both the index and value conditions.

> [!example]
> **Input:** `nums = [1,5,9,1]`, `indexDiff = 3`, `valueDiff = 3`
> **Output:** `true`
> **Explanation:** `nums[0] = 1` and `nums[3] = 1` satisfy both conditions.

---

## ⚠️ Constraints
> [!warning]
> - `2 <= nums.length <= 100000`
> - `-2147483648 <= nums[i] <= 2147483647`
> - `0 <= indexDiff <= 100000`
> - `0 <= valueDiff <= 2147483647`

---

## 💡 Solutions

### 🟢 Approach 1: Sliding Window + TreeSet

**Intuition:**
For every current element `nums[i]`, we need to check whether any recent element falls within the value range `[curr - valueDiff, curr + valueDiff]`.

The index condition `|i - j| <= indexDiff` means we only care about elements within the last `indexDiff` positions — a classic **sliding window**. We maintain a `TreeSet<Long>` of recent elements. Because `TreeSet` stores elements in sorted order, `set.ceiling(x)` gives the smallest element `>= x` in `O(log k)` time.

**Why `ceiling()` alone is enough:**
Given `curr = 10`, `valueDiff = 3` → valid range `[7, 13]`. We call `set.ceiling(7)`:
- If result `<= 13` → valid pair found.
- If result `> 13` → no valid pair, because `TreeSet` is sorted and every subsequent element is even larger.

One candidate check is sufficient.

**Sliding Window — keeping index condition valid:**

At index `i`, only indices `[i - indexDiff, i - 1]` matter. We remove `nums[i - indexDiff]` from the set once the window exceeds size `indexDiff`.

Example — `nums = [4, 10, 15, 7]`, `indexDiff = 2`:

| i | action | set after |
|---|--------|-----------|
| 0 | add `4` | `{4}` |
| 1 | add `10` | `{4, 10}` |
| 2 | add `15`, remove `nums[0]=4` | `{10, 15}` |
| 3 | check against `{10, 15}` (indices 1, 2 only) | — |

**Dry Run — `nums = [1,5,9,1]`, `indexDiff = 3`, `valueDiff = 3`:**

| i | curr | range | `ceiling(L)` | valid? | set after |
|---|------|-------|--------------|--------|-----------|
| 0 | `1` | `[-2, 4]` | `null` | — | `{1}` |
| 1 | `5` | `[2, 8]` | `null` | — | `{1, 5}` |
| 2 | `9` | `[6, 12]` | `null` | — | `{1, 5, 9}` |
| 3 | `1` | `[-2, 4]` | `1` | `1 <= 4` ✅ | return `true` |

**Edge Cases:**
- `valueDiff = 0` — requires exact duplicates within `indexDiff` distance.
- `indexDiff = 0` — no valid pair can exist (indices must differ).
- Integer overflow — `curr + valueDiff` can overflow `int`; use `long`.
- Negative numbers — `TreeSet` handles them correctly.

---

### ✅ Java Implementation

```java
class Solution {
    public boolean containsNearbyAlmostDuplicate(
            int[] nums,
            int indexDiff,
            int valueDiff
    ) {

        TreeSet<Long> set = new TreeSet<>();

        for(int i = 0; i < nums.length; i++) {

            long curr = nums[i];

            Long candidate =
                    set.ceiling(curr - valueDiff);

            if(candidate != null &&
               candidate <= curr + valueDiff) {
                return true;
            }

            set.add(curr);

            if(i >= indexDiff) {
                set.remove((long) nums[i - indexDiff]);
            }
        }

        return false;
    }
}
```

---

## 🔑 Key Insights
- The value condition converts to a range query: `[curr - valueDiff, curr + valueDiff]`.
- `TreeSet` stores elements in sorted order — `ceiling(x)` finds the smallest valid candidate in `O(log k)`.
- Checking only one candidate is sufficient because the set is sorted.
- Sliding window enforces the index condition automatically — only the last `indexDiff` elements stay in the set.
- Use `long` throughout to prevent integer overflow on `curr + valueDiff`.

---

## 🧩 Patterns
- Sliding Window
- Ordered Set
- Range Query
- Balanced BST
- Search in Sorted Structure

---

## ⚠️ Pitfalls
> [!warning]
> - Using `int` instead of `long` causes overflow on large values.
> - Incorrect sliding window removal — removing the wrong element breaks the index constraint.
> - Confusing `indexDiff` with window size (window holds `indexDiff` elements, not `indexDiff + 1`).
> - Using `HashSet` instead of `TreeSet` — unordered sets cannot do range queries.
> - Forgetting that `ceiling()` can return `null` when no element `>= x` exists.

---

## ⏱️ Complexity
- **Time:** `O(n log k)` — each `TreeSet` operation (`add`, `remove`, `ceiling`) is `O(log k)`, done `n` times
- **Space:** `O(k)` — the `TreeSet` holds at most `k = indexDiff` elements
