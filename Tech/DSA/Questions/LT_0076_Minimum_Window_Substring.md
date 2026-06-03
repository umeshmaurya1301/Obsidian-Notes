---
created: 2026-06-01 11:00
tags:
  - dsa
  - strings
  - hash-table
  - sliding-window
source: https://leetcode.com/problems/minimum-window-substring/
problem_id: "76"
difficulty: Hard
status: Solved
review_date:
---
# LT_0076 – Minimum Window Substring

**Link:** [Open Problem](https://leetcode.com/problems/minimum-window-substring/)

---

## 📝 Problem Description
> [!info]
> Given two strings `s` and `t` of lengths `m` and `n` respectively, return the **minimum window substring** of `s` such that every character in `t` (including duplicates) is included in the window.
>
> If there is no such substring, return the empty string `""`.
>
> The testcases will be generated such that the answer is **unique**.

---

## 🧪 Examples
> [!example]
> **Input:** `s = "ADOBECODEBANC"`, `t = "ABC"`
> **Output:** `"BANC"`
> **Explanation:** The minimum window `"BANC"` includes `'A'`, `'B'`, and `'C'` from `t`.

> [!example]
> **Input:** `s = "a"`, `t = "a"`
> **Output:** `"a"`
> **Explanation:** The entire string `s` is the minimum window.

> [!example]
> **Input:** `s = "a"`, `t = "aa"`
> **Output:** `""`
> **Explanation:** Both `'a'`s from `t` must be included. The largest window of `s` has only one `'a'`.

---

## ⚠️ Constraints
> [!warning]
> - `m == s.length()`, `n == t.length()`
> - `1 <= m, n <= 10^5`
> - `s` and `t` consist of uppercase and lowercase English letters.
>
> **Follow-up:** Can you find an algorithm that runs in `O(m + n)` time?

---

## 🔍 Intuition

The window must contain every character from `t` with the correct frequency. The brute force — check every substring — is `O(m² · n)`. Instead, use a sliding window: expand `right` to pull characters in, and shrink `left` whenever the window is valid to try to minimize it.

The real trick is avoiding an `O(|t|)` validity check at every step. We track two things: `required` (distinct character types in `t`) and `formed` (how many of those types are currently fully satisfied in the window). When `window[ch]` reaches exactly `target[ch]`, we increment `formed`. When shrinking causes `window[leftChar]` to fall below `target[leftChar]`, we decrement `formed`. Both updates are `O(1)`, so the full algorithm is `O(m + n)`.

> 🟢 *Sliding Window + Two HashMaps + Formed/Required Counter*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Sliding Window + Formed/Required Counter

**Why this works:**
- `required = target.size()` counts distinct character types in `t` — not total characters.
- `formed` tracks how many of those types are fully satisfied in the window at any moment.
- `formed == required` is an `O(1)` validity check — no need to scan the entire map.
- We record the minimum window before shrinking, then shrink aggressively until the window becomes invalid.

**Dry Run** (`s = "ADOBECODEBANC"`, `t = "ABC"`):

`target = {A:1, B:1, C:1}`, `required = 3`

**Phase 1 — Expand until first valid window:**

| `right` | `ch` | `window` (relevant) | `formed` | action |
|---------|------|---------------------|----------|--------|
| 0 | A | A:1 | 1 | A satisfied |
| 1 | D | — | 1 | skip |
| 2 | O | — | 1 | skip |
| 3 | B | B:1 | 2 | B satisfied |
| 4 | E | — | 2 | skip |
| 5 | C | C:1 | **3** | C satisfied → window valid! |

Window `[0,5]` = `"ADOBEC"`, len=6 → `minLen=6, start=0`

**Phase 2 — Shrink while valid:**

Remove `s[0]=A`: `window[A]=0 < target[A]=1` → `formed=2`, `left=1`. Window invalid, expand.

**Phase 3 — Expand right again to re-satisfy `A`:**

| `right` | `ch` | `formed` |
|---------|------|----------|
| 6 | O | 2 |
| 7 | D | 2 |
| 8 | E | 2 |
| 9 | B | 2 (B was already satisfied, window[B] goes 1→2, no change) |
| 10 | A | **3** (A:1 = target[A]:1 → satisfied again) |

Window `[1,10]` = `"DOBECODEBA"`, len=10 → no update (10 > 6).

**Phase 4 — Shrink aggressively:**

| remove | `left` | `formed` | new window len | update? |
|--------|--------|----------|----------------|---------|
| D | 2 | 3 | 9 | no |
| O | 3 | 3 | 8 | no |
| B | 4 | 3 | 7 | no (window[B]=1, still == target[B]=1, don't decrement formed) |
| E | 5 | 3 | 6 | no |
| C | 6 | 2 | — | window[C]=0 < target[C]=1 → formed=2, left=6. Invalid! |

**Phase 5 — Expand to re-satisfy `C`:**

| `right` | `ch` | `formed` |
|---------|------|----------|
| 11 | N | 2 |
| 12 | C | **3** |

Window `[6,12]` = `"ODEBANC"`, len=7 → no update.

**Phase 6 — Shrink again:**

| remove | `left` | `formed` | new window len | update? |
|--------|--------|----------|----------------|---------|
| O | 7 | 3 | 6 | no |
| D | 8 | 3 | 5 | **yes** → `minLen=5, start=8` → `"EBANC"` |
| E | 9 | 3 | 4 | **yes** → `minLen=4, start=9` → `"BANC"` ✅ |
| B | 10 | 2 | — | window[B]=0 < target[B]=1 → formed=2, left=10. Invalid! |

Loop ends. `s.substring(9, 9+4)` = **`"BANC"`** ✅

```java
class Solution {
    public String minWindow(String s, String t) {

        if (s.length() < t.length()) {
            return "";
        }

        Map<Character, Integer> target = new HashMap<>();

        for (char ch : t.toCharArray()) {
            target.put(ch, target.getOrDefault(ch, 0) + 1);
        }

        int required = target.size();
        int formed = 0;

        Map<Character, Integer> window = new HashMap<>();

        int left = 0;

        int minLen = Integer.MAX_VALUE;
        int start = 0;

        for (int right = 0; right < s.length(); right++) {

            char ch = s.charAt(right);

            window.put(ch, window.getOrDefault(ch, 0) + 1);

            if (target.containsKey(ch) &&
                window.get(ch).intValue() == target.get(ch).intValue()) {
                formed++;
            }

        while (formed == required) {

                if (right - left + 1 < minLen) {
                    minLen = right - left + 1;
                    start = left;
                }

                char leftChar = s.charAt(left);

                window.put(leftChar, window.get(leftChar) - 1);

                if (target.containsKey(leftChar) &&
                    window.get(leftChar) < target.get(leftChar)) {
                    formed--;
                }

                left++;
            }
        }

        return minLen == Integer.MAX_VALUE
                ? ""
                : s.substring(start, start + minLen);
    }
}
```

---

## 🔑 Key Insights

- **`required` vs `formed` counter trick** — instead of checking all characters in `target` each time, maintain `formed` as a running counter of satisfied character types. This collapses an O(|t|) check into O(1).
- **Record minimum before shrinking, not after** — the minimum is captured at the top of the `while` loop, before the left pointer moves. This ensures we record every valid window before invalidating it.
- **Shrink aggressively** — stay in the `while` loop as long as `formed == required`, capturing smaller and smaller windows. When you overshoot and `formed` drops, the outer `for` takes over.
- **`target.size()` not `t.length()`** — `required` counts distinct character *types*, not total characters. `t = "AAB"` gives `required = 2` ({A:2, B:1}), meaning both A-count and B-count must be satisfied simultaneously.
- **Why `.intValue()` instead of `==`** — Java caches `Integer` objects only for values −128 to 127. For frequencies above 127, `window.get(ch) == target.get(ch)` compares object references (not values) and can silently return `false`. `.intValue()` forces primitive int comparison, making it correct for all inputs.

---

## ⚠️ Pitfalls
> [!warning]
> - Using `==` to compare `Integer` objects from the map — works for small values (cached range −128..127) but silently breaks for larger frequencies. Always use `.intValue()` or `Objects.equals()`.
> - Incrementing `formed` when `window.get(ch) > target.get(ch)` — `formed` should only increment when the count transitions from `target[ch]-1` to exactly `target[ch]` (i.e., `==`, not `>=`). The current code uses `==` correctly; using `>=` would over-count `formed`.
> - Decrementing `formed` only when `window.get(leftChar) < target.get(leftChar)` — correct. If window still has enough of that character after removal (count stays ≥ target), `formed` should not change.
> - Off-by-one in result: use `s.substring(start, start + minLen)` not `s.substring(start, start + minLen - 1)`.
> - Forgetting to check `minLen == Integer.MAX_VALUE` before returning — if no valid window exists, `start + minLen` would overflow.

---

## ⏱️ Complexity
- **Time:** `O(m + n)` — building `target` costs `O(n)`; each character in `s` enters and exits the window at most once, so the two pointers together traverse `s` at most twice → `O(m)`.
- **Space:** `O(m + n)` — `target` holds at most `O(n)` distinct characters; `window` holds at most `O(m)` distinct characters (bounded by the character set size, so in practice `O(1)` for ASCII/Unicode alphabet, but `O(m)` in the general case).
