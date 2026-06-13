---
created: 2026-05-27 00:00
tags:
  - dsa
  - array
  - hash-table
  - prefix-sum
source: https://leetcode.com/problems/subarray-sums-divisible-by-k/
problem_id: "974"
difficulty: Medium
status: Solved
review_date:
---
# LT_0974 – Subarray Sums Divisible by K

**Link:** [Open Problem](https://leetcode.com/problems/subarray-sums-divisible-by-k/)

---

## 📝 Problem Description
> [!info]
> Given an integer array `nums` and an integer `k`, return the number of non-empty subarrays that have a sum divisible by `k`.
>
> A **subarray** is a contiguous part of an array.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [4, 5, 0, -2, -3, 1]`, `k = 5`
> **Output:** `7`
> **Explanation:** There are 7 subarrays with a sum divisible by 5: `[4,5,0,-2,-3,1]`, `[5]`, `[5,0]`, `[5,0,-2,-3]`, `[0]`, `[0,-2,-3]`, `[-2,-3]`.

> [!example]
> **Input:** `nums = [5]`, `k = 5`
> **Output:** `1`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 3 * 10^4`
> - `-10^4 <= nums[i] <= 10^4`
> - `2 <= k <= 10^4`

---

## 🔍 Intuition

A subarray `nums[i..j]` has a sum divisible by `k` if and only if `prefixSum[j] % k == prefixSum[i-1] % k` — because if both prefix sums share the same remainder, their difference (the subarray sum) is divisible by `k`. Instead of checking all O(n²) pairs, I maintain a running `prefixSum` and a frequency map of remainders seen so far. Each time I compute the current remainder, the number of previous prefixes with that same remainder tells me exactly how many valid subarrays end at the current index — I add that count directly and update the map. The `((prefixSum % k) + k) % k` normalisation handles negative values, since Java's `%` can return negative results for negative operands. The map is seeded with `{0: 1}` to account for subarrays starting at index 0 whose sum is itself divisible by `k`.

> 🟢 *Prefix Sum + Remainder Frequency Map*

---

## 🧠 Evolution of Solutions

### Solution 1 — Prefix Sum + HashMap

**Why this works:**
- If `prefixSum[j] ≡ prefixSum[i-1] (mod k)`, then `(prefixSum[j] - prefixSum[i-1]) % k == 0`, meaning the subarray `nums[i..j]` is divisible by `k`. Counting matching-remainder pairs in one pass gives the answer.
- `remainderCount.getOrDefault(remainder, 0)` accumulates the count of all previous prefix sums sharing the same remainder — each represents one valid subarray ending at the current index.
- Seeding the map with `{0: 1}` is essential: it models the empty prefix (before index 0), so subarrays that start at index 0 are correctly counted when their full prefix sum has remainder 0.

**Dry Run** (`nums = [4, 5, 0, -2, -3, 1]`, `k = 5`):

| `num` | `prefixSum` | `remainder` | Added to `count` | `count` | Map after |
|-------|-------------|-------------|------------------|---------|-----------|
| — | 0 | — | — | 0 | `{0:1}` |
| 4 | 4 | 4 | 0 | 0 | `{0:1, 4:1}` |
| 5 | 9 | 4 | 1 | 1 | `{0:1, 4:2}` |
| 0 | 9 | 4 | 2 | 3 | `{0:1, 4:3}` |
| -2 | 7 | 2 | 0 | 3 | `{0:1, 4:3, 2:1}` |
| -3 | 4 | 4 | 3 | 6 | `{0:1, 4:4, 2:1}` |
| 1 | 5 | 0 | 1 | **7** | `{0:2, 4:4, 2:1}` |

Return **7** ✅

```java
class Solution {
    public int subarraysDivByK(int[] nums, int k) {        
        Map<Integer, Integer> remainderCount = new HashMap<>();
        remainderCount.put(0, 1); // Important: empty prefix sum

        int prefixSum = 0;
        int count = 0;

        for (int num : nums) {
            prefixSum += num;

            int remainder = ((prefixSum % k) + k) % k;
            count += remainderCount.getOrDefault(remainder, 0);
            remainderCount.put(remainder, remainderCount.getOrDefault(remainder, 0) + 1);
        }

        return count;
    }    
}
```

---

### ✅ Solution 2 — Prefix Mod + Array (Optimal)

**Why this works:**
- Since remainders are always in `[0, k-1]`, a fixed-size `int[]` of length `k` replaces the `HashMap` entirely — direct array indexing is O(1) with no hashing overhead or boxing cost.
- `prefixMod` is updated incrementally: `(prefixMod + num % k + k) % k`. This is equivalent to `(fullPrefixSum) % k` but avoids accumulating a large integer; the `+k` inside is the negative-remainder fix applied at the single-number level before folding into the running mod.
- `modGroups[prefixMod]++` after adding ensures we count the current prefix for future elements, not the current one itself.

> [!info] **Why `modGroups[0] = 1`?**
> `modGroups[r]` counts how many prefix sums so far have remainder `r`. Before we process any element, there is exactly one prefix — the **empty prefix** (sum = 0, remainder = 0). Initialising `modGroups[0] = 1` inserts this virtual prefix into the frequency table. Without it, any subarray starting at index 0 whose sum is divisible by `k` would find `modGroups[0] == 0` and be missed entirely. Think of it as: "the subarray `nums[0..j]` is valid whenever `prefixMod` reaches 0, and `modGroups[0]` must already be 1 for that to register."

> [!info] **Why `(prefixMod + num % k + k) % k`?**
> Java's `%` operator follows **truncated division**: the result has the same sign as the dividend, not the divisor. So `-2 % 5 == -2` in Java, not `3`. This becomes a problem because `-2` and `3` are the same mathematical remainder mod 5, but they would map to different array indices. The fix is a three-step normalisation:
> 1. `num % k` — reduces `num` to the range `[-(k-1), k-1]`.
> 2. `+ k` — shifts the worst-case negative `-(k-1)` up to `+1`, so the result lands in `[1, 2k-1]` (always positive).
> 3. Add `prefixMod` (in `[0, k-1]`) → total in `[1, 3k-2]`. Final `% k` collapses this back to `[0, k-1]`.
>
> A single `+k` is sufficient because `num % k` can be at most `-(k-1)`, and adding `k` once always makes it non-negative.

**Dry Run** (`nums = [4, 5, 0, -2, -3, 1]`, `k = 5`):

| `num` | `num % k` | new `prefixMod` | `result +=` | `result` | `modGroups` (indices 0–4) |
|-------|-----------|-----------------|-------------|----------|---------------------------|
| — | — | 0 | — | 0 | `[1,0,0,0,0]` |
| 4 | 4 | (0+4+5)%5 = **4** | `[4]`=0 | 0 | `[1,0,0,0,1]` |
| 5 | 0 | (4+0+5)%5 = **4** | `[4]`=1 | 1 | `[1,0,0,0,2]` |
| 0 | 0 | (4+0+5)%5 = **4** | `[4]`=2 | 3 | `[1,0,0,0,3]` |
| -2 | -2 | (4−2+5)%5 = **2** | `[2]`=0 | 3 | `[1,0,1,0,3]` |
| -3 | -3 | (2−3+5)%5 = **4** | `[4]`=3 | 6 | `[1,0,1,0,4]` |
| 1 | 1 | (4+1+5)%5 = **0** | `[0]`=1 | **7** | `[2,0,1,0,4]` |

Return **7** ✅

```java
class Solution {
    public int subarraysDivByK(int[] nums, int k) {
        int n = nums.length;
        int prefixMod = 0, result = 0;

        // There are k mod groups 0...k-1.
        int[] modGroups = new int[k];
        modGroups[0] = 1;

        for (int num: nums) {
            // Take modulo twice to avoid negative remainders.
            prefixMod = (prefixMod + num % k + k) % k;
            // Add the count of subarrays that have the same remainder as the current
            // one to cancel out the remainders.
            result += modGroups[prefixMod];
            modGroups[prefixMod]++;
        }

        return result;
    }
}
```

---

## 🔑 Key Insights
- The core identity: `subarray(i, j) % k == 0` ⟺ `prefixSum[j] % k == prefixSum[i-1] % k`. This converts an O(n²) search into counting remainder collisions in one pass.
- Remainders always land in `[0, k-1]` — a fixed `int[k]` array replaces a `HashMap` entirely, with guaranteed O(1) access and no boxing overhead.
- The empty prefix (sum = 0) must be pre-counted: `modGroups[0] = 1`. It represents the imaginary prefix before index 0, enabling subarrays starting at index 0 to be counted correctly.
- Java's `%` is truncated, not mathematical: `(-2 % 5) == -2`. The pattern `(x % k + k) % k` is the standard fix — adding `k` once is always enough since `x % k ≥ -(k-1)`.

---

## ⚠️ Pitfalls
> [!warning]
> - Omitting `modGroups[0] = 1` (or `map.put(0, 1)`) — subarrays starting at index 0 are missed; this is the single most common error on this problem.
> - Using raw `num % k` or `prefixSum % k` without the `+k` fix — negative inputs silently produce wrong (negative) indices, causing incorrect counts or an `ArrayIndexOutOfBoundsException` in the array approach.
> - Thinking the answer is just the count of times `prefixMod == 0` — that only finds subarrays from index 0, not all valid subarrays.

---

## ⏱️ Complexity
- **Time:** `O(n)` — single pass; all array/map operations are O(1).
- **Space:** `O(k)` — exactly `k` buckets for remainders 0 through k-1 (array approach is tighter in practice than HashMap due to no boxing or rehashing).

---

## 🧰 Generalizable Toolkit — Subarray Sum Patterns

> [!info]
> These four patterns appear constantly across subarray-sum problems on LeetCode. Recognising which one applies is half the solution.

**1. Core algebraic trick**
Any subarray sum is a difference of two prefix sums: `sum(i..j) = prefixSum[j] - prefixSum[i-1]`. Whenever a problem asks "subarray sum satisfies condition X," translate it into a condition on that difference, then figure out what it implies about the two prefix sums individually.

**2. Divisibility → congruence → equality of remainders**
Condition: *sum divisible by k.*
`prefixSum[j] - prefixSum[i-1] ≡ 0 (mod k)`
→ `prefixSum[j] ≡ prefixSum[i-1] (mod k)`
→ `prefixSum[j] % k == prefixSum[i-1] % k` (after normalisation)
**Action:** count pairs of prefix sums with equal remainders using a frequency map/array.

**3. Exact sum → equality of a shifted prefix sum**
Condition: *sum equals target.* (LC 560 — Subarray Sum Equals K)
`prefixSum[j] - prefixSum[i-1] = target`
→ `prefixSum[i-1] = prefixSum[j] - target`
**Action:** for each `j`, look up how many earlier prefix sums equal `prefixSum[j] - target`. Same skeleton as pattern 2, different lookup value.

**4. Normalisation for negative remainders (Java / C++ only)**
`((x % k) + k) % k`
Java/C++ `%` is a *remainder* operator — result has the same sign as the dividend, so negative inputs give negative remainders. A single `+k` shifts the worst case `-(k-1)` to positive before the final `% k`. Python's `%` already returns non-negative results for positive `k`, so this step is unnecessary there.
