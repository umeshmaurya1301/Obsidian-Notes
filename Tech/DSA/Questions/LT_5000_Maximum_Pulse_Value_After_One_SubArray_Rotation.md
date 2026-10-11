---
created: 2026-09-20 00:00
tags:
  - dsa
  - arrays
  - prefix-sum
source: https://leetcode.com/contest/weekly-contest-520/problems/maximum-pulse-value-after-one-subarray-rotation/
problem_id: "5000"
difficulty: Medium
status: Solved
review_date:
---
# LT_5000 – Maximum Pulse Value After One Sub Array Rotation

**Link:** [Open Problem](https://leetcode.com/contest/weekly-contest-520/problems/maximum-pulse-value-after-one-subarray-rotation/)

> [!warning]
> No permanent LeetCode problem number exists yet for this contest problem (Weekly Contest 520, Q3) — `problem_id: "5000"` is a placeholder. Rename the file and update the frontmatter once LeetCode assigns the real id.

---

## 📝 Problem Description
> [!info]
> You are given an integer array `nums` of length `n`. Define the pulse value of an integer array `arr` as the alternating sum starting at index 0: `pulse(arr) = arr[0] - arr[1] + arr[2] - arr[3] + ...`.
> You may perform at most one operation on `nums`: choose two indices `l` and `r` such that `0 <= l < r <= n - 1`, and left-rotate the subarray `nums[l..r]` by exactly one position (e.g. `[a,b,c,d]` becomes `[b,c,d,a]`). Return the maximum pulse value obtainable after at most one such operation.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [1,5,2]`
> **Output:** `6`
> **Explanation:** The original pulse value is `1 - 5 + 2 = -2`. Rotating `nums[0..1]` from `[1,5]` to `[5,1]` gives `[5,1,2]`, with pulse value `5 - 1 + 2 = 6`.

> [!example]
> **Input:** `nums = [6,4,3]`
> **Output:** `7`
> **Explanation:** The original pulse value is `6 - 4 + 3 = 5`. Rotating `nums[1..2]` from `[4,3]` to `[3,4]` gives `[6,3,4]`, with pulse value `6 - 3 + 4 = 7`.

> [!example]
> **Input:** `nums = [9,7]`
> **Output:** `2`
> **Explanation:** The original pulse value `9 - 7 = 2` is already maximum, so no rotation is required.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= n == nums.length <= 1e5`
> - `-1e9 <= nums[i] <= 1e9`

---

## 🔍 Intuition

`pulse(arr)` is just `Σ sign(i) * arr[i]` where `sign(i) = +1` for even `i` and `-1` for odd `i`. A single left-rotation of `nums[l..r]` doesn't change the multiset of values — it only changes which *index* (and therefore which sign) each shifted value lands on. Every element strictly inside `(l, r]` slides one position left, which flips its sign contribution; `nums[l]` alone jumps all the way to position `r`. So instead of materializing the rotated array and recomputing the pulse from scratch (`O(n)` per rotation, `O(n^3)` overall), I only need the *change* (`delta`) caused by one `(l, r)` choice, added to the original pulse. Once `delta` is expressed as `(sign(r) - sign(l)) * nums[l] - 2 * (range sum of sign(k)*nums[k] for k in l+1..r)`, the range-sum part becomes a classic prefix-sum lookup, dropping each pair's delta to `O(1)`.

> 🟢 *Prefix Sum over Signed Array*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Alternating-Sign Prefix Sum (Pairwise Delta)

**Why this works:**
- `pulse(nums)` is precomputed once as `Σ sign(i)*nums[i]`.
- For every candidate `(l, r)`, the rotation's effect decomposes into: `nums[l]` moving from `sign(l)` to `sign(r)`, plus every `k` in `(l, r]` flipping sign — the second part is `-2 * Σ_{k=l+1}^{r} sign(k)*nums[k]`, which is a range sum on the precomputed `altPrefix` array.
- Trying every `(l, r)` pair and taking the best `pulse + delta` is correct because the delta formula exactly reproduces what a real rotation would do to the pulse, without ever touching the array.

**Dry Run** (`nums = [1,5,2]`):

| step | `i` | `val = sign(i)*nums[i]` | `pulse` | `altPrefix[i+1]` |
|---|---|---|---|---|
| build | 0 | `+1` | `1` | `1` |
| build | 1 | `-5` | `-4` | `-4` |
| build | 2 | `+2` | `-2` | `-2` |

`ans` starts at `pulse = -2`. Then scanning pairs:

| `l` | `r` | `rangeSum = altPrefix[r+1]-altPrefix[l+1]` | `delta = (signR-signL)*nums[l] - 2*rangeSum` | `pulse+delta` | `ans` |
|---|---|---|---|---|---|
| 0 | 1 | `-4 - 1 = -5` | `(-1-1)*1 - 2*(-5) = 8` | `6` | `6` |
| 0 | 2 | `-2 - 1 = -3` | `(1-1)*1 - 2*(-3) = 6` | `4` | `6` |
| 1 | 2 | `-2 - (-4) = 2` | `(1-(-1))*5 - 2*2 = 6` | `4` | `6` |

Final `ans = 6`, matching the expected output (rotating `[0..1]` to get `[5,1,2]`).

```java
class Solution {
    static int LEN;

    public long maxValue(int[] nums) {
        LEN = nums.length;
        long pulse = 0;
        long[] altPrefix = new long[LEN + 1];

        for (int i = 0; i < LEN; i++) {
            long val = (i % 2 == 0) ? nums[i] : -nums[i];
            pulse += val;
            altPrefix[i + 1] = altPrefix[i] + val;
        }

        long ans = pulse;
        for (int l=0; l<LEN; l++) {

            int signL = (l%2==0) ? 1 : -1;

            for (int r=l+1; r<LEN; r++) {
                
                int signR = (r%2==0) ? 1 : -1;
                long rangeSum = altPrefix[r+1] - altPrefix[l+1];
                long delta = (long) (signR - signL) * nums[l] - 2L * rangeSum;

                ans = Math.max(ans, pulse + delta);
            }
        }

        return ans;
    }
}
```

- **Time:** `O(n^2)` (all `(l, r)` pairs, `O(1)` work each) · **Space:** `O(n)` (the `altPrefix` array)

> [!note]
> This passes but is not the intended complexity for `n <= 1e5`. `delta` can be split into a term depending only on `r` and a term depending only on `l` — `Δ(l,r) = A(r) + B(l)` — which lets a single left-to-right scan over `r` keep a running best `B(l)` and reach `O(n)`. That rewrite hasn't been implemented yet; add it here as **Solution 2** when done.

---

## 🔑 Key Insights
- `pulse(arr) = Σ sign(i)*arr[i]` with `sign(i) = +1` for even `i`, `-1` for odd `i` — rotation only reshuffles which sign each value gets, never the values themselves.
- A left-rotation of `nums[l..r]` shifts every element in `(l, r]` one index left (sign flips), while `nums[l]` alone teleports to index `r` (sign becomes `sign(r)` directly, not just flipped).
- Precomputing `alt[i] = sign(i)*nums[i]` and its prefix sum turns the range term of `delta` into an `O(1)` lookup: `altPrefix[r+1] - altPrefix[l+1]`.
- The still-open `O(n)` refinement comes from separating `delta` into an `r`-only part and an `l`-only part so the best `l` can be tracked while scanning `r` once.

---

## ⚠️ Pitfalls
> [!warning]
> - Off-by-one on the prefix array: the range sum for `k = l+1..r` is `altPrefix[r+1] - altPrefix[l+1]`, not `altPrefix[r] - altPrefix[l]`.
> - `nums[l]` does **not** just flip sign like the rest of the shifted range — it jumps straight to `sign(r)`; folding it into the range-sum term instead of handling it separately gives a wrong `delta`.
> - `nums[i]` up to `1e9` and `n` up to `1e5` means `pulse`/prefix sums can reach ~`1e14` — everything must be `long`, not `int`.

---

## ⏱️ Complexity
- **Time:** `O(n^2)`
- **Space:** `O(n)`
