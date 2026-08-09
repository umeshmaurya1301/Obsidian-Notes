---
created: 2026-08-09 18:31
tags:
  - dsa
  - dynamic-programming
  - strings
  - hashing
  - memoization
source: https://leetcode.com/problems/word-break/
problem_id: "139"
difficulty: Medium
status: Solved
review_date:
---
# LT_0139 – Word Break

**Link:** [Open Problem](https://leetcode.com/problems/word-break/)

---

## 📝 Problem Description
> [!info]
> Given a string `s` and a dictionary of strings `wordDict`, return `true` if `s` can be segmented into a space-separated sequence of one or more dictionary words.
>
> Note that the same word in the dictionary may be reused **multiple times** in the segmentation.

---

## 🧪 Examples
> [!example]
> **Input:** `s = "leetcode", wordDict = ["leet","code"]`
> **Output:** `true`
> **Explanation:** Return true because `"leetcode"` can be segmented as `"leet code"`.

> [!example]
> **Input:** `s = "applepenapple", wordDict = ["apple","pen"]`
> **Output:** `true`
> **Explanation:** Return true because `"applepenapple"` can be segmented as `"apple pen apple"`. Note that you are allowed to reuse a dictionary word.

> [!example]
> **Input:** `s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]`
> **Output:** `false`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= s.length <= 300`
> - `1 <= wordDict.length <= 1000`
> - `1 <= wordDict[i].length <= 20`
> - `s` and `wordDict[i]` consist of only lowercase English letters.
> - All the strings of `wordDict` are unique.

---

## 🔍 Intuition

The whole problem collapses once I see it as **"where do I place the first cut?"**. If some prefix `s[start..end)` is a dictionary word, then the answer for `s` is exactly the answer for the leftover suffix starting at `end` — the prefix is already paid for and never needs revisiting. That's textbook optimal substructure, so I recurse on the suffix and try every cut point.

Pure recursion re-solves the same suffix over and over: `"catsandog"` reaches index `4` via both `"cats"` and `"cat"`+... paths, and each time it redoes the whole tail. Since the **only** thing that determines the answer is `start` — not how I got there — the state is one integer and memoising on it kills the exponential blowup.

The second speed-up is the dictionary itself: scanning `wordDict` linearly for each substring would cost `O(m)` per check, so I dump it into a `HashSet` for `O(1)` lookups. Brute force falls short because there are `2^(n-1)` ways to place cuts; memoisation reduces that to `n` distinct states, each doing `O(n)` substring work.

> 🟢 *Top-Down DP on Suffix Index + HashSet Lookup*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Top-Down DP (Memoization) + HashSet

**Why this works:**
- **State is just `start`** — "can `s[start..n)` be fully segmented?" The path taken to reach `start` is irrelevant, so one `Map<Integer, Boolean>` covers every subproblem.
- **Every cut is tried:** the loop `end = start+1 .. n` enumerates all prefixes of the suffix, so no valid segmentation is missed. Word reuse is free — nothing marks a dictionary word as consumed.
- **`HashSet` lookup** turns "is this substring a word?" from an `O(m·L)` scan into `O(L)` hashing, so the dictionary size drops out of the complexity entirely.

**Dry Run** (`s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]`):

| call | prefixes found in dict | recurses to | memo written |
|------|-----------------------|-------------|--------------|
| `canBreak(0)` | `"cat"` (end=3), `"cats"` (end=4) | 3, then 4 | — |
| `canBreak(3)` | `"sand"` (end=7) | 7 | — |
| `canBreak(7)` | none (`"o"`, `"og"`) | — | `memo[7] = false` |
| `canBreak(3)` | exhausted | — | `memo[3] = false` |
| `canBreak(4)` | `"and"` (end=7) | 7 → **memo hit** `false` | `memo[4] = false` |
| `canBreak(0)` | exhausted | — | `memo[0] = false` |

Result: `false` ✅ — and note `canBreak(7)` was computed **once**, then served from the memo.

```java
public class Solution {
    public boolean wordBreak(String s, List<String> wordDict) {
        Set<String> wordSet = new HashSet<>(wordDict);  // for O(1) lookup
        Map<Integer, Boolean> memo = new HashMap<>();
        return canBreak(s, 0, wordSet, memo);
    }

    private boolean canBreak(String s, int start, Set<String> wordSet, Map<Integer, Boolean> memo) {
        if (start == s.length()) return true;  // reached end successfully
        if (memo.containsKey(start)) return memo.get(start);

        for (int end = start + 1; end <= s.length(); end++) {
            String sub = s.substring(start, end);
            if (wordSet.contains(sub) && canBreak(s, end, wordSet, memo)) {
                memo.put(start, true);
                return true;
            }
        }

        memo.put(start, false);
        return false;
    }
}
```

- **Time:** `O(n² · L)` — `n` states × `n` cut points, each doing an `O(L)` substring + hash (`L ≤ 20`) · **Space:** `O(n + m·L)` — memo + recursion stack + the word set

---

## 🔑 Key Insights
- **The state is the suffix start, not the path.** Two different prefix decompositions that land on the same index share the same answer — that single observation is what makes memoisation legal.
- **`start == s.length()` returns `true`, not `false`.** Falling off the end means every character was consumed by some word — that's success, and it's the base case that makes the whole recursion bottom out correctly.
- **Reuse needs no special handling.** Because the dictionary is a read-only `Set` and recursion only advances `start`, a word can be matched any number of times for free.
- Constraints (`wordDict[i].length <= 20`) mean the inner loop could be capped at `start + 20` — a real optimisation, but the plain `n` bound is already fast enough at `n = 300`.

---

## ⚠️ Pitfalls
> [!warning]
> - **Forgetting to memoise the `false` branch.** It's tempting to only cache successes, but the failures are exactly what makes `"aaaa…aab"`-style inputs exponential. Both outcomes must be written.
> - **Greedy matching.** Taking the *longest* (or *shortest*) matching prefix and committing to it is wrong — `"cats"` vs `"cat"` in Example 3 shows both must be explored.
> - **Off-by-one in `end`.** The loop must run `end <= s.length()`, since `substring(start, end)` is exclusive on `end` — stopping at `< s.length()` silently drops the final word.

---

## ⏱️ Complexity
- **Time:** `O(n² · L)` where `n = s.length()` and `L` is the max word length
- **Space:** `O(n + m·L)` — memo map + recursion depth `O(n)` + the `HashSet` of `m` words
