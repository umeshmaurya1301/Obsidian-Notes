---
created: 2026-08-16 12:00
tags:
  - dsa
  - string
  - enumeration
  - palindrome
  - modular-arithmetic
source: https://leetcode.com/problems/minimum-operations-to-make-a-rotated-palindrome-i/
problem_id: "4021"
difficulty: Medium
status: Solved
review_date:
---
# LT_4021 – Minimum Operations to Make a Rotated Palindrome I

**Link:** [Open Problem](https://leetcode.com/problems/minimum-operations-to-make-a-rotated-palindrome-i/)

---

## 📝 Problem Description
> [!info]
> You are given a string `s` consisting of lowercase English letters.
>
> You can perform the following operations any number of times (including zero) and in any order:
> - **Increment:** Choose any index `i` and replace `s[i]` with the next lowercase English letter. The letter after `'z'` is `'a'`.
> - **Left rotate:** Move the first character of the string to the end.
>
> Return the minimum number of operations required to make `s` a palindrome.

---

## 🧪 Examples
> [!example]
> **Input:** `s = "abc"`
> **Output:** `2`
> **Explanation:** Left rotate `"abc" -> "bca"`, then increment `'a'` to `'b'`: `"bca" -> "bcb"`. `"bcb"` is a palindrome. Total operations = 2.

> [!example]
> **Input:** `s = "yb"`
> **Output:** `3`
> **Explanation:** Increment the first character three times: `"yb" -> "zb" -> "ab" -> "bb"`. `"bb"` is a palindrome. Total operations = 3.

---

## ⚠️ Constraints
> [!warning]
> - `2 <= s.length <= 2000`
> - `s` consists only of lowercase English letters.

---

## 🔍 Intuition

The trap here is seeing two operation types and jumping straight to DP over sequences of moves. The way out is an exchange argument: rotations only move characters around, increments only change characters, and those two effects never interact — a rotation never cares what letter sits at a position, and an increment never cares where that position is. So any interleaved sequence of rotate/increment operations can be reordered into "do all `k` rotations first, then all increments," with identical total cost. That collapses "any sequence of operations" down to "pick a total rotation count `k`," and there are only `n` distinct values of `k` to try (rotating `n` times returns to the original string).

Once `k` is fixed, only increments remain, and a palindrome constrains index `i` and index `n-1-i` to be equal — pairs that are completely independent of each other. So the increment cost for a fixed rotation is just the sum of per-pair costs. For a pair of characters `(a, b)`, the cheapest way to make them equal is to walk one of them forward (cyclically, since `'z'` wraps to `'a'`) to meet the other — pick whichever direction is shorter: `a` catching up to `b`, or `b` catching up to `a`. Any later common target only adds equal extra distance to both, so it's never better. Try all `n` rotations, take the minimum total (rotation cost + pairwise increment cost), and that's the answer.

> 🟢 *Enumerate the Cheap Dimension, Decompose the Rest*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Enumerate Rotation + Greedy Pairwise Increment

**Why this works:**
- The exchange argument (rotations and increments commute) means trying "rotate `k` times then increment" for every `k` from `0` to `n-1` covers every reachable final palindrome — no interleaving can beat the best of these `n` candidates.
- Once `k` is fixed, the palindrome condition decomposes into `n/2` independent index pairs, so the total increment cost is just their sum — no cross-pair interaction to worry about.
- For each pair, `(a - b + 26) % 26` and `(b - a + 26) % 26` give the cyclic distance in each direction; the smaller one is the cheapest way to make the pair equal, since overshooting to a farther shared letter costs both characters extra.

**Dry Run** (`s = "abc"`, `n = 3`):

| `k` (rotation cost) | pair checked (via `(k+i)%n`, `(k+n-1-i)%n`) | pair cost | total |
|---|---|---|---|
| `0` | `s[0]='a'`, `s[2]='c'` | `min((0-2+26)%26, (2-0+26)%26) = min(24, 2) = 2` | `0 + 2 = 2` |
| `1` | `s[1]='b'`, `s[0]='a'` | `min((1-0+26)%26, (0-1+26)%26) = min(1, 25) = 1` | `1 + 1 = 2` |
| `2` | `s[2]='c'`, `s[1]='b'` | `min((2-1+26)%26, (1-2+26)%26) = min(1, 25) = 1` | `2 + 1 = 3` |

`ans = min(2, 2, 3) = 2` ✅ (matches rotating once to `"bca"` and incrementing `'a'` to `'b'`, giving `"bcb"`)

```java
class Solution {
    public int minOperations(String s) {
        int n = s.length();
        int ans = Integer.MAX_VALUE;

        for (int k = 0; k < n; k++) {
            int cost = k; // rotation cost

            for (int i = 0; i < n / 2; i++) {
                char left = s.charAt((k + i) % n);
                char right = s.charAt((k + (n - 1 - i)) % n);

                int a = left - 'a';
                int b = right - 'a';

                int diff1 = (a - b + 26) % 26;
                int diff2 = (b - a + 26) % 26;

                cost += Math.min(diff1, diff2);
            }

            ans = Math.min(ans, cost);
        }

        return ans;
    }
}
```

- **Time:** `O(n^2)` — `n` candidate rotations, each scanned in `O(n)` · **Space:** `O(1)`

---

## 🔑 Key Insights
- **Rotations and increments commute** — they act on disjoint aspects of the string (position vs. character), so any operation sequence can be rearranged into "all rotations, then all increments" at no extra cost. This is what rules out a DP-over-sequences approach entirely.
- There are only `n` distinct rotations of a length-`n` string, so "try every rotation" is exhaustive, not a heuristic.
- A palindrome's constraints are pairwise and independent (`i` with `n-1-i`), so the total cost is a **sum of per-pair minimums** — no need to jointly optimize pairs.
- The cheapest way to equalize a cyclic pair is `min(cyclic distance a→b, cyclic distance b→a)`, computed as `(a - b + 26) % 26` and its mirror.

---

## ⚠️ Pitfalls
> [!warning]
> - Forgetting the alphabet wraps (`'z' -> 'a'`) — cyclic distance needs `% 26` in both directions, not a plain subtraction.
> - Forgetting to add the rotation cost `k` itself to the total — it's easy to compute only the pairwise increment cost and drop the rotation operations from the count.
> - Indexing bugs when simulating rotation without actually rotating the string: both `(k + i) % n` and `(k + (n - 1 - i)) % n` must index into the **original** `s`, not a physically rotated copy.

---

## ⏱️ Complexity
- **Time:** `O(n^2)`
- **Space:** `O(1)`
