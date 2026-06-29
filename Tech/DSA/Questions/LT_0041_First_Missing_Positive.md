---
created: 2026-05-22 00:00
tags:
  - dsa
  - array
  - hash-table
  - cyclic-sort
source: https://leetcode.com/problems/first-missing-positive/description/
problem_id: "41"
difficulty: Hard
status: Solved
review_date:
---
# LT_0041 – First Missing Positive

**Link:** [Open Problem](https://leetcode.com/problems/first-missing-positive/description/)

---

## 📝 Problem Description
> [!info]
> Given an unsorted integer array `nums`, return the smallest missing positive integer.
>
> You must implement an algorithm that runs in `O(n)` time and uses `O(1)` auxiliary space.

---

## 🧪 Examples
> [!example]
> **Input:** `nums = [1,2,0]`
> **Output:** `3`
> **Explanation:** The numbers in the range [1,2] are all in the array.

> [!example]
> **Input:** `nums = [3,4,-1,1]`
> **Output:** `2`
> **Explanation:** 1 is in the array but 2 is missing.

> [!example]
> **Input:** `nums = [7,8,9,11,12]`
> **Output:** `1`
> **Explanation:** The smallest positive integer 1 is missing.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= nums.length <= 10^5`
> - `-2^31 <= nums[i] <= 2^31 - 1`

---

## 🔍 Intuition

The answer must lie in `[1, n+1]` where `n = nums.length` — if all of `1..n` are present, the answer is `n+1`. This bounds the search and lets us use the array itself as a presence marker: value `v` belongs at index `v-1`. We scan through and keep swapping each number to its correct index; once placement is done, the first index where `nums[i] != i+1` reveals the missing positive. A HashSet would work in `O(n)` time but costs `O(n)` space — treating indices as buckets eliminates that entirely.

> 🟢 *Cyclic Sort / Index-as-Hashmap*

---

### 🧩 Deep Dive — Deriving `nums[i] != nums[nums[i]-1]` From Scratch

Most explanations say: *"We check `nums[i] != nums[nums[i]-1]` to avoid infinite loops."*
That is true, but it doesn't answer **how someone invents this condition**. Here's the derivation.

---

#### Step 1 — Forget the code. Think about the goal.

Suppose `nums = [3,4,-1,1]`. If you solved this manually, you'd arrange the positives in order:

```
1 ✓
2 ✗  ← answer = 2
```

The first thought: **if every positive number `x` could be placed at index `x-1`, the answer becomes obvious.**

---

#### Step 2 — This gives us a mapping

Instead of sorting, we invent a **positional mapping**:

| Value | Belongs at index |
|-------|-----------------|
| `1`   | `0`             |
| `2`   | `1`             |
| `3`   | `2`             |
| `n`   | `n-1`           |

So whenever we see `nums[i] = x`, its correct home is index `x - 1`.

Hence the swap:
```java
swap(nums, i, nums[i] - 1);
```

---

#### Step 3 — But should we always swap?

Consider `nums = [1,2,3]`. At `i = 0`, value `1` belongs at index `0` — it's already there. Swapping is pointless.

So we add the check: **`nums[i] != i + 1`** (value is not already in its correct slot).

But wait — that still misses something.

---

#### Step 4 — The duplicate problem

Consider `[1,1]`. At `i = 1`, `nums[i] = 1` belongs at index `0`.

```
Before swap: [1, 1]
After  swap: [1, 1]   ← nothing changed!
```

The array is identical after swapping. Next iteration: same condition, same swap, forever. **Infinite loop.**

Why? Because the destination (`index 0`) already holds value `1` — the exact value we're trying to place. Swapping two identical values is a no-op.

---

#### Step 5 — So what do we actually check?

Before swapping, ask: **"Does the destination already hold the correct value?"**

- Destination index = `nums[i] - 1`
- Value there = `nums[nums[i] - 1]`
- Value we want to place = `nums[i]`

If `nums[i] == nums[nums[i] - 1]`, the home already contains our value. Swapping is useless.

So we swap **only when**:

```java
nums[i] != nums[nums[i] - 1]
```

> [!info] Read it in plain English
> *"The value I'm trying to place is **not** already sitting at its correct position."*
> That's it. The infinite-loop prevention is a **consequence** of this deeper idea, not the cause.

---

#### Step 6 — Full condition walkthrough

Before any swap, three things must be true:

```
1. nums[i] > 0          → only positive numbers have a valid home
2. nums[i] <= n         → home index must be within bounds
3. nums[i] != nums[nums[i]-1]  → home doesn't already contain this value
```

**Example trace** (`nums = [3,4,-1,1]`):

| `i` | `nums[i]` | Home index | `nums[home]` | `nums[i] != nums[home]`? | Action |
|-----|-----------|------------|--------------|--------------------------|--------|
| 0   | 3         | 2          | -1           | ✅ 3 ≠ -1                | swap(0,2) → `[-1,4,3,1]` |
| 0   | -1        | —          | —            | ❌ out of range           | skip   |
| 1   | 4         | 3          | 1            | ✅ 4 ≠ 1                 | swap(1,3) → `[-1,1,3,4]` |
| 1   | 1         | 0          | -1           | ✅ 1 ≠ -1                | swap(1,0) → `[1,-1,3,4]` |
| 1   | -1        | —          | —            | ❌ out of range           | skip   |
| 2   | 3         | 2          | 3            | ❌ 3 = 3 (already home)  | skip   |
| 3   | 4         | 3          | 4            | ❌ 4 = 4 (already home)  | skip   |

**Scan:** index 1 has `-1` instead of `2` → **return 2**.

**Duplicate trace** (`nums = [1,1]`):

| `i` | `nums[i]` | Home index | `nums[home]` | `nums[i] != nums[home]`? | Action |
|-----|-----------|------------|--------------|--------------------------|--------|
| 1   | 1         | 0          | 1            | ❌ 1 = 1                 | skip (infinite loop avoided) |

---

#### The One-Line Intuition to Remember

> `nums[i] != nums[nums[i]-1]` does not mean *"avoid infinite loops."*
> It means **"only move a value if its correct position doesn't already contain that value."**
> The loop prevention is a consequence. The insight is about making *progress*.

---

## 🧠 Evolution of Solutions

### ✅ Solution — Cyclic Sort (In-place Index Placement)

**Why this works:**
- The missing positive is always in `[1, n+1]`, so only values in that range matter.
- Placing value `v` at index `v-1` encodes presence without extra space.
- A single scan after placement finds the first "hole" — the index where the value is wrong.

**Dry Run** (`nums = [3,4,-1,1]`):

| Step | i | nums | Action |
|------|---|------|--------|
| 1 | 0 | `[3, 4, -1, 1]` | `nums[0]=3` belongs at index 2 → swap(0,2) |
| 2 | 0 | `[-1, 4, 3, 1]` | `nums[0]=-1` out of range → move on |
| 3 | 1 | `[-1, 4, 3, 1]` | `nums[1]=4` belongs at index 3 → swap(1,3) |
| 4 | 1 | `[-1, 1, 3, 4]` | `nums[1]=1` belongs at index 0 → swap(1,0) |
| 5 | 1 | `[1, -1, 3, 4]` | `nums[1]=-1` out of range → move on |
| scan | 0 | `[1, -1, 3, 4]` | index 0 → 1 ✅ |
| scan | 1 | — | index 1 → expected 2, found -1 → **return 2** |

```java
class Solution {

    public int firstMissingPositive(int[] nums) {

        int n = nums.length;

        for (int i = 0; i < n; i++) {

            while (
                nums[i] > 0 &&
                nums[i] <= n &&
                nums[i] != nums[nums[i] - 1]
            ) {

                swap(nums, i, nums[i] - 1);
            }
        }

        for (int i = 0; i < n; i++) {

            if (nums[i] != i + 1) {
                return i + 1;
            }
        }

        return n + 1;
    }

    private void swap(int[] nums, int i, int j) {

        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
}
```

---

## 🔑 Key Insights
- Use `while`, not `if` — one swap may bring another valid number to index `i` that also needs placing. Only stop when `nums[i]` is out of range or already at its correct slot.
- The guard `nums[i] != nums[nums[i] - 1]` is not just loop-prevention — it encodes the idea that **we only move a value when moving it makes progress** (its destination doesn't already have it).
- Total swaps across the entire loop is at most `n`, so despite the nested `while`, overall time is `O(n)`.
- Same **Cyclic Sort** pattern applies to: Find All Duplicates, Find Missing Numbers, Set Mismatch, Find the Duplicate Number.

---

## ⚠️ Pitfalls
> [!warning]
> - Using `if` instead of `while` — misses chained placements and produces wrong answers.
> - Forgetting the duplicate guard `nums[i] != nums[nums[i]-1]` — causes an infinite swap loop on arrays like `[1,1]`.
> - Off-by-one: value `v` maps to index `v-1`, not index `v`.

---

## ⏱️ Complexity
- **Time:** `O(n)` — each element is swapped at most once to its final position.
- **Space:** `O(1)` — placement is done in-place; no auxiliary data structures.
