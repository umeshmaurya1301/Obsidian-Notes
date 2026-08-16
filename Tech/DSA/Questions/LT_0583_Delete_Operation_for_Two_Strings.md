---
created: 2026-08-10 12:35
tags:
  - dsa
  - dynamic-programming
  - memoization
  - strings
  - lcs
source: https://leetcode.com/problems/delete-operation-for-two-strings/description/
problem_id: "583"
difficulty: Medium
status: Solved
review_date:
---
# LT_0583 – Delete Operation for Two Strings

**Link:** [Open Problem](https://leetcode.com/problems/delete-operation-for-two-strings/description/)

---

## 📝 Problem Description
> [!info]
> Given two strings `word1` and `word2`, return the **minimum number of steps** required to make `word1` and `word2` the same.
>
> In one step, you can delete exactly **one character** in either string.

---

## 🧪 Examples
> [!example]
> **Input:** `word1 = "sea"`, `word2 = "eat"`
> **Output:** `2`
> **Explanation:** You need one step to make `"sea"` into `"ea"` and another step to make `"eat"` into `"ea"`.

> [!example]
> **Input:** `word1 = "leetcode"`, `word2 = "etco"`
> **Output:** `4`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= word1.length, word2.length <= 500`
> - `word1` and `word2` consist of only lowercase English letters.

---

## 🔍 Intuition

Deletion is the *only* operation, so whatever survives in both strings must appear in both, in order — that is, the survivor is a **common subsequence**. And since every deletion costs the same `1`, minimising deletions is exactly the same as **maximising what survives**. So the problem is [[LT_1143_Longest_Common_Subsequence]] with a one-line wrapper.

Once I know `lcs = LCS(word1, word2)`, the arithmetic falls out: `word1` must shed `len1 - lcs` characters and `word2` must shed `len2 - lcs`, giving

```
answer = (len1 - lcs) + (len2 - lcs) = len1 + len2 - 2·lcs
```

Check it on Example 1: `LCS("sea", "eat") = "ea"` → `3 + 3 - 2·2 = 2` ✅.

This is also the cleanest way to see how [[LT_0072_Edit_Distance]] differs: Edit Distance permits **replace**, which fixes a mismatched pair for `1` instead of `2`. Strip replace out and Edit Distance collapses to precisely this formula.

> 🟢 *LCS + arithmetic — minimise deletions ⇔ maximise the common subsequence*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — LCS by Memoization, then `len1 + len2 - 2·lcs`

**Why this works:**
- **Every deletion costs 1 and no operation can create characters**, so the two strings can only meet at a string that is a subsequence of both. The cheapest meeting point is therefore the *longest* such string.
- **The `helper` is verbatim LCS** — match consumes both for `+1`, mismatch takes the better of the two skips.
- **Each surviving character is spared in both strings simultaneously**, which is why `lcs` is subtracted twice rather than once.

**Dry Run** (`word1 = "sea"`, `word2 = "eat"`):

```
helper(0,0)  's' vs 'e'  ->  max( helper(0,1), helper(1,0) )
  helper(0,1)  's' vs 'a'  ->  max( helper(0,2), helper(1,1) )
    helper(0,2)  's' vs 't'  ->  max( helper(0,3)=0, helper(1,2) )
      helper(1,2)  'e' vs 't'  ->  max( helper(1,3)=0, helper(2,2) )
        helper(2,2)  'a' vs 't'  ->  max( helper(2,3)=0, helper(3,2)=0 ) = 0
      helper(1,2) = 0
    helper(0,2) = 0
    helper(1,1)  'e' vs 'a'  ->  max( helper(1,2)=0, helper(2,1) )
      helper(2,1)  'a' == 'a'  ->  1 + helper(3,2) = 1 + 0 = 1
    helper(1,1) = 1
  helper(0,1) = 1
  helper(1,0)  'e' == 'e'  ->  1 + helper(2,1) = 1 + 1 = 2
helper(0,0) = max(1, 2) = 2        ->  lcs = "ea"
```

Then: `len1 + len2 - 2·lcs = 3 + 3 - 4 = 2` ✅ — delete `'s'` from `"sea"`, delete `'t'` from `"eat"`, both become `"ea"`.

Example 2 as a check: `LCS("leetcode", "etco") = "etco"` (indices `1,3,4,5` of `"leetcode"`) → `8 + 4 - 2·4 = 4` ✅.

```java
class Solution {
    public int minDistance(String word1, String word2) {
        int len1 = word1.length();
        int len2 = word2.length();
        int[][] dp = new int[len1][len2];
        for (int[] a : dp)
            Arrays.fill(a, -1);
        int lcs = helper(word1, word2, 0, 0, dp);
        return len1 + len2 - 2 * lcs;
    }

    private int helper(String w1, String w2, int i, int j, int[][] dp) {
        int len1 = w1.length();
        int len2 = w2.length();
        if (i == len1 || j == len2)
            return 0;

        if (dp[i][j] != -1)
            return dp[i][j];

        int val = 0;
        if (w1.charAt(i) == w2.charAt(j)) {
            val = 1 + helper(w1, w2, i + 1, j + 1, dp);
        } else {
            val = helper(w1, w2, i, j + 1, dp);
            val = Math.max(val, helper(w1, w2, i + 1, j, dp));
        }

        return dp[i][j] = val;
    }
}
```

- **Time:** `O(m·n)` · **Space:** `O(m·n)` memo + `O(m + n)` recursion stack

---

## 🔑 Key Insights
- **"Minimum deletions to make equal" is a disguised maximisation.** Recognising the flip — minimise removed ⇔ maximise kept — turns a fresh-looking problem into a solved one in one sentence.
- **`2 · lcs`, not `lcs`.** Every kept character is kept *twice*, once per string. Subtracting once is the classic wrong answer and gives `4` instead of `2` on Example 1.
- **This is Edit Distance minus the replace operation.** Holding both in your head as one family makes it obvious why 583's tidy formula can't be reused on 72.
- You could also solve it directly with a `min`-based recursion (`1 + min(skip left, skip right)` on mismatch) — same complexity, but the LCS reduction is less code and less to get wrong.

---

## ⚠️ Pitfalls
> [!warning]
> - Returning `lcs` instead of `len1 + len2 - 2 * lcs` — easy to do after copy-pasting an LCS solve.
> - The base case must precede the memo lookup; `dp` is `[len1][len2]` and cannot be indexed at the boundary.
> - The answer is a count of *steps*, and a step deletes from **either** string — not a count of deletions from `word1` alone.
> - Both strings are guaranteed non-empty here, so `new int[len1][len2]` is always valid — but the same code with `0`-length input would need the base case exactly where it already is.

---

## ⏱️ Complexity
- **Time:** `O(m·n)`
- **Space:** `O(m·n)`
