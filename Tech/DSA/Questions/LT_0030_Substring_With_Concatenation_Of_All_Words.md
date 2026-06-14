---
created: 2026-06-14 10:30
tags:
  - dsa
  - hash-table
  - string
  - sliding-window
source: https://leetcode.com/problems/substring-with-concatenation-of-all-words/
problem_id: "30"
difficulty: Hard
status: Solved
review_date:
---
# LT_0030 – Substring with Concatenation of All Words

**Link:** [Open Problem](https://leetcode.com/problems/substring-with-concatenation-of-all-words/)

---

## 📝 Problem Description
> [!info]
> You are given a string `s` and an array of strings `words`. All the strings of `words` are of the **same length**.
>
> A **concatenated string** is a string that exactly contains all the strings of any permutation of `words` concatenated.
>
> - For example, if `words = ["ab","cd","ef"]`, then `"abcdef"`, `"abefcd"`, `"cdabef"`, `"cdefab"`, `"efabcd"`, and `"efcdab"` are all concatenated strings. `"acdbef"` is **not** a concatenated string because it is not the concatenation of any permutation of `words`.
>
> Return an array of the **starting indices** of all the concatenated substrings in `s`. You can return the answer in **any order**.

---

## 🧪 Examples
> [!example]
> **Input:** `s = "barfoothefoobarman", words = ["foo","bar"]`
> **Output:** `[0,9]`
> **Explanation:** The substring starting at `0` is `"barfoo"` — the concatenation of `["bar","foo"]`, a permutation of `words`. The substring starting at `9` is `"foobar"` — the concatenation of `["foo","bar"]`.

> [!example]
> **Input:** `s = "wordgoodgoodgoodbestword", words = ["word","good","best","word"]`
> **Output:** `[]`
> **Explanation:** There is no concatenated substring. Note `"word"` appears twice, so we need two `"word"`s but they never line up with a single `"good"` and `"best"`.

> [!example]
> **Input:** `s = "barfoofoobarthefoobarman", words = ["bar","foo","the"]`
> **Output:** `[6,9,12]`
> **Explanation:** The substrings starting at `6` (`"foobarthe"`), `9` (`"barthefoo"`), and `12` (`"thefoobar"`) are each a permutation of `words`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= s.length <= 10^4`
> - `1 <= words.length <= 5000`
> - `1 <= words[i].length <= 30`
> - `s` and `words[i]` consist of lowercase English letters.

---

## 🔍 Intuition

Every word has the **same length** `wordLen`, so a valid window is always a run of whole word-blocks. That's the unlock: instead of treating `s` as characters, I treat it as a sequence of fixed-size tokens and the problem collapses into the classic *"find all anagrams"* sliding window — except the alphabet is **words**, not letters. The second unlock is alignment: any valid starting index `i` and `i + wordLen` land on the same block boundary, so there are only `wordLen` distinct alignments to consider. I run an **independent sliding window for each offset `0..wordLen-1`**, sliding the right edge forward one whole word at a time. Brute-forcing every index and re-scanning `wordCount` words each time is wasteful and re-reads the same blocks repeatedly; the offset trick lets each block be parsed once per offset and reuses window state via shrink-instead-of-reset.

> 🟢 *Sliding Window over Word-Aligned Offsets (word-bucket anagram)*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Sliding Window per Offset + HashMap Counts

**Why this works:**
- A valid window is exactly `wordCount` consecutive blocks whose multiset of words equals `target`. Tracking `window` counts + `matchedWords` lets me detect that in `O(1)` per step.
- Because valid starts share an alignment, looping `offset = 0..wordLen-1` and stepping `right += wordLen` covers **every** candidate window with no gaps and no double work.
- Three cases keep the window valid: unknown word → hard reset; over-count of a known word → shrink from `left` until balanced; full match → record and slide by one word so adjacent/overlapping windows are still found.

**Dry Run** (`s = "barfoothefoobarman", words = ["foo","bar"]`, `wordLen=3`, `wordCount=2`, `target={foo:1, bar:1}`):

Only `offset = 0` produces hits (offsets 1 and 2 immediately hit unknown words like `"arf"`, `"oth"`).

| `right` | block | action | `window` | `matched` | `left` | result |
|---|---|---|---|---|---|---|
| 0 | `bar` | add | `{bar:1}` | 1 | 0 | — |
| 3 | `foo` | add → **match** at `left=0`, then shrink `bar` | `{bar:0,foo:1}` | 2→1 | 0→3 | `[0]` |
| 6 | `the` | unknown → clear, jump | `{}` | 0 | 9 | `[0]` |
| 9 | `foo` | add | `{foo:1}` | 1 | 9 | `[0]` |
| 12 | `bar` | add → **match** at `left=9`, then shrink `foo` | `{foo:0,bar:1}` | 2→1 | 9→12 | `[0,9]` |
| 15 | `man` | unknown → clear, jump | `{}` | 0 | 18 | `[0,9]` |

Final → `[0, 9]`.

```java
class Solution {

    public List<Integer> findSubstring(String s, String[] words) {

        List<Integer> result = new ArrayList<>();

        if (s == null || words == null || words.length == 0) {
            return result;
        }

        int wordLen = words[0].length();
        int wordCount = words.length;

        Map<String, Integer> target = new HashMap<>();

        for (String word : words) {
            target.merge(word, 1, Integer::sum);
        }

        for (int offset = 0; offset < wordLen; offset++) {

            Map<String, Integer> window = new HashMap<>();

            int left = offset;
            int matchedWords = 0;

            for (int right = offset;
                 right + wordLen <= s.length();
                 right += wordLen) {

                String word =
                        s.substring(right, right + wordLen);

                if (!target.containsKey(word)) {
                    window.clear();
                    matchedWords = 0;
                    left = right + wordLen;
                    continue;
                }

                window.merge(word, 1, Integer::sum);
                matchedWords++;

                while (window.get(word) > target.get(word)) {

                    String leftWord =
                            s.substring(left, left + wordLen);

                    window.merge(leftWord, -1, Integer::sum);

                    matchedWords--;
                    left += wordLen;
                }

                if (matchedWords == wordCount) {

                    result.add(left);

                    String leftWord =
                            s.substring(left, left + wordLen);

                    window.merge(leftWord, -1, Integer::sum);

                    matchedWords--;
                    left += wordLen;
                }
            }
        }

        return result;
    }
}
```

---

## 🔑 Key Insights
- **Alignment reduces the search space:** only `wordLen` offsets matter, not every character index. This is the whole reason the solution beats brute force.
- **Words are the alphabet:** each `wordLen` slice is one token, turning this into the find-all-anagrams sliding window — counts in a map, not a set, so duplicate words (e.g. two `"word"`s) are handled correctly.
- **Shrink, don't restart, on overflow:** when a known word over-counts, only pop from the left until balanced — the window state is reused, keeping each offset pass linear.
- **On a full match, slide by one word** (`left += wordLen`) instead of resetting, so overlapping valid windows like `[6,9,12]` are all captured.

---

## ⚠️ Pitfalls
> [!warning]
> - Iterating only from index `0` (forgetting the `offset` loop) misses windows that don't start on the first alignment.
> - Using a `Set` instead of count `Map` breaks on repeated words in `words` (Example 2).
> - After a match you must record `left`, shrink one word, and **continue** — breaking or clearing the window loses adjacent answers.
> - Boundary `right + wordLen <= s.length()` is required; an off-by-one throws `StringIndexOutOfBounds`.
> - The answer is the **left boundary** of the window (`left`), not `right`.

---

## ⏱️ Complexity
- **Time:** `O(n × wordLen)` — there are `wordLen` offset passes; across a pass every block of `s` is hashed a constant number of times (amortized via the shrink), and each `substring` + map op costs `O(wordLen)`. With `n = s.length()`.
- **Space:** `O(words.length × wordLen)` — the `target` and `window` maps hold up to `words.length` distinct keys, each a string of length `wordLen`.
