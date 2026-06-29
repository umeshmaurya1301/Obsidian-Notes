---
created: 2026-06-28 00:00
tags:
  - dsa
  - array
  - two-pointers
  - dynamic-programming
  - stack
  - monotonic-stack
source: https://leetcode.com/problems/trapping-rain-water/description/
problem_id: "42"
difficulty: Hard
status: Solved
review_date:
---
# LT_0042 – Trapping Rain Water

**Link:** [Open Problem](https://leetcode.com/problems/trapping-rain-water/description/)

---

## 📝 Problem Description
> [!info]
> Given `n` non-negative integers representing an elevation map where the width of each bar is `1`, compute how much water it can trap after raining.

---

## 🧪 Examples
> [!example]
> **Input:** `height = [0,1,0,2,1,0,1,3,2,1,2,1]`
> **Output:** `6`
> **Explanation:** The elevation map traps 6 units of rain water in the valleys between bars.

> [!example]
> **Input:** `height = [4,2,0,3,2,5]`
> **Output:** `9`

---

## ⚠️ Constraints
> [!warning]
> - `n == height.length`
> - `1 <= n <= 2 * 10^4`
> - `0 <= height[i] <= 10^5`

---

## 🔍 Intuition

Water trapped at any position `i` equals the minimum of the tallest bar to its left and the tallest bar to its right, minus its own height:

```
water[i] = min(maxLeft[i], maxRight[i]) - height[i]
```

The brute force computes `maxLeft` and `maxRight` for every `i` by scanning — `O(n²)`. The DP approach precomputes both in arrays — `O(n)` time and space. The key insight for Two Pointers: **we never need both arrays at the same time.** If `height[left] <= height[right]`, the right side is guaranteed to provide a wall at least as tall as `height[left]`, so `leftMax` is the binding constraint for the left position regardless of what `rightMax` actually is — and we can safely compute water there without scanning right. This eliminates the extra arrays entirely.

> 🟢 *Two Pointers — Space-Optimised*

---

## 🧠 Evolution of Solutions

### 🔵 Approach 1 — Brute Force

For each index, scan left to find `maxLeft` and scan right to find `maxRight`.

- **Time:** `O(n²)` — double scan per element.
- **Space:** `O(1)`

---

### 🔵 Approach 2 — DP (Precomputed Max Arrays)

Precompute `leftMax[]` (max from 0 to i) and `rightMax[]` (max from i to n-1), then one pass to accumulate water.

- **Time:** `O(n)`
- **Space:** `O(n)` — two extra arrays.

---

### ✅ Approach 3 — Two Pointers (Space-Optimised)

**Why this works:**

- Water at position `left` = `min(leftMax, rightMax) - height[left]`.
- When `height[left] <= height[right]`: the right pointer is a wall at least as tall as the current left bar. So `rightMax >= height[right] >= height[left]`, meaning even the worst-case right boundary is sufficient. The limiting factor is `leftMax` — compute water on the left and advance.
- When `height[left] > height[right]`: the symmetric argument applies — process the right side.
- Both pointers converge inward, each element processed exactly once.

**Dry Run** (`height = [4,2,0,3,2,5]`):

| `left` | `right` | `leftMax` | `rightMax` | `h[l]` | `h[r]` | Action | `water` |
|--------|---------|-----------|------------|--------|--------|--------|---------|
| 0      | 5       | 4         | 5          | 4      | 5      | h[l]≤h[r] → leftMax=4, +0, l++ | 0 |
| 1      | 5       | 4         | 5          | 2      | 5      | h[l]≤h[r] → leftMax=4, +2, l++ | 2 |
| 2      | 5       | 4         | 5          | 0      | 5      | h[l]≤h[r] → leftMax=4, +4, l++ | 6 |
| 3      | 5       | 4         | 5          | 3      | 5      | h[l]≤h[r] → leftMax=4, +1, l++ | 7 |
| 4      | 5       | 4         | 5          | 2      | 5      | h[l]≤h[r] → leftMax=4, +2, l++ | 9 |
| 5      | 5       | 5         | 5          | 5      | 5      | h[l]≤h[r] → leftMax=5, +0, l++ | 9 |
| 6 > 5  | —       | —         | —          | —      | —      | exit loop | **9** |

```java
class Solution {
    public int trap(int[] height) {
        int len=height.length;
        int left=0;
        int right=len-1;

        int leftMax=height[0];
        int rightMax=height[len-1];

        int water=0;

        while (left<=right) {
            if(height[left] <= height[right]) {
                leftMax = Math.max(leftMax, height[left]);
                water += leftMax - height[left];
                left++;
            } else {
                rightMax = Math.max(rightMax, height[right]);
                water += rightMax - height[right];
                right--;
            }
        }
        return water;
    }
}
```

---

## 🔑 Key Insights
- `water[i] = min(maxLeft, maxRight) - height[i]` is the core formula; everything else is an optimisation on how you compute those two maxes.
- The pointer with the **smaller current height** is always processed — that side's max is the binding constraint regardless of what the other side turns out to be.
- `leftMax` and `rightMax` are initialised to `height[0]` and `height[len-1]` respectively — they are updated before adding water, so a bar that extends the max contributes `0` water (max - height = 0).
- The `while (left <= right)` condition (not `<`) ensures the pointers meet and the last element is processed.

---

## ⚠️ Pitfalls
> [!warning]
> - Using `left < right` instead of `left <= right` — skips the middle element when pointers converge, causing under-count.
> - Updating `leftMax` / `rightMax` **after** computing water instead of before — produces negative water on bars that are new maximums.
> - Confusing which pointer to move: always move the side whose **current height** is smaller, not whose max is smaller.

---

## ⏱️ Complexity
- **Time:** `O(n)` — each element visited exactly once.
- **Space:** `O(1)` — only four integer variables; no auxiliary arrays.
