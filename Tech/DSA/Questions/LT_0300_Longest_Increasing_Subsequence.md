---
created: 2026-08-03 09:28
tags:
  - dsa
  - dynamic-programming
  - memoization
  - binary-search
  - arrays
source: https://leetcode.com/problems/longest-increasing-subsequence/
problem_id: "300"
difficulty: Medium
status: Solved
review_date:
---
# LT_0300 – Longest Increasing Subsequence

**Link:** [Open Problem](https://leetcode.com/problems/longest-increasing-subsequence/)

---

## 📝 Problem Description
> [!info]
> Given an integer array `nums`, return the length of the **longest strictly increasing subsequence**.
>
> A **subsequence** is a sequence derived from the array by deleting some or no elements **without changing the order** of the remaining elements.
> e.g. `[3, 6, 2, 7]` is a subsequence of `[0, 3, 1, 6, 2, 2, 7]`.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [10, 9, 2, 5, 3, 7, 101, 18]`
> **Output:** `4`
> **Explanation:** The longest increasing subsequence is `[2, 3, 7, 101]`, therefore the length is `4`.

> [!example]
> **Input:** `nums = [0, 1, 0, 3, 2, 3]`
> **Output:** `4`
> **Explanation:** `[0, 1, 2, 3]`.

> [!example]
> **Input:** `nums = [7, 7, 7, 7, 7, 7, 7]`
> **Output:** `1`
> **Explanation:** Increasing must be **strict**, so equal values can't chain. Any single `7` is the best we get.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 2500`
> - `-10^4 <= nums[i] <= 10^4`
>
> **Follow-up:** Can you come up with an algorithm that runs in `O(n log n)` time complexity?

---

## 🔍 Intuition

At every index I face the same binary decision — **take this element into my subsequence, or skip it**. I can only take it if it is strictly greater than the last element I picked, so the decision isn't free-standing: it depends on history. That means the state of my recursion needs two things — *where I am* (`curr`) and *what I last committed to* (`prev`). Brute force explores all `2^n` take/skip paths, but the same `(curr, prev)` pair gets re-asked over and over across different paths, so memoizing on that pair collapses the exponential tree into `O(n²)` distinct states. The `prev + 1` offset in the table exists purely because `prev` starts at `-1` (nothing picked yet) and Java arrays can't be indexed negatively.

Once I see that "take vs skip with a constraint on the previous pick" is the shape, this generalises to a whole family — Longest Divisible Subset, Russian Doll Envelopes, Longest String Chain.

> 🟢 *Take-or-Skip DP on `(index, previousIndex)` → later refined to Patience Sorting*

---

## ❌ A Tempting but Wrong State

Before landing on `dp[curr][prev+1]`, it's worth seeing *why* the obvious range-based state fails — this is the standard trap for LIS.

```text
dp[i][j] = length of the LIS in the range [i...j]
```

**Why this breaks:** this state only encodes *which elements remain* — it has no memory of what was already picked before index `i`. But whether `nums[i]` can be taken depends entirely on the previously chosen element, so the same range can legitimately have different answers.

**Concrete counterexample** — `nums = [5, 1, 2]`, range `[1, 2]` → `{1, 2}`:

| Previous pick | Comparison | Answer |
|---|---|---|
| None (`prev = -1`) | `0 < 1 < 2` | **2** |
| `nums[0] = 5` | `5 > 1` and `5 > 2` | **0** |

Same range `[1...2]`, two different answers depending on context outside the range. A valid DP state must resolve to **one** answer no matter which path reached it — `dp[i][j]` fails that test, so it isn't a real memoizable state.

**The fix:** fold the missing information — *what was the last picked element* — into the state itself. That's exactly `dp[curr][prev+1]`: `prev = -1` (nothing picked yet) lives at column `0` since arrays can't be indexed negatively.

> [!tip]
> **General rule for designing any DP state:** *if two different recursion paths land on the same state, will they always get the same answer?* If no, the state is missing information. For LIS, `(curr, prev)` passes this test — a naive range `(i, j)` does not.

---

## 🧩 The Mental Model — DP as a Function Cache, Not a Table

This is the part that trips everyone up. Don't try to give `dp[curr][prev+1]` an elegant English definition. **It is just a cache of return values.**

```java
dfs(curr, prev)
```

Ask: *what question does this function answer?* For `nums = [3, 5, 4, 8]`:

| Call | The question it asks |
|---|---|
| `dfs(2, 0)` | "I'm at index 2. I already picked index 0 (value `3`). Best I can build **from here**?" |
| `dfs(3, 2)` | "I'm at index 3. I already picked index 2 (value `4`). Best **from here**?" |
| `dfs(0, -1)` | "I'm at index 0. I've picked nothing. Best **from here**?" ← the whole problem |

So:

> **`dp[curr][prev+1]` stores the answer returned by `dfs(curr, prev)`.** Nothing more.

**Why is the answer at `dp[0][0]`?** Because the very first question asked was `dfs(0, -1)`, and `prev + 1 = 0`. The answer to the whole problem is the answer to the **first** question — the *starting* state, not the last one.

> [!tip]
> **The game framing.** Every state is `(current position, last picked)`. Each state asks: *"If I start playing from here, what's the max score?"* The answer to the game is the score from the **starting** state. That's why we read `dp[0][0]` and not `max(dp[i])`.

### The two LIS formulations don't mean the same thing

| | Memoized (this code) | Classic iterative |
|---|---|---|
| State | `dfs(curr, prev)` | `dp[i]` |
| Meaning | "From this point **onward**, best I can do" | "LIS **ending at** index `i`" |
| Direction | Suffix / forward-looking | Prefix / backward-looking |
| Answer | `dfs(0, -1)` → `dp[0][0]` | `max(dp[i])` |

The `dp[i]` definition is far more intuitive, which is why most people learn it first. For interviews, don't burn time verbalising the memo state — just remember it's a function cache.

---

## 🧠 Evolution of Solutions

### 🟠 Step 0 — Pure Recursion (TLE)

Same `dfs`, no `dp` array. Every index branches into take/skip → `O(2^n)`. At `n = 2500` this is hopeless, but it's the honest starting point and the memo version is a one-line upgrade from it.

---

### ✅ Solution 1 — Memoization on `(curr, prev)`

**Why this works:**
- The recursion is **exhaustive** — every element is offered both take and skip, so no valid subsequence is missed.
- The `nums[curr] > nums[prev]` guard is the only thing enforcing strictness; `prev == -1` short-circuits it for the very first pick.
- There are only `n × (n+1)` reachable `(curr, prev)` pairs, so caching turns exponential work into quadratic.

**Dry Run** (`nums = [3, 5, 4, 8]` — smaller than Example 1 so the whole tree fits):

Resolving bottom-up (the code actually descends the `skip` branch first, but the resolved values are what matter):

| State `dfs(curr, prev)` | `skip` | `take` | Result | Cached at |
|---|---|---|---|---|
| `dfs(4, *)` | — | — | `0` (base case) | — |
| `dfs(3, 2)` prev=`4` | `0` | `8 > 4` → `1 + 0 = 1` | **1** | `dp[3][3]` |
| `dfs(3, 1)` prev=`5` | `0` | `8 > 5` → `1` | **1** | `dp[3][2]` |
| `dfs(3, 0)` prev=`3` | `0` | `8 > 3` → `1` | **1** | `dp[3][1]` |
| `dfs(3, -1)` | `0` | free pick → `1` | **1** | `dp[3][0]` |
| `dfs(2, 1)` prev=`5` | `dfs(3,1) = 1` | `4 > 5` ✗ → `0` | **1** | `dp[2][2]` |
| `dfs(2, 0)` prev=`3` | `dfs(3,0) = 1` | `4 > 3` → `1 + dfs(3,2) = 2` | **2** | `dp[2][1]` |
| `dfs(2, -1)` | `dfs(3,-1) = 1` | `1 + dfs(3,2) = 2` | **2** | `dp[2][0]` |
| `dfs(1, 0)` prev=`3` | `dfs(2,0) = 2` | `5 > 3` → `1 + dfs(2,1) = 2` | **2** | `dp[1][1]` |
| `dfs(1, -1)` | `dfs(2,-1) = 2` | `1 + dfs(2,1) = 2` | **2** | `dp[1][0]` |
| `dfs(0, -1)` | `dfs(1,-1) = 2` | `1 + dfs(1,0) = 3` | **3** ✅ | `dp[0][0]` |

Read the answer out of `dp[0][0]` → **3** (`[3, 5, 8]` or `[3, 4, 8]`).

Notice `dfs(3, ...)` was asked four separate times with different `prev` — but `dfs(2, 1)` and `dfs(3, 2)` each get computed **once** and reused. That reuse is the entire win.

```java
class Solution {
    public int lengthOfLIS(int[] nums) {
        int len = nums.length;
        int[][] dp = new int[len][len+1];
        for (int[] a : dp) Arrays.fill(a, -1);
        dfs(nums, 0, -1,  dp);
        // System.out.println(Arrays.deepToString(dp));
        return dp[0][0];
    }

    private int dfs (int[] nums, int curr, int prev, int[][] dp) {
        
        if (curr==nums.length) return 0;
        if (dp[curr][prev+1] != -1) return dp[curr][prev+1];

        int skip = dfs(nums, curr+1, prev, dp);
        int take = 0;
        if (prev == -1 || nums[curr] > nums[prev]) {
            take = 1 + dfs (nums, curr+1, curr, dp);
        }

        return dp[curr][prev+1] = Math.max(take, skip);
    }
}
```

- **Time:** `O(n²)` — `n × (n+1)` states, `O(1)` work each
- **Space:** `O(n²)` table + `O(n)` recursion stack

---

### ✅ Solution 2 — Classic Tabulation, `dp[i] = LIS ending at i`

The intuitive formulation. Flip the meaning of the state: `dp[i]` is the length of the longest increasing subsequence that **ends exactly at index `i`**. Every such subsequence must have some predecessor `j < i` with `nums[j] < nums[i]`, so just look back at all of them.

Because a subsequence can end anywhere, the answer is `max(dp[i])`, not `dp[0]`.

```java
class Solution {
    public int lengthOfLIS(int[] nums) {
        int n = nums.length;
        int[] dp = new int[n];
        Arrays.fill(dp, 1);          // every element alone is an LIS of length 1

        int best = 1;
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (nums[j] < nums[i]) {
                    dp[i] = Math.max(dp[i], dp[j] + 1);
                }
            }
            best = Math.max(best, dp[i]);
        }
        return best;
    }
}
```

- **Time:** `O(n²)` — **Space:** `O(n)` (drops the quadratic table and the stack)

---

### 🏆 Solution 3 — Patience Sorting / Binary Search (`O(n log n)`)

The follow-up answer. Maintain a list `tails` where `tails[k]` = **the smallest possible tail value** of an increasing subsequence of length `k+1` seen so far. Keeping tails as small as possible leaves the most room to extend later.

For each `x`, binary-search the **first tail ≥ x** (lower bound):
- Found → overwrite it. Same length, smaller tail — strictly better for the future.
- Not found (`x` beats every tail) → append. The LIS just got one longer.

> [!important]
> `tails` is **not** an actual increasing subsequence — its contents can be a mix of values from different candidate chains. Only its **length** is meaningful. This is the classic gotcha if an interviewer asks you to reconstruct the sequence itself (you'd need a parent-pointer array for that).

Using lower bound (`>= x`) is what enforces **strict** increase; a `> x` upper bound would solve the *non-decreasing* variant instead.

```java
class Solution {
    public int lengthOfLIS(int[] nums) {
        List<Integer> tails = new ArrayList<>();

        for (int x : nums) {
            // first index with tails[idx] >= x
            int lo = 0, hi = tails.size();
            while (lo < hi) {
                int mid = lo + (hi - lo) / 2;
                if (tails.get(mid) < x) lo = mid + 1;
                else hi = mid;
            }

            if (lo == tails.size()) tails.add(x);   // extend
            else tails.set(lo, x);                  // tighten
        }

        return tails.size();
    }
}
```

**Quick trace** — `nums = [10, 9, 2, 5, 3, 7, 101, 18]`:

| `x` | Action | `tails` after |
|---|---|---|
| `10` | append | `[10]` |
| `9` | replace idx 0 | `[9]` |
| `2` | replace idx 0 | `[2]` |
| `5` | append | `[2, 5]` |
| `3` | replace idx 1 | `[2, 3]` |
| `7` | append | `[2, 3, 7]` |
| `101` | append | `[2, 3, 7, 101]` |
| `18` | replace idx 3 | `[2, 3, 7, 18]` |

Length = **4** ✅ (note the final `tails` happens to be a valid LIS here, but that's luck, not a guarantee).

- **Time:** `O(n log n)` — **Space:** `O(n)`

---

## 🔑 Key Insights
- **The memo state is a cache key, not a theorem.** `dp[curr][prev+1]` = the value `dfs(curr, prev)` returned. Resist inventing a prettier definition.
- **`prev + 1` is pure index hygiene** — `prev = -1` means "nothing picked yet", and that has to map to column `0`. This is why the table is `n × (n+1)`, not `n × n`.
- **Suffix DP answers at the start, prefix DP answers at the max.** `dfs(0, -1)` → `dp[0][0]` for the forward-looking form; `max(dp[i])` for the "ending at `i`" form. Mixing these up is the #1 source of wrong answers here.
- **`tails` in the binary-search solution is a length-tracker, not a subsequence.** Smallest-possible-tail-per-length is the invariant that makes greedy overwriting safe.

---

## ⚠️ Pitfalls
> [!warning]
> - **`return dp[0][0]` instead of the `dfs` return value.** It only works because `dfs(0, -1)` writes exactly that cell before returning. It's correct here, but returning `dfs(nums, 0, -1, dp)` directly is safer and self-documenting — and it would survive `nums.length == 0` (the current version would throw `ArrayIndexOutOfBoundsException` on an empty array; constraints guarantee `n >= 1`, so LeetCode never hits it).
> - **`O(n²)` memory is tight.** At `n = 2500`, `dp` is ~6.25M ints ≈ **25 MB**. It passes, but the tabulated `dp[i]` form is `O(n)` and strictly better — prefer it if an interviewer asks about space.
> - **Strict vs non-strict.** `nums[curr] > nums[prev]` must be `>`, not `>=`. With `>=`, `[7,7,7,7]` would return `4` instead of `1`. Same trap in the binary search: lower bound (`>= x`) for strict, upper bound (`> x`) for non-decreasing.
> - **Forgetting `Arrays.fill(dp, 1)` in the tabulation.** A default of `0` makes every answer off by one, since a single element is already an LIS of length `1`.

---

## ⏱️ Complexity

| Approach | Time | Space |
|---|---|---|
| Pure recursion | `O(2^n)` | `O(n)` stack |
| **Memoization (this solution)** | **`O(n²)`** | **`O(n²)` + `O(n)` stack** |
| Tabulation `dp[i]` | `O(n²)` | `O(n)` |
| Patience sorting + binary search | `O(n log n)` | `O(n)` |

---

## 🔗 Same Pattern
- **Longest Divisible Subset** — swap the `>` guard for a divisibility check
- **Russian Doll Envelopes** — sort, then LIS on the second dimension
- **Longest String Chain** — LIS where "increasing" means "is a predecessor string"
- **Number of Longest Increasing Subsequences** — same `dp[i]` skeleton plus a count array
