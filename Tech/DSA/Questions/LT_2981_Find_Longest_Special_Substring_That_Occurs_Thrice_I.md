---
created: 2026-05-31 00:00
tags:
  - dsa
  - string
  - hash-map
  - counting
  - run-length
source: https://leetcode.com/problems/find-longest-special-substring-that-occurs-thrice-i/
problem_id: "2981"
difficulty: Medium
status: Solved
review_date:
---
# LT_2981 – Find Longest Special Substring That Occurs Thrice I

**Link:** [Open Problem](https://leetcode.com/problems/find-longest-special-substring-that-occurs-thrice-i/)

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

---

## 🧪 Examples
> [!example]
> **Input:** `s = "aaaa"`
> **Output:** `2`
> **Explanation:** The longest special substring which occurs at least thrice is `"aa"`, which occurs 3 times at overlapping positions.

> [!example]
> **Input:** `s = "abcdef"`
> **Output:** `-1`
> **Explanation:** Every special substring is a single unique character — each appears only once. No special substring occurs thrice.

> [!example]
> **Input:** `s = "abcaba"`
> **Output:** `1`
> **Explanation:** The longest special substring occurring at least thrice is `"a"`, which appears exactly 3 times.

---

## ⚠️ Constraints
> [!warning]
> - `3 <= s.length <= 50`
> - `s` consists of only lowercase English letters.

---

## 🔍 Intuition

A special substring is made of a single character, so it can only exist within a consecutive run of that character — cross-run substrings are never special. Rather than checking every substring (O(n²) pairs × O(n) comparison), I group the string into contiguous character runs and record each run's length. The crucial counting insight: a run of length `len` contributes exactly `len - l + 1` occurrences of any special substring of length `l` (it slides from position 0 to `len - l` within the run). I accumulate these counts across all runs of the same character, then sweep from the largest `l` downward — the first `l` with a count ≥ 3 is the answer for that character.

> 🟢 *Run-Length Grouping + Frequency Counting*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Run-Length Grouping + Frequency Counting

**Why this works:**
- Special substrings are confined to single-character runs, so only run lengths matter — we never need to examine cross-run positions.
- For a run of length `len`, the formula `len - l + 1` gives the exact count of length-`l` special substrings within it; summing across runs of the same character gives the global count.
- Sweeping `l` from 50 → 1 finds the maximum valid length in one pass without needing to sort.

**Dry Run** (`s = "aaaa"`):

Run extraction scan:
```
i=0, ch='a', j runs to 4 → len=4
map = { 'a': [4] }
```

Counting for `ch = 'a'`, `lens = [4]`:

| `l` | formula `4 - l + 1` | `count[l]` |
|-----|---------------------|------------|
| 1   | 4                   | 4          |
| 2   | 3                   | 3          |
| 3   | 2                   | 2          |
| 4   | 1                   | 1          |

Sweep `l = 50 → 1`:
- `l=4`: `count[4]=1` < 3 ✗
- `l=3`: `count[3]=2` < 3 ✗
- `l=2`: `count[2]=3` ≥ 3 ✓ → `maxLen = 2`, break

**Return:** `2` ✓

```java
public class Solution {
    public int maximumLength(String s) {
        Map<Character, List<Integer>> map = new HashMap<>();

        int n = s.length();
        for (int i = 0; i < n;) {
            char ch = s.charAt(i);
            int j = i;
            while (j < n && s.charAt(j) == ch) {
                j++;
            }
            int len = j - i;
            map.computeIfAbsent(ch, k -> new ArrayList<>()).add(len);
            i = j;
        }

        int maxLen = -1;

        for (char ch : map.keySet()) {
            List<Integer> lens = map.get(ch);
            int[] count = new int[51]; // since max len = 70
            for (int len : lens) {
                for (int l = 1; l <= len; l++) {
                    count[l] += (len - l + 1); // FIXED LINE
                }
            }

            for (int l = 50; l >= 1; l--) {
                if (count[l] >= 3) {
                    maxLen = Math.max(maxLen, l);
                    break;
                }
            }
        }

        return maxLen;
    }
}
```

---

## 🔑 Key Insights
- `len - l + 1` is the exact number of times a special substring of length `l` appears within a single run of length `len` — this is the core formula.
- Runs of the same character are independent contributors; their counts simply add up.
- Store only run lengths, not positions — positions are irrelevant once you know the count formula.
- Sweeping from large `l` to small gives the maximum valid length without a separate `max` scan.

---

## ⚠️ Pitfalls
> [!warning]
> - Using `count[l] += 1` (flat count) instead of `count[l] += (len - l + 1)` — this undercounts overlapping occurrences within a run.
> - Overwriting `count[l]` on each new `len` instead of accumulating across all runs of the same character.
> - Returning `0` instead of `-1` when no valid substring exists — the problem explicitly requires `-1`.

---

## ⏱️ Complexity
- **Time:** `O(n²)` — run extraction is `O(n)`; counting is `O(Σ run_len²)` which is `O(n²)` worst case (one long run); sweep is `O(26 × 50) = O(1)`.
- **Space:** `O(n)` — storing run lengths in the map; `count` array is `O(1)` per character.
