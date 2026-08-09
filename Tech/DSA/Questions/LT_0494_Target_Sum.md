---
created: 2026-08-09 18:31
tags:
  - dsa
  - dynamic-programming
  - hashing
  - memoization
source: https://leetcode.com/problems/target-sum/
problem_id: "494"
difficulty: Medium
status: Solved
review_date:
---
# LT_0494 – Target Sum

**Link:** [Open Problem](https://leetcode.com/problems/target-sum/)

---

## 📝 Problem Description
> [!info]
> You are given an integer array `nums` and an integer `target`.
>
> You want to build an expression out of `nums` by adding one of the symbols `'+'` and `'-'` before each integer in `nums` and then concatenate all the integers.
>
> - For example, if `nums = [2, 1]`, you can add a `'+'` before `2` and a `'-'` before `1` and concatenate them to build the expression `"+2-1"`.
>
> Return the number of different expressions that you can build, which evaluates to `target`.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [1,1,1,1,1], target = 3`
> **Output:** `5`
> **Explanation:** There are 5 ways to assign symbols to make the sum of `nums` be target 3.
> ```
> -1 + 1 + 1 + 1 + 1 = 3
> +1 - 1 + 1 + 1 + 1 = 3
> +1 + 1 - 1 + 1 + 1 = 3
> +1 + 1 + 1 - 1 + 1 = 3
> +1 + 1 + 1 + 1 - 1 = 3
> ```

> [!example]
> **Input:** `nums = [1], target = 1`
> **Output:** `1`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 20`
> - `0 <= nums[i] <= 1000`
> - `0 <= sum(nums[i]) <= 1000`
> - `-1000 <= target <= 1000`

---

## 🔍 Intuition

Every element gets exactly one of two signs, so the whole search space is a **binary tree of depth `n`** with `2^n` leaves — and I need to count the leaves that land on `target`. The natural recursion is "assign a sign to `nums[idx]`, carry the *remaining* target forward, recurse on `idx+1`", and since I'm counting rather than deciding, the two branches get **added**, not OR-ed.

The trick that keeps it readable is tracking `curr` as **how much target is still owed** rather than the running sum. A `'+'` on `nums[idx]` pays down the debt (`curr - nums[idx]`); a `'-'` increases it (`curr + nums[idx]`). Then success is just `curr == 0` at the moment the array runs out.

`n <= 20` means brute force at `2^20 ≈ 10⁶` would actually pass — but the state `(idx, curr)` repeats heavily (all the `1`s in Example 1 make most paths converge), so memoising is both cheap and principled. The wrinkle is that `curr` **goes negative**, which a plain `int[][]` can't index — hence the `HashMap` with a `"idx,curr"` string key, sidestepping the offset arithmetic entirely.

> 🟢 *Count-the-Ways DP over (index, remaining target) with a Hashed State Key*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Top-Down DP with a `HashMap` Memo

**Why this works:**
- **Both branches are always taken and summed:** unlike a subset-sum *predicate*, there's no early exit — `plusWays + minusWays` accumulates every sign assignment that reaches `target`, and each leaf is counted exactly once because the sign choices form a complete binary tree.
- **`curr` folds sign choices into one number.** Carrying "remaining target" instead of "running sum plus a separate target" halves the state, and makes the success test the single condition `curr == 0`.
- **Hashing `idx + "," + curr` handles negative and out-of-range `curr` for free.** `curr` roams over `[target - sum, target + sum]`, so an array memo would need an offset of `sum`; the map skips that bookkeeping and only materialises states actually visited.

**Dry Run** (`nums = [1,1,1,1,1], target = 3`):

Reading bottom-up, `f(idx, curr)` = ways to settle `curr` using `nums[idx..4]`:

| `idx` | non-zero states | value |
|-------|-----------------|-------|
| 5 (base) | `curr = 0` | 1 |
| 4 | `f(4,1)`, `f(4,-1)` | 1, 1 |
| 3 | `f(3,2)=1`, `f(3,0)=2`, `f(3,-2)=1` | — |
| 2 | `f(2,3)=1`, `f(2,1)=3`, `f(2,-1)=3`, `f(2,-3)=1` | — |
| 1 | `f(1,4)=1`, `f(1,2)=4`, … | — |
| 0 | `f(0,3) = f(1,2) + f(1,4) = 4 + 1` | **5** |

Result: `5` ✅ — the Pascal's-triangle shape in the middle column is exactly the memo paying off.

```java
class Solution {
    public int findTargetSumWays(int[] nums, int target) {
        Map<String, Integer> dp = new HashMap<>();
        return dfs(nums, dp, 0, target);

    }

    private int dfs(int[] nums, Map<String, Integer> dp, int idx, int curr) {
        int len = nums.length;
        if (curr==0 && idx==len) return 1;
        if (idx>=nums.length) return 0;

        String key = idx + "," + curr;
        if(dp.containsKey(key)) return dp.get(key);

        int plusWays = dfs(nums, dp, idx+1, curr - nums[idx]);
        int minusWays = dfs(nums, dp, idx+1, curr + nums[idx]);
        int ways = plusWays + minusWays;
        dp.put(key, ways);
        return ways;
    }
}
```

- **Time:** `O(n · sum)` — at most `20 × 2001` reachable states, each `O(1)` amortised plus string-key construction · **Space:** `O(n · sum)` map entries + `O(n)` recursion depth

---

## 🔑 Key Insights
- **The base case is an ordered pair of checks, and the order is load-bearing.** `curr == 0 && idx == len` must be tested *before* `idx >= len`, otherwise a completed, successful assignment falls through to `return 0`. Note this is the opposite of [[LT_0416_Partition_Equal_Subset_Sum]], where hitting the target early is a legitimate success — here every element must be signed, so both conditions are required together.
- **Counting ⇒ add the branches; deciding ⇒ OR them.** Same recursion tree as subset-sum, different accumulator. Spotting which one a problem wants is most of the work.
- **A `HashMap` memo is the escape hatch for signed or sparse state.** It costs constant-factor speed (string building, boxing) but removes the entire offset-index class of bugs. With `n <= 20` that trade is clearly worth it.
- **The classic rewrite:** let `P` be the positively-signed subset. Then `P - (sum - P) = target` ⇒ `P = (sum + target) / 2`, turning this into a plain subset-sum count — `O(n · sum)` with a 1D array and no signed indices. Worth knowing as the follow-up answer.

---

## ⚠️ Pitfalls
> [!warning]
> - **Indexing a plain `int[][]` by `curr`.** `curr` legitimately goes negative, so an unoffset array throws `ArrayIndexOutOfBoundsException`. Either add a `+sum` offset or use the map, as here.
> - **Stopping the recursion when `curr == 0` mid-array.** Tempting, but wrong: the remaining elements still need signs, and e.g. `[1,-1]`-style cancellations mean there may be many further valid completions. Every index must be consumed.
> - **`sum + target` being odd in the subset-sum rewrite.** If you take the `P = (sum + target) / 2` shortcut, an odd numerator (or `|target| > sum`) means zero ways — guard it, or integer division silently returns a wrong count.

---

## ⏱️ Complexity
- **Time:** `O(n · sum)` — bounded by the number of distinct `(idx, curr)` states
- **Space:** `O(n · sum)` for the memo, plus `O(n)` recursion stack
