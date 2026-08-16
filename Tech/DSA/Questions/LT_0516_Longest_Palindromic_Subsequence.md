---
created: 2026-08-10 11:55
tags:
  - dsa
  - dynamic-programming
  - memoization
  - strings
  - interval-dp
  - palindrome
source: https://leetcode.com/problems/longest-palindromic-subsequence/description/
problem_id: "516"
difficulty: Medium
status: Solved
review_date:
---
# LT_0516 – Longest Palindromic Subsequence

**Link:** [Open Problem](https://leetcode.com/problems/longest-palindromic-subsequence/description/)

---

## 📝 Problem Description
> [!info]
> Given a string `s`, find the longest palindromic **subsequence**'s length in `s`.
>
> A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.

---

## 🧪 Examples
> [!example]
> **Input:** `s = "bbbab"`
> **Output:** `4`
> **Explanation:** One possible longest palindromic subsequence is `"bbbb"`.

> [!example]
> **Input:** `s = "cbbd"`
> **Output:** `2`
> **Explanation:** One possible longest palindromic subsequence is `"bb"`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= s.length <= 1000`
> - `s` consists only of lowercase English letters.

---

## 🔍 Intuition

A palindrome is defined by its **two ends**, so the state should be an *interval* `[i, j]`, not a single index. `f(i, j)` = the longest palindromic subsequence inside `s[i..j]`.

From there the recursion writes itself:
- **`s[i] == s[j]`** — those two characters can wrap *any* palindrome found strictly inside, so take them both: `2 + f(i+1, j-1)`. Like LCS's match case, this is never wrong to do — a longer answer never comes from discarding a matching outer pair.
- **`s[i] != s[j]`** — the two ends can't both be in the answer, so shrink from one side or the other and keep the better: `max(f(i+1, j), f(i, j-1))`.

Two base cases carry the parity: `i == j` is a single character (a palindrome of length 1), and `i > j` is an empty window (length 0). The `i > j` case is exactly what the even-length branch falls into when `j - i == 1` and the two characters match — `2 + f(i+1, i)` = `2 + 0` = `2`. That's why both bases are needed, not just one.

There's also a slicker framing worth remembering: **LPS(s) = LCS(s, reverse(s))**. Same answer, and it's a good one-liner if you've already written [[LT_1143_Longest_Common_Subsequence]]. The interval version is more direct and generalises better to interval-DP problems.

> 🟢 *Interval DP — expand/shrink on `[i, j]`, matching ends contribute 2*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Interval Memoization on `(i, j)`

**Why this works:**
- **Interval states are closed under the transitions.** Every recursive call keeps `i <= j + 1`, so the `n × n` table (upper triangle plus the diagonal) covers every reachable state — `O(n²)` of them, `O(1)` work each.
- **Matching ends are unconditionally taken.** If `s[i] == s[j]`, some optimal LPS of `s[i..j]` uses both — so no `max` is needed in that branch.
- **Both base cases matter.** `i == j` handles odd-length centres; `i > j` handles even-length ones (and empty windows). Dropping either breaks one parity class.

**Dry Run** (`s = "bbbab"`, indices `0..4`):

```
f(0,4)  s[0]='b' == s[4]='b'   ->  2 + f(1,3)
  f(1,3)  s[1]='b' vs s[3]='a' ->  max( f(2,3), f(1,2) )
    f(2,3)  s[2]='b' vs s[3]='a' -> max( f(3,3), f(2,2) )
      f(3,3)  i == j            ->  1
      f(2,2)  i == j            ->  1
    f(2,3) = 1
    f(1,2)  s[1]='b' == s[2]='b' -> 2 + f(2,1)
      f(2,1)  i > j             ->  0
    f(1,2) = 2
  f(1,3) = max(1, 2) = 2
f(0,4) = 2 + 2 = 4   ✅
```

The `f(2,1)` call — `i > j` — is the even-length base firing on the adjacent matching pair `"bb"`. The answer `4` corresponds to `"bbbb"` (indices `0,1,2,4`).

Second example (`s = "cbbd"`): `f(0,3)`: `'c'` vs `'d'` → `max(f(1,3), f(0,2))`; `f(1,2)` = `'b' == 'b'` → `2 + f(2,1)` = `2`, which propagates up → answer `2`.

```java
class Solution {
    public int longestPalindromeSubseq(String s) {
        int n = s.length();
        int[][] dp = new int[n][n];
        for(int[] a : dp) Arrays.fill(a, -1);
        return helper(s, 0, n-1, dp);
    }

    private int helper(String s, int i, int j, int[][] dp) {
        if(i>j) return 0;
        if(i==j) return 1;
        if(dp[i][j]!=-1) return dp[i][j];

        if(s.charAt(i)==s.charAt(j)) {
            return dp[i][j] = 2 + helper(s, i+1, j-1, dp);
        } else {
            return dp[i][j] = Math.max(helper(s, i+1, j, dp), helper(s, i, j-1, dp));
        }
    }
}
```

- **Time:** `O(n²)` · **Space:** `O(n²)` memo + `O(n)` recursion stack

---

## 🔑 Key Insights
- **Palindrome ⇒ interval state.** Any time correctness depends on *both* ends of a range, `(i, j)` is the state and `(left+1, right)` / `(left, right-1)` are the moves. Same shape as Palindrome Partitioning and Burst Balloons.
- **`LPS(s) == LCS(s, reverse(s))`.** Worth knowing as a sanity check and as an alternate answer under time pressure. It works because a palindromic subsequence reads the same in both directions, so it is common to `s` and its reverse.
- **Subsequence, not substring.** [[LT_0647_Palindromic_Substrings]] is the contiguous cousin and needs a completely different technique — don't reach for this recursion there.
- The order of the two base cases matters for readability but not correctness: `i > j` can only be reached from the matching branch, never from the shrink branches.

---

## ⚠️ Pitfalls
> [!warning]
> - Forgetting the `i > j` base breaks every even-length palindrome — `"bb"` would recurse into `f(1,0)` and index out of bounds or loop.
> - `2 + f(i+1, j-1)` — not `1 +`. Both ends are consumed.
> - The answer is `f(0, n-1)`, not `dp[0][0]`. Reading `dp[0][0]` returns the LPS of a single character.
> - A length-1 string never enters the memo at all (`i == j` returns before the lookup), which is correct but means `dp` stays all `-1` — don't debug by inspecting the table on tiny inputs.

---

## ⏱️ Complexity
- **Time:** `O(n²)`
- **Space:** `O(n²)`
