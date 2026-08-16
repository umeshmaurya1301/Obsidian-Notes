---
created: 2026-08-10 12:45
tags:
  - dsa
  - dynamic-programming
  - memoization
  - strings
  - lcs
source: https://leetcode.com/problems/minimum-ascii-delete-sum-for-two-strings/description/
problem_id: "712"
difficulty: Medium
status: Solved
review_date:
---
# LT_0712 – Minimum ASCII Delete Sum for Two Strings

**Link:** [Open Problem](https://leetcode.com/problems/minimum-ascii-delete-sum-for-two-strings/description/)

---

## 📝 Problem Description
> [!info]
> Given two strings `s1` and `s2`, return the **lowest ASCII sum of deleted characters** to make the two strings equal.

---

## 🧪 Examples
> [!example]
> **Input:** `s1 = "sea"`, `s2 = "eat"`
> **Output:** `231`
> **Explanation:** Deleting `"s"` from `"sea"` adds the ASCII value of `"s"` (115) to the sum. Deleting `"t"` from `"eat"` adds 116 to the sum. At the end, both strings are equal, and `115 + 116 = 231` is the minimum sum possible.

> [!example]
> **Input:** `s1 = "delete"`, `s2 = "leet"`
> **Output:** `403`
> **Explanation:** Deleting `"dee"` from `"delete"` to turn the string into `"let"` adds `100[d] + 101[e] + 101[e]`. Deleting `"e"` from `"leet"` adds `101[e]`. Both strings become `"let"`, and the answer is `100+101+101+101 = 403`. Turning both into `"lee"` or `"eet"` would give 433 or 417, which are higher.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= s1.length, s2.length <= 1000`
> - `s1` and `s2` consist of lowercase English letters.

---

## 🔍 Intuition

This is [[LT_0583_Delete_Operation_for_Two_Strings]] with the cost of a deletion changed from `1` to the character's ASCII value — and that single change breaks the naive reduction. **Minimising the ASCII sum deleted is no longer the same as maximising the LCS *length*; it's maximising the LCS *ASCII weight*.** A shorter common subsequence made of heavy characters can beat a longer one made of light ones, so plain LCS gives the wrong answer.

Example 2 is the built-in proof. `"lee"`, `"eet"` and `"let"` are all common subsequences of length 3, but they carry weights `310`, `318` and `325`. Only the heaviest — `"let"` — yields the true minimum.

So the recursion is LCS with `1 +` replaced by `s1.charAt(i) +`, maximising the retained weight. Then the arithmetic mirrors 583, weighted:

```
answer = totalAsciiSum(s1) + totalAsciiSum(s2) − 2 · maxRetainedWeight
```

The `2 ·` is the same "each kept character is kept in *both* strings" argument as before.

Verify on Example 1: total = `(115+101+97) + (101+97+116) = 313 + 314 = 627`; best retained is `"ea"` = `198`; `627 − 396 = 231` ✅.

> 🟢 *Weighted LCS — maximise retained ASCII, not retained length*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Maximum-ASCII Common Subsequence, then Subtract Twice

**Why this works:**
- **Every character is either kept or paid for.** The total ASCII of both strings is fixed, so minimising what's deleted is exactly maximising what's retained — and retained characters must form a common subsequence.
- **`val = s1.charAt(i) + helper(i+1, j+1)` is the only edit to LCS.** `char` promotes to `int` in arithmetic context, so `s1.charAt(i)` *is* its ASCII value — no cast needed.
- **Matching is still unconditional.** With non-negative weights (ASCII is always positive), keeping a matching pair never lowers the total, so the exchange argument from LCS survives.
- **The mismatch branch still uses `Math.max`** — now maximising weight rather than count.

**Dry Run** (`s1 = "sea"`, `s2 = "eat"`):

ASCII: `s = 115`, `e = 101`, `a = 97`, `t = 116`.

```
helper(0,0)  's' vs 'e'  ->  max( helper(0,1), helper(1,0) )
  helper(0,1)  's' vs 'a'  ->  max( helper(0,2), helper(1,1) )
    helper(0,2)  's' vs 't'  ->  max( helper(0,3)=0, helper(1,2) )
      helper(1,2)  'e' vs 't'  ->  max( helper(1,3)=0, helper(2,2) )
        helper(2,2)  'a' vs 't'  ->  max( 0, 0 ) = 0
      helper(1,2) = 0
    helper(0,2) = 0
    helper(1,1)  'e' vs 'a'  ->  max( helper(1,2)=0, helper(2,1) )
      helper(2,1)  'a' == 'a'  ->  97 + helper(3,2) = 97
    helper(1,1) = 97
  helper(0,1) = 97
  helper(1,0)  'e' == 'e'  ->  101 + helper(2,1) = 101 + 97 = 198
helper(0,0) = max(97, 198) = 198      ->  retained "ea", weight 198
```

Then:
```
asciiSum = (115 + 101 + 97) + (101 + 97 + 116) = 627
answer   = 627 − 2 × 198 = 231   ✅
```

Example 2 shows why weight beats length:

| Common subsequence | Length | ASCII weight | Resulting answer |
|---|---|---|---|
| `"lee"` | 3 | `108+101+101 = 310` | `1053 − 620 = 433` |
| `"eet"` | 3 | `101+101+116 = 318` | `1053 − 636 = 417` |
| `"let"` | 3 | `108+101+116 = **325**` | `1053 − 650 = **403**` ✅ |

All three tie on length — only the weighted DP separates them.

```java
class Solution {
    public int minimumDeleteSum(String s1, String s2) {

        int len1 = s1.length();
        int len2 = s2.length();

        int[][] dp = new int[len1][len2];
        for(int[] a: dp) Arrays.fill(a, -1);
        int valToSubstract = helper(s1, s2, 0, 0 , dp);

        int ascciSum = 0;
        for(int i=0; i<len1; i++) {
            ascciSum += s1.charAt(i);
        }
        for(int i=0; i<len2; i++) {
            ascciSum += s2.charAt(i);
        }

        return ascciSum - 2*valToSubstract;
    }

    private int helper(String s1, String s2, int i, int j, int[][] dp) {
        int len1 = s1.length();
        int len2 = s2.length();

        if (i == len1 || j == len2)
            return 0;
        if (dp[i][j] != -1)
            return dp[i][j];

        int val = 0;

        if (s1.charAt(i) == s2.charAt(j)) {
            val = s1.charAt(i) + helper(s1, s2, i + 1, j + 1, dp);
        } else {
            val = helper(s1, s2, i, j + 1, dp);
            val = Math.max(val, helper(s1, s2, i + 1, j, dp));
        }

        return dp[i][j] = val;

    }
}
```

- **Time:** `O(m·n)` · **Space:** `O(m·n)` memo + `O(m + n)` recursion stack

---

## 🔑 Key Insights
- **Weighted LCS ≠ longest LCS.** This is the whole point of the problem, and Example 2 exists specifically to fail anyone who solves it as `583` with a post-hoc sum. Internalise the counterexample.
- **"Minimise removed" ⇒ "maximise kept" works for any additive, non-negative cost.** The reduction survives the reweighting because the total is invariant; only the objective inside the DP changes.
- **`char` arithmetic is implicit ASCII in Java.** `s1.charAt(i) + x` already gives the code point — writing `(int) s1.charAt(i)` is redundant.
- Solvable directly as a `min`-cost DP too (`min(s1[i] + f(i+1,j), s2[j] + f(i,j+1))` on mismatch), which avoids the total-sum bookkeeping. Same complexity; pick whichever you can derive under pressure.

---

## ⚠️ Pitfalls
> [!warning]
> - Reusing an LCS-by-length solve and summing the deleted characters afterwards gives `417` or `433` on `"delete"`/`"leet"` instead of `403`.
> - `2 * valToSubstract`, not `valToSubstract` — the retained characters are counted once in each string's total.
> - The maximum total is `2 × 1000 × 122 = 244000`, comfortably inside `int`. No overflow concern here, unlike some weighted-DP problems.
> - `-1` remains a safe sentinel since all weights are positive, so a real cell value is never negative — but note `0` is legitimate (no common characters) and must not be used as the sentinel.

---

## ⏱️ Complexity
- **Time:** `O(m·n)`
- **Space:** `O(m·n)`
