---
created: 2026-07-11 18:14
tags:
  - dsa
  - array
  - dynamic-programming
source: https://leetcode.com/problems/maximum-product-subarray/
problem_id: "152"
difficulty: Medium
status: Solved
review_date:
---
# LT_152 – Maximum Product SubArray

**Link:** [Open Problem](https://leetcode.com/problems/maximum-product-subarray/)

---

## 📝 Problem Description
> [!info]
> Given an integer array `nums`, find a subarray that has the largest product, and return the product.
>
> The test cases are generated so that the answer will fit in a **32-bit** integer.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [2,3,-2,4]`
> **Output:** `6`
> **Explanation:** `[2,3]` has the largest product `6`.

> [!example]
> **Input:** `nums = [-2,0,-1]`
> **Output:** `0`
> **Explanation:** The result cannot be `2`, because `[-2,-1]` is not a subarray.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 2 * 10^4`
> - `-10 <= nums[i] <= 10`
> - The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.

---

## 🔍 Intuition

The twist here versus "maximum sum subarray" (Kadane) is the **sign flip**: a negative number turns a large positive product into a large negative one, and — crucially — a *second* negative can turn a large negative product back into the maximum. So tracking only the running max is not enough; the current minimum (most negative) product is a candidate for the *next* max as soon as we hit another negative. That's why I carry **both** `maxEnding` and `minEnding` at each index. At every element the best product ending here is one of three things: the number alone (restart), `maxEnding*num`, or `minEnding*num`. This also handles zeros for free — multiplying by `0` collapses both, and the standalone `num` option lets the window restart on the next element.

> 🟢 *Kadane's Variant — Track Max & Min (DP on running extremes)*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Kadane's Variant (Track Running Max & Min)

**Why this works:**
- The optimal product ending at `i` must be `num` (fresh start), `maxEnding*num`, or `minEnding*num` — no other candidate can beat these because products are built multiplicatively from the previous extremes.
- Keeping the running **minimum** captures the "large negative that a future negative flips into a large positive" case, which a max-only Kadane would miss.
- Using `temp` variables ensures `maxEnding` and `minEnding` are both updated from the *same* previous state, not a half-updated one.

**Dry Run** (`nums = [2,3,-2,4]`):

| `i` | `num` | `maxEnding*num` | `minEnding*num` | `tempMax` | `tempMin` | `answer` |
|-----|-------|-----------------|-----------------|-----------|-----------|----------|
| init | 2 | — | — | 2 | 2 | 2 |
| 1 | 3 | `2*3=6` | `2*3=6` | `max(3,6,6)=6` | `min(3,6,6)=3` | 6 |
| 2 | -2 | `6*-2=-12` | `3*-2=-6` | `max(-2,-12,-6)=-2` | `min(-2,-12,-6)=-12` | 6 |
| 3 | 4 | `-2*4=-8` | `-12*4=-48` | `max(4,-8,-48)=4` | `min(4,-8,-48)=-48` | 6 |

Final `answer = 6`. Note how at `i=2` the `minEnding` becomes `-12`, kept alive in case a later negative flips it positive.

```java
class Solution {
    public int maxProduct(int[] nums) {
        
        int maxEnding = nums[0];
        int minEnding = nums[0];
        int answer = nums[0];

        for (int i=1; i<nums.length; i++) {
            int num = nums[i];

            int tempMax = Math.max( num, Math.max (maxEnding*num, minEnding*num) );
            int tempMin = Math.min( num, Math.min (maxEnding*num, minEnding*num) );

            maxEnding = tempMax;
            minEnding = tempMin;

            answer = Math.max (answer, maxEnding);
        }

        return answer;
    }
}
```

---

## 🔑 Key Insights
- Carry **both** max and min ending here — a negative number swaps their roles, so today's min can become tomorrow's max.
- The `num` term in each `Math.max`/`Math.min` is the **restart** option; it resets the window after a `0` or when the accumulated product is worse than starting fresh.
- Zeros need no special-casing: they zero out both extremes, and the next element restarts via the standalone `num`.
- Initialize all three (`maxEnding`, `minEnding`, `answer`) to `nums[0]`, then iterate from index `1`.

---

## ⚠️ Pitfalls
> [!warning]
> - Don't update `maxEnding` before computing `minEnding` — you'd feed a mutated max into the min calculation. Use the `temp` variables.
> - Don't forget the standalone `num` candidate; without it, a single large positive after a run of small products (or after a zero) is missed.
> - A max-only Kadane fails on inputs like `[-2,3,-4]` where the answer (`24`) comes from flipping a negative min.

---

## ⏱️ Complexity
- **Time:** `O(n)` — single pass.
- **Space:** `O(1)` — three scalar variables.
