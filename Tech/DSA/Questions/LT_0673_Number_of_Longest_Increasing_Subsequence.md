---
created: 2026-08-10 11:20
tags:
  - dsa
  - dynamic-programming
  - tabulation
  - lis
  - counting-dp
source: https://leetcode.com/problems/number-of-longest-increasing-subsequence/description/
problem_id: "673"
difficulty: Medium
status: Solved
review_date:
---
# LT_0673 – Number of Longest Increasing Subsequence

**Link:** [Open Problem](https://leetcode.com/problems/number-of-longest-increasing-subsequence/description/)

---

## 📝 Problem Description
> [!info]
> Given an integer array `nums`, return the **number of longest increasing subsequences**.
>
> Notice that the sequence has to be **strictly** increasing.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [1,3,5,4,7]`
> **Output:** `2`
> **Explanation:** The two longest increasing subsequences are `[1, 3, 4, 7]` and `[1, 3, 5, 7]`.

> [!example]
> **Input:** `nums = [2,2,2,2,2]`
> **Output:** `5`
> **Explanation:** The length of the longest increasing subsequence is 1, and there are 5 increasing subsequences of length 1, so the output is 5.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 2000`
> - `-10^6 <= nums[i] <= 10^6`
> - The answer is guaranteed to fit inside a 32-bit integer.

---

## 🔍 Intuition

This is [[LT_0300_Longest_Increasing_Subsequence]] with a second ledger bolted on. The `O(n²)` LIS tabulation already computes `length[i]` = "length of the longest increasing subsequence **ending exactly at** `i`". To also count them, I carry `count[i]` = "how many distinct LIS of that length end at `i`" and update the two arrays in lockstep.

The whole problem lives in one `if/else`. When I find a valid predecessor `j` (`nums[j] < nums[i]`):
- If `length[j] + 1 > length[i]` — I've found a **strictly longer** way to end at `i`. Every LIS I'd counted so far is now obsolete, so I **overwrite**: `count[i] = count[j]`.
- If `length[j] + 1 == length[i]` — I've found **another** way to hit the same best length. So I **accumulate**: `count[i] += count[j]`.

That reset-vs-accumulate distinction is the entire trick, and it's exactly what makes this Medium rather than Easy.

The last subtlety is the answer itself. It isn't `count[argmax]` — several indices can tie for the longest length, and each contributes its own subsequences. So I take `maxLen` first, then sum `count[i]` over every `i` where `length[i] == maxLen`. Example 2 (`[2,2,2,2,2]`) is the sanity check: `maxLen = 1`, five indices tie, answer `5`.

> 🟢 *Counting DP — pair every "best value" array with a "how many ways" array*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Parallel `length[]` + `count[]` Tabulation

**Why this works:**
- **`count[i]` is only ever meaningful relative to the *current* `length[i]`.** The moment `length[i]` improves, the old count describes shorter subsequences and must be discarded — that's why the `>` branch assigns rather than adds.
- **`count[j]`, not `1`.** Extending index `j` by `nums[i]` produces one new LIS *per* LIS ending at `j`. Adding `1` would count paths, not subsequences.
- **Both arrays start at `1`.** Every element is trivially an increasing subsequence of length 1, exactly one way — which is also what makes `[2,2,2,2,2]` fall out correctly with no special case.
- **The final sweep sums all tied maxima**, so ties across different tails are handled without extra bookkeeping.

**Dry Run** (`nums = [1,3,5,4,7]`):

Start: `length = [1,1,1,1,1]`, `count = [1,1,1,1,1]`, `maxLen = 1`.

| `i` | `nums[i]` | inner `j` steps | `length[i]` | `count[i]` |
|---|---|---|---|---|
| 0 | `1` | — | `1` | `1` |
| 1 | `3` | `j=0`: `1<3`, `1+1 > 1` → **reset** | `2` | `count[0] = 1` |
| 2 | `5` | `j=0`: `1+1 > 1` → reset → `(2, 1)`<br>`j=1`: `2+1 > 2` → **reset** | `3` | `count[1] = 1` |
| 3 | `4` | `j=0`: reset → `(2, 1)`<br>`j=1`: `2+1 > 2` → **reset**<br>`j=2`: `5 < 4` false | `3` | `count[1] = 1` |
| 4 | `7` | `j=0`: reset → `(2, 1)`<br>`j=1`: reset → `(3, 1)`<br>`j=2`: `3+1 > 3` → **reset** → `(4, count[2]=1)`<br>`j=3`: `3+1 == 4` → **accumulate** `+= count[3]` | `4` | `1 + 1 = 2` |

Final: `length = [1,2,3,3,4]`, `count = [1,1,1,1,2]`, `maxLen = 4`.
Only `i = 4` has `length[i] == 4`, so the answer is `count[4] = 2` ✅ — matching `[1,3,5,7]` and `[1,3,4,7]`.

Note how index `3` (`nums = 4`) never wins on its own but feeds its single count into index `4` through the `==` branch. That's the accumulate case doing its job.

```java
class Solution {
    public int findNumberOfLIS(int[] nums) {

        int len = nums.length;
        int[] length = new int[len];
        int[] count = new int[len];

        Arrays.fill(length, 1);
        Arrays.fill(count, 1);

        int maxLen = 1;

        for (int i=0; i<len; i++) {

            for (int j=0; j<i; j++) {

                if (nums[i] > nums[j]) {

                    if (length[j] + 1 > length[i]) {

                        length[i] = length[j] + 1;
                        count[i] = count[j];

                    } else if (length[j] + 1 == length[i]) {
                        count[i] += count[j];
                    }

                }

            }
            maxLen = Math.max(maxLen, length[i]);
        }

        int ans = 0;
        for (int i=0; i<len; i++) {
            if (length[i]==maxLen) ans += count[i];
        }

        return ans;

    }
}
```

- **Time:** `O(n²)` · **Space:** `O(n)`

> [!info]
> The raw notes carried a second version of this solution, but it's the same algorithm — `length[i] < length[j]+1` is just `length[j]+1 > length[i]` rewritten, plus some `System.out.println` debugging. Only one is kept here and in the repo.

---

## 🔑 Key Insights
- **Reset on strictly better, accumulate on equal.** Getting these two branches the wrong way round is the defining bug of this problem — an `+=` in the `>` branch inflates the answer with stale shorter subsequences.
- **`count[i] += count[j]`, never `count[i] += 1`.** The number of ways to extend is the number of ways to arrive.
- **The answer sums over *all* indices achieving `maxLen`.** `[2,2,2,2,2] → 5` exists in the examples precisely to catch people who return the count at a single index.
- **`length[j] + 1` appears three times** — computing it once into a local (`int cand = length[j] + 1;`) makes the branch structure much easier to read under interview pressure.
- Unlike [[LT_0300_Longest_Increasing_Subsequence]], the `O(n log n)` patience-sorting trick does **not** extend to counting without a Fenwick tree — `O(n²)` is the expected answer here, and `n <= 2000` confirms it.

---

## ⚠️ Pitfalls
> [!warning]
> - Initialising `count` to `0` instead of `1` zeroes the whole answer — a single element is one subsequence, not zero.
> - `maxLen` must start at `1`, not `0`. With `0` it still works here (every `length[i] >= 1`), but the habit breaks on problems where the array can be empty.
> - Strictly increasing means `nums[i] > nums[j]`, not `>=`. Using `>=` turns `[2,2,2,2,2]` into a length-5 run and returns `1`.
> - Don't try to shortcut with `count[maxIndex]`. Ties are the common case, not the edge case.

---

## ⏱️ Complexity
- **Time:** `O(n²)`
- **Space:** `O(n)`
