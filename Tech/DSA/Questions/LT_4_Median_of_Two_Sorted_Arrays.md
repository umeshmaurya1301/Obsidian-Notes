---
created: 2026-02-03 07:30
tags:
  - Arrays
  - BinarySearch
source: https://leetcode.com/problems/median-of-two-sorted-arrays/
problem_id: "4"
difficulty: Hard
status: Completed
review_date:
---
# LT_4 – Median of Two Sorted Arrays

**Link:** [Open Problem](https://leetcode.com/problems/median-of-two-sorted-arrays/)

---

## 📝 Problem Description
> [!info]
> Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the **median** of the two sorted arrays.  
>  
> The overall run time complexity should be **O(log(m + n))**.

---

## 🧪 Examples
> [!example]
> **Input:** `nums1 = [1,3], nums2 = [2]`  
> **Output:** `2.00000`  
> **Explanation:** merged array = `[1,2,3]` and median is `2`.

> [!example]
> **Input:** `nums1 = [1,2], nums2 = [3,4]`  
> **Output:** `2.50000`  
> **Explanation:** merged array = `[1,2,3,4]` and median is `(2 + 3) / 2 = 2.5`.

---

## ⚠️ Constraints
> [!warning]
> - `nums1.length == m`, `nums2.length == n`
> - `0 <= m, n <= 1000`
> - `1 <= m + n <= 2000`
> - `-10^6 <= nums1[i], nums2[i] <= 10^6`

---

## 🔍 Intuition (Symmetry Based)

This problem can be solved by **thinking in terms of symmetry and balance**.

Instead of merging both sorted arrays, we try to **partition** them into two halves such that:

- The **Left Set** contains exactly half of the total elements  
- Every element in the Left Set is **≤** every element in the Right Set  

Once such a partition is found, the median depends only on the **boundary elements**:
- `max(Left Set)`
- `min(Right Set)`

---

## 🧠 Symmetry Explanation (Example Driven)

Consider:

a1 = [1, 3, 4, 7, 10, 12]
a2 = [2, 3, 6, 15]


- `a1` has 6 elements  
- `a2` has 4 elements  
- Total elements = 10  

If merged (conceptually):

combined = [1, 2, 3, 3, 4, 6, 7, 10, 12, 15]


Since the total length is even,  
📌 **Median = average of 5th and 6th elements**

median = (4 + 6) / 2 = 5


---

## 🪜 Partitioning Step by Step

We want **exactly 5 elements on the left side** in total.

Instead of merging, we try different valid splits while maintaining order.

---

### 🔹 Case 1: 0 elements from `a2`, 5 from `a1`

a1 = [1, 3, 4, 7, 10] | [12]
a2 = [] | [2, 3, 6, 15]


❌ Invalid  
`max(left) = 10` and `min(right) = 2` → `10 > 2`

---

### 🔹 Case 2: 1 element from `a2`, 4 from `a1`

a1 = [1, 3, 4, 7] | [10, 12]
a2 = [2] | [3, 6, 15]


❌ Invalid  
`max(left) = 7` and `min(right) = 3` → `7 > 3`

---

### 🔹 Case 3: 2 elements from `a2`, 3 from `a1`

a1 = [1, 3, 4] | [7, 10, 12]
a2 = [2, 3] | [6, 15]


✅ **Valid Partition**

- Left Set  = `{1, 3, 4, 2, 3}`
- Right Set = `{7, 10, 12, 6, 15}`

Boundary values:
- `max(left) = 4`
- `min(right) = 6`

Since total length is even:

median = (4 + 6) / 2 = 5


---

## 🔑 Key Insight

- We never build the merged array
- We only compare **boundary elements**
- Taking more elements from one array means taking fewer from the other
- This monotonic behavior allows **Binary Search on the smaller array**

---

## ⏱️ Complexity

- **Time:** `O(log(min(m, n)))`
- **Space:** `O(1)`

---

### 🔍 Step-by-Step Explanation

Let `nums1` be the smaller array.

Example:
nums1 = [2, 3, 6, 15] (m = 4)
nums2 = [1, 3, 4, 7, 10, 12] (n = 6)

Total Elements = 10
Half Size = 5


Cut `nums1` after 2 elements → `{2, 3}`  
Then take `5 - 2 = 3` elements from `nums2` → `{1, 3, 4}`

**Left Set:** `{2, 3, 1, 3, 4}` → max = `4`  
**Right Set:** `{6, 15, 7, 10, 12}` → min = `6`

✅ Valid partition  
Median = `(4 + 6) / 2 = 5`

---

## 🧩 Edge Cases
- One array empty
- Odd vs Even total length
- Partition at index `0` or at array end
- Handled using `Integer.MIN_VALUE` and `Integer.MAX_VALUE`

---

## ⏱️ Complexity
- **Time:** `O(log(min(m, n)))`
- **Space:** `O(1)`

---

## ✅ Java Implementation

```java
class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        int m = nums1.length;
        int n = nums2.length;

        // Always binary search on smaller array
        if (m > n) {
            return findMedianSortedArrays(nums2, nums1);
        }

        int low = 0, high = m;

        while (low <= high) {
            int mid1 = low + (high - low) / 2;
            int mid2 = (m + n + 1) / 2 - mid1;

            int l1 = (mid1 == 0) ? Integer.MIN_VALUE : nums1[mid1 - 1];
            int l2 = (mid2 == 0) ? Integer.MIN_VALUE : nums2[mid2 - 1];
            int r1 = (mid1 == m) ? Integer.MAX_VALUE : nums1[mid1];
            int r2 = (mid2 == n) ? Integer.MAX_VALUE : nums2[mid2];

            if (l1 <= r2 && l2 <= r1) {
                if ((m + n) % 2 == 0) {
                    return (Math.max(l1, l2) + Math.min(r1, r2)) / 2.0;
                } else {
                    return Math.max(l1, l2);
                }
            } else if (l1 > r2) {
                high = mid1 - 1;
            } else {
                low = mid1 + 1;
            }
        }

        return 0.0;
    }
}
