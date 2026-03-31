---
created: 2026-03-26 23:59
tags:
  - Strings
  - DynamicProgramming
source: https://leetcode.com/problems/longest-palindromic-substring/
problem_id: "5"
difficulty: Medium
status: Completed
review_date:
---

# LT_0005 – Longest Palindromic Substring

## Problem Description
Given a string `s`, return the **longest palindromic substring** in `s`.

## Examples

| Input   | Output | Explanation                     |
|---------|--------|---------------------------------|
| "babad" | "bab"  | "aba" is also a valid answer    |
| "cbbd"  | "bb"   |                                 |
| "a"     | "a"    | Single character edge case      |
| "ac"    | "a"    | Any one valid single char       |

## Constraints
- `1 <= s.length <= 1000`
- `s` consists of only digits and English letters

## Approach

### Intuition
A palindrome mirrors around its center. We can use **Dynamic Programming** to track palindromic substrings:
- Let `dp[i][j] = true` if the substring `s[i...j]` is a palindrome.
- We build the solution bottom-up using smaller substrings to determine the validity of larger ones.

### Invariant
At any point during the DP execution:
- `dp[i][j]` is true **iff**:
  - The outer characters match: `s[i] == s[j]` AND
  - The inner substring is a palindrome: `dp[i+1][j-1]` is true.

## Dry Run

Example: `"babad"`

| i | j | Substring | Condition                     | dp[i][j] | Best |
|---|---|-----------|-------------------------------|----------|------|
| 0 | 0 | b         | single char                   | true     | b    |
| 1 | 1 | a         | single char                   | true     | b    |
| 2 | 2 | b         | single char                   | true     | b    |
| 0 | 2 | bab       | s[i]==s[j] && dp[1][1]        | true     | bab  |
| 1 | 3 | aba       | s[i]==s[j] && dp[2][2]        | true     | aba  |

## Code

```java
// Approach 1: Bottom-Up DP
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

// Approach 2: Top-Down DP (Memoization)
class Solution2 {
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

## Complexity

| Approach                 | Time Complexity | Space Complexity |
|--------------------------|-----------------|------------------|
| Bottom-Up DP             | O(n^2)          | O(n^2)           |
| Top-Down DP (Memoization)| O(n^2)          | O(n^2)           |

## Pattern
- Dynamic Programming on Substrings
- Palindrome DP

## Pitfalls
- Missing base cases (checking for length = 1, length = 2 separately).
- Incorrect index calculation for substring boundaries (`j = i + len - 1`).
- Failing to properly update the `bestLen` and `start` variables.
- Confusion when initializing memoization array (e.g., using `1` vs `-1` for true/false instead of a Boolean object to distinguish uncomputed `0` values).

## Optimization
- **Expand Around Center:** We can optimize the Space Complexity to O(1) while keeping Time Complexity at O(n^2). Treat every character (and every space between characters) as a potential center and expand outward.
- **Manacher's Algorithm:** Can further optimize Time Complexity to O(n), though often considered overkill for general interviews.