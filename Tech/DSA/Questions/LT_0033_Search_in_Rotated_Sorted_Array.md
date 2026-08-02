---
created: 2026-08-02 11:05
tags:
  - dsa
  - binary-search
  - arrays
source: https://leetcode.com/problems/search-in-rotated-sorted-array/
problem_id: "33"
difficulty: Medium
status: Solved
review_date:
---
# LT_0033 – Search in Rotated Sorted Array

**Link:** [Open Problem](https://leetcode.com/problems/search-in-rotated-sorted-array/)

---

## 📝 Problem Description
> [!info]
> There is an integer array `nums` sorted in ascending order (with **distinct** values).
>
> Prior to being passed to your function, `nums` is **possibly rotated** at an unknown pivot index `k` (`1 <= k < nums.length`) such that the resulting array is `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]` (**0-indexed**). For example, `[0,1,2,4,5,6,7]` might be rotated at pivot index `3` and become `[4,5,6,7,0,1,2]`.
>
> Given the array `nums` **after** the possible rotation and an integer `target`, return *the index of* `target` *if it is in* `nums`*, or* `-1` *if it is not in* `nums`.
>
> You must write an algorithm with `O(log n)` runtime complexity.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [4,5,6,7,0,1,2], target = 0`
> **Output:** `4`
> **Explanation:** `0` sits at index `4` in the rotated array.

> [!example]
> **Input:** `nums = [4,5,6,7,0,1,2], target = 3`
> **Output:** `-1`
> **Explanation:** `3` is not present anywhere in `nums`.

> [!example]
> **Input:** `nums = [1], target = 0`
> **Output:** `-1`
> **Explanation:** Single-element array that does not contain the target.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 5000`
> - `-10^4 <= nums[i] <= 10^4`
> - All values of `nums` are **unique**
> - `nums` is an ascending array that is possibly rotated
> - `-10^4 <= target <= 10^4`

---

## 🔍 Intuition

Plain binary search dies here because the array isn't globally sorted — comparing `target` with `nums[mid]` no longer tells me which side to discard. But the array isn't random either: a rotation just cuts a sorted array once and swaps the two pieces. That means **at least one of the two halves around `mid` is always fully sorted** — if the cut lands in the left half, the right half is clean, and vice versa. That's the invariant the whole solution leans on.

So each iteration does two things instead of one: first *identify* the sorted half, then *decide* using it. `nums[lo] <= nums[mid]` tells me the left half is sorted (no pivot inside it); otherwise the right half must be. Once I have a fully sorted half, I can ask a question I can actually answer — "does `target` lie inside this half's `[low, high]` range?" If yes I move into it; if no, the answer can only be in the other half, so I discard the sorted one. Either way I halve the search space, which keeps the whole thing `O(log n)`.

What I like about this version is that it never finds the pivot explicitly. The two-pass alternative (binary search for the rotation point, then binary search the correct segment) works, but this does it in one pass with no extra state — the pivot's location is *inferred* every iteration from the `nums[lo] <= nums[mid]` comparison rather than computed once.

> 🟢 *Modified Binary Search — Identify the Sorted Half*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Modified Binary Search (Sorted-Half Detection)

**Why this works:**

- **One rotation ⇒ at most one "break point".** A single break can live in only one of the two halves, so the other half is guaranteed to be a plain ascending run. That guarantee is what restores binary search's ability to discard half the range with certainty.
- **The sorted half gives an exact membership test.** In an ascending run `[a .. b]`, `target` is present *only if* `a <= target <= b`. That's an `O(1)` range check — no scan needed. If it fails, the target is definitively not in that half, so throwing it away is safe.
- **The unsorted half needs no analysis.** I never reason about the messy half directly. I only ever test the clean one and take the complement, which is why the branch logic stays this short.
- **`nums[lo] <= val` uses `<=` deliberately.** When the window shrinks to one or two elements, `lo == mid`, so `nums[lo] == val`. The `<=` classifies that as "left sorted", which is correct; a strict `<` would misroute into the else-branch and lose valid answers.

**Dry Run** (`nums = [4,5,6,7,0,1,2], target = 0`):

| Iter | `lo` | `hi` | `mid` | `val` | Which half is sorted? | Decision | Next window |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | `7` | `nums[0]=4 <= 7` → **left** `[4..7]` sorted | Is `4 <= 0 < 7`? **No** → target not in left | `lo = 4` |
| 2 | 4 | 6 | 5 | `1` | `nums[4]=0 <= 1` → **left** `[0..1]` sorted | Is `0 <= 0 < 1`? **Yes** → go left | `hi = 4` |
| 3 | 4 | 4 | 4 | `0` | — | `val == target` ✅ | **return `4`** |

Note iteration 1: the target `0` is *smaller* than `nums[mid]`, which in a normal sorted array would say "go left". Here the range check overrules that instinct — `0` is below the left half's floor of `4`, so it must live in the rotated tail on the right.

Second trace, the **right-sorted** branch — `nums = [5,6,7,0,1,2,4], target = 1`:

| Iter | `lo` | `hi` | `mid` | `val` | Which half is sorted? | Decision | Next window |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | `0` | `nums[0]=5 <= 0`? **No** → **right** `[0..4]` sorted | Is `1 > 0 && 1 <= nums[6]=4`? **Yes** → go right | `lo = 4` |
| 2 | 4 | 6 | 5 | `2` | `nums[4]=1 <= 2` → **left** sorted | Is `1 <= 1 < 2`? **Yes** → go left | `hi = 4` |
| 3 | 4 | 4 | 4 | `1` | — | `val == target` ✅ | **return `4`** |

```java
class Solution {
    public int search(int[] nums, int target) {
        int len = nums.length;
        int lo = 0;
        int hi = len-1;

        while (lo <= hi) {
            int mid = lo + (hi-lo)/2;
            int val = nums[mid];
            if (val == target) return mid;
            if (nums[lo] <= val) {

                if (nums[lo] <= target && target < val) {
                    hi = mid - 1;
                } else {
                    lo = mid + 1;
                }

            } else {

                if (target>val && target<=nums[hi]) {
                    lo = mid + 1;
                } else {
                    hi = mid - 1;
                }
            }
        }

        return -1;
    }
}
```

---

## 🔑 Key Insights

- **At least one half is always sorted** — this is *the* takeaway, and it generalises to *Find Minimum in Rotated Sorted Array* (`153`) and *Search in Rotated Sorted Array II* (`81`). Learn the invariant, not the branch soup.
- **Compare against the boundary, not the middle.** The decision uses `nums[lo]` / `nums[hi]` as range endpoints, not `nums[mid]` alone. In an unsorted array the midpoint value carries no directional information by itself — only the *interval* does.
- **Boundary strictness is asymmetric but safe.** `nums[lo] <= target && target < val` includes the low end and excludes `val`; `target > val && target <= nums[hi]` does the reverse. Both are fine because `val == target` was already returned above, so the excluded endpoint can never be the answer.
- **`lo + (hi - lo) / 2` avoids overflow.** `(lo + hi) / 2` can overflow `int` on huge ranges. Irrelevant at `n <= 5000`, but it's the habit interviewers look for.

---

## ⚠️ Pitfalls
> [!warning]
> - **Writing `nums[lo] < val` instead of `nums[lo] <= val`.** On `nums = [3,1], target = 1`: `mid = 0`, `val = 3`, and `nums[lo] < val` is `3 < 3` → false, so it wrongly enters the right-sorted branch, checks `1 > 3` → false, sets `hi = -1`, and returns `-1`. The correct answer is `1`. Strict `<` breaks every window where `lo == mid`.
> - **Reasoning about the unsorted half.** Tempting to add checks for the rotated side — don't. Always test the *sorted* half and take the else. Trying to bound the messy half is where most people's branch logic falls apart.
> - **Using stale endpoints.** `nums[hi]` must be the *current* `hi`, not `nums[len-1]`. After a few iterations the window has moved, and the old endpoint no longer bounds the half being tested.
> - **Assuming this survives duplicates.** With repeated values (`[3,1,3,3,3]`), `nums[lo] == nums[mid]` no longer proves the left half is sorted, and worst case degrades to `O(n)`. That's problem `81` — a different beast; this code relies on the "distinct values" constraint.

---

## ⏱️ Complexity
- **Time:** `O(log n)` — every iteration discards exactly half the window, regardless of which branch is taken
- **Space:** `O(1)` — iterative, with only `lo`, `hi`, `mid`, and `val` held

---

## 💡 Mental Model

```
A rotated sorted array = one sorted array cut once and swapped.
One cut ⇒ at most one half around mid can be broken.

Each step:
  1. Which half is clean?   nums[lo] <= nums[mid]  → left is clean
                            otherwise              → right is clean
  2. Does target fit inside the clean half's range?
         yes → move into it
         no  → it must be in the other half; discard the clean one

Never analyse the broken half. Just test the clean one and invert.
```

Standard binary search asks *"is target bigger or smaller than mid?"*. Here that question is meaningless — the fix is to ask *"is target inside this known-sorted interval?"* instead.
