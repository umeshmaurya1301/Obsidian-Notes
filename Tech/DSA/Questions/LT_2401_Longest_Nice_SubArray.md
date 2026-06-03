---
created: 2026-05-30 07:30
tags:
  - dsa
  - arrays
  - bit-manipulation
  - sliding-window
source: https://leetcode.com/problems/longest-nice-subarray/
problem_id: "2401"
difficulty: Medium
status: Solved
review_date:
---
# LT_2401 – Longest Nice Subarray

**Link:** [Open Problem](https://leetcode.com/problems/longest-nice-subarray/)

---

## 📝 Problem Description
> [!info]
> You are given an array `nums` consisting of **positive** integers.
>
> We call a subarray of `nums` **nice** if the bitwise **AND** of every pair of elements that are in **different** positions in the subarray is equal to `0`.
>
> Return the length of the **longest** nice subarray.
>
> A **subarray** is a contiguous part of an array.
> Note that subarrays of length `1` are always considered nice.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [1, 3, 8, 48, 10]`
> **Output:** `3`
> **Explanation:** The longest nice subarray is `[3, 8, 48]`.
> - `3 AND 8 = 0` ✅
> - `3 AND 48 = 0` ✅
> - `8 AND 48 = 0` ✅
>
> No longer nice subarray can be found.

> [!example]
> **Input:** `nums = [3, 1, 5, 11, 13]`
> **Output:** `1`
> **Explanation:** Any subarray of length ≥ 2 contains numbers that share a bit. Answer is `1`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 10^5`
> - `1 <= nums[i] <= 10^9`

---

## 🔍 What Does "AND = 0" Actually Mean?

`a AND b = 0` means `a` and `b` share **no common 1-bits** — every bit set in `a` is unset in `b`, and vice versa.

```
3  = 0...011
8  = 0...100 0
       ------
AND = 0...000  ✅  No overlap

3  = 0...011
6  = 0...110
       ------
AND = 0...010  ❌  Bit 1 is shared
```

So a **nice** subarray is one where all numbers have **non-overlapping bits** — like puzzle pieces each occupying unique slots.

---

## 🧠 Key Insight — Bit Slots

Think of 32 bits as 32 parking slots. Each number "parks" in whichever slots correspond to its 1-bits.

A subarray is **nice** if and only if **no two numbers park in the same slot**.

```
Bit position:  7  6  5  4  3  2  1  0
              ┌──┬──┬──┬──┬──┬──┬──┬──┐
3  (011)      │  │  │  │  │  │  │ 3│ 3│   ← slots 0, 1
8  (1000)     │  │  │  │  │ 8│  │  │  │   ← slot 3
48 (110000)   │  │  │48│48│  │  │  │  │   ← slots 4, 5
              └──┴──┴──┴──┴──┴──┴──┴──┘
```

No two numbers share a slot → `[3, 8, 48]` is **nice** ✅

---

## 🪜 Why Not Check All Pairs?

For a window of length `k`, checking all pairs costs `O(k²)` — giving **O(n³)** overall for all subarrays. Way too slow for `n = 10⁵`.

**Better idea:** Maintain a single bitmask `mask` = OR of all numbers in the current window. It tracks every occupied bit slot at once.

- `mask & newNum != 0` → at least one slot conflicts → **shrink window**
- `mask & newNum == 0` → no conflicts → **safe to add**

This reduces pair-checking from `O(k)` to **O(1)**.

---

## 🔑 The Bitmask Sliding Window

| Operation | Code | Effect |
|---|---|---|
| Add `nums[right]` | `mask \|= nums[right]` | Marks its bits as occupied |
| Remove `nums[left]` | `mask ^= nums[left]` | Clears its bits from the mask |
| Conflict check | `(mask & nums[right]) != 0` | True if any slot is already taken |

> [!tip]
> **Why is XOR safe for removal?**
> In a valid nice window, each bit has exactly one owner. So `mask ^= nums[left]` cleanly flips only that number's bits back off — no risk of accidentally clearing a bit that belongs to another number still in the window.

---

## 🔬 Dry Run — `nums = [1, 3, 8, 48, 10]`

```
Binary reference:
1  = 00000001
3  = 00000011
8  = 00001000
48 = 00110000
10 = 00001010
```

**right = 0, nums[right] = 1**
```
mask & 1 = 0  → no conflict
mask |= 1  →  mask = 00000001
window = [1],  len = 1,  maxLen = 1
```

**right = 1, nums[right] = 3**
```
mask & 3 = 00000001 & 00000011 = 00000001 ≠ 0  → CONFLICT (bit 0 shared)
  Shrink: mask ^= nums[0]=1  →  mask = 00000000,  left = 1
mask & 3 = 0  → no conflict
mask |= 3  →  mask = 00000011
window = [3],  len = 1,  maxLen = 1
```

**right = 2, nums[right] = 8**
```
mask & 8 = 00000011 & 00001000 = 0  → no conflict
mask |= 8  →  mask = 00001011
window = [3, 8],  len = 2,  maxLen = 2
```

**right = 3, nums[right] = 48**
```
mask & 48 = 00001011 & 00110000 = 0  → no conflict
mask |= 48  →  mask = 00111011
window = [3, 8, 48],  len = 3,  maxLen = 3  ✅
```

**right = 4, nums[right] = 10**
```
mask & 10 = 00111011 & 00001010 = 00001010 ≠ 0  → CONFLICT (bits 1 and 3)
  Shrink: mask ^= nums[1]=3   →  mask = 00111000,  left = 2
  mask & 10 = 00111000 & 00001010 = 00001000 ≠ 0  → still conflict
  Shrink: mask ^= nums[2]=8   →  mask = 00110000,  left = 3
  mask & 10 = 0  → no conflict
mask |= 10  →  mask = 00111010
window = [48, 10],  len = 2,  maxLen = 3 (unchanged)
```

**Answer = 3** ✅

---

## ✅ Solution — Bitmask Sliding Window

```java
class Solution {
    public int longestNiceSubarray(int[] nums) {

        int left  = 0;
        int mask  = 0;   // OR of all numbers currently in the window
        int maxLen = 0;

        for (int right = 0; right < nums.length; right++) {

            // Shrink window from left until no bit conflict with nums[right]
            while ((mask & nums[right]) != 0) {
                mask ^= nums[left];   // remove nums[left]'s bits from mask
                left++;
            }

            // Safely add nums[right] — no shared bits
            mask |= nums[right];

            // Update answer
            maxLen = Math.max(maxLen, right - left + 1);
        }

        return maxLen;
    }
}
```

---

## ⚠️ Edge Cases
> [!warning]
> **All elements conflict** — e.g. `[3, 1, 5, 11, 13]`. Every number shares bits with its neighbour; answer is always `1`. Handled naturally since the window never grows past size 1.

> [!warning]
> **Single element** — `nums.length == 1`. The while loop never fires, `maxLen` becomes `1`. Correct.

---

## ⏱️ Complexity
- **Time:** `O(n)` — each element enters and exits the window at most once; the nested `while` has amortised `O(1)` cost per element
- **Space:** `O(1)` — only three integer variables, no auxiliary structures

---

## 💡 Mental Model

```
32 bits = 32 parking slots.
Each number claims the slots matching its 1-bits.
Nice subarray = no two numbers share any slot.

mask  = map of all currently occupied slots

New number wants a taken slot?  → Evict leftmost numbers until it's free.
New number is conflict-free?    → Let it park; update the occupied map.
After each step, record window length if it's the largest seen.
```

The bitmask collapses an `O(k)` pair-check into a single `O(1)` AND — that's what makes this `O(n)` instead of `O(n²)`.
