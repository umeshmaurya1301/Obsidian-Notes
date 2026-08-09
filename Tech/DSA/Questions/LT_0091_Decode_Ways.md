---
created: 2026-08-09 18:18
tags:
  - dsa
  - string
  - dynamic-programming
  - recursion
source: https://leetcode.com/problems/decode-ways/
problem_id: "91"
difficulty: Medium
status: Solved
review_date:
---
# LT_0091 – Decode Ways

**Link:** [Open Problem](https://leetcode.com/problems/decode-ways/)

---

## 📝 Problem Description
> [!info]
> You have intercepted a secret message encoded as a string of numbers. The message is decoded via the following mapping:
>
> `"1" -> 'A'`, `"2" -> 'B'`, … , `"25" -> 'Y'`, `"26" -> 'Z'`
>
> However, while decoding the message, you realize that there are many different ways you can decode the message because some codes are contained in other codes (`"2"` and `"5"` vs `"25"`).
>
> For example, `"11106"` can be decoded into:
> - `"AAJF"` with the grouping `(1, 1, 10, 6)`
> - `"KJF"` with the grouping `(11, 10, 6)`
> - The grouping `(1, 11, 06)` is **invalid** because `"06"` is not a valid code (only `"6"` is valid).
>
> Note: there may be strings that are impossible to decode.
>
> Given a string `s` containing only digits, return *the number of ways to decode it*. If the entire string cannot be decoded in any valid way, return `0`.
>
> The test cases are generated so that the answer fits in a 32-bit integer.

---

## 🧪 Examples
> [!example]
> **Input:** `s = "12"`
> **Output:** `2`
> **Explanation:** `"12"` could be decoded as `"AB"` (1 2) or `"L"` (12).

> [!example]
> **Input:** `s = "226"`
> **Output:** `3`
> **Explanation:** `"226"` could be decoded as `"BZ"` (2 26), `"VF"` (22 6), or `"BBF"` (2 2 6).

> [!example]
> **Input:** `s = "06"`
> **Output:** `0`
> **Explanation:** `"06"` cannot be mapped to `"F"` because of the leading zero (`"6"` is different from `"06"`). In this case, the string is not a valid encoding, so return `0`.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= s.length <= 100`
> - `s` contains only digits and may contain leading zero(s).

---

## 🔍 Intuition

Standing at index `idx`, the only decision I have is **how much of the string to bite off next** — one digit or two — and once I've bitten it, *how I split everything before `idx` is irrelevant*. That independence is the whole problem: `dfs(idx)` = "number of ways to decode the suffix `s[idx..]`", a function of the index alone, so this is a plain 1-D DP, not the exponential tree it first looks like. Naive recursion re-solves the same suffix once per path reaching it (Fibonacci-shaped, `O(2ⁿ)`), so I cache it in `dp[idx]` and the whole thing collapses to `O(n)`. The two rules that make it a *counting* problem rather than a *feasibility* problem are the base cases: reaching `idx == s.length()` means I consumed the string cleanly, so that's **one** valid decoding — return `1`, not `0`, because these values get summed up the call chain and a `0` would annihilate the entire branch. And `'0'` maps to no letter at all, so any suffix beginning with `'0'` is instantly dead — that check is what encodes the "`06` is not `F`" rule, and it must come *before* anything else.

> 🟢 *1-D DP on suffix index (Fibonacci-shaped counting)*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Top-Down DP: Memoized DFS on Suffix Index

**Why this works:**
- **State is one integer.** `dfs(idx)` counts decodings of the suffix `s[idx..]`, independent of the prefix's split — so there are exactly `n` distinct subproblems, each resolved in `O(1)` work.
- **The recurrence is a sum of two disjoint choices:** take one digit (`dfs(idx+1)`, always allowed once we know `s[idx] != '0'`), plus take two digits (`dfs(idx+2)`) *only* when `s[idx..idx+1]` reads as `10…26`. Disjoint because a decoding is fully determined by the length of its first code, so no double-counting.
- **Base case returns `1`, not `0`.** Consuming the string exactly is one complete decoding; that `1` is the unit that propagates back up and gets summed into the answer.
- **`s.charAt(idx) == '0'` short-circuits to `0`** before the memo lookup. A `'0'` can never start a code, so the entire suffix is undecodable — this single line is what kills `"06"` and `"100"`-style inputs.

**Dry Run** (`s = "226"` — richer than Example 1 because it exercises the memo):

| Call | `s.charAt(idx)` | one-digit branch | two-digit check | `dp[idx]` |
|---|---|---|---|---|
| `dfs(0)` | `'2'` ✓ | `dfs(1)` → `2` | `num = 22` ✓ → `+ dfs(2)` = `1` | `3` |
| `dfs(1)` | `'2'` ✓ | `dfs(2)` → `1` | `num = 26` ✓ → `+ dfs(3)` = `1` | `2` |
| `dfs(2)` | `'6'` ✓ | `dfs(3)` → `1` | `idx+1 = 3` not `< 3`, skipped | `1` |
| `dfs(3)` | — | `idx == len` → base case | — | *(not stored)* |

Resolution order is `dfs(3) → dfs(2) → dfs(1) → dfs(0)`; when `dfs(0)` asks for `dfs(2)` it's a **memo hit** on `dp[2] = 1`, already computed inside `dfs(1)`. Final answer `dp[0] = 3` ✅ — matching `(2,2,6)`, `(2,26)`, `(22,6)`.

On `"06"`: `dfs(0)` sees `'0'` immediately and returns `0` without recursing ✅.

```java
class Solution {

    public int numDecodings(String s) {
        int n = s.length();
        int[] dp = new int[n];

        Arrays.fill(dp, -1);

        return dfs(0, s, dp);
    }

    private int dfs(int idx, String s, int[] dp) {

        if (idx == s.length()) {
            return 1;
        }

        if (s.charAt(idx) == '0') {
            return 0;
        }

        if (dp[idx] != -1) {
            return dp[idx];
        }

        int ways = dfs(idx + 1, s, dp);

        if (idx + 1 < s.length()) {

            int num =
                (s.charAt(idx) - '0') * 10 +
                (s.charAt(idx + 1) - '0');

            if (num >= 10 && num <= 26) {
                ways += dfs(idx + 2, s, dp);
            }
        }

        return dp[idx] = ways;
    }
}
```

- **Time:** `O(n)` · **Space:** `O(n)` (`n`-slot memo + up to `O(n)` recursion stack)

---

## 🔑 Key Insights
- **This is Fibonacci in disguise.** For a string of all-safe digits like `"1111"`, `dp[i] = dp[i+1] + dp[i+2]` exactly — so the answer for `n` ones is `Fib(n+1)`. That's also the proof that plain recursion without the memo is exponential.
- **Order of the three guards is load-bearing.** Base case → `'0'` check → memo lookup. The `'0'` check sitting *above* the memo means those indices never get written to `dp` (they stay `-1`), which is harmless: the answer there is the constant `0`, recomputed in `O(1)` each time.
- **`dp` is sized `n`, not `n + 1`** — legal only because `idx == s.length()` returns before any `dp[idx]` access. Reordering the memo lookup above the base case would throw `ArrayIndexOutOfBoundsException`.
- **`num >= 10` is technically redundant** given the `'0'` guard already ran (if `s.charAt(idx) != '0'` then `num >= 10` automatically), but it's worth keeping — it states the "no leading zero inside a two-digit code" rule explicitly instead of relying on a guard three lines up.

---

## ⚠️ Pitfalls
> [!warning]
> - **Returning `0` at the base case.** It's the single most common bug here — every branch would collapse to `0` since the values are summed, not maxed. Reaching the end *is* a success, worth `1`.
> - **Skipping the `'0'` guard, or placing it after the memo check.** Without it `"06"` returns `1` and `"100"` returns `1` instead of `0`; placed after the memo, a poisoned `dp[idx]` from a legitimate path could be returned for a `'0'` index.
> - **Checking only `num <= 26`.** Then `"06"` counts as a valid two-digit code and `"106"` returns `2` instead of `1`. The window must be `10 <= num <= 26`.
> - **Forgetting the `idx + 1 < s.length()` bound** before reading `s.charAt(idx + 1)` → `StringIndexOutOfBoundsException` on the last character.

---

## ⏱️ Complexity
- **Time:** `O(n)`
- **Space:** `O(n)` — reducible to `O(1)` with a bottom-up two-variable rolling DP.
