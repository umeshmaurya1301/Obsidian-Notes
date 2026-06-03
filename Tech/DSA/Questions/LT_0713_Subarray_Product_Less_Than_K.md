---
created: 2026-06-01 10:00
tags:
  - dsa
  - arrays
  - sliding-window
source: https://leetcode.com/problems/subarray-product-less-than-k/
problem_id: "713"
difficulty: Medium
status: Solved
review_date:
---
# LT_0713 – Subarray Product Less Than K

**Link:** [Open Problem](https://leetcode.com/problems/subarray-product-less-than-k/description/)

---

## 📝 Problem Description
> [!info]
> Given an array of integers `nums` and an integer `k`, return the number of **contiguous subarrays** where the product of all the elements in the subarray is **strictly less than** `k`.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [10,5,2,6]`, `k = 100`
> **Output:** `8`
> **Explanation:** The 8 subarrays with product < 100 are:
> `[10]`, `[5]`, `[2]`, `[6]`, `[10,5]`, `[5,2]`, `[2,6]`, `[5,2,6]`
> Note: `[10,5,2]` is excluded — product `100` is not strictly less than `100`.

> [!example]
> **Input:** `nums = [1,2,3]`, `k = 0`
> **Output:** `0`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 3 * 10^4`
> - `1 <= nums[i] <= 1000`
> - `0 <= k <= 10^6`

---

## 🔍 Intuition

The key observation is that if a window `[left, right]` has product `< k`, then every sub-window ending at `right` with a start anywhere from `left` to `right` also has product `< k` — removing elements from the left can only decrease the product. This means at each `right` we can directly count all new valid subarrays that end there: there are exactly `right - left + 1` of them. A sliding window maintains the product efficiently, and the `while` loop shrinks from the left only until the product is valid again.

> 🟢 *Sliding Window + Running Product*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Sliding Window + Running Product

**Why this works:**
- At each `right`, the window `[left, right]` is the **longest** valid window ending at `right`.
- All sub-windows `[left, right], [left+1, right], ..., [right, right]` are valid — product only decreases when we narrow from left.
- So `right - left + 1` is exactly the count of new valid subarrays introduced by this `right`.

**Dry Run** (`nums = [10,5,2,6]`, `k = 100`):

| `right` | `nums[right]` | `prod` (before shrink) | shrink? | `left` | `prod` (after) | added | `count` |
|---------|--------------|----------------------|---------|--------|----------------|-------|---------|
| 0 | 10 | 10 | No | 0 | 10 | 1 | 1 |
| 1 | 5 | 50 | No | 0 | 50 | 2 | 3 |
| 2 | 2 | 100 | Yes → `100/10=10`, `left=1` | 1 | 10 | 2 | 5 |
| 3 | 6 | 60 | No | 1 | 60 | 3 | **8** |

```java
class Solution {
    public int numSubarrayProductLessThanK(int[] nums, int k) {
        int left = 0;
        int len = nums.length;
        int count = 0;
        int prod = 1;
        if(k<=1) return 0;

        for(int right = 0; right<len; right++) {
            prod = prod * nums[right];

            while(prod >= k) {
                prod = prod/nums[left];
                left++;
            }
            count += right-left+1;
        }
        return count;
    }
}
```

---

## 🔢 Why `count += right - left + 1` Counts Exactly the Right Subarrays

> [!info]
> `count += right - left + 1` does **not** count all valid subarrays seen so far.
> It only counts the **new valid subarrays that end at the current `right` index**.

Each `right` step introduces subarrays that weren't counted before — those are exactly the subarrays that end at `right`. The number of such subarrays equals the number of valid starting positions, which are all indices from `left` to `right` inclusive → `right - left + 1` choices.

### Walk-through: `nums = [10,5,2,6]`, `k = 120`

**right = 0**, window = `[10]`

Valid subarrays **ending at index 0**: `[10]`
```
count += 0 - 0 + 1 = 1    total = 1
```

**right = 1**, window = `[10,5]`, product = 50 < 120

Valid subarrays **ending at index 1**: `[5]`, `[10,5]`
```
count += 1 - 0 + 1 = 2    total = 3
```
Cumulative: `[10]`, `[5]`, `[10,5]`

**right = 2**, window = `[10,5,2]`, product = 100 < 120

Valid subarrays **ending at index 2**: `[2]`, `[5,2]`, `[10,5,2]`
```
count += 2 - 0 + 1 = 3    total = 6
```
Cumulative: `[10]`, `[5]`, `[2]`, `[10,5]`, `[5,2]`, `[10,5,2]`

This matches your manual count of 6 exactly. ✅

### What if product becomes invalid?

`nums = [10,5,2,6]`, `k = 50`, at `right = 2`:

```
prod = 10 * 5 * 2 = 100 ≥ 50  →  shrink

  remove nums[0]=10 → prod = 10, left = 1
  10 < 50 → stop

Window is now [5,2], left=1
```

Valid subarrays ending at index 2:
```
start at 2 → [2]
start at 1 → [5,2]
start at 0 → [10,5,2]  ✗ product=100, invalid
```

Only `[2]` and `[5,2]` qualify → count = `right - left + 1 = 2 - 1 + 1 = 2` ✅

**The shrink step automatically excludes invalid starting positions** by pushing `left` past them. Any start index before `left` would create a window whose product `≥ k`, so they are never counted.

### The mental model

```
At each right, ask: "How many valid subarrays end here?"
Answer: exactly the number of valid starting positions = right - left + 1

New subarrays ending at right:
  [right]
  [right-1, right]
  [right-2, right]
  ...
  [left, right]

Each of these is new — none of them ended at any previous right.
No double-counting, no gaps.
```

---

## 🔑 Key Insights
- Reframe the counting: instead of "how many total valid subarrays", think "how many new valid subarrays end at `right` this step". This avoids double-counting entirely.
- `right - left + 1` works because the product is monotonically non-decreasing as you extend left — once a starting position is valid, all later starting positions (still ending at `right`) are also valid.
- `if(k <= 1) return 0` is necessary: since all `nums[i] >= 1`, the minimum product of any subarray is `1`, which is never strictly less than `0` or `1`.
- Division `prod / nums[left]` is safe for shrinking because all `nums[i] >= 1` (no zeros, no overflow issues when dividing).

---

## ⚠️ Pitfalls
> [!warning]
> - Missing the `k <= 1` early return — without it, `k=0` or `k=1` lets `left` run past `right` since the while never terminates correctly, giving a negative window.
> - Thinking `count += right - left + 1` counts all subarrays seen so far — it only counts subarrays **ending at the current right**. The total accumulates across all iterations.
> - Using `>=` in the while condition, not `>` — the problem asks for **strictly less than** `k`, so product equal to `k` must also trigger a shrink.

---

## ⏱️ Complexity
- **Time:** `O(n)` — each element is added and removed from the window at most once; the inner `while` has amortised `O(1)` cost per element.
- **Space:** `O(1)` — only a handful of integer variables, no auxiliary structures.
