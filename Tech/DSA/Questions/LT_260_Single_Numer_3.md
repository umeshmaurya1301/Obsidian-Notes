---
title: Single Number III
difficulty: Medium
tags: Bit_Manipulation
link: https://leetcode.com/problems/single-number-iii/
---

# Problem Statement

Given an integer array `nums`, in which exactly two elements appear only once and all the other elements appear exactly twice. Find the two elements that appear only once.

## Example

```
Input: [2, 4, 2, 14, 3, 7, 7, 3]
Output: [4, 14]
```

In this example, 14 and 4 are distinct.

# Approach

## Key Insight

If two numbers are distinct, there will be at least one bit that will be different.

In the case of 14 and 4:
- Binary of 14: `1110`
- Binary of 4:  `0100`

The second and fourth bits are different.

## Using Buckets Concept

We will use the concept of buckets and isolate the rightmost set bit to separate the two unique numbers.

### Rightmost Set Bit Isolation

We can take either the rightmost set bit or the leftmost set bit. Here we'll use the rightmost set bit.

```
if num =                    1  0  1  0  1  0  0 
then num-1 =                1  0  1  0  0  1  1    -> Everything right of the rightmost set bit set to zero, every bit right to that set to one, rest are same.
num & (num - 1) =           1  0  1  0  0  0  0    -> Everything from rightmost set bit set to zero in the right direction, rest is same.
(num & (num - 1)) ^ num =   0  0  0  0  1  0  0    -> Isolation of rightmost set bit
```

### Algorithm Steps

Now in the example where 14 and 4 are unique:

1. Let `num = 14 ^ 4 = 1010`
2. Compute `(num & (num - 1)) = 0010` to get the rightmost different bit
3. Create two buckets:
   - **Bucket 1**: All numbers whose second bit is 1 → `[2, 2, 14, 3, 3, 7, 7]`
   - **Bucket 2**: All numbers whose second bit is 0 → `[4]`
4. XOR all numbers in bucket 1 and bucket 2 to get the desired answer

# Solution

```java
class Solution {
    public int[] singleNumber(int[] nums) {
        // Get XOR of all numbers
        int xor = 0;
        for (int num : nums) {
            xor ^= num;
        }
        
        // Isolate the rightmost set bit
        int rightmostSetBit = (xor & (xor - 1)) ^ xor;
        
        // Create two buckets
        int bucket1 = 0, bucket2 = 0;
        for (int num : nums) {
            if ((num & rightmostSetBit) != 0) {
                bucket1 ^= num;
            } else {
                bucket2 ^= num;
            }
        }
        
        return new int[]{bucket1, bucket2};
    }
}
```

# Time and Space Complexity

- **Time Complexity**: O(n) - Single pass through the array
- **Space Complexity**: O(1) - Only using constant extra space

# Remarks

- This approach efficiently separates the two unique numbers using bit manipulation
- The rightmost set bit isolation technique is a common pattern in bit manipulation problems


