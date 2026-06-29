---
created: 2026-03-26 23:59
tags:
  - dsa
  - string
  - dynamic-programming
  - two-pointers
source: https://leetcode.com/problems/longest-palindromic-substring/
problem_id: "5"
difficulty: Medium
status: Solved
review_date:
---
# LT_0005 – Longest Palindromic Substring

**Link:** [Open Problem](https://leetcode.com/problems/longest-palindromic-substring/)

---

## 📝 Problem Description
> [!info]
> Given a string `s`, return the **longest palindromic substring** in `s`.

---

## 🧪 Examples
> [!example]
> **Input:** `s = "babad"`
> **Output:** `"bab"`
> **Explanation:** `"aba"` is also a valid answer.

> [!example]
> **Input:** `s = "cbbd"`
> **Output:** `"bb"`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= s.length <= 1000`
> - `s` consists of only digits and English letters.

---

## 🔍 Intuition

Every palindrome has exactly one center — either a single character (odd length) or a gap between two characters (even length). Instead of checking every possible substring pair `(i, j)`, we can iterate over every possible center and expand outward as long as the characters match. There are `2n - 1` possible centers (`n` character centers + `n-1` gap centers), and each expansion costs at most `O(n)`, giving `O(n²)` overall. Compared to DP, this is identical in time but uses `O(1)` space — no table, no recursion, no HashMap.

> 🟢 *Expand Around Center*

---

## 🧠 Evolution of Solutions

### 🔵 Approach 1 — Top-Down DP (Memoization)

`isPal(i, j)` is true if `s[i] == s[j]` and `isPal(i+1, j-1)` is true. Cache in a 2D array using sentinel values (`1` = palindrome, `-1` = not).

- **Time:** `O(n²)` | **Space:** `O(n²)`

```java
class Solution {
    public String longestPalindrome(String s) {
        int n = s.length();
        int[][] memo = new int[n][n];

        int bestLen = 1, bestStart = 0;

        for (int i = 0; i < n; i++) {
            for (int j = i; j < n; j++) {
                if (isPal(s, i, j, memo) == 1 && (j - i + 1) > bestLen) {
                    bestLen = j - i + 1;
                    bestStart = i;
                }
            }
        }

        return s.substring(bestStart, bestStart + bestLen);
    }

    private int isPal(String s, int i, int j, int[][] memo) {
        if (i >= j) return 1;

        if (memo[i][j] != 0) return memo[i][j];

        if (s.charAt(i) == s.charAt(j) && isPal(s, i + 1, j - 1, memo) == 1) {
            memo[i][j] = 1;
        } else {
            memo[i][j] = -1;
        }

        return memo[i][j];
    }
}
```

---

### 🔵 Approach 2 — Bottom-Up DP (Tabulation)

Fill `dp[i][j]` bottom-up: all length-1 substrings are palindromes, then length-2, then length-3 and beyond.

- **Time:** `O(n²)` | **Space:** `O(n²)`

```java
class Solution {
    public String longestPalindrome(String s) {
        int n = s.length();
        if (n <= 1) return s;

        boolean[][] dp = new boolean[n][n];
        int bestLen = 1, start = 0;

        for (int i = 0; i < n; i++) {
            dp[i][i] = true;
        }

        for (int i = 0; i < n - 1; i++) {
            if (s.charAt(i) == s.charAt(i + 1)) {
                dp[i][i + 1] = true;
                start = i;
                bestLen = 2;
            }
        }

        for (int len = 3; len <= n; len++) {
            for (int i = 0; i + len - 1 < n; i++) {
                int j = i + len - 1;

                if (s.charAt(i) == s.charAt(j) && dp[i + 1][j - 1]) {
                    dp[i][j] = true;

                    if (len > bestLen) {
                        bestLen = len;
                        start = i;
                    }
                }
            }
        }

        return s.substring(start, start + bestLen);
    }
}
```

---

### ✅ Approach 3 — Expand Around Center

**Why this works:**
- Every palindrome has a unique center: a character (odd) or gap between two characters (even).
- For each index `i`, expand both `(i, i)` and `(i, i+1)` to catch both center types — missing either means missing whole categories of palindromes.
- `start`/`end` are recovered from the center index and length using integer-division formulas that work for both odd and even cases without branching.

**Dry Run** (`s = "babad"`):

| `i` | `expand(i,i)` | `len1` | `expand(i,i+1)` | `len2` | `len` | `start` | `end` | result |
|-----|--------------|--------|----------------|--------|-------|---------|-------|--------|
| 0   | "b"          | 1      | b≠a → ""       | 0      | 1     | 0       | 0     | "b"    |
| 1   | "bab"        | 3      | a≠b → ""       | 0      | 3     | 0       | 2     | "bab"  |
| 2   | "aba"        | 3      | b≠a → ""       | 0      | 3     | —       | —     | (same) |
| 3   | "a"          | 1      | a≠d → ""       | 0      | 1     | —       | —     | —      |
| 4   | "d"          | 1      | out of bounds  | 0      | 1     | —       | —     | —      |

Final: `s.substring(0, 3)` = **"bab"**

```java
class Solution {
    public String longestPalindrome(String s) {
        int start = 0;
        int end = 0;

        for (int i = 0; i < s.length(); i++) {

            int len1 = expand(s, i, i);       // Odd palindrome
            int len2 = expand(s, i, i + 1);   // Even palindrome

            int len = Math.max(len1, len2);

            if (len > end - start + 1) {

                start = i - (len - 1) / 2;
                end   = i + len / 2;
            }
        }

        return s.substring(start, end + 1);
    }

    private int expand(String s, int left, int right) {

        while (left >= 0 &&
               right < s.length() &&
               s.charAt(left) == s.charAt(right)) {

            left--;
            right++;
        }

        return right - left - 1;
    }
}
```

---

### 🧩 Deep Dive — How Every Piece of This Solution Is Derived

#### Why check both `expand(i, i)` and `expand(i, i+1)`?

There are exactly two center types:

**Odd length** — center is a character.
```
r a c e c a r
      ^
expand(3, 3)
```

**Even length** — center is the gap between two characters.
```
a b b a
  ^ ^
expand(1, 2)
```

If we only call `expand(i, i)` — even palindromes like `"abba"` are never found.
If we only call `expand(i, i+1)` — odd palindromes like `"racecar"` are never found.
Both calls are mandatory, and for the same `i`, both can fire simultaneously (e.g., `"aaaa"` at `i=1` finds `"aaa"` odd and `"aaaa"` even).

---

#### Why `return right - left - 1` in `expand()`?

After the loop exits, `left` and `right` have each gone **one step past** the palindrome boundary.

Example — `expand("aba", 1, 1)`:
```
Start:  left=1, right=1  →  match 'a'
Step 1: left=0, right=2  →  match 'a','a'... wait, s[0]='a', s[2]='a'? For "aba": s[0]='a', s[1]='b', s[2]='a'
Step 1: left=0, right=2  → s[0]='a' == s[2]='a' → left=-1, right=3
Exit: left=-1, right=3
Length = right - left - 1 = 3 - (-1) - 1 = 3  ✓
```

The `-1` corrects for the one over-expanded step on each side.

---

#### Why does `start = i - (len-1)/2` and `end = i + len/2` work for both odd and even?

The formula relies on integer division:

| `len` | `(len-1)/2` | `len/2` | Behaviour |
|-------|------------|---------|-----------|
| 1     | 0          | 0       | center only |
| 2     | 0          | 1       | even: start at i, end at i+1 |
| 3     | 1          | 1       | odd: symmetric around i |
| 4     | 1          | 2       | even: left-biased center |
| 5     | 2          | 2       | odd: symmetric around i |
| 6     | 2          | 3       | even: left-biased center |

For **odd** lengths: `(len-1)/2 == len/2` → perfectly symmetric around `i`.
For **even** lengths: `len/2` is one larger → the extra character lands to the right of `i`, matching how `expand(i, i+1)` works (right center is at `i+1`).

Verification:

`"racecar"` — `i=3`, `len=7`:
```
start = 3 - (7-1)/2 = 3 - 3 = 0
end   = 3 + 7/2     = 3 + 3 = 6  ✓
```

`"abba"` — `i=1`, `len=4`:
```
start = 1 - (4-1)/2 = 1 - 1 = 0
end   = 1 + 4/2     = 1 + 2 = 3  ✓
```

No `if`/`else` needed. One formula covers both.

---

#### Approach comparison

| Approach              | Time     | Space    |
|-----------------------|----------|----------|
| Memoization (Top-Down)| `O(n²)`  | `O(n²)`  |
| Tabulation (Bottom-Up)| `O(n²)`  | `O(n²)`  |
| Expand Around Center  | `O(n²)`  | **`O(1)`** |
| Manacher's Algorithm  | `O(n)`   | `O(n)`   |

Expand Around Center is the **interview sweet spot** — same time as DP with no extra space and simpler code. Manacher's is rarely expected.

---

## 🔑 Key Insights
- There are exactly `2n - 1` centers (`n` characters + `n-1` gaps); iterating over all of them covers every possible palindrome.
- `expand()` returns the length, not the indices — recovering `(start, end)` from center + length via `i - (len-1)/2` and `i + len/2` is cleaner than returning a pair.
- For the same index `i`, both `len1` (odd) and `len2` (even) can be nonzero simultaneously — `"aaaa"` at `i=1` finds both `"aaa"` (len 3) and `"aaaa"` (len 4).
- The `while` in `expand()` exits one step past the valid palindrome on each side — hence the `-1` in `right - left - 1`.

---

## ⚠️ Pitfalls
> [!warning]
> - Calling only `expand(i, i)` — misses all even-length palindromes entirely.
> - Off-by-one in `expand()`: forgetting the `-1` in `right - left - 1` overcounts by 2.
> - Using `s.substring(start, end)` instead of `s.substring(start, end + 1)` — `end` is inclusive here, but `substring` is exclusive at the right boundary.
> - Initialising `start = end = 0` means the default answer is `s.charAt(0)` — correct since the minimum palindrome is a single character, but confirm the condition `len > end - start + 1` holds (it starts at 1, so `len >= 2` triggers an update).

---

## ⏱️ Complexity
- **Time:** `O(n²)` — `2n - 1` centers, each expansion up to `O(n)` in the worst case.
- **Space:** `O(1)` — only four integer variables; no auxiliary arrays.
