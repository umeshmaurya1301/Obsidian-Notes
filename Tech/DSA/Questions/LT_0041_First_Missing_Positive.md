---
created: 2026-05-22 00:00
tags:
  - dsa
  - array
  - hash-table
  - cyclic-sort
source: https://leetcode.com/problems/first-missing-positive/description/
problem_id: "41"
difficulty: Hard
status: Solved
review_date:
---
# LT_0041 – First Missing Positive

**Link:** [Open Problem](https://leetcode.com/problems/first-missing-positive/description/)

---

## 📝 Problem Description
> [!info]
> Given an unsorted integer array `nums`, return the smallest missing positive integer.
>
> You must implement an algorithm that runs in `O(n)` time and uses `O(1)` auxiliary space.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [1,2,0]`
> **Output:** `3`
> **Explanation:** The numbers in the range [1,2] are all in the array.

> [!example]
> **Input:** `nums = [3,4,-1,1]`
> **Output:** `2`
> **Explanation:** 1 is in the array but 2 is missing.

> [!example]
> **Input:** `nums = [7,8,9,11,12]`
> **Output:** `1`
> **Explanation:** The smallest positive integer 1 is missing.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 10^5`
> - `-2^31 <= nums[i] <= 2^31 - 1`

---

## 🔍 Intuition

The answer must lie in `[1, n+1]` where `n = nums.length` — if all of `1..n` are present, the answer is `n+1`. This bounds the search and lets us use the array itself as a presence marker: value `v` belongs at index `v-1`. We scan through and keep swapping each number to its correct index; once placement is done, the first index where `nums[i] != i+1` reveals the missing positive. A HashSet would work in `O(n)` time but costs `O(n)` space — treating indices as buckets eliminates that entirely.

> 🟢 *Cyclic Sort / Index-as-Hashmap*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Cyclic Sort (In-place Index Placement)

**Why this works:**
- The missing positive is always in `[1, n+1]`, so only values in that range matter.
- Placing value `v` at index `v-1` encodes presence without extra space.
- A single scan after placement finds the first "hole" — the index where the value is wrong.

**Dry Run** (`nums = [3,4,-1,1]`):

| Step | i | nums | Action |
|------|---|------|--------|
| 1 | 0 | `[3, 4, -1, 1]` | `nums[0]=3` belongs at index 2 → swap(0,2) |
| 2 | 0 | `[-1, 4, 3, 1]` | `nums[0]=-1` out of range → move on |
| 3 | 1 | `[-1, 4, 3, 1]` | `nums[1]=4` belongs at index 3 → swap(1,3) |
| 4 | 1 | `[-1, 1, 3, 4]` | `nums[1]=1` belongs at index 0 → swap(1,0) |
| 5 | 1 | `[1, -1, 3, 4]` | `nums[1]=-1` out of range → move on |
| scan | 0 | `[1, -1, 3, 4]` | index 0 → 1 ✅ |
| scan | 1 | — | index 1 → expected 2, found -1 → **return 2** |

```java
class Solution {

    public int firstMissingPositive(int[] nums) {

        int n = nums.length;

        for (int i = 0; i < n; i++) {

            while (
                nums[i] > 0 &&
                nums[i] <= n &&
                nums[i] != nums[nums[i] - 1]
            ) {

                swap(nums, i, nums[i] - 1);
            }
        }

        for (int i = 0; i < n; i++) {

            if (nums[i] != i + 1) {
                return i + 1;
            }
        }

        return n + 1;
    }

    private void swap(int[] nums, int i, int j) {

        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
}
```

---

## 🔑 Key Insights
- Use `while`, not `if` — one swap may bring another valid number to index `i` that also needs placing. Only stop when `nums[i]` is out of range or already at its correct slot.
- The guard `nums[i] != nums[nums[i] - 1]` prevents infinite loops on duplicates (e.g. `[1,1]` would otherwise swap forever).
- Total swaps across the entire loop is at most `n`, so despite the nested `while`, overall time is `O(n)`.
- Same **Cyclic Sort** pattern applies to: Find All Duplicates, Find Missing Numbers, Set Mismatch, Find the Duplicate Number.

---

## ⚠️ Pitfalls
> [!warning]
> - Using `if` instead of `while` — misses chained placements and produces wrong answers.
> - Forgetting the duplicate guard `nums[i] != nums[nums[i] - 1]` — causes an infinite swap loop on arrays like `[1,1]`.
> - Off-by-one: value `v` maps to index `v-1`, not index `v`.

---

## ⏱️ Complexity
- **Time:** `O(n)` — each element is swapped at most once to its final position.
- **Space:** `O(1)` — placement is done in-place; no auxiliary data structures.
