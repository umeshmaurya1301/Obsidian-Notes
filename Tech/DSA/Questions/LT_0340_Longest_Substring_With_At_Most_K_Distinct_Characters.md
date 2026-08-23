---
created: 2026-08-22 00:00
tags:
  - dsa
  - sliding-window
  - hash-table
source: https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/
problem_id: "340"
difficulty: Medium
status: Solved
review_date:
---
# LT_0340 – Longest Substring With At Most K Distinct Characters

**Link:** [Open Problem](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/)

---

## 📝 Problem Description
> [!info]
> Given a string `s` and an integer `k`, return the length of the longest substring of `s` that contains **at most `k` distinct characters**.

---

## 🧪 Examples
> [!example]
> **Input:** `s = "eceba", k = 2`
> **Output:** `3`
> **Explanation:** The substring is `"ece"` with length `3`.

> [!example]
> **Input:** `s = "aa", k = 1`
> **Output:** `2`
> **Explanation:** The substring is `"aa"` with length `2`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= s.length <= 5 * 10^4`
> - `0 <= k <= 50`

---

## 🔍 Intuition

This is a variable-size sliding window where the window's validity condition is "at most `k` distinct characters" instead of a fixed length or sum. As `right` advances, I only ever *add* one character, so the map's distinct-character count can only grow past `k` by exactly one — I never need to shrink more than one character out per step to restore validity. The trick is knowing **which** character to evict: not the physically leftmost index of the window, but the character whose *most recent* occurrence is furthest left, because that's the one that isn't seen again until later and can be safely dropped without losing any better answer.

Storing `char -> lastSeenIndex` in a map instead of a raw frequency count is what makes eviction cheap to reason about: once a character's last-seen index is smaller than the new `left`, it's genuinely gone from the window, so removing it from the map and jumping `left` straight to `lastSeenIndex + 1` is correct — no need to shrink one position at a time.

> 🟢 *Sliding Window + Map (char → last seen index)*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Sliding Window with Last-Seen-Index Map

**Why this works:**
- The map holds at most `k+1` entries at any point in the loop body (it's only ever one over budget, right after inserting the new character), so as soon as `size == k+1` there is exactly one character to evict.
- The evicted character is the one with the **smallest last-seen index** — i.e., the character that would otherwise force a much smaller window if kept, since it hasn't appeared again since that earliest point.
- `left` jumps directly to `evictedIndex + 1` in one shot rather than incrementally shrinking, since everything strictly before that index is guaranteed to belong to already-evicted or still-valid characters.
- `maxLen` is updated every iteration (not just after an eviction), so a window that stays valid without ever needing to evict is still captured.

**Dry Run** (`s = "eceba", k = 2`):

| `right` | `currChar` | map after put | size | evict? | `left` | `maxLen` |
|---|---|---|---|---|---|---|
| 0 | `e` | `{e:0}` | 1 | no | 0 | 1 |
| 1 | `c` | `{e:0, c:1}` | 2 | no | 0 | 2 |
| 2 | `e` | `{e:2, c:1}` | 2 | no | 0 | 3 |
| 3 | `b` | `{e:2, c:1, b:3}` | 3 | yes → min value is `c:1` → remove `c` | 2 | 3 |
| 4 | `a` | `{e:2, b:3, a:4}` | 3 | yes → min value is `e:2` → remove `e` | 3 | 3 |

Final `maxLen = 3` (the window `"ece"` at `right=2`), matching the expected output.

```java
class Solution {
    public int lengthOfLongestSubstringKDistinct(String s, int k) {
        int len = s.length();
        if (len < (k+1)) return len;
        if (k==0) return 0;

        int left = 0;        

        Map<Character, Integer> map = new HashMap<>();
        int maxLen = 1;

        for (int right=0; right<len; right++) {
            char currChar = s.charAt(right);
            map.put(currChar, right);

            if (map.size() == k+1) {
                int leftMostIdxToDelete = Collections.min(map.values());
                char charKey = s.charAt(leftMostIdxToDelete);
                map.remove(charKey);
                left = leftMostIdxToDelete + 1;
            }
            maxLen = Math.max(maxLen, right-left + 1);
        }

        return maxLen;        
    }
}
```

- **Time:** `O(n * k)` · **Space:** `O(k)`

---

## 🔑 Key Insights
- Track **last-seen index** per character, not just a frequency count — that's what lets `left` jump directly to `evictedIndex + 1` instead of shrinking one step at a time.
- The character to evict is the one with the **smallest last-seen index**, since it's the one that's been "dead weight" the longest and can't extend the window any further without violating the `k`-distinct condition.
- `Collections.min(map.values())` scans at most `k+1` entries every time it's called, so this version is `O(n * k)`, not `O(n)`. A `LinkedHashMap` (evict-oldest-on-access) or a small ordered structure (TreeMap/deque of indices) removes that scan and gets to `O(n log k)` or `O(n)` — worth mentioning as the optimization if asked to improve it.
- The `len < k+1` early return is a valid shortcut: if the string is short enough that it can't even contain `k+1` distinct characters, the whole string is trivially a valid answer.

---

## ⚠️ Pitfalls
> [!warning]
> - **Evicting by window position instead of by last-seen index.** The character to remove is whichever has the smallest value in the map (its most recent occurrence), *not* necessarily `s.charAt(left)` — the two only coincide by accident.
> - **Forgetting the `k == 0` edge case.** With `k = 0` no substring can have any distinct characters, so the answer is always `0`; the main loop's map-size logic never naturally reaches this case since a single character always makes `size == 1`.
> - **Assuming this is `O(n)`.** `Collections.min` over the map's values is a linear scan of up to `k+1` elements, run inside the main loop — the true complexity is `O(n * k)`, which matters if asked to justify or optimize the approach.

---

## ⏱️ Complexity
- **Time:** `O(n * k)` — for each of the `n` characters, evicting (when triggered) scans up to `k+1` map values to find the minimum
- **Space:** `O(k)` — the map holds at most `k+1` distinct characters at any time
