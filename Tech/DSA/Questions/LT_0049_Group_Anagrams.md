---
created: 2026-05-18 00:00
tags:
  - Arrays
  - Strings
  - HashMap
  - Sorting
source: https://leetcode.com/problems/group-anagrams/description/
problem_id: "49"
difficulty: Medium
status: Completed
review_date:
---
# LT_0049 – Group Anagrams

**Link:** [Open Problem](https://leetcode.com/problems/group-anagrams/description/)

---

## 📝 Problem Description
> [!info]
> Given an array of strings `strs`, group the anagrams together.
>
> Two strings are anagrams if they contain the same characters with the same frequencies, but the order of characters may differ.
>
> Return the grouped anagrams in any order.

---

## 🧪 Examples
> [!example]
> **Input:** `strs = ["eat","tea","tan","ate","nat","bat"]`
> **Output:** `[["eat","tea","ate"],["tan","nat"],["bat"]]`
> **Explanation:** `"eat"`, `"tea"`, and `"ate"` are anagrams — sorted they all become `"aet"`. Similarly `"tan"` and `"nat"` become `"ant"`.

> [!example]
> **Input:** `strs = [""]`
> **Output:** `[[""]]`
> **Explanation:** Empty string forms a single anagram group.

> [!example]
> **Input:** `strs = ["a"]`
> **Output:** `[["a"]]`
> **Explanation:** Single character string forms one group.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= strs.length <= 10000`
> - `0 <= strs[i].length <= 100`
> - `strs[i]` consists of lowercase English letters.

---

## 💡 Solutions

### 🟢 Approach 1: Sorting-Based Key

**Intuition:**
Two strings are anagrams if they become identical after sorting. Use the sorted string as a canonical HashMap key, then group all originals that share the same key.

Example — `"eat"` → `"aet"`, `"tea"` → `"aet"`, `"ate"` → `"aet"` — all map to the same group.

**Dry Run — `strs = ["eat","tea","tan","ate","nat","bat"]`:**

| str | sorted key | map after |
|-----|------------|-----------|
| `"eat"` | `"aet"` | `{aet: [eat]}` |
| `"tea"` | `"aet"` | `{aet: [eat, tea]}` |
| `"tan"` | `"ant"` | `{aet: [eat, tea], ant: [tan]}` |
| `"ate"` | `"aet"` | `{aet: [eat, tea, ate], ant: [tan]}` |
| `"nat"` | `"ant"` | `{aet: [eat, tea, ate], ant: [tan, nat]}` |
| `"bat"` | `"abt"` | `{aet: [eat, tea, ate], ant: [tan, nat], abt: [bat]}` |

Return: `[["eat","tea","ate"],["tan","nat"],["bat"]]`

**Edge Cases:**
- Empty string `""` — sorts to `""`, forms its own group.
- Duplicate strings like `["eat","eat"]` — both map to the same key → `[["eat","eat"]]`.
- All unique strings — every string forms its own group.

---

### ✅ Java Implementation — Approach 1

```java
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {

        Map<String, List<String>> map = new HashMap<>();

        for(String str : strs) {

            char[] arr = str.toCharArray();

            Arrays.sort(arr);

            String key = new String(arr);

            map.putIfAbsent(key, new ArrayList<>());

            map.get(key).add(str);
        }

        return new ArrayList<>(map.values());
    }
}
```

---

### 🟡 Approach 2: Frequency Count Key (Optimal)

**Intuition:**
Instead of sorting (which costs `O(k log k)` per string), build a key from the character frequency array. Encode the 26 counts separated by `#` to avoid key collisions.

Example — `"eat"` → freq `[1,0,0,0,1,0,...,1,0,0]` → key `"1#0#0#0#1#0#...#1#0#0#"`.

**Why the `#` separator matters:**

Without separator, frequencies `[1, 11]` and `[11, 1]` both produce `"111"` — collision. With `#`: `"1#11#"` vs `"11#1#"` — unique keys.

This avoids sorting entirely and brings time complexity down to `O(n * k)`.

---

### ✅ Java Implementation — Approach 2

```java
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        for(String s : strs) {
            int[] freq = new int[26];
            for(char c : s.toCharArray()) {
                freq[c-'a']++;
            }
            StringBuilder builder = new StringBuilder();
            for(int n : freq) {
                builder.append(String.valueOf(n)+"#");
            }
            String key = new String(builder);
            List<String> values = map.getOrDefault(key, new ArrayList<>());
            values.add(s);
            map.put(key, values);
        }

        return new ArrayList<>(map.values());        
    }
}
```

---

## 🔑 Key Insights
- Anagrams become identical after sorting — sorted string is a valid canonical key.
- Frequency count key avoids sorting and is strictly faster: `O(k)` vs `O(k log k)` per string.
- The `#` separator in the frequency key prevents collisions between different frequency distributions.
- Store original strings in the map, not the sorted/transformed keys.

---

## 🧩 Patterns
- HashMap Grouping
- Canonical Representation
- Sorting
- String Transformation
- Frequency Counting

---

## ⚠️ Pitfalls
> [!warning]
> - Using `char[]` directly as a HashMap key won't work — arrays use reference equality, not value equality.
> - Forgetting to convert sorted `char[]` back to `String` before using as a key.
> - Omitting the `#` separator in the frequency key causes collisions (e.g. counts `1,11` and `11,1` both produce `"111"`).
> - Confusing the sorted/encoded key with the original string — always store originals in the value list.

---

## ⏱️ Complexity

| Approach | Time | Space |
|---|---|---|
| Approach 1 (Sorting) | `O(n * k log k)` | `O(n * k)` |
| Approach 2 (Frequency) | `O(n * k)` | `O(n * k)` |

`n` = number of strings, `k` = average string length.
