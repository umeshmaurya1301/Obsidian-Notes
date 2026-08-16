---
created: 2026-08-10 11:45
tags:
  - dsa
  - dynamic-programming
  - memoization
  - strings
  - lcs
source: https://leetcode.com/problems/longest-common-subsequence/description/
problem_id: "1143"
difficulty: Medium
status: Solved
review_date:
---
# LT_1143 – Longest Common Subsequence

**Link:** [Open Problem](https://leetcode.com/problems/longest-common-subsequence/description/)

---

## 📝 Problem Description
> [!info]
> Given two strings `text1` and `text2`, return the length of their **longest common subsequence**. If there is no common subsequence, return `0`.
>
> A **subsequence** of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters. For example, `"ace"` is a subsequence of `"abcde"`.
>
> A **common subsequence** of two strings is a subsequence that is common to both strings.

---

## 🧪 Examples
> [!example]
> **Input:** `text1 = "abcde"`, `text2 = "ace"`
> **Output:** `3`
> **Explanation:** The longest common subsequence is `"ace"` and its length is 3.

> [!example]
> **Input:** `text1 = "abc"`, `text2 = "abc"`
> **Output:** `3`
> **Explanation:** The longest common subsequence is `"abc"` and its length is 3.

> [!example]
> **Input:** `text1 = "abc"`, `text2 = "def"`
> **Output:** `0`
> **Explanation:** There is no such common subsequence, so the result is 0.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= text1.length, text2.length <= 1000`
> - `text1` and `text2` consist of only lowercase English characters.

---

## 🔍 Intuition

This is the **root of a whole family** — Edit Distance, Delete Operation, Minimum ASCII Delete Sum, Longest Palindromic Subsequence and Shortest Common Supersequence are all this recursion with a different accumulator. Learn it once, properly.

Two pointers `i` and `j` walk the two strings. At every step there are only two situations:
- **The characters match.** Then it is *always* optimal to take them. There's no scenario where skipping a matching pair helps — any common subsequence that skips `s1[i]` and `s2[j]` can be rewritten to include them without getting shorter. So: `1 + f(i+1, j+1)`, no branching.
- **They don't match.** At most one of them can be part of the answer at this position, so I try discarding each in turn and take the better: `max(f(i+1, j), f(i, j+1))`.

Naively that's `2^(m+n)` branches, but the state is just `(i, j)` — only `m × n = 10^6` distinct pairs — and paths collide constantly. Memoizing turns exponential into `O(m·n)`.

The base case is where the elegance is: running off either string means no characters left to match, so `0`. No special-casing empty strings.

> 🟢 *Two-Pointer String DP — match ⇒ consume both, mismatch ⇒ max of two skips*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Top-Down Memoization on `(i, j)`

**Why this works:**
- **The greedy "always take a match" step is provably safe** — this is the exchange argument that makes the recursion two-way instead of three-way, and it's what an interviewer will ask you to justify.
- **`(i, j)` fully describes the remaining problem.** Nothing about how I got here matters, only the two suffixes `s1[i..]` and `s2[j..]` — which is exactly the property memoization needs.
- **`-1` is a safe sentinel** because an LCS length is never negative.

**Dry Run** (`text1 = "abcde"`, `text2 = "ace"`):

```
f(0,0)  'a' == 'a'  ->  1 + f(1,1)
  f(1,1)  'b' vs 'c'  ->  max( f(1,2), f(2,1) )
    f(1,2)  'b' vs 'e'  ->  max( f(1,3), f(2,2) )
      f(1,3)  j hits end            ->  0
      f(2,2)  'c' vs 'e'  ->  max( f(2,3)=0, f(3,2) )
        f(3,2)  'd' vs 'e'  ->  max( f(3,3)=0, f(4,2) )
          f(4,2)  'e' == 'e'  ->  1 + f(5,3) = 1
        f(3,2) = 1
      f(2,2) = 1
    f(1,2) = 1
    f(2,1)  'c' == 'c'  ->  1 + f(3,2) = 1 + 1 = 2
  f(1,1) = max(1, 2) = 2
f(0,0) = 1 + 2 = 3   ✅
```

Note `f(3,2)` is computed once and reused twice — that single cache hit is the whole reason this isn't exponential.

The characters taken were `'a'` at `(0,0)`, `'c'` at `(2,1)`, `'e'` at `(4,2)` → `"ace"`.

```java
class Solution {
    public int longestCommonSubsequence(String text1, String text2) {
        int len1 = text1.length();
        int len2 = text2.length();

        int[][] dp = new int[len1][len2];
        for(int[] a: dp) Arrays.fill(a, -1);
        return helper(text1, text2, 0, 0 , dp);
    }

    private int helper(String s1, String s2, int i, int j, int[][] dp) {
        int len1 = s1.length();
        int len2 = s2.length();

        if(i==len1 || j==len2) return 0;
        if(dp[i][j]!=-1) return dp[i][j];

        int val = 0;

        if(s1.charAt(i)==s2.charAt(j)) {
            val = 1 + helper(s1, s2, i+1, j+1, dp);
        } else {
            val = helper(s1, s2, i, j+1, dp);
            val = Math.max(val, helper(s1, s2, i+1, j, dp));
        }

        return dp[i][j] = val;

    }
}
```

- **Time:** `O(m·n)` · **Space:** `O(m·n)` memo + `O(m + n)` recursion stack

---

## 🔑 Key Insights
- **The whole LCS family is one recursion with a different accumulator.** Swap `1 +` for something else and you get a different problem:

| Problem | Match branch | Mismatch branch | Final answer |
|---|---|---|---|
| [[LT_1143_Longest_Common_Subsequence]] | `1 + f(i+1,j+1)` | `max` of two skips | `f(0,0)` |
| [[LT_0583_Delete_Operation_for_Two_Strings]] | same | same | `m + n - 2·lcs` |
| [[LT_0712_Minimum_ASCII_Delete_Sum_for_Two_Strings]] | `s1[i] + f(...)` (ASCII weight) | same | `asciiSum - 2·best` |
| [[LT_0072_Edit_Distance]] | `f(i+1,j+1)`, no cost | `1 + min` of **three** ops | `f(0,0)` |
| [[LT_0115_Distinct_Subsequences]] | **sum** of take + skip | skip only | `f(0,0)` |
| [[LT_0516_Longest_Palindromic_Subsequence]] | `2 + f(i+1,j-1)` on one string | `max` of two shrinks | `f(0, n-1)` |

- **Matching is never a branch point.** Recognising that the match case has no `max` is what separates an `O(m·n)` solve from a confused three-way recursion.
- **Suffix-indexed, not prefix-indexed.** This version recurses forward from `(0,0)`; the classic tabulation runs backwards from lengths. Both are `O(m·n)` — just don't mix the conventions mid-solution.

---

## ⚠️ Pitfalls
> [!warning]
> - `dp` is sized `[len1][len2]`, so it can only be indexed while `i < len1 && j < len2`. The base case **must** be checked before the memo lookup, or you get an `ArrayIndexOutOfBoundsException`.
> - Don't confuse subsequence with **substring** — subsequences may skip characters, substrings may not. `"ace"` is a subsequence of `"abcde"` but not a substring.
> - At `1000 × 1000` the recursion depth reaches `2000`; fine for the default JVM stack, but a bottom-up table avoids the question entirely.

---

## ⏱️ Complexity
- **Time:** `O(m·n)`
- **Space:** `O(m·n)`
