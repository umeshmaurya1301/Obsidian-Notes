---
created: 2026-09-14 00:00
tags:
  - dsa
  - string
  - greedy
source: https://leetcode.com/problems/orderly-queue/description/
problem_id: "899"
difficulty: Hard
status: Solved
review_date:
---
# LT_0899 – Orderly Queue

**Link:** [Open Problem](https://leetcode.com/problems/orderly-queue/description/)

---

## 📝 Problem Description
> [!info]
> You are given a string `s` and an integer `k`. You can choose one of the first `k` letters of `s` and append it at the end of the string.
>
> Return the lexicographically smallest string you could have after applying the mentioned step any number of moves.

---

## 🧪 Examples
> [!example]
> **Input:** `s = "cba", k = 1`
> **Output:** `"acb"`
> **Explanation:** In the first move, we move the 1st character `'c'` to the end, obtaining the string `"bac"`. In the second move, we move the 1st character `'b'` to the end, obtaining the final result `"acb"`.

> [!example]
> **Input:** `s = "baaca", k = 3`
> **Output:** `"aaabc"`
> **Explanation:** In the first move, we move the 1st character `'b'` to the end, obtaining the string `"aacab"`. In the second move, we move the 3rd character `'c'` to the end, obtaining the final result `"aaabc"`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= k <= s.length <= 1000`
> - `s` consist of lowercase English letters.

---

## 🔍 Intuition

The whole problem splits cleanly on whether `k == 1` or `k > 1`. When `k == 1`, the only legal move is "chop the first character off and re-append it" — that's exactly a left-rotation, and repeating it can only ever cycle through the `n` rotations of `s`, never anything else. So the answer is just the minimum over all rotations. When `k >= 2`, the extra freedom of picking either the 1st or 2nd character turns out to be enough to simulate an **adjacent swap**: send the 2nd character to the end, then rotate the whole string once, and the net effect is that the 1st and 2nd characters have traded places with everything else shifted back into position. Once adjacent swaps are available, bubble-sort logic says any permutation of `s` is reachable — so the lexicographically smallest reachable string is simply the sorted string. Brute force falls short here because trying to simulate the moves directly is unnecessary once you recognize the reachable-set argument for each case.

> 🟢 *Case Split: Min-Rotation vs Sort*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Case Split (Min Rotation for k=1, Sort for k>1)

**Why this works:**
- `k == 1` restricts every move to "move first char to end," so the reachable set is exactly `{rotation_0, rotation_1, ..., rotation_{n-1}}` — checking all `n` of them and keeping the smallest is correct and exhaustive.
- `k >= 2` lets you simulate an adjacent swap of the first two characters (`x y rest -> x rest y -> y x rest` via "send 2nd char to end" then "rotate once"), and repeating this anywhere in the string means any permutation is reachable, so sorting the characters gives the global minimum.

**Dry Run** (`s = "cba", k = 1`):

| `i` | `temp = s.substring(i) + s.substring(0, i)` | Compare to current `ans` | New `ans`? |
|---|---|---|---|
| 0 | `"cba"` | equals initial `ans` | `"cba"` |
| 1 | `"bac"` | `"bac" < "cba"` | `"bac"` |
| 2 | `"acb"` | `"acb" < "bac"` | `"acb"` |

Final `ans = "acb"` ✅ matches expected output.

**Dry Run** (`s = "baaca", k = 3`):
```
k >= 2 → skip rotation logic entirely
chars = ['b','a','a','c','a'] → sort → ['a','a','a','b','c']
return "aaabc"
```

```java
class Solution {
    public String orderlyQueue(String s, int k) {
        if (k == 1) {
            String ans = s;
            for (int i = 0; i < s.length(); ++i) {
                String temp = s.substring(i) + s.substring(0, i);
                if (temp.compareTo(ans) < 0) {
                    ans = temp;
                }
            }
            return ans;
        } else {
            char[] chars = s.toCharArray();
            Arrays.sort(chars);
            return new String(chars);
        }
    }
}
```

- **Time:** `O(n^2)` for `k == 1` (`n` rotations, each a `substring` + `compareTo` costing `O(n)`); `O(n log n)` for `k > 1` (sort). Bounded by `n <= 1000`, so both are fast enough.
- **Space:** `O(n)` — each rotated string / the sorted `char[]` copy.

---

## 🔑 Key Insights
- The `k >= 2` "any permutation reachable" claim isn't obvious — it needs the adjacent-swap construction (`x y rest -> x rest y -> y x rest`) to justify rigorously, especially in an interview.
- For `k == 1`, the reachable set is bounded (only `n` rotations), so brute force is not just acceptable but the simplest correct approach — no need for Booth's algorithm or other O(n) minimum-rotation tricks given `n <= 1000`.
- The two cases have genuinely different reachable sets (`n` rotations vs. all `n!` permutations), which is why the optimal strategy is completely different in each branch.

---

## ⚠️ Pitfalls
> [!warning]
> - Don't try to actually simulate the moves for `k > 1` — the reachable-set argument (sort suffices) is the whole point; simulating would be needlessly complex and slow.
> - Forgetting the `k == 1` special case and always sorting gives a wrong answer whenever `k == 1` and `s` isn't already sorted (e.g. `"cba"` would wrongly return `"abc"`, which isn't reachable with only rotations).
> - `s.substring(i) + s.substring(0, i)` — easy to swap the argument order and produce a right-rotation instead of a left-rotation.

---

## ⏱️ Complexity
- **Time:** `O(n^2)` (dominated by the `k == 1` branch; `O(n log n)` when `k > 1`)
- **Space:** `O(n)`
