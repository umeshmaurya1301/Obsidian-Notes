---
created: 2026-05-27 00:00
tags:
  - dsa
  - array
  - hash-table
source: https://leetcode.com/problems/4sum-ii/description/
problem_id: "454"
difficulty: Medium
status: Solved
review_date:
---
# LT_0454 – 4Sum II

**Link:** [Open Problem](https://leetcode.com/problems/4sum-ii/description/)

---

## 📝 Problem Description
> [!info]
> Given four integer arrays `nums1`, `nums2`, `nums3`, and `nums4`, each of length `n`, return the number of tuples `(i, j, k, l)` such that:
> - `0 <= i, j, k, l < n`
> - `nums1[i] + nums2[j] + nums3[k] + nums4[l] == 0`

---

## 🧪 Examples
> [!example]
> **Input:** `nums1 = [1,2]`, `nums2 = [-2,-1]`, `nums3 = [-1,2]`, `nums4 = [0,2]`
> **Output:** `2`
> **Explanation:**
> - `(0,0,0,0)`: `1 + (-2) + (-1) + 0 = 0` ✓
> - `(1,1,0,0)`: `2 + (-1) + (-1) + 0 = 0` ✓

> [!example]
> **Input:** `nums1 = [0]`, `nums2 = [0]`, `nums3 = [0]`, `nums4 = [0]`
> **Output:** `1`

---

## ⚠️ Constraints
> [!warning]
> - `n == nums1.length == nums2.length == nums3.length == nums4.length`
> - `1 <= n <= 200`
> - `-2^28 <= nums1[i], nums2[i], nums3[i], nums4[i] <= 2^28`

---

## 🔍 Intuition

Brute force over all four arrays is O(n⁴) — completely infeasible at n=200. The key observation is that `a + b + c + d == 0` is the same as `a + b == -(c + d)`. This lets me split the problem in half: compute every pairwise sum from `nums1 × nums2` and store their frequencies in a HashMap, then for every pair from `nums3 × nums4` look up its negation as the complement. Each lookup directly tells me how many valid tuples that pair can form. This "meet in the middle" trick collapses O(n⁴) into two O(n²) passes. Crucially, the problem counts *tuples by index*, not distinct value combinations, so a frequency map (not a set) is required — duplicate pair sums must each be counted.

> 🟢 *Meet in the Middle — Two-Half HashMap*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Split into Two 2-Sum Halves + HashMap

**Why this works:**
- `a + b + c + d == 0` ⟺ `(a + b) == -(c + d)`. Computing one half's sums upfront lets every query from the other half be answered in O(1).
- The map stores *frequencies*, not just presence — multiple `(a,b)` pairs can produce the same sum, and each independently forms a valid tuple with any matching `(c,d)` pair.
- No deduplication is needed (unlike 4Sum I): `i, j, k, l` are independent indices, so every matching combination is a distinct valid tuple.

**Dry Run** (`nums1=[1,2]`, `nums2=[-2,-1]`, `nums3=[-1,2]`, `nums4=[0,2]`):

*Phase 1 — build `map` of `nums1[i] + nums2[j]` sums:*

| `a` | `b` | `a+b` | map after |
|-----|-----|-------|-----------|
| 1 | -2 | **-1** | `{-1:1}` |
| 1 | -1 | **0** | `{-1:1, 0:1}` |
| 2 | -2 | **0** | `{-1:1, 0:2}` |
| 2 | -1 | **1** | `{-1:1, 0:2, 1:1}` |

*Phase 2 — scan `nums3[k] + nums4[l]`, look up `-(c+d)`:*

| `c` | `d` | `c+d` | `target=-(c+d)` | `map[target]` | `count` |
|-----|-----|-------|-----------------|---------------|---------|
| -1 | 0 | -1 | **1** | 1 | 1 |
| -1 | 2 | 1 | **-1** | 1 | 2 |
| 2 | 0 | 2 | **-2** | 0 | 2 |
| 2 | 2 | 4 | **-4** | 0 | 2 |

Return **2** ✅

```java
class Solution {

    public int fourSumCount(
            int[] nums1,
            int[] nums2,
            int[] nums3,
            int[] nums4) {

        Map<Integer, Integer> map = new HashMap<>();

        // Store all sums of nums1 + nums2
        for (int a : nums1) {
            for (int b : nums2) {

                int sum = a + b;

                map.put(sum, map.getOrDefault(sum, 0) + 1);
            }
        }

        int count = 0;

        // Find complements from nums3 + nums4
        for (int c : nums3) {
            for (int d : nums4) {

                int target = -(c + d);

                count += map.getOrDefault(target, 0);
            }
        }

        return count;
    }
}
```

---

## 🔑 Key Insights
- **Meet in the middle**: splitting 4 loops into 2+2 reduces O(n⁴) to O(n²) — the standard trick whenever you have an even-count sum-to-zero condition across independent arrays.
- **Frequency map, not a set**: two different `(a,b)` pairs can share the same sum; each independently combines with every valid `(c,d)` pair, so you must count multiplicities, not just presence.
- **4Sum II ≠ 4Sum I**: here, no two indices are from the same array, so there are no duplicates to skip — no sorting, no deduplication, no two-pointer cleanup needed.
- The complement relationship `target = -(c + d)` means you only need one map covering one half; the second half probes it, keeping space O(n²).

---

## ⚠️ Pitfalls
> [!warning]
> - Using a `Set` instead of a frequency `Map` — correctly identifies *whether* a complement exists but misses that multiple `(a,b)` pairs can match the same `(c,d)`, undercounting the result.
> - Applying 4Sum I deduplication logic here — indices are independent across four separate arrays, so every `(i,j,k,l)` combination is inherently distinct; deduplication would undercount.
> - Integer overflow: values can be up to `2^28`, so `a + b` can reach `2^29` — fits safely in `int` (max ~`2^31 - 1`), but worth being aware of when adapting to larger ranges.

---

## ⏱️ Complexity
- **Time:** `O(n²)` — two separate O(n²) nested loops; each `HashMap` operation is O(1) average.
- **Space:** `O(n²)` — the map holds up to n² distinct sums from `nums1 × nums2`.
