---
created: 2026-08-10 12:25
tags:
  - dsa
  - dynamic-programming
  - memoization
  - strings
  - counting-dp
source: https://leetcode.com/problems/distinct-subsequences/description/
problem_id: "115"
difficulty: Hard
status: Solved
review_date:
---
# LT_0115 – Distinct Subsequences

**Link:** [Open Problem](https://leetcode.com/problems/distinct-subsequences/description/)

---

## 📝 Problem Description
> [!info]
> Given two strings `s` and `t`, return the number of **distinct subsequences of `s` which equals `t`**.
>
> The test cases are generated so that the answer fits on a 32-bit signed integer.

---

## 🧪 Examples
> [!example]
> **Input:** `s = "rabbbit"`, `t = "rabbit"`
> **Output:** `3`
> **Explanation:** There are 3 ways to generate `"rabbit"` from `"rabbbit"` — each one drops a different `'b'` from the run of three.

> [!example]
> **Input:** `s = "babgbag"`, `t = "bag"`
> **Output:** `5`
> **Explanation:** There are 5 ways to pick the characters `b`, `a`, `g` in order out of `"babgbag"`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= s.length, t.length <= 1000`
> - `s` and `t` consist of English letters.

---

## 🔍 Intuition

Same two-pointer skeleton as [[LT_1143_Longest_Common_Subsequence]], but the accumulator changes from `max` to **`+`** — and that one swap changes the meaning of the match branch completely.

`f(i, j)` = the number of ways to build `t[j..]` out of `s[i..]`. When `s[i] == t[j]` I have a genuine **choice**, and unlike LCS both options can lead to valid answers, so I must count *both*:
- **Use** `s[i]` to satisfy `t[j]` → `f(i+1, j+1)`
- **Skip** `s[i]` anyway and satisfy `t[j]` with a later character → `f(i+1, j)`

Their sum is the answer. This is the crucial difference from LCS: in LCS, taking the match is provably optimal so skipping can be discarded; here, skipping produces *different subsequences*, and they all count.

When the characters differ there's no choice — `s[i]` can't help, so discard it: `f(i+1, j)`.

The base cases encode "success" and "failure": running out of `t` (`j == len2`) means one complete match has been assembled → return **`1`**; running out of `s` first (`i == len1`) means the build failed → return **`0`**. Order matters — `j == len2` must be checked first, otherwise a match that finishes exactly as `s` runs out gets miscounted as a failure.

> 🟢 *Counting DP over two strings — match ⇒ take **plus** skip, mismatch ⇒ skip*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Memoized "Take + Skip" Counting on `(i, j)`

**Why this works:**
- **Each `(i, j)` counts a disjoint set of subsequences**, so summing the two branches double-counts nothing: the "use `s[i]`" subsequences all contain index `i`, the "skip" ones all don't.
- **The base-case ordering is the correctness hinge.** `j == len2` first means "`t` fully matched" wins over "`s` exhausted" — which is right, since the leftover suffix of `s` is simply unused.
- **`-1` is a safe sentinel** because a count is never negative, and `0` (a legitimate answer) is distinguishable from it.
- The answer is guaranteed to fit in a signed 32-bit `int` by the problem statement, so no `long` or modulo is needed — unusual for a counting problem, and worth noticing.

**Dry Run** (`s = "babgbag"`, `t = "bag"`):

`dp[i][j]` = ways to form `t[j..]` from `s[i..]`. Filled from the bottom:

| `i` | `s[i]` | `j=0` `'b'` | `j=1` `'a'` | `j=2` `'g'` |
|---|---|---|---|---|
| 0 | `b` | **5** | 3 | 2 |
| 1 | `a` | 2 | 3 | 2 |
| 2 | `b` | 2 | 1 | 2 |
| 3 | `g` | 1 | 1 | 2 |
| 4 | `b` | 1 | 1 | 1 |
| 5 | `a` | 0 | 1 | 1 |
| 6 | `g` | 0 | 0 | 1 |

Three cells worked through:
```
(6,2):  'g' == 'g'  ->  dp[7][3] + dp[7][2]  =  1 + 0  =  1
                        (j hits end -> 1;  i hits end -> 0)

(1,1):  'a' == 'a'  ->  dp[2][2] + dp[2][1]  =  2 + 1  =  3
                        take the 'a' at index 1, or save it for the 'a' at index 5

(0,0):  'b' == 'b'  ->  dp[1][1] + dp[1][0]  =  3 + 2  =  5   ✅
                        use s[0] as the 'b', or defer to a later 'b'
```

The `3` at `(1,1)` is the interesting one — it is only `3` because both branches were summed. An LCS-style `max` there would return `2` and the final answer would be wrong.

```java
class Solution {
    public int numDistinct(String s, String t) {
        int len1 = s.length();
        int len2 = t.length();

        int[][] dp = new int[len1][len2];
        for (int[] a : dp) Arrays.fill(a, -1);
        dfs(s,t,dp,0,0);
        return dp[0][0];
    }

    private int dfs(String s, String t, int[][] dp, int i, int j) {
        int len1 = s.length();
        int len2 = t.length();

        if (j==len2) return 1;
        if (i==len1) return 0;

        if (dp[i][j]!=-1) return dp[i][j];

        int ways = 0;
        if (s.charAt(i) == t.charAt(j)) {
            ways += dfs (s, t, dp, i+1, j+1);
            ways += dfs (s, t, dp, i+1, j);
        } else {
            ways = dfs (s, t, dp, i+1, j);
        }

        return dp[i][j] = ways;
    }

}
```

- **Time:** `O(m·n)` · **Space:** `O(m·n)` memo + `O(m)` recursion stack

---

## 🔑 Key Insights
- **`max` → `+` is the whole difference from LCS.** Any "count the ways" variant of an optimisation DP is usually the same recursion with the combiner swapped — recognising that saves rederiving the transitions from scratch.
- **Only `s` advances.** `i` moves on every branch; `j` moves only on a consumed match. So `t` is a target being *consumed*, not a string being *aligned* — which is why the two base cases are asymmetric (`1` vs `0`) rather than both `0`.
- **The match case is a real fork, not a greedy step.** `"babgbag"` has two `'b'`s that can each serve as the first character; both must be explored.
- Sibling problems: [[LT_1143_Longest_Common_Subsequence]] (max), [[LT_0072_Edit_Distance]] (min over three), this one (sum over two). Same lattice, three combiners.

---

## ⚠️ Pitfalls
> [!warning]
> - **Swapping the base cases silently loses answers.** If `i == len1` is checked first, a match that completes at the very end of `s` returns `0` instead of `1`.
> - The driver calls `dfs(...)` and then reads `dp[0][0]` instead of using the return value. That works *only* because the constraints guarantee `s.length() >= 1 && t.length() >= 1`, so `(0,0)` never hits a base case and always writes the memo. With empty-string inputs allowed it would return a stale `-1`. Returning `dfs(...)` directly is the safer habit.
> - Don't add a `mod` — the problem guarantees a 32-bit fit, and applying one would produce wrong output.
> - "Distinct subsequences" counts distinct **index sets**, not distinct resulting strings — every valid pick counts even though they all spell `t`.

---

## ⏱️ Complexity
- **Time:** `O(m·n)`
- **Space:** `O(m·n)`
