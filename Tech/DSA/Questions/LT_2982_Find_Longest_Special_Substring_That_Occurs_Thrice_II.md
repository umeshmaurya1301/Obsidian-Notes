---
created: 2026-05-31 00:00
tags:
  - dsa
  - string
  - prefix-sum
  - counting
  - run-length
source: https://leetcode.com/problems/find-longest-special-substring-that-occurs-thrice-ii/
problem_id: "2982"
difficulty: Medium
status: Solved
review_date:
---
# LT_2982 – Find Longest Special Substring That Occurs Thrice II

**Link:** [Open Problem](https://leetcode.com/problems/find-longest-special-substring-that-occurs-thrice-ii/)

---

## 📝 Problem Description
> [!info]
> You are given a string `s` that consists of lowercase English letters.
>
> A string is called **special** if it is made up of only a single character. For example, `"abc"` is not special, whereas `"ddd"`, `"zz"`, and `"f"` are special.
>
> Return the length of the **longest special substring** of `s` which occurs **at least thrice**, or `-1` if no special substring occurs at least thrice.
>
> A **substring** is a contiguous non-empty sequence of characters within a string.
>
> **Note:** This is the same problem as 2981 but with `n` up to `5 × 10^5`, requiring an O(n) solution.

---

## 🧪 Examples
> [!example]
> **Input:** `s = "aaaa"`
> **Output:** `2`
> **Explanation:** The longest special substring occurring at least thrice is `"aa"`, appearing at 3 overlapping positions.

> [!example]
> **Input:** `s = "abcdef"`
> **Output:** `-1`
> **Explanation:** Every special substring is a unique single character — none appear thrice.

> [!example]
> **Input:** `s = "abcaba"`
> **Output:** `1`
> **Explanation:** `"a"` appears exactly 3 times; no longer special substring reaches that threshold.

---

## ⚠️ Constraints
> [!warning]
> - `3 <= s.length <= 5 * 10^5`
> - `s` consists of only lowercase English letters.

---

## 🔍 Intuition

A special substring lives entirely within a consecutive run of one character, so runs are the only thing that matters. The challenge versus problem 2981 is that n can be 5×10^5, so we need O(n) rather than an inner per-run loop over all lengths. The trick is a two-phase mark-and-sweep on a 2D array `lenArr[26][n+1]`. In the **mark phase**, for a run of length `len`, I increment `lenArr[ch][k]` for every `k` from 1 to `len` — the total work across all runs equals n, since every character belongs to exactly one run. After marking, `lenArr[ch][k]` equals the number of runs of character ch whose length is ≥ k. A **right-to-left suffix sum** then transforms this: after the sum, `lenArr[ch][j]` equals the total number of occurrences of the length-j special substring of ch across the whole string (because a run of length L contributes exactly `L - j + 1` such substrings, which is what the suffix sum computes). Finally, a downward sweep per character finds the maximum length with count ≥ 3.

> 🟢 *Run-Length Marking + Suffix Sum*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Run-Length Marking + Suffix Sum

**Why this works:**
- After the mark phase, `lenArr[ch][k]` = number of runs with length ≥ k; the suffix sum converts this into total occurrence counts in O(26n) without any per-run length loop.
- The mathematical identity: suffix sum at position j = Σ over runs of `max(0, run_len - j + 1)`, which is exactly the total occurrences of a length-j special substring.
- Sweeping from high j to low gives the maximum valid length in a single pass per character.

**Dry Run** (`s = "aaaa"`, n = 4):

**Phase 1 — Mark:**
- Run: `ch='a'`, `len=4` → `lenArr[0][1..4]` each get `++`
- `lenArr[0]` = `[0, 1, 1, 1, 1]` (indices 0 to 4)

**Phase 2 — Suffix Sum (character 'a'):**

| `j` | `val` (before) | running `sum` | `lenArr[0][j]` (after) |
|-----|----------------|---------------|------------------------|
| 4   | 1              | 1             | 1                      |
| 3   | 1              | 2             | 2                      |
| 2   | 1              | 3             | 3                      |
| 1   | 1              | 4             | 4                      |

`lenArr[0]` = `[0, 4, 3, 2, 1]`
→ length-1 substrings: 4 occurrences, length-2: 3, length-3: 2, length-4: 1 ✓

**Phase 3 — Sweep:**
- `j=3`: `lenArr[0][3]=2` < 3 ✗
- `j=2`: `lenArr[0][2]=3` ≥ 3 ✓ → `max=2`, break

**Return:** `2` ✓

```java
class Solution {
    public int maximumLength(String s) {
        int n = s.length();
        int[][] lenArr = new int[26][n+1];

        for(int i=0; i<n;) {
            char ch = s.charAt(i);
            int j=i;
            while(j<n && ch== s.charAt(j)) {
                j++;
            }
            int len = j-i;
            for(int k=1; k<=len; k++) {
                lenArr[ch-'a'][k]++;
            }
            i=j;
        }

        for(int i=0; i<lenArr.length; i++) {
            int sum = 0;
            for (int j=n; j>=1; j--) {
                int val = lenArr[i][j];
                sum += val;
                lenArr[i][j] = sum;
            }
        }

        int max = -1;
        for(int i=0; i<lenArr.length; i++) {
            for(int j=n-1; j>=0; j--) {
                if(lenArr[i][j]>=3) {
                    max = Math.max(max, j);
                    break;
                }
            }
        }
        return max;
    }
}
```

---

## 🔑 Key Insights
- After the mark phase, `lenArr[ch][k]` = count of runs with length ≥ k (not total occurrences yet).
- The suffix sum does the heavy lifting: it transforms "count of runs ≥ k" into "total occurrences of length-j substrings" via the identity: `Σ_{k=j}^{n} f(k) = Σ over runs of max(0, len - j + 1)`.
- Total marks in phase 1 = Σ run lengths = n — so the mark phase is O(n) despite the inner loop.
- Compare to 2981: that solution computed `count[l] += (len - l + 1)` directly in the inner loop — same math, but the suffix-sum form here separates concerns cleanly and scales to large n.

---

## ⚠️ Pitfalls
> [!warning]
> - Misreading phase 1 output: after marking, `lenArr[ch][k]` is **not** occurrence count yet — it's "how many runs have length ≥ k". Skipping the suffix sum gives wrong answers.
> - The suffix sum loop must run from `j=n` down to `j=1`; starting from `j=n-1` misses the longest run contribution.
> - `lenArr[i][0]` is never written in phase 1 and not touched in the suffix sum loop (which starts at j=1) — the sweep correctly bottoms out at 0 without false positives.

---

## ⏱️ Complexity
- **Time:** `O(n)` — mark phase is O(n) (each character visited once), suffix sum is O(26n), sweep is O(26n).
- **Space:** `O(26n)` for the `lenArr` table.
