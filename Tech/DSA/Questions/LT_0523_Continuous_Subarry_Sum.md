---
created: 2026-04-01 00:00
tags:
  - Arrays
  - PrefixSum
  - Hashing
  - Modulo
source: https://leetcode.com/problems/continuous-subarray-sum/
problem_id: "523"
difficulty: Medium
status: Completed
review_date:
---

# LT_0523 – Continuous Subarray Sum

**Link:** [Open Problem](https://leetcode.com/problems/continuous-subarray-sum/)

---

## 📝 Problem Description
> [!info]
> Given an integer array `nums` and an integer `k`, return `true` if the array has a **continuous subarray of size at least 2** whose sum is a multiple of `k`.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [23,2,4,6,7], k = 6`  
> **Output:** `true`  
> **Explanation:** `[2,4]` → sum = 6 (multiple of k)

> **Input:** `nums = [23,2,6,4,7], k = 6`  
> **Output:** `true`

> **Input:** `nums = [23,2,6,4,7], k = 13`  
> **Output:** `false`

---

## ⚠️ Constraints
> [!warning]
> - `1 ≤ nums.length ≤ 10⁵`
> - `0 ≤ nums[i] ≤ 10⁹`
> - `0 ≤ sum(nums) ≤ 2³¹ - 1`
> - `1 ≤ k ≤ 2³¹ - 1`

---

## 💡 Core Intuition

### 🔥 Step 1: Convert to Prefix Sum

We know:
```text
subarraySum(i → j) = prefix[j] - prefix[i]
```

We need:
```text
(prefix[j] - prefix[i]) % k == 0
```

---

### 🔥 Step 2: Key Mathematical Insight

```text
(A - B) % k == 0
⇔ A % k == B % k
```

👉 This is the **entire problem**

---

### 🧠 Meaning

If at two indices:
```text
prefix[j] % k == prefix[i] % k
```

Then:
```text
subarray (i+1 → j) is divisible by k
```

---

## 🧠 Mental Model

Think of remainders as buckets:

```text
k = 6 → buckets = {0,1,2,3,4,5}
```

While iterating:
```text
5 → 1 → 5
```

👉 Same remainder appears again  
👉 Means: in between sum is divisible by k ✅

---

## 🔁 Dry Run

`nums = [23,2,4,6,7], k = 6`

| i | sum | sum % 6 |
|--|-----|--------|
| 0 | 23 | 5 |
| 1 | 25 | 1 |
| 2 | 29 | 5 ✅ |

👉 Same remainder `5` seen again  
👉 `29 - 23 = 6` → valid subarray `[2,4]`

---

## 💡 Approach 1: Prefix Sum + HashMap

### 🔥 Idea
- Store: `remainder → first index`
- If same remainder appears again:
  - Check subarray length ≥ 2

---

### ⚠️ Important Conditions

#### 1. Subarray length ≥ 2

```java
if (i - map.get(rem) > 1)
```

👉 Ensures valid subarray size

---

#### 2. Base Case

```java
map.put(0, -1);
```

👉 Means:
```text
prefix sum before array = 0
```

👉 Handles subarrays starting from index 0

---

## ✅ Java Implementation

```java
class Solution {
    public boolean checkSubarraySum(int[] nums, int k) {
        Map<Integer, Integer> map = new HashMap<>();
        map.put(0, -1); // base case

        int sum = 0;

        for (int i = 0; i < nums.length; i++) {
            sum += nums[i];

            int rem = sum % k;

            if (map.containsKey(rem)) {
                if (i - map.get(rem) > 1) {
                    return true;
                }
            } else {
                map.put(rem, i);
            }
        }

        return false;
    }
}
```

---

## 🧠 Discussion Insights (Important)

### 🔥 Why not store full prefix sum?

❌ Wrong:
```java
set.add(sum);
```

👉 Leads to:
```text
O(N²) approach (checking multiples of k)
```

---

### ✅ Correct Thinking

Instead of:
```text
preSum - k*n
```

Use:
```text
preSum % k
```

👉 Same logic, optimized

---

### 🔥 Why HashMap instead of Set?

| Structure | Use |
|----------|-----|
| Set | Only checks existence |
| Map | Stores index → needed for length ≥ 2 |

---

### 🔥 Why `i - prevIndex > 1`?

```text
Subarray length = i - prevIndex
```

We need:
```text
≥ 2
```

---

### 🔥 Why `map.put(0, -1)`?

Handles:
```text
subarray starting from index 0
```

Example:
```text
[2,4], k=6 → valid
```

Without this → missed case ❌

---

### 🔥 Your Approach vs Optimal

| Your Idea | Optimized Version |
|----------|-----------------|
| preSum - k*n loop | modulo trick |
| Set of sums | Map of remainders |
| O(N²) | O(N) |
| complex check() | single pass |

---

## ⏱️ Complexity

| Metric | Value |
|------|------|
| Time | O(N) |
| Space | O(N) |

---

## 🧩 Pattern

- Prefix Sum
- Modulo Arithmetic
- HashMap
- Subarray Problems

---

## ⚠️ Pitfalls

- Forgetting `map.put(0, -1)`
- Not checking subarray length ≥ 2
- Using Set instead of Map
- Misunderstanding modulo logic

---

## 🚀 Optimization / Variants

- Count subarrays divisible by k → frequency map
- Subarray sum equals k → prefix sum + hashmap
- Binary array variants → same pattern

---

## 🧠 One-Line Takeaway

```text
Same remainder ⇒ subarray sum divisible by k
```