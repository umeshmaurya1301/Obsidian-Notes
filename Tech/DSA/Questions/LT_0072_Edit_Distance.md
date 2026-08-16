---
created: 2026-08-10 12:15
tags:
  - dsa
  - dynamic-programming
  - memoization
  - strings
  - lcs
source: https://leetcode.com/problems/edit-distance/description/
problem_id: "72"
difficulty: Medium
status: Solved
review_date:
---
# LT_0072 – Edit Distance

**Link:** [Open Problem](https://leetcode.com/problems/edit-distance/description/)

---

## 📝 Problem Description
> [!info]
> Given two strings `word1` and `word2`, return the **minimum number of operations** required to convert `word1` to `word2`.
>
> You have the following three operations permitted on a word:
> - Insert a character
> - Delete a character
> - Replace a character

---

## 🧪 Examples
> [!example]
> **Input:** `word1 = "horse"`, `word2 = "ros"`
> **Output:** `3`
> **Explanation:**
> `horse -> rorse` (replace `'h'` with `'r'`)
> `rorse -> rose` (remove `'r'`)
> `rose -> ros` (remove `'e'`)

> [!example]
> **Input:** `word1 = "intention"`, `word2 = "execution"`
> **Output:** `5`
> **Explanation:**
> `intention -> inention` (remove `'t'`)
> `inention -> enention` (replace `'i'` with `'e'`)
> `enention -> exention` (replace `'n'` with `'x'`)
> `exention -> exection` (replace `'n'` with `'c'`)
> `exection -> execution` (insert `'u'`)

---

## ⚠️ Constraints
> [!warning]
> - `0 <= word1.length, word2.length <= 500`
> - `word1` and `word2` consist of lowercase English letters.

---

## 🔍 Intuition

Levenshtein distance — the canonical string DP, and structurally the same walk as [[LT_1143_Longest_Common_Subsequence]] with three moves instead of two.

Two pointers `i` into `word1` and `j` into `word2`. If the characters agree, there is nothing to pay and nothing to decide — advance both, cost `0`. That "free match" is the same exchange argument as LCS: no optimal edit script ever benefits from touching a pair of characters that already match.

If they disagree, every one of the three permitted operations is a *different way to make progress*, and each costs exactly `1`:
- **Insert** a character into `word1` to line up with `word2[j]` → that character is now consumed on the right side only → `dp(i, j+1)`
- **Delete** `word1[i]` → consumed on the left side only → `dp(i+1, j)`
- **Replace** `word1[i]` with `word2[j]` → both consumed → `dp(i+1, j+1)`

Take the cheapest. The base cases are the tidy part: if one string runs out, the only thing left to do is insert (or delete) the rest of the other — `word2.length() - j` and `word1.length() - i` respectively.

The state is just `(i, j)`, so `500 × 500 = 250k` subproblems, `O(1)` each.

> 🟢 *Two-String DP — free on match, `1 + min(insert, delete, replace)` on mismatch*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Top-Down Memoization on `(i, j)`

**Why this works:**
- **The three operations map exactly onto the three ways to advance the pointer pair** — `(i, j+1)`, `(i+1, j)`, `(i+1, j+1)`. Every edit script is some path through that lattice, so minimising over the three covers all of them.
- **Matching costs nothing and needs no `min`.** Skipping a match to "save" an operation is never cheaper, so the branch is unconditional.
- **`Integer[][]` (boxed) uses `null` as "not computed"**, which is necessary here because `0` is a perfectly legal distance (identical strings).
- **The base cases are computed, not recursed** — `word2.length() - j` collapses an entire chain of inserts into one arithmetic step.

**Dry Run** (`word1 = "horse"`, `word2 = "ros"`):

`memo[i][j]` = edit distance between the suffixes `horse[i..]` and `ros[j..]`. Filling from the bottom-right:

| | `j=0` `'r'` | `j=1` `'o'` | `j=2` `'s'` | `j=3` (end) |
|---|---|---|---|---|
| `i=0` `'h'` | **3** | 3 | 4 | 5 |
| `i=1` `'o'` | 3 | 2 | 3 | 4 |
| `i=2` `'r'` | 2 | 2 | 2 | 3 |
| `i=3` `'s'` | 3 | 2 | 1 | 2 |
| `i=4` `'e'` | 3 | 2 | 1 | 1 |
| `i=5` (end) | 3 | 2 | 1 | 0 |

Two cells worked through:
```
(3,2): 's' == 's'  ->  free  ->  memo[4][3] = 1
(0,0): 'h' != 'r'  ->  1 + min( insert  memo[0][1] = 3,
                                delete  memo[1][0] = 3,
                                replace memo[1][1] = 2 )
                    =  1 + 2 = 3   ✅
```
The winning move at `(0,0)` is **replace** — which is exactly the `h -> r` in the problem's explanation.

```java
class Solution {
    public int minDistance(String word1, String word2) {
        int m = word1.length();
        int n = word2.length();
        Integer[][] memo = new Integer[m][n];
        return dp(word1, word2, 0, 0, memo);
    }

    private int dp(String word1, String word2, int i, int j, Integer[][] memo) {
        // If one string is exhausted, we need to insert/delete remaining characters
        if (i == word1.length()) return word2.length() - j;
        if (j == word2.length()) return word1.length() - i;

        // Check memo
        if (memo[i][j] != null) return memo[i][j];

        if (word1.charAt(i) == word2.charAt(j)) {
            // No operation needed
            memo[i][j] = dp(word1, word2, i + 1, j + 1, memo);
        } else {
            // Three possible operations:
            int insertOp = 1 + dp(word1, word2, i, j + 1, memo);      // Insert
            int deleteOp = 1 + dp(word1, word2, i + 1, j, memo);      // Delete
            int replaceOp = 1 + dp(word1, word2, i + 1, j + 1, memo); // Replace

            memo[i][j] = Math.min(insertOp, Math.min(deleteOp, replaceOp));
        }
        return memo[i][j];
    }
}
```

- **Time:** `O(m·n)` · **Space:** `O(m·n)` memo + `O(m + n)` recursion stack

---

## 🔑 Key Insights
- **Insert vs. delete is a matter of which pointer moves**, and it's the single most confusing part of this problem. Anchor it once: *insert* into `word1` matches `word2[j]`, so only `j` advances; *delete* from `word1` discards `word1[i]`, so only `i` advances. Get this backwards and the code still runs — it just silently computes the distance to the wrong target on asymmetric inputs.
- **Replace is the only three-way state that consumes both pointers at a cost.** A match consumes both for free; replace consumes both for `1`. Same move, different price.
- **Edit distance and LCS are relatives, not the same problem.** If replace were forbidden, `editDistance = m + n - 2·LCS` — which is exactly [[LT_0583_Delete_Operation_for_Two_Strings]]. Adding replace strictly lowers the answer, which is why 583's formula doesn't apply here.
- **`0 <= length` means both strings can be empty.** `new Integer[0][0]` is legal and the base case fires immediately, so no guard is needed — but only because the base cases sit *above* the memo lookup.

---

## ⚠️ Pitfalls
> [!warning]
> - The memo is `[m][n]`, so `memo[i][j]` is only in range when `i < m && j < n`. Both base cases **must** precede the memo access — reordering them is an `ArrayIndexOutOfBoundsException` on any input where one string runs out first.
> - Using `int[][]` with `-1` as the sentinel also works, but `Integer[][]`/`null` is safer here since `0` is a valid answer and easy to confuse with an uninitialised cell if you ever switch to `0`-fill.
> - Don't apply `1 +` to the match branch. It's free.
> - The greedy "just count differing positions" idea fails the moment lengths differ — `"horse"` vs `"ros"` needs alignment, not position-wise comparison.

---

## ⏱️ Complexity
- **Time:** `O(m·n)`
- **Space:** `O(m·n)` — reducible to `O(min(m, n))` with a rolling row in the bottom-up form
