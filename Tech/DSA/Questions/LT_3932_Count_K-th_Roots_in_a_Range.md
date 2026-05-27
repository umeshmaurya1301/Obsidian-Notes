---
created: 2026-05-26 00:00
tags:
  - dsa
  - math
  - number-theory
source: https://leetcode.com/problems/count-k-th-roots-in-a-range/
problem_id: "3932"
difficulty: Medium
status: Solved
review_date:
---
# LT_3932 – Count K-th Roots in a Range

**Link:** [Open Problem](https://leetcode.com/problems/count-k-th-roots-in-a-range/)

---

## 📝 Problem Description
> [!info]
> Given three integers `l`, `r`, and `k`. An integer `y` is said to be a **perfect k-th power** if there exists an integer `x` such that `y = x^k`. Return the number of integers `y` in the range `[l, r]` (inclusive) that are perfect k-th powers.

---

## 🧪 Examples
> [!example]
> **Input:** `l = 1, r = 9, k = 3`
> **Output:** `2`
> **Explanation:** The perfect cubes in [1, 9] are 1 = 1³ and 8 = 2³.

> [!example]
> **Input:** `l = 8, r = 30, k = 2`
> **Output:** `3`
> **Explanation:** The perfect squares in [8, 30] are 9 = 3², 16 = 4², 25 = 5².

---

## ⚠️ Constraints
> [!warning]
> - `0 <= l <= r <= 10^9`
> - `1 <= k <= 30`

---

## 🔍 Intuition

Instead of iterating every `y` in `[l, r]` and checking if it's a perfect k-th power — O(r), too slow for r up to 10⁹ — invert the question: find the range of valid integer bases `x` such that `x^k ∈ [l, r]`. Taking k-th roots on both sides gives `ceil(l^(1/k)) ≤ x ≤ floor(r^(1/k))`, so the answer is simply `maxX - minX + 1`. The tricky part is that `Math.pow()` uses double arithmetic, which drifts by ±1 ULP for exact perfect powers (e.g., `Math.pow(27, 1.0/3) ≈ 2.9999999` instead of `3.0`). We fix this by nudging `minX` and `maxX` by at most ±1 using an exact integer `pow()` helper that uses `long` arithmetic with an early-exit overflow cap at `2×10⁹`.

> 🟢 *Math — K-th Root Inversion + Floating Point Correction*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Math + Floating Point Correction

**Why this works:**
- Inverting `x^k ∈ [l, r]` to `x ∈ [l^(1/k), r^(1/k)]` collapses an O(r) scan into O(1) range math
- `Math.pow()` drifts ±1 ULP for exact integer roots — two one-step corrections (walk up if too low, walk down if too high) are always sufficient
- Long arithmetic + overflow cap in `pow()` gives exact comparisons against `r ≤ 10⁹` without integer overflow

**Dry Run** (`l = 8, r = 30, k = 2`):

| Step | Variable | Value | Note |
|------|----------|-------|------|
| Init | `minX` | `3` | `Math.ceil(√8) = Math.ceil(2.828)` |
| Init | `maxX` | `5` | `Math.floor(√30) = Math.floor(5.477)` |
| minX walk-up | `pow(3,2) = 9 >= 8` | ✓ | no adjustment needed |
| minX walk-down | `pow(2,2) = 4 >= 8`? | ✗ | no adjustment needed |
| maxX walk-up | `pow(6,2) = 36 <= 30`? | ✗ | no adjustment needed |
| maxX walk-down | `pow(5,2) = 25 > 30`? | ✗ | no adjustment needed |
| Result | `5 - 3 + 1` | **3** | ✓ |

```java
class Solution {
    public int countKthRoots(int l, int r, int k) {
        // Find smallest x where x^k >= l
        int minX = (int) Math.ceil(Math.pow(l, 1.0 / k));
        // Find largest x where x^k <= r
        int maxX = (int) Math.floor(Math.pow(r, 1.0 / k));

        // Adjust for floating point errors
        // Walk minX down if needed
        while (pow(minX, k) < l) minX++;
        while (minX > 1 && pow(minX - 1, k) >= l) minX--;

        // Walk maxX up if needed  
        while (pow(maxX + 1, k) <= r) maxX++;
        while (pow(maxX, k) > r) maxX--;

        return maxX >= minX ? maxX - minX + 1 : 0;
    }

    // Safe integer power to avoid overflow — use long
    private long pow(long base, int exp) {
        long result = 1;
        for (int i = 0; i < exp; i++) {
            result *= base;
            if (result > (long) 2e9) return (long) 2e9; // cap to avoid overflow
        }
        return result;
    }
}
```

---

## 🔑 Key Insights
- Count valid bases `x`, not valid powers `y`: inverting `x^k ∈ [l, r]` turns an O(r) scan into O(1) range math
- `Math.pow()` drifts ±1 ULP for exact integer roots — always walk-correct `minX` and `maxX` by at most ±1 step
- The `minX > 1` guard prevents `pow(0, k) = 0` from triggering an infinite walk-down when `l = 0`
- Overflow cap at `2×10⁹` in `pow()` keeps comparisons exact: anything above is definitely `> r ≤ 10⁹`

---

## ⚠️ Pitfalls
> [!warning]
> - Forgetting floating point correction — `Math.pow(27, 1.0/3)` returns `2.9999...`, making `maxX = 2` instead of `3`
> - Using `int` inside `pow()` — intermediate products overflow before the cap can trigger
> - Missing the `minX > 1` guard — without it, the walk-down loop runs forever when `l = 0`

---

## ⏱️ Complexity
- **Time:** `O(k)` — `pow()` loops `k` times; boundary corrections call it O(1) times
- **Space:** `O(1)`
