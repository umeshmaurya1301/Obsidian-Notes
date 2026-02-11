# LT_992 – Subarrays with K Different Integers

**Link:** https://leetcode.com/problems/subarrays-with-k-different-integers/

---

## 📝 Problem Description
> [!info]
> Given an integer array `nums` and an integer `k`, return the number of **good subarrays** of `nums`.
>  
> A subarray is called **good** if it contains **exactly `k` distinct integers**.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [1,2,1,2,3], k = 2`  
> **Output:** `7`  
> **Explanation:**  
> The good subarrays are:  
> `[1,2]`, `[2,1]`, `[1,2]`, `[2,3]`, `[1,2,1]`, `[2,1,2]`, `[1,2,1,2]`

> [!example]
> **Input:** `nums = [1,2,1,3,4], k = 3`  
> **Output:** `3`  
> **Explanation:**  
> `[1,2,1,3]`, `[2,1,3]`, `[1,3,4]`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 2 * 10^4`  
> - `1 <= nums[i], k <= nums.length`

---

## 🔍 Intuition (Why Normal Sliding Window Fails)

This problem asks for **exactly `k` distinct integers** in a subarray.

Standard sliding window works when the condition is **monotonic** (once invalid, shrinking the window will eventually make it valid again in a predictable way).  
However, **"exactly `k` distinct" is NOT monotonic**.

When a window has exactly `k` distinct values, there can be **multiple valid subarrays ending at the same right pointer**.  
As soon as the right pointer moves forward and the window becomes invalid, we lose all those combinations at once.

---

## 🧠 Why Exactly K is Hard with Direct Sliding Window (Example)

Consider:

nums = [1,2,1,1,1,2,3,4,5,6], k = 3


Suppose at some point:

i = 1, j = 6
window = [2,1,1,1,2,3]
distinct = {1,2,3} ✅ exactly k


Now valid subarrays ending at `j = 6` are:

(1,6), (2,6), (3,6), (4,6), (5,6)


If we move `j` to `7`:

window = [2,1,1,1,2,3,4]
distinct = {1,2,3,4} ❌ (k+1 distinct)


Now to make the window valid again, we must move `i` one by one.  
But all previous valid combinations are already lost.  
Re-counting them leads to **O(n²)** in worst case.

👉 Hence, direct sliding window for **exactly K** is inefficient.

---

## 🔑 Key Insight

Instead of directly finding **exactly `k`**, we use this identity:

Subarrays with Exactly K distinct
= Subarrays with At Most K distinct

Subarrays with At Most (K - 1) distinct


This works because:

- `AtMost(K)` counts all subarrays having **≤ K** distinct elements  
- `AtMost(K-1)` counts all subarrays having **≤ K-1** distinct elements  
- Their difference leaves only subarrays with **exactly K** distinct elements

---

## 🪜 How At Most K Works (Sliding Window)

For **at most `k` distinct**, the condition is **monotonic**, so sliding window works.

Steps:

1. Expand `j` (right pointer)  
2. Maintain frequency map of elements  
3. If distinct count > `k`, move `i` (left pointer)  
4. For each `j`, number of valid subarrays ending at `j` is:  
(j - i + 1)


---

## 🧩 Edge Cases
- `k = 0` → answer is `0`  
- All elements same  
- All elements unique  
- Very small arrays  

---

## ⏱️ Complexity

- **Time:** `O(n)`  
- **Space:** `O(k)`

---

## ✅ Java Implementation

```java
class Solution {
 public int subarraysWithKDistinct(int[] nums, int k) {
     return atMost(nums, k) - atMost(nums, k - 1);
 }

 private int atMost(int[] nums, int limit) {
     if (limit < 0) return 0;

     int count = 0;
     Map<Integer, Integer> map = new HashMap<>();

     int i = 0;
     int j = 0;

     while (j < nums.length) {
         map.put(nums[j], map.getOrDefault(nums[j], 0) + 1);

         while (map.size() > limit) {
             map.put(nums[i], map.get(nums[i]) - 1);
             if (map.get(nums[i]) == 0) {
                 map.remove(nums[i]);
             }
             i++;
         }

         count += j - i + 1;
         j++;
     }

     return count;
 }
}
