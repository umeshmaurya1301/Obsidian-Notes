---
created: 2026-08-09 18:31
tags:
  - dsa
  - dynamic-programming
  - strings
  - two-pointers
source: https://leetcode.com/problems/palindromic-substrings/
problem_id: "647"
difficulty: Medium
status: Solved
review_date:
---
# LT_0647 – Palindromic Substrings

**Link:** [Open Problem](https://leetcode.com/problems/palindromic-substrings/)

---

## 📝 Problem Description
> [!info]
> Given a string `s`, return the **number** of palindromic substrings in it.
>
> A string is a **palindrome** when it reads the same backward as forward.
>
> A **substring** is a contiguous sequence of characters within the string.

---

## 🧪 Examples
> [!example]
> **Input:** `s = "abc"`
> **Output:** `3`
> **Explanation:** Three palindromic strings: `"a"`, `"b"`, `"c"`.

> [!example]
> **Input:** `s = "aaa"`
> **Output:** `6`
> **Explanation:** Six palindromic strings: `"a"`, `"a"`, `"a"`, `"aa"`, `"aa"`, `"aaa"`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= s.length <= 1000`
> - `s` consists of lowercase English letters.

---

## 🔍 Intuition

Unlike [[LT_0005_Longest_Palindromic_Substring]], I'm not looking for the *best* palindrome — I need to **count every one of them**, and identical strings at different positions count separately (`"aaa"` gives three `"a"`s, not one). So the natural framing is: enumerate all `O(n²)` `(i, j)` index pairs and ask "is `s[i..j]` a palindrome?".

The answer to that question has clean recursive structure: `s[i..j]` is a palindrome iff `s[i] == s[j]` **and** `s[i+1..j-1]` is a palindrome. That's the DP relation, and it's why a 2D table over `(i, j)` is the right shape — the state is exactly the substring bounds.

The version below keeps the `O(n²)` enumeration but answers each check with a **two-pointer scan** rather than reading a cached inner result, so it lands at `O(n³)` in the worst case. That's still comfortably inside `n = 1000` for this problem, but the honest observation is that the `dp` table it allocates never actually serves a hit — see the note under the solution. The real `O(n²)` version either fills the table in increasing-length order, or expands around each of the `2n-1` centres.

> 🟢 *2D Substring Enumeration + Palindrome Check*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Enumerate All `(i, j)` Pairs + Two-Pointer Check

**Why this works:**
- **The enumeration is exhaustive:** the outer loop fixes the start `i`, the inner loop runs `j` from `i` to `n-1`, so every one of the `n(n+1)/2` substrings is visited exactly once — and counted at most once. Duplicate strings at different positions are naturally counted separately, which is what the problem wants.
- **`isPal(s, i, j)` is a plain converging two-pointer walk:** mismatch → bail out `false`; pointers cross → every mirrored pair matched → `true`. The `i <= j` guard handles both odd centres (pointers land on the same char) and even ones (they cross).
- **Single-character substrings are free:** `i == j` makes the while loop body run once and immediately cross, so each of the `n` single chars contributes `1` without a special case.

> [!warning]
> **The `dp` table here is vestigial.** `dp` starts filled with `-1`, and the double loop visits every `(i, j)` exactly once — so `dp[i][j] != -1` is **never** true when the pair is reached, and the cached `1` values are written but never read. Removing `dp` entirely gives the same answer at the same cost. Worth knowing before quoting this as "the DP solution" in an interview.

**Dry Run** (`s = "aaa"`):

| `i` | `j` | substring | `isPal` | `count` |
|-----|-----|-----------|---------|---------|
| 0 | 0 | `"a"` | ✅ | 1 |
| 0 | 1 | `"aa"` | ✅ | 2 |
| 0 | 2 | `"aaa"` | ✅ (outer `a==a`, inner lands on `s[1]`) | 3 |
| 1 | 1 | `"a"` | ✅ | 4 |
| 1 | 2 | `"aa"` | ✅ | 5 |
| 2 | 2 | `"a"` | ✅ | 6 |

Result: `6` ✅

```java
class Solution {
    public int countSubstrings(String s) {
        int len = s.length();
        int[][] dp = new int[len][len];
        for(int [] a : dp) Arrays.fill(a, -1);
        int count = 0;
        for (int i=0; i<len; i++) {
            for(int j=i; j<len; j++) {
                if(dp[i][j]!=-1) {
                    count += dp[i][j];
                }  else {
                    if(isPal(s, i, j)) {
                        dp[i][j] = 1;
                        count += 1;
                    }
                }
            }
        }

        return count;
    }

    private boolean isPal (String s, int i, int j) {
        while (i<=j) {
            if(s.charAt(i)==s.charAt(j)) {
                i++;
                j--;
            } else {
                return false;
            }
        }
        return true;
    }
}
```

- **Time:** `O(n³)` — `O(n²)` pairs × `O(n)` per check · **Space:** `O(n²)` — the (unused) `dp` table

---

## 🔑 Key Insights
- **Counting ≠ maximising.** The same `isPal(i, j)` machinery as [[LT_0005_Longest_Palindromic_Substring]] powers both — only the accumulator changes (`count++` vs. track-best-length). Recognising that saves re-deriving the recurrence in an interview.
- **A memo only pays off when states repeat.** Here the driver loop already visits each `(i, j)` once, so caching the *result* is useless — the win has to come from reusing the **inner** subproblem `(i+1, j-1)`, which means either recursing into `isPal` with the table, or filling the table by increasing substring length.
- **The `O(n²)` route in one line:** expand around each of the `2n-1` centres (`n` odd + `n-1` even) and increment the count on every successful expansion step — no table at all, `O(1)` space.
- `n <= 1000` is the constraint that lets `O(n³)` pass here; the same code would time out if the bound were `10⁵`.

---

## ⚠️ Pitfalls
> [!warning]
> - **De-duplicating the substrings.** Putting them in a `Set` gives `3` for `"aaa"` instead of `6` — the problem counts *occurrences*, not distinct strings.
> - **Inner loop starting at `0` instead of `i`.** That double-counts every substring (and visits invalid `i > j` pairs) — `j` must start at `i`.
> - **Believing the `dp` array is doing work.** As flagged above, it is dead weight in this shape; the complexity is `O(n³)`, not `O(n²)`, and saying otherwise in an interview is an easy way to get caught.

---

## ⏱️ Complexity
- **Time:** `O(n³)` — `O(n²)` substrings, each checked in `O(n)`
- **Space:** `O(n²)` for the `dp` table (`O(1)` if it's dropped, since nothing reads it)
