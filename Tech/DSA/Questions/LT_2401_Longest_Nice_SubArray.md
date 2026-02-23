**Link:** https://leetcode.com/problems/longest-nice-subarray/

---

## 📝 Problem Description
> [!info]
> You are given an array of positive integers `nums`.  
> You must return the length of the **longest nice subarray**.
>  
> A subarray is considered **nice** if the bitwise AND (`&`) of every pair of elements in the subarray is exactly `0`. (In other words, no two numbers share a set bit).

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [1,3,8,48,10]`  
> **Output:** `3`  
> **Explanation:** > Best nice subarray: `[3,8,48]` → max length = 3. 
> 3 (000011), 8 (001000), 48 (110000) share no bits.

> [!example]
> **Input:** `nums = [3,1,5,11,13]`  
> **Output:** `1`  
> **Explanation:** > Any subarray of length 2 or more contains numbers that share a bit. Longest nice subarray length is 1.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 10^5`  
> - `1 <= nums[i] <= 10^9`

---

## 🔍 Intuition

We need the longest subarray where **no two numbers share the same bit**.
Instead of checking every pair, we can track all the bits currently "in use" within our window using a single integer `mask`.

This is a powerful combo:
> 🟢 *Sliding Window + Bitmasking*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Optimal Bitmask Sliding Window
**Why this is the best:**
• Uses a single integer (`mask`) to represent all bits in the current window.
• Shrinks the window exactly when a bit collision occurs.
• Clean, fast `O(n)` time, and `O(1)` space.

```java
class Solution {
    public int longestNiceSubarray(int[] nums) {

        int left = 0;
        int mask = 0;
        int maxLen = 0;

        for (int right = 0; right < nums.length; right++) {

            // shrink window until no conflict
            while ((mask & nums[right]) != 0) {
                mask ^= nums[left];
                left++;
            }

            // add current number
            mask |= nums[right];

            // update answer
            maxLen = Math.max(maxLen, right - left + 1);
        }

        return maxLen;
    }
}