---
title: Counting Bits
difficulty: Easy
tags: Bit_Manipulation
link: https://leetcode.com/problems/counting-bits/
---

# Approach

Step 1 - We want `ans[i]` = number of 1s (set bits) in the binary representation of `i`.

Step 2 - Observe the relation between i and i/2

If you divide a number by 2 (or right shift by 1), you're just **dropping the last bit** from its binary representation.

Step 3 - Translate that to code logic

**Part 1: Right-shifting by one (`i >> 1`)**

Right-shifting by one (`i >> 1`) means integer divide by 2.

**Part 2: `(i & 1)`**

This extracts the **last bit** of `i`:

- If `i` is even → last bit = 0
- If `i` is odd → last bit = 1

So `(i & 1)` gives either 0 or 1, which exactly represents **"did we drop a 1?"**

# Solution

```java
class Solution {
    public int[] countBits(int n) {
        int[] ans = new int[n + 1];
        
        for (int i = 1; i <= n; i++) {
            ans[i] = ans[i >> 1] + (i & 1);
        }
        
        return ans;
    }
}
```
