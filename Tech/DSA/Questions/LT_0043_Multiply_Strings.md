---
created: 2026-05-17 14:00
tags:
  - Math
  - String
  - Simulation
source: https://leetcode.com/problems/multiply-strings/
problem_id: "43"
difficulty: Medium
status: Completed
review_date:
---
# LT_0043 – Multiply Strings

**Link:** [Open Problem](https://leetcode.com/problems/multiply-strings/)

---

## 📝 Problem Description
> [!info]
> Given two non-negative integers `num1` and `num2` represented as strings, return the product of `num1` and `num2`, also represented as a string.
>
> **Note:** You must not use any built-in BigInteger library or convert the inputs to integer directly.

---

## 🧪 Examples
> [!example]
> **Input:** `num1 = "2"`, `num2 = "3"`
> **Output:** `"6"`
> **Explanation:** Basic single-digit multiplication.

> [!example]
> **Input:** `num1 = "123"`, `num2 = "456"`
> **Output:** `"56088"`
> **Explanation:** Standard multi-digit multiplication.

> [!example]
> **Input:** `num1 = "0"`, `num2 = "523"`
> **Output:** `"0"`
> **Explanation:** Any number multiplied by 0 is 0.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= num1.length, num2.length <= 200`
> - `num1` and `num2` consist of digits only.
> - Both `num1` and `num2` do not contain any leading zero, except the number `0` itself.

---

## 💡 Solutions

### 🟢 Approach 1: Array Simulation (Elementary Multiplication)

**Intuition:**
We simulate the standard manual multiplication process from elementary school. When multiplying `num1` by `num2`, each digit pair `num1[i] × num2[j]` contributes to exactly two positions in the result. The maximum possible length of the product of two numbers with lengths `m` and `n` is `m + n`.

We use an integer array `pos` of size `m + n` for intermediate sums. Iterating right to left, `num1[i] × num2[j]` maps to `pos[i + j]` (carry) and `pos[i + j + 1]` (remainder).

**Dry Run — `num1 = "12"`, `num2 = "34"`:**

Initial `pos = [0, 0, 0, 0]`

| Step | i (digit) | j (digit) | mul | p1 | p2 | sum | pos after |
|------|-----------|-----------|-----|----|----|-----|-----------|
| 1 | 1 (2) | 1 (4) | 8 | 2 | 3 | 8 | `[0, 0, 0, 8]` |
| 2 | 1 (2) | 0 (3) | 6 | 1 | 2 | 6 | `[0, 0, 6, 8]` |
| 3 | 0 (1) | 1 (4) | 4 | 1 | 2 | 10 | `[0, 1, 0, 8]` |
| 4 | 0 (1) | 0 (3) | 3 | 0 | 1 | 4 | `[0, 4, 0, 8]` |

Skip leading `0` → result = `"408"` ✅

**Edge Cases:**
- Either string is `"0"` — handled upfront, returns `"0"` immediately to avoid `"0000"`.
- Drastically different lengths (e.g. 200 vs 1) — handled naturally by nested loop bounds.

---

### ✅ Java Implementation

```java
class Solution {
    public String multiply(String num1, String num2) {
        if ("0".equals(num1) || "0".equals(num2)) {
            return "0";
        }

        int m = num1.length();
        int n = num2.length();
        int[] pos = new int[m + n];

        for (int i = m - 1; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                int mul = (num1.charAt(i) - '0') * (num2.charAt(j) - '0');

                int p1 = i + j;
                int p2 = i + j + 1;

                int sum = mul + pos[p2];

                pos[p1] += sum / 10;
                pos[p2] = sum % 10;
            }
        }

        StringBuilder sb = new StringBuilder();
        for (int p : pos) {
            if (!(sb.length() == 0 && p == 0)) {
                sb.append(p);
            }
        }

        return sb.toString();
    }
}
```

---

## 🔑 Key Insights
- The maximum digits in the product of lengths `m` and `n` is always `m + n`.
- The index mapping is perfectly predictable: `num1[i] × num2[j]` always writes to `pos[i + j]` (carry) and `pos[i + j + 1]` (remainder).

---

## 🧩 Patterns
- String Manipulation
- Array Simulation
- Elementary Math Simulation

---

## ⚠️ Pitfalls
> [!warning]
> - Failing to handle the `"0"` edge case — leads to empty or all-zero result strings.
> - Incorrectly calculating `p1` and `p2` index alignments.
> - Forgetting to subtract `'0'` when extracting digit values from characters.
> - Casting strings to large numbers — violates the constraint and causes integer overflow on length-200 inputs.

---

## ⏱️ Complexity
- **Time:** `O(m × n)` — constant work per digit pair
- **Space:** `O(m + n)` — the `pos` intermediate array
