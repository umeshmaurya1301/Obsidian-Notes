---
created: 2026-08-10 12:55
tags:
  - dsa
  - dynamic-programming
  - memoization
  - strings
  - recursion
source: https://leetcode.com/problems/regular-expression-matching/description/
problem_id: "10"
difficulty: Hard
status: Solved
review_date:
---
# LT_0010 – Regular Expression Matching

**Link:** [Open Problem](https://leetcode.com/problems/regular-expression-matching/description/)

---

## 📝 Problem Description
> [!info]
> Given an input string `s` and a pattern `p`, implement regular expression matching with support for `'.'` and `'*'` where:
> - `'.'` matches any single character.
> - `'*'` matches **zero or more** of the preceding element.
>
> Return a boolean indicating whether the matching covers the **entire** input string (not partial).

---

## 🧪 Examples
> [!example]
> **Input:** `s = "aa"`, `p = "a"`
> **Output:** `false`
> **Explanation:** `"a"` does not match the entire string `"aa"`.

> [!example]
> **Input:** `s = "aa"`, `p = "a*"`
> **Output:** `true`
> **Explanation:** `'*'` means zero or more of the preceding element, `'a'`. Therefore, by repeating `'a'` once, it becomes `"aa"`.

> [!example]
> **Input:** `s = "ab"`, `p = ".*"`
> **Output:** `true`
> **Explanation:** `".*"` means "zero or more (`*`) of any character (`.`)".

---

## ⚠️ Constraints
> [!warning]
> - `1 <= s.length <= 20`
> - `1 <= p.length <= 20`
> - `s` contains only lowercase English letters.
> - `p` contains only lowercase English letters, `'.'`, and `'*'`.
> - It is guaranteed that for each appearance of the character `'*'`, there will be a previous valid character to match.

---

## 🔍 Intuition

The mental unlock is to stop reading `p` character by character and start reading it as a sequence of **tokens**: either a bare character (`a`, `.`) or a *starred group* (`a*`, `.*`). A `'*'` is never a token on its own — it always belongs to the character before it. So at pattern position `j`, the first thing to ask is "does `p[j+1] == '*'`?", because that decides which of two completely different transitions applies.

**Bare token** — `p[j]` must consume exactly one character of `s`. Both must be present and compatible, then advance both: `firstMatch && dp(i+1, j+1)`.

**Starred token `p[j]p[j+1]`** — this is the branch, and it has exactly two options:
- **Use it zero times**: skip the whole two-character group, `dp(i, j+2)`. Note `s` doesn't move.
- **Use it once more**: consume one character of `s` but **stay at `j`**, `dp(i+1, j)`. Staying is what lets `*` match many — the group remains available for the next character too.

`||` between them means "either works", which is exactly the semantics of `*`.

The base case is the elegant part: only `j == p.length()` is a terminal, returning `i == s.length()`. There is deliberately **no** `i == s.length()` base case, because `s` running out is not failure — a trailing `a*b*c*` can still match empty. That case is handled naturally: `firstMatch` becomes `false` (guarded by `i < s.length()`), which kills the "use it once more" branch while leaving the "zero times" skip free to keep consuming the pattern.

With states `(i, j)` bounded by `21 × 21`, memoizing turns the exponential backtracking into `O(m·n)`.

> 🟢 *Two-Pointer Recursive Matching — look ahead for `*`, branch on zero-vs-more*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Memoized Recursion with `'*'` Lookahead

**Why this works:**
- **Looking ahead at `p[j+1]` is what makes the token boundary visible.** Reading `'*'` when you land on it is too late — you've already lost the character it modifies.
- **`dp(i+1, j)` — not `dp(i+1, j+2)` — is the "one more" branch.** Advancing `j` would let `a*` match exactly one character; staying lets it match arbitrarily many.
- **The `i < s.length()` guard inside `firstMatch` is load-bearing.** Without it, `charAt(i)` throws the moment `s` is exhausted but `p` still has starred groups to skip.
- **Only `j` has a base case.** Matching must cover *all* of `s`, so success is "pattern exhausted **and** string exhausted" — `ans = (i == s.length())`.
- **`Boolean[][]` (boxed) uses `null` for "not computed"**, which is required because `false` is a legitimate memoized result.

**Dry Run** (`s = "aa"`, `p = "a*"`):

```
dp(0,0)   p[1] == '*'  ->  zero-times  OR  one-more
  |
  +-- dp(0,2)   j == p.length()  ->  (i==0) == (s.length()==2)?  ->  false
  |
  +-- firstMatch: s[0]='a' == p[0]='a'  ->  true,  so try dp(1,0)
        dp(1,0)   p[1] == '*'  ->  zero-times  OR  one-more
          |
          +-- dp(1,2)   j == end  ->  (1 == 2)?  ->  false
          |
          +-- firstMatch: s[1]='a' == p[0]='a'  ->  true,  so try dp(2,0)
                dp(2,0)   p[1] == '*'  ->  zero-times  OR  one-more
                  |
                  +-- dp(2,2)   j == end  ->  (2 == 2)?  ->  TRUE
                  |
                  +-- firstMatch: i=2 is not < s.length()=2  ->  false (short-circuits)
                dp(2,0) = true
          dp(1,0) = false || (true && true) = true
  dp(0,0) = false || (true && true) = true      ✅
```

The `a*` group is entered three times at `j = 0` — consuming `'a'`, `'a'`, then bailing out through the zero-times skip once `s` is spent. That "stay at `j`" loop is the star.

Example 1 for contrast (`s = "aa"`, `p = "a"`):
```
dp(0,0)   j+1 = 1 is not < p.length() = 1  ->  bare-token branch
          firstMatch = true  ->  dp(1,1)
            dp(1,1)   j == end  ->  (1 == 2)?  ->  false
dp(0,0) = false      ✅   ("a" cannot cover both characters)
```

```java
class Solution {
    private Boolean[][] memo;

    public boolean isMatch(String s, String p) {
        memo = new Boolean[s.length() + 1][p.length() + 1];
        return dp(0, 0, s, p);
    }

    private boolean dp(int i, int j, String s, String p) {
        // return cached result
        if (memo[i][j] != null) return memo[i][j];

        boolean ans;

        if (j == p.length()) {
            ans = (i == s.length());
        } else {
            boolean firstMatch = (i < s.length() &&
                    (s.charAt(i) == p.charAt(j) || p.charAt(j) == '.'));

            if (j + 1 < p.length() && p.charAt(j + 1) == '*') {
                // case 1: skip "char*"
                // case 2: consume one character if match
                ans = dp(i, j + 2, s, p) || (firstMatch && dp(i + 1, j, s, p));
            } else {
                ans = firstMatch && dp(i + 1, j + 1, s, p);
            }
        }

        memo[i][j] = ans;
        return ans;
    }
}
```

- **Time:** `O(m·n)` · **Space:** `O(m·n)` memo + `O(m + n)` recursion stack

---

## 🔑 Key Insights
- **`'*'` binds backwards.** Every decision is made at the position of the character it modifies, with a one-slot lookahead. This is the difference between a clean solve and an unfixable tangle.
- **Zero-or-more is a genuine `||` fork, not a greedy loop.** `s = "aab"`, `p = "c*a*b"` needs `c*` to match zero times *and* `a*` to match twice — no greedy rule gets both right.
- **Not having an `i == s.length()` base case is intentional.** Trailing starred groups must still be allowed to match empty. Adding `if (i == s.length()) return j == p.length();` looks harmless and breaks `s = "a"`, `p = "ab*"`.
- **Memo is `[m+1][n+1]`.** Both indices legitimately reach their string's length — sizing it `[m][n]` throws on the very first terminal call.
- `'.'` matches one character; `".*"` matches any run. Conflating them is the fastest way to a wrong answer on Example 3.

---

## ⚠️ Pitfalls
> [!warning]
> - `firstMatch && dp(i + 1, j, s, p)` relies on short-circuit evaluation — the `firstMatch` check must come **first**, or `dp(i+1, ...)` can be called with `i` past the end.
> - `memo` is an **instance field** reallocated per `isMatch` call. That's fine for a single solve, but it makes the class non-reentrant — two threads sharing one instance would corrupt each other. Passing the array as a parameter (as the other DP solutions in this vault do) avoids the question.
> - The matching must cover the entire string. Returning `true` as soon as the pattern is exhausted — without checking `i == s.length()` — turns this into a prefix matcher.
> - The `'*'` lookahead needs `j + 1 < p.length()` *before* `p.charAt(j + 1)`; the constraints guarantee a `'*'` always has a preceding character, but they do **not** guarantee `j + 1` is in range.

---

## ⏱️ Complexity
- **Time:** `O(m·n)`
- **Space:** `O(m·n)`
