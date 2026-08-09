---
created: 2026-08-09 18:23
tags:
  - dsa
  - dynamic-programming
  - string
source: https://leetcode.com/problems/decode-ways-ii/
problem_id: "639"
difficulty: Hard
status: Solved
review_date:
---
# LT_0639 – Decode Ways II

**Link:** [Open Problem](https://leetcode.com/problems/decode-ways-ii/)

---

## 📝 Problem Description
> [!info]
> A message containing letters from A-Z can be encoded into numbers using the mapping `'A' -> "1"`, `'B' -> "2"`, … `'Z' -> "26"`.
>
> To decode an encoded message, all the digits must be grouped then mapped back into letters using the reverse of the mapping above (there may be multiple ways). For example, `"11106"` can be mapped into `"AAJF"` with the grouping `(1 1 10 6)` or `"KJF"` with the grouping `(11 10 6)`. Note that the grouping `(1 11 06)` is invalid because `"06"` cannot be mapped into `'F'` — `"6"` is different from `"06"`.
>
> In addition, an encoded message may contain the `'*'` character, which can represent any digit from `'1'` to `'9'` (`'0'` is excluded). For example, `"1*"` may represent any of `"11"`, `"12"`, …, `"19"`. Decoding `"1*"` is equivalent to decoding any of the messages it can represent.
>
> Given a string `s` consisting of digits and `'*'` characters, return the number of ways to decode it, modulo `10^9 + 7`.

---

## 🧪 Examples
> [!example]
> **Input:** `s = "*"`
> **Output:** `9`
> **Explanation:** `*` can be any of `"1"`–`"9"`, decoding to `"A"`–`"I"`. Total = 9.

> [!example]
> **Input:** `s = "1*"`
> **Output:** `18`
> **Explanation:** `"1*"` represents `"11"`–`"19"`, and each of those has 2 decodings (e.g. `"11"` → `"AA"` or `"K"`). Total = 9 × 2 = 18.

> [!example]
> **Input:** `s = "2*"`
> **Output:** `15`
> **Explanation:** `"2*"` represents `"21"`–`"29"`. `"21"`–`"26"` have 2 decodings each, `"27"`–`"29"` have only 1. Total = (6 × 2) + (3 × 1) = 15.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= s.length <= 10^5`
> - `s[i]` is a digit or `'*'`

---

## 🔍 Intuition

Strip out the `'*'` and this is plain **Decode Ways (LC 91)**: `dp[i] = dp[i-1] + dp[i-2]`, a Fibonacci walk where each step is gated on whether the last one or two characters form a legal code. The `'*'` changes only one thing — the gates stop being **boolean** and become **counts**. A `'*'` standing alone isn't "valid or not", it's 9 different letters; the pair `"**"` isn't one grouping, it's 15 of them (`11`–`19` plus `21`–`26`). So the recurrence becomes `dp[i] = dp[i-1] * single(s[i-1]) + dp[i-2] * pair(s[i-2], s[i-1])`, and the entire difficulty of the problem collapses into writing those two little counting helpers correctly. Once I isolate them as functions, the DP body is three lines and I never have to reason about `'*'` inside the loop. The `10^5` length bound also quietly rules out top-down recursion — depth equals `n`, so it stack-overflows — which makes the bottom-up rolling form the only shape that survives.

> 🟢 *Fibonacci-Style DP with Counted Transitions (Decode Ways I generalised)*

---

## 🧠 Evolution of Solutions

### ❌ Solution 1 — Top-Down Memoization (first attempt, broken)

**Why it's bad:** it is a correct solution to **Decode Ways I** with `'*'` handling bolted on that never actually works — it returns `1` for `"*"` (expected `9`), `2` for `"1*"` (expected `18`), and `-1` for `"0"`. Kept here because the root-cause bug is a trap worth remembering.

```java
class Solution {
    public int numDecodings(String s) {
        int len = s.length();
        int[] dp = new int[len];
        Arrays.fill(dp, -1);
        dfs(s, dp, 0);
        System.out.println(Arrays.toString(dp));
        return dp[0];
    }

    private int dfs(String s, int[] dp, int idx) {
        if (idx == s.length())
            return 1;
        if (s.charAt(idx) == '0')
            return 0;
        if (dp[idx] != -1)
            return dp[idx];

        int ways = ways = dfs(s, dp, idx + 1);

        if (idx+1 < s.length()) {

            if (s.charAt(idx) == '*') {
                for (int i=1; i<=9; i++) {
                    int num = ((s.charAt(idx) - '0') * 10) + i;
                    if (num <= 26) ways += dfs (s, dp, idx + 2);    
                }

            } else {
                int num = ((s.charAt(idx) - '0') * 10) + (s.charAt(idx+1) - '0');
                if (num <= 26) ways += dfs (s, dp, idx + 2);
            }

        }

        return dp[idx] = ways;
    }
}
```

**What's wrong with it:**

| # | Bug | Symptom |
|---|-----|---------|
| 1 | `'*' - '0'` is **`-6`**, not a digit (`'*'`=42, `'0'`=48). In the `*` branch `num = -60 + i` is *always* `<= 26`, so it adds `dfs(idx+2)` nine times unconditionally. | `"**"` → 10, expected 96 |
| 2 | The `i` loop never indexes the string — `s.charAt(idx+1)` is never read in that branch, so the second character is ignored entirely. | all `*`-pair counts wrong |
| 3 | A lone `'*'` counts **1** way instead of 9 — needs `ways = 9 * dfs(idx+1)`. | `"*"` → 1, expected 9 |
| 4 | `s.charAt(idx+1) == '*'` falls into the digit branch: `"1*"` computes `num = 10 + (-6) = 4`, adding 1 way instead of 9. | `"1*"` → 2, expected 18 |
| 5 | No `% 1_000_000_007`. | `int` overflow on long inputs |
| 6 | `return dp[0]` instead of the `dfs` return — when `s.charAt(0) == '0'` the method returns before writing `dp[0]`, leaking the `-1` sentinel. | `"0"` → -1, expected 0 |
| 7 | Recursion depth = `n`, and `n` can be `10^5`. | `StackOverflowError` at the limit |

Also cosmetic: `int ways = ways = dfs(...)` is a self-assignment typo (it compiles, but says nothing), and the debug `System.out.println(Arrays.toString(dp))` fires on every call.

---

### ✅ Solution 2 — Bottom-Up DP, `O(1)` Space (corrected)

**Why this works:**
- Every `'*'`-related decision is pulled out into `single()` and `pair()`, which return **how many** valid codes a position admits rather than whether one exists. The DP loop then never mentions `'*'`.
- `dp[i]` depends only on `dp[i-1]` and `dp[i-2]`, so two `long` variables replace the whole array — and going bottom-up removes the `10^5`-deep recursion that killed Solution 1.
- `long` accumulators keep the pre-modulo product safe: the largest possible step is `prev1 * 9 + prev2 * 15 < 2.4 × 10^10`, far under `Long.MAX_VALUE`.

**Dry Run** (`s = "2*"`, Example 3):

`prev2 = dp[0] = 1` (empty prefix decodes one way), `prev1 = dp[1] = single('2') = 1`.

| `i` | term 1 — `prev1 * single(s[i-1])` | term 2 — `prev2 * pair(s[i-2], s[i-1])` | `cur` |
|-----|-----------------------------------|------------------------------------------|-------|
| 2 | `1 * single('*') = 1 * 9 = 9` | `1 * pair('2','*') = 1 * 6 = 6` | **15** |

Answer = **15** ✅ — note the DP splits it as `9 + 6` (nine ways where `*` is its own letter after `"B"`, six where `"2*"` is a single letter `U`–`Z`), whereas the problem statement splits the same 15 as `6×2 + 3×1`. Different partition, same total.

A three-character trace (`s = "*1*"`) to show the roll:

| `i` | `prev2` | `prev1` | `cur = prev1·single + prev2·pair` | |
|-----|---------|---------|------------------------------------|---|
| — | 1 | `single('*')` = 9 | initial | |
| 2 | 1 | 9 | `9·single('1')=9` + `1·pair('*','1')=2` | **11** |
| 3 | 9 | 11 | `11·single('*')=99` + `9·pair('1','*')=81` | **180** |

Answer = **180**.

```java
class Solution {
    private static final int MOD = 1_000_000_007;

    public int numDecodings(String s) {
        int n = s.length();
        long prev2 = 1;                    // dp[0] — empty prefix decodes one way
        long prev1 = single(s.charAt(0));  // dp[1]

        for (int i = 2; i <= n; i++) {
            long cur = (prev1 * single(s.charAt(i - 1))
                      + prev2 * pair(s.charAt(i - 2), s.charAt(i - 1))) % MOD;
            prev2 = prev1;
            prev1 = cur;
        }

        return (int) prev1;
    }

    // ways this character decodes on its own
    private int single(char c) {
        if (c == '*') return 9;      // 1..9
        return c == '0' ? 0 : 1;
    }

    // ways (c1, c2) forms a valid two-digit code 10..26
    private int pair(char c1, char c2) {
        if (c1 == '*' && c2 == '*') return 15;      // 11-19, 21-26
        if (c1 == '*') return c2 <= '6' ? 2 : 1;    // 1x always; 2x only when x <= 6
        if (c2 == '*') {
            if (c1 == '1') return 9;                // 11-19
            return c1 == '2' ? 6 : 0;               // 21-26
        }
        if (c1 == '1') return 1;                    // 10-19
        return (c1 == '2' && c2 <= '6') ? 1 : 0;    // 20-26
    }
}
```

- **Time:** `O(n)` · **Space:** `O(1)`

---

## 🔑 The Transition Table

The whole problem is this table. Memorise it and the code writes itself.

**`single(c)`** — ways `c` decodes alone:

| `c` | ways |
|-----|------|
| `'*'` | 9 &nbsp;<sub>(1–9)</sub> |
| `'0'` | 0 |
| any other digit | 1 |

**`pair(c1, c2)`** — ways `c1c2` forms one code in `10..26`:

| `c1` \ `c2` | digit `d` | `'*'` |
|---|---|---|
| `'1'` | 1 | 9 &nbsp;<sub>(11–19)</sub> |
| `'2'` | `d <= 6` → 1, else 0 | 6 &nbsp;<sub>(21–26)</sub> |
| other digit | 0 | 0 |
| `'*'` | `d <= 6` → 2, else 1 | 15 &nbsp;<sub>(11–19, 21–26)</sub> |

---

## 🔑 Key Insights
- The leap from LC 91 is **boolean gates → counted gates**. `dp[i] = dp[i-1] + dp[i-2]` becomes `dp[i] = dp[i-1]·single + dp[i-2]·pair`; LC 91 is the special case where both helpers only ever return `0` or `1`.
- `'*'` is `1..9`, **not** `0..9`. That's why `pair('*','*')` is 15 and not 16 — `"*0"` can't come from the first star being `0`, and `"10"`/`"20"` are already counted from the `2` in `pair('*','0')`.
- `pair('*', d)` for `d <= '6'` is **2**, and this correctly covers `d == '0'`: both `"10"` and `"20"` are legal, while `single('0') = 0` makes sure a `'0'` can never stand alone. The two helpers cover `'0'` between them without a special case.
- The `10^5` bound is a design constraint, not decoration — it's what forces bottom-up. Any `O(n)`-depth recursion dies here regardless of how correct the logic is.

---

## ⚠️ Pitfalls
> [!warning]
> - **Never do arithmetic on `'*'`.** `'*' - '0' == -6`, and because `-60 + i <= 26` is always true it fails *silently* — no exception, just wrong counts. Branch on `c == '*'` before any `- '0'`.
> - Forgetting `pair('*','*') == 15`. Easy to write 16 (thinking `1*` gives 10 and `2*` gives 6) or 18 (`9 + 9`).
> - `pair(c1, '*')` when `c1` is a digit needs 9 and 6, not 1 — the second star multiplies the branch, it doesn't just make it valid.
> - Taking the modulo only at the end, or on `int`s. Multiply in `long`, `%` every iteration.
> - Returning a memo slot (`dp[0]`) rather than the function's own return value — any early-exit path that skips the memo write leaks the `-1` sentinel.

---

## ⏱️ Complexity
- **Time:** `O(n)` — one pass, both helpers are `O(1)`.
- **Space:** `O(1)` — two rolling `long`s.

---

## 🔗 Related
- **LC 91 — Decode Ways** — the same recurrence with boolean gates. Solve that first; this is that plus a counting table.
