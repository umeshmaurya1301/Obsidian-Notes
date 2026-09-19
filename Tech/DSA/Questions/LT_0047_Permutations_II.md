---
created: 2026-09-13 00:00
tags:
  - dsa
  - backtracking
  - recursion
  - permutations
source: https://leetcode.com/problems/permutations-ii/
problem_id: "47"
difficulty: Medium
status: Solved
review_date:
---
# LT_0047 – Permutations II

**Link:** [Open Problem](https://leetcode.com/problems/permutations-ii/)

---

## 📝 Problem Description
> [!info]
> Given a collection of numbers, `nums`, that might contain duplicates, return all possible unique permutations in any order.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [1,1,2]`
> **Output:** `[[1,1,2],[1,2,1],[2,1,1]]`

> [!example]
> **Input:** `nums = [1,2,3]`
> **Output:** `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]`

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 8`
> - `-10 <= nums[i] <= 10`

---

## 🔍 Intuition

Plain permutation backtracking (pick an unvisited index at each level, recurse, undo) generates every arrangement — but when the input has duplicates, it generates the *same* arrangement multiple times, once per way of assigning identical values to identical slots. The fix isn't to dedupe the output afterward with a `Set`; it's to stop the duplicate branch from ever being explored. Sorting the array first is what makes duplicates adjacent, which turns "is this a duplicate of something already tried at this level" into a cheap `nums[i] == nums[i-1]` check.

The subtle part is *which* duplicate to skip. Label the two equal `1`s as `1a` (index 0) and `1b` (index 1) after sorting. At the top level, trying `1a` first and then `1b` produces identical subtrees — so only one of them should ever start a branch. The rule `if (nums[i] == nums[i-1] && !visited[i-1]) continue;` says: skip `1b` only when `1a` is *not currently in the path* — meaning `1a` is still sitting unused at this same recursion level, about to produce (or having just produced) the exact same branch. Once `1a` *is* in the path (`visited[i-1] == true`), picking `1b` next is legal and necessary — it's what builds `[1a, 1b, 2]` correctly.

- **Why brute force + `Set` dedup is worse:** it still explores every one of the `n!` raw permutations (here `3! = 6` instead of the `3` unique ones) and pays hashing/boxing cost per full permutation just to throw half of them away. Skipping at the branch level prunes before wasted recursive calls even happen.

> 🟢 *Backtracking + Sorted-Array Duplicate Skip*

---

## 🧠 Evolution of Solutions

### ✅ Solution 1 — Backtracking with Visited Array + Sorted Duplicate Skip

**Why this works:**

- **Sorting groups equal values together**, so any duplicate that would create a redundant branch is always at `nums[i-1]` relative to `nums[i]`.
- **`visited[]` (not index removal) tracks what's in the current path**, so the same physical slot is never reused twice in one branch, while still allowing the *value* to reappear from a different slot.
- **The skip condition `!visited[i-1]` distinguishes "sibling choice" from "already chosen ancestor."** If `nums[i-1]` is currently in the path (`visited[i-1] == true`), `nums[i]` is a legitimate *next* pick, not a duplicate restart of the same branch.

**Dry Run** (`nums = [1,1,2]`, sorted → `[1a, 1b, 2]`):

| Path so far | Try index | Value | Decision |
|---|---|---|---|
| `[]` | 0 (`1a`) | 1 | place → `[1a]` |
| `[1a]` | 1 (`1b`) | 1 | `visited[0]=true` → allowed → `[1a,1b]` |
| `[1a,1b]` | 2 | 2 | place → `[1a,1b,2]` → **record `[1,1,2]`** |
| `[1a]` (after undo `1b`) | 2 | 2 | place → `[1a,2]` |
| `[1a,2]` | 1 (`1b`) | 1 | `visited[0]=true` → allowed → `[1a,2,1b]` → **record `[1,2,1]`** |
| `[]` (after full undo) | 1 (`1b`) | 1 | `nums[1]==nums[0]` and `visited[0]=false` → **skip** |
| `[]` | 2 | 2 | place → `[2]` |
| `[2]` | 0 (`1a`) | 1 | place → `[2,1a]` |
| `[2,1a]` | 1 (`1b`) | 1 | `visited[0]=true` → allowed → `[2,1a,1b]` → **record `[2,1,1]`** |
| `[2]` | 1 (`1b`) | 1 | `nums[1]==nums[0]` and `visited[0]=false` → **skip** |

Result: `[[1,1,2],[1,2,1],[2,1,1]]` — exactly the 3 unique permutations, no duplicates generated or filtered after the fact.

```java
class Solution {

    public List<List<Integer>> permuteUnique(int[] nums) {

        Arrays.sort(nums);

        List<List<Integer>> ans = new ArrayList<>();
        boolean[] visited = new boolean[nums.length];

        backTrack(nums, visited, new ArrayList<>(), ans);

        return ans;
    }

    private void backTrack(int[] nums,
                           boolean[] visited,
                           List<Integer> path,
                           List<List<Integer>> ans) {

        if (path.size() == nums.length) {
            ans.add(new ArrayList<>(path));
            return;
        }

        for (int i = 0; i < nums.length; i++) {

            if (visited[i]) {
                continue;
            }

            // Skip duplicate branches
            if (i > 0 &&
                nums[i] == nums[i - 1] &&
                !visited[i - 1]) {
                continue;
            }

            visited[i] = true;
            path.add(nums[i]);

            backTrack(nums, visited, path, ans);

            path.remove(path.size() - 1);
            visited[i] = false;
        }
    }
}
```

- **Time:** `O(n! · n)` worst case (unique elements) · **Space:** `O(n)` for `visited` and recursion depth, excluding output

---

## 🔑 Key Insights
- **Sort first, always.** The `nums[i] == nums[i-1]` duplicate check is only correct because sorting makes equal values adjacent — without it, indices of equal values could be scattered and the check would miss cases.
- **`!visited[i-1]` is the crux, not just `nums[i] == nums[i-1]`.** The visited-check distinguishes "this duplicate is a sibling I haven't tried yet at this level" (skip) from "this duplicate is next after its twin is already placed" (allow).
- **This pattern generalizes** to any "unique combinations/subsets/permutations with duplicates" problem (e.g. Subsets II, Combination Sum II) — sort + skip adjacent-equal siblings at the same recursion level.

---

## ⚠️ Pitfalls
> [!warning]
> - **Forgetting to sort `nums` first** — the duplicate-skip logic silently does nothing (or skips the wrong things) on unsorted input.
> - **Using `visited[i-1]` instead of `!visited[i-1]`** (or omitting the visited check entirely and just checking `nums[i] == nums[i-1]`) — this either fails to skip anything or incorrectly blocks valid permutations where the duplicate is legitimately next in the path.
> - **Not undoing `visited[i] = false` and `path.remove(...)` symmetrically** — leaves stale state that corrupts sibling branches later in the loop.

---

## ⏱️ Complexity
- **Time:** `O(n! · n)` — up to `n!` permutations, each costing `O(n)` to copy into `ans`; the duplicate skip only prunes, it doesn't change the asymptotic worst case for distinct elements.
- **Space:** `O(n)` for the `visited` array and recursion stack depth, excluding the output list itself.
