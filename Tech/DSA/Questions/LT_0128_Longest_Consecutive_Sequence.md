---
created: 2026-05-27 00:00
tags:
  - dsa
  - array
  - hash-table
  - union-find
source: https://leetcode.com/problems/longest-consecutive-sequence/description/
problem_id: "128"
difficulty: Medium
status: Solved
review_date:
---
# LT_0128 – Longest Consecutive Sequence

**Link:** [Open Problem](https://leetcode.com/problems/longest-consecutive-sequence/description/)

---

## 📝 Problem Description
> [!info]
> Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence.
>
> You must write an algorithm that runs in `O(n)` time.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [100, 4, 200, 1, 3, 2]`
> **Output:** `4`
> **Explanation:** The longest consecutive elements sequence is `[1, 2, 3, 4]`. Therefore its length is 4.

> [!example]
> **Input:** `nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]`
> **Output:** `9`
> **Explanation:** The longest consecutive sequence is `[0, 1, 2, 3, 4, 5, 6, 7, 8]`.

---

## ⚠️ Constraints
> [!warning]
> - `0 <= nums.length <= 10^5`
> - `-10^9 <= nums[i] <= 10^9`

---

## 🔍 Intuition

A consecutive sequence has exactly one valid starting point: a number `n` where `n - 1` does **not** exist. If I only begin counting streaks from such "sequence heads," each sequence is counted exactly once — no redundant work. I dump all numbers into a `HashSet` first for O(1) lookups, then for every number that qualifies as a head, I walk forward (`curr + 1`, `curr + 2`, …) until the chain breaks. The critical guard `!set.contains(n - 1)` is what collapses what would otherwise be an O(n²) nested scan into a single O(n) pass — every element participates in at most one walk.

> 🟢 *HashSet + Sequence-Head Detection*

---

## 🧠 Evolution of Solutions

### ✅ Solution — HashSet + Sequence-Head Detection

**Why this works:**
- `HashSet` deduplicates input and gives O(1) membership checks, so `contains(n - 1)` and `contains(curr + 1)` are both constant time.
- By skipping any `n` whose predecessor exists, we guarantee we only enter the `while` loop from the true beginning of each sequence — each element is touched by the inner `while` at most once across the entire outer loop, keeping total work O(n).
- Iterating over `set` (not `nums`) means duplicates never trigger extra streak walks.

**Dry Run** (`nums = [100, 4, 200, 1, 3, 2]`):

| Current `n` | `n-1` in set? | Action | `curr` walk | `streak` | `longest` |
|-------------|--------------|--------|-------------|----------|-----------|
| 100 | 99 → No | Start streak | 100 → (101? No) | 1 | 1 |
| 200 | 199 → No | Start streak | 200 → (201? No) | 1 | 1 |
| 1 | 0 → No | Start streak | 1→2→3→4→(5? No) | 4 | **4** |
| 4 | 3 → Yes | Skip | — | — | 4 |
| 3 | 2 → Yes | Skip | — | — | 4 |
| 2 | 1 → Yes | Skip | — | — | 4 |

Return **4** ✅

```java
class Solution {

    public int longestConsecutive(int[] nums) {

        Set<Integer> set = new HashSet<>();

        for (int n : nums) {
            set.add(n);
        }

        int longest = 0;

        for (int n : set) {

            // Start only if sequence beginning
            if (!set.contains(n - 1)) {

                int curr = n;
                int streak = 1;

                while (set.contains(curr + 1)) {
                    curr++;
                    streak++;
                }

                longest = Math.max(longest, streak);
            }
        }

        return longest;
    }
}
```

---

## 🔑 Key Insights
- The `!set.contains(n - 1)` guard is the entire trick — it turns O(n²) brute-force into O(n) by ensuring each element is walked at most once across all streak expansions.
- `HashSet` insertion naturally deduplicates, so duplicate values in `nums` are harmless.
- Iterating over `set` instead of `nums` avoids redundant outer-loop iterations caused by duplicates.
- Total inner-loop (`while`) steps across all iterations ≤ n, because each element can only be "consumed" by one streak.

---

## ⚠️ Pitfalls
> [!warning]
> - Omitting `!set.contains(n - 1)` — without it, streaks restart from every element in the sequence, making it O(n²).
> - Iterating over `nums` instead of `set` — duplicates cause redundant `while` walks (still correct, but wastes work).
> - Initialising `streak = 0` instead of `1` — the starting element itself counts as length 1.

---

## ⏱️ Complexity
- **Time:** `O(n)` — O(n) to build the set; outer loop is O(n) over set elements; all `while` expansions combined are O(n) since each element is visited at most once.
- **Space:** `O(n)` — the `HashSet` stores up to n distinct elements.
