---
created: 2026-08-07 00:00
tags:
  - dsa
  - backtracking
  - string
source: https://leetcode.com/problems/letter-combinations-of-a-phone-number/
problem_id: "17"
difficulty: Medium
status: Solved
review_date:
---
# LT_0017 – Letter Combinations of a Phone Number

**Link:** [Open Problem](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)

---

## 📝 Problem Description
> [!info]
> Given a string containing digits from `2-9` inclusive, return all possible letter combinations that the number could represent. Return the answer in **any order**.
>
> A mapping of digits to letters (just like on the telephone buttons) is given below. Note that `1` does not map to any letters.

---

## 🧪 Examples
> [!example]
> **Input:** `digits = "23"`
> **Output:** `["ad","ae","af","bd","be","bf","cd","ce","cf"]`

> [!example]
> **Input:** `digits = ""`
> **Output:** `[]`

> [!example]
> **Input:** `digits = "2"`
> **Output:** `["a","b","c"]`

---

## ⚠️ Constraints
> [!warning]
> - `0 <= digits.length <= 4`
> - `digits[i]` is a digit in the range `['2', '9']`.

---

## 🔍 Intuition

Each digit independently maps to 3–4 letters, and the full output is the Cartesian product of these letter sets across all digit positions — a natural fit for backtracking: fix a letter for the current digit, recurse into the next position, then undo the choice and try the next letter. The `KEYPAD` array is indexed directly by digit value (`digits.charAt(index) - '0'`), giving O(1) lookup of the candidate letters without a `HashMap`. Because we always advance to `index + 1` and never revisit a digit, there's no need for a "used" tracker like in permutation problems — each recursive call operates on a completely fresh sub-problem (the remaining suffix of `digits`). The empty-string case needs its own early return: without it, `backtrack` would still hit the base case immediately (`index == digits.length() == 0`) and emit a single empty string, whereas LeetCode expects an empty list, not a list containing `""`.

> 🟢 *Backtracking / DFS over a Keypad Mapping*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Backtracking with a Static Keypad Array

**Why this works:**
- The recursion tree has exactly `digits.length()` levels, and at each level it branches over every letter mapped to that digit — visiting every combination exactly once.
- `StringBuilder path` is mutated in place (`append` / `deleteCharAt`) instead of rebuilding strings, so each branch/unbranch step is O(1) rather than O(n) string concatenation.
- The base case (`index == digits.length()`) is reached only after a full combination has been built, at which point `path.toString()` snapshots it into `result`.

**Dry Run** (`digits = "23"`):

| Call | letters tried | path after append | action |
|---|---|---|---|
| backtrack(0) | `"abc"` (digit `2`) | `"a"` | recurse into index 1 |
| backtrack(1) | `"def"` (digit `3`) | `"ad"` | index 2 == len → add `"ad"` |
| — | | `"ae"` | add `"ae"` |
| — | | `"af"` | add `"af"` |
| backtrack(0) | | `"b"` | recurse into index 1 → adds `"bd"`, `"be"`, `"bf"` |
| backtrack(0) | | `"c"` | recurse into index 1 → adds `"cd"`, `"ce"`, `"cf"` |

Result: `["ad","ae","af","bd","be","bf","cd","ce","cf"]` ✅

```java
class Solution {

    private static final String[] KEYPAD = {
        "",     // 0
        "",     // 1
        "abc",  // 2
        "def",  // 3
        "ghi",  // 4
        "jkl",  // 5
        "mno",  // 6
        "pqrs", // 7
        "tuv",  // 8
        "wxyz"  // 9
    };

    public List<String> letterCombinations(String digits) {
        List<String> result = new ArrayList<>();
        
        if (digits == null || digits.length() == 0) {
            return result;
        }

        backtrack(digits, 0, new StringBuilder(), result);
        return result;
    }

    private void backtrack(String digits, int index, StringBuilder path, List<String> result) {
        // Base case
        if (index == digits.length()) {
            result.add(path.toString());
            return;
        }

        String letters = KEYPAD[digits.charAt(index) - '0'];

        for (char ch : letters.toCharArray()) {
            path.append(ch);
            backtrack(digits, index + 1, path, result);
            path.deleteCharAt(path.length() - 1); // backtrack
        }
    }
}
```

---

## 🔑 Key Insights
- Indexing `KEYPAD` directly by `digit - '0'` avoids a `HashMap<Character, String>` entirely — the digit value *is* the index.
- No "used" set is needed, unlike permutation backtracking: each recursive level consumes a distinct digit position, so there's no possibility of revisiting the same slot.
- `StringBuilder` append/`deleteCharAt` is the standard O(1) backtrack-undo pattern — far cheaper than building new `String` objects at every branch.
- Recursion depth equals `digits.length()` (max 4 per the constraints), so there's no stack-depth concern here.

---

## ⚠️ Pitfalls
> [!warning]
> - Skipping the `digits.length() == 0` early return — the base case fires immediately at `index == 0`, producing `[""]` instead of the expected `[]`.
> - Calling `path.deleteCharAt(...)` *before* the recursive call returns, instead of after — this corrupts the prefix for sibling branches still being explored.
> - Assuming `KEYPAD` needs an offset; it doesn't — indices `0` and `1` are deliberately empty strings so `digits.charAt(index) - '0'` can be used directly without adjusting for the fact that `'0'`/`'1'` map to nothing.

---

## ⏱️ Complexity
- **Time:** `O(4^n × n)` where `n = digits.length()` — up to 4 letters per digit (digits `7` and `9`), and copying each finished combination into `result` costs `O(n)`.
- **Space:** `O(n)` for the recursion stack and `path`, plus `O(4^n × n)` for the output list itself.
