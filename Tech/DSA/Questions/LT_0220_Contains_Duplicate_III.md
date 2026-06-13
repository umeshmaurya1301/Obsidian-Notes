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

### 🟢 Approach: Sliding Window + TreeSet

---

#### Step 1: Understand the Conditions

We need to find indices `i` and `j` such that:
1. `|i - j| <= indexDiff`
2. `|nums[i] - nums[j]| <= valueDiff`

---

#### Step 2: Convert the Value Condition into a Range

Given `|nums[i] - nums[j]| <= valueDiff`, let `curr = nums[i]`:

```
|curr - nums[j]|  <=  valueDiff
⟹  curr - valueDiff  <=  nums[j]  <=  curr + valueDiff
```

For every `curr`, we look for a previous value lying inside `[curr - valueDiff, curr + valueDiff]`.
These are simply the **left** and **right** boundaries of the valid range.

---

#### Step 3: Satisfy the Index Condition

Since we process left to right (`j < i`):

```
|i - j|  =  i - j  <=  indexDiff
```

So before checking `nums[i]`, we only keep `nums[i - indexDiff] … nums[i - 1]` inside the TreeSet — this is the **sliding window**.

---

#### Step 4: What Does the TreeSet Contain?

At iteration `i`, the TreeSet holds values whose indices satisfy:

```
max(0, i - indexDiff)  <=  j  <  i
```

Every value inside the TreeSet automatically satisfies `|i - j| <= indexDiff`.
**✅ Index condition is already handled.**

---

#### Step 5 & 6: Checking the Value Condition — Why `ceiling(curr - valueDiff)`?

`ceiling(x)` returns the **smallest element ≥ x** in `O(log k)` time. One call is sufficient:

> [!example]
> `curr = 20`, `valueDiff = 5` → required range `[15, 25]`
> TreeSet: `{ 3, 8, 17, 30 }`
> `set.ceiling(15)` → `17`
> `17 <= 25` ✅ → valid pair found

> [!example]
> **No-match case:**
> TreeSet: `{ 3, 8, 30 }`, range `[15, 25]`
> `set.ceiling(15)` → `30`
> `30 <= 25` ❌ → no element in range

---

#### Step 7: Why Is One Candidate Enough?

> [!info]
> The TreeSet is **sorted**. `ceiling(L)` gives the **minimum** value ≥ L.
> - If `candidate <= R` → it lies in `[L, R]` → valid pair ✅
> - If `candidate > R` → every subsequent element is even larger → no pair ❌
>
> One check covers all cases.

---

#### Final Mapping

| Condition | Handled by |
|-----------|------------|
| `\|i - j\| <= indexDiff` | Sliding window — TreeSet holds only last `indexDiff` elements |
| `\|nums[i] - nums[j]\| <= valueDiff` | Range query: `ceiling(curr - valueDiff) <= curr + valueDiff` |

**Complete thought process:**
1. Keep only nearby indices in TreeSet → index condition satisfied
2. Convert value condition into range `[curr - valueDiff, curr + valueDiff]`
3. Find first value ≥ left boundary: `ceiling(curr - valueDiff)`
4. If it is also ≤ right boundary → value condition satisfied
5. Both satisfied → `return true`

---

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
