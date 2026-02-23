---
created: 2026-01-28 00:36
tags:
  - Arrays
  - SlidingWindow
source: https://leetcode.com/problems/longest-substring-without-repeating-characters/
problem_id: "3"
difficulty: Medium
status: Completed
review_date:
---
# LT_3810 – Longest Substring Without Repeating Characters

**Link:** [Open Problem](DSS)

---

## 📝 Problem Description
> [!info]
> Given a string `s`, find the length of the **longest substring without duplicate characters**.

---

## 🧪 Examples
> [!example]
> **Input:** `"abcabcbb"`  
> **Output:** `3`  
> **Explanation:** `"abc"` is the longest substring without repeating characters.

---

## ⚠️ Constraints
> [!warning]
> - `0 ≤ s.length ≤ 10⁵`
> - `s` consists of English letters, digits, symbols, and spaces

---

## 💡 Solutions

### 🟢 Approach 1: Sliding Window + HashMap

**Intuition:**  
We maintain a sliding window using two pointers.  
A `HashMap` stores the **last seen index** of each character.

When a duplicate is found:
- Move `left` pointer **after** the previous occurrence
- Update the maximum window size

---

### ✅ Java Implementation

```java
class Solution {
    public int lengthOfLongestSubstring(String s) {
        int bestLen = 0;
        Map<Character, Integer> map = new HashMap<>();
        int left = 0;

        for (int right = 0; right < s.length(); right++) {
            char ch = s.charAt(right);

            if (map.containsKey(ch)) {
                left = Math.max(map.get(ch) + 1, left);
            }

            map.put(ch, right);
            bestLen = Math.max(bestLen, right - left + 1);
        }

        return bestLen;
    }
}
