

**Link:** https://leetcode.com/problems/maximum-erasure-value/

---

## 📝 Problem Description
> [!info]
> You are given an array of positive integers `nums`.  
> You must erase **exactly one subarray** and return the **maximum possible sum** of elements in the erased subarray.
>  
> A subarray is valid only if **all its elements are unique**.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [4,2,4,5,6]`  
> **Output:** `17`  
> **Explanation:**  
> Best subarray: `[2,4,5,6]` → sum = 17

> [!example]
> **Input:** `nums = [5,2,1,2,5,2,1,2,5]`  
> **Output:** `8`  
> **Explanation:**  
> Best unique subarray is `[5,2,1]` or `[1,2,5]` → sum = 8

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 10^5`  
> - `1 <= nums[i] <= 10^4`

---

## 🔍 Intuition

We need the **maximum sum of a subarray with all unique elements**.

This is a classic:
> 🟢 *Sliding Window with uniqueness + running sum*

---

## 🧠 Evolution of Solutions

You can solve this problem in multiple ways.  
Below are **three approaches**, exactly as discussed:

---

## ❌ Solution 1 — Wrong + Over-Engineered + O(n²)

### Why it’s bad:
• Recomputes sum using a loop → `O(n)` inside window  
• Overall → **O(n²)**  
• Too much logic for a simple sliding window problem

```java
class Solution {
    public int maximumUniqueSubarray(int[] nums) {
        int len = nums.length;
        if (len == 1)
            return nums[0];
        int i = 0;
        int j = 1;
        Map<Integer, Integer> map = new HashMap<>();
        map.put(nums[i], i);
        int sum = nums[i];
        int globalMax = Integer.MIN_VALUE;
        while (j < len) {
            int val = nums[j];
            if (map.containsKey(val)) {
                int prevIdx = map.get(val);
                int tempSum = 0;
                for (int idx = i; idx <= prevIdx; idx++)
                    tempSum += nums[idx];
                sum = sum - tempSum;
                i = prevIdx + 1;

                map.put(val, j);
                sum += val;
                j++;
            } else {
                map.put(val, j);
                j++;
                sum += val;
            }
            globalMax = Math.max(sum, globalMax);
        }
        return globalMax;
    }
}

⚠️ Solution 2 — Correct but Over-Engineered
Why it works:

• Uses sliding window + Set
• Removes elements one by one when duplicate appears
Why it’s not optimal style:

• You shrink blindly instead of jumping using last index
• Still correct, but not the cleanest

class Solution {
    public int maximumUniqueSubarray(int[] nums) {
        int n = nums.length;
        int left = 0, right = 0;
        int sum = 0, max = 0;
        Set<Integer> set = new HashSet<>();

        while (right < n) {
            if (!set.contains(nums[right])) {
                set.add(nums[right]);
                sum += nums[right];
                max = Math.max(max, sum);
                right++;
            } else {
                set.remove(nums[left]);
                sum -= nums[left];
                left++;
            }
        }

        return max;
    }
}

✅ Solution 3 — Correct + Simplified + Best
Why this is the best:

• Uses Map → last seen index
• Jumps i directly instead of removing blindly
• Maintains running sum → no recomputation
• Clean, fast, and interview-ready

class Solution {
    public int maximumUniqueSubarray(int[] nums) {
        int len = nums.length;
        if (len == 1) return nums[0];

        int i = 0;
        int j = 0;

        Map<Integer, Integer> map = new HashMap<>();
        int sum = 0;
        int globalMax = 0;

        while (j < len) {
            int val = nums[j];

            if (map.containsKey(val) && map.get(val) >= i) {
                int prevIdx = map.get(val);

                // shrink window from left until i > prevIdx
                while (i <= prevIdx) {
                    sum -= nums[i];
                    i++;
                }
            }

            map.put(val, j);
            sum += val;
            globalMax = Math.max(globalMax, sum);
            j++;
        }

        return globalMax;
    }
}

🧠 Final Mental Template

    Maximum / Longest Subarray with Unique Elements
    → Sliding Window + Map (last seen index) + Running Sum

⏱️ Complexity
Solution	Time	Space	Verdict
1st	O(n²)	O(n)	❌ Wrong / Over-Engineered
2nd	O(n)	O(n)	⚠️ Correct but indirect
3rd	O(n)	O(n)	✅ Best / Optimal