---
created: 2026-06-22 00:00
tags:
  - dsa
  - dynamic-programming
  - array
  - hash-table
source: https://leetcode.com/problems/delete-and-earn/
problem_id: "740"
difficulty: Medium
status: Solved
review_date:
---
# LT_0740 – Delete And Earn

**Link:** [Open Problem](https://leetcode.com/problems/delete-and-earn/)

---

## 📝 Problem Description
> [!info]
> You are given an integer array `nums`. You want to maximize the number of points you get by performing the following operation any number of times:
>
> - Pick any `nums[i]` and delete it to earn `nums[i]` points. Afterwards, you must delete every element equal to `nums[i] - 1` and every element equal to `nums[i] + 1`.
>
> Return the maximum number of points you can earn by applying the above operation some number of times.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [3,4,2]`
> **Output:** `6`
> **Explanation:** Delete 4 to earn 4 points (3 is also deleted). Then delete 2 to earn 2 points. Total = 6.

> [!example]
> **Input:** `nums = [2,2,3,3,3,4]`
> **Output:** `9`
> **Explanation:** Delete a 3 to earn 3 points — all 2s and 4s are deleted. Repeat for the remaining 3s. Total = 9.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 2 * 10^4`
> - `1 <= nums[i] <= 10^4`

---

## 🔍 Intuition

If I take value `x`, I must delete all `x-1` and `x+1`. This means adjacent values can never be taken together — which is exactly the **House Robber** constraint. The key insight is to collapse duplicates first: instead of tracking individual elements, build a `points[]` array where `points[i]` = sum of all occurrences of value `i`. Now the problem becomes — given a points array, pick non-adjacent indices to maximise total points. The recurrence is: at each index `i`, either take `points[i]` and jump to `i+2`, or skip and move to `i+1`. Top-down memoization fills this out in O(maxValue) states.

> 🟢 *House Robber — Top-Down Memoization on Frequency Points Array*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Top-Down DP (House Robber on Points Array)

**Why this works:**
- Taking value `x` forbids `x-1` and `x+1`, which maps directly to the "can't rob adjacent houses" rule.
- Collapsing duplicates into `points[i]` eliminates repeated sub-problems — we only need to decide once per distinct value.
- Memoization ensures each of the O(maxValue) states is computed exactly once.

**Dry Run** (`nums = [2,2,3,3,3,4]`):

Points array after preprocessing:
```
index:  0  1  2  3  4
points: 0  0  4  9  4
```

| Call         | take                        | skip           | memo[i] |
|--------------|-----------------------------|----------------|---------|
| `helper(4)`  | base: `i == len-1`          | —              | 4       |
| `helper(3)`  | `helper(5)=0 + points[3]=9` | `helper(4)=4`  | 9       |
| `helper(2)`  | `helper(4)=4 + points[2]=4` | `helper(3)=9`  | 9       |
| `helper(1)`  | `helper(3)=9 + points[1]=0` | `helper(2)=9`  | 9       |
| `helper(0)`  | `helper(2)=9 + points[0]=0` | `helper(1)=9`  | 9       |

Answer = **9** ✅ (take all 3s: 3+3+3 = 9)

```java
class Solution {
    public int deleteAndEarn(int[] nums) {
        int max = 0;
        for (int num : nums) {
            max = Math.max(max, num);
        }

        // Step 1: Prepare points array
        int[] points = new int[max + 1];
        for (int num : nums) {
            points[num] += num;
        }

        // Step 2: Memoization array
        int[] memo = new int[max + 1];
        Arrays.fill(memo, -1);

        return helper(0, points, memo);
    }

    private int helper(int i, int[] points, int[] memo) {
        int len = memo.length;
        if (i == len-1) return points[len-1];
        if (i >= len) return 0;
        if (memo[i] != -1) return memo[i];

        // Either take i or skip it
        int take = helper(i + 2, points, memo) + points[i];
        int skip = helper(i + 1, points, memo);

        memo[i] = Math.max(take, skip);
        return memo[i];
    }
}
```

---

## 🔑 Key Insights
- `points[i] = 0` for values not present in `nums` — they act as free skips and don't disrupt the recurrence.
- The `helper` goes **forward** (`i+1`, `i+2`), which is equivalent to the classic backward House Robber recurrence `dp[i] = max(dp[i-1], dp[i-2] + points[i])` — same answer, different traversal direction.
- The base case `i == len-1` (not `i == 0`) is needed because we start from index 0 going forward; reaching the last index means there's nothing left to skip into.

---

## ⚠️ Pitfalls
> [!warning]
> - Forgetting the `i == len-1` base case causes an off-by-one: `helper(len)` returns 0 but `helper(len-1)` never gets called with its correct value.
> - Using `memo[-1] != -1` guard before the bounds check would cause `ArrayIndexOutOfBoundsException` — bounds check must come first.
> - `points[num] += num` not `+= 1` — we accumulate the **value**, not the count.

---

## ⏱️ Complexity
- **Time:** `O(n + maxValue)` — O(n) to build `points[]`, O(maxValue) DP states each computed once.
- **Space:** `O(maxValue)` — `points[]`, `memo[]`, and recursion stack all scale with `maxValue`.
