---
created: 2026-08-06 00:00
tags:
  - dsa
  - dynamic-programming
  - binary-search
  - sorting
  - arrays
source: https://leetcode.com/problems/russian-doll-envelopes/
problem_id: "354"
difficulty: Hard
status: Solved
review_date:
---
# LT_0354 – Russian Doll Envelopes

**Link:** [Open Problem](https://leetcode.com/problems/russian-doll-envelopes/)

---

## 📝 Problem Description
> [!info]
> You are given a 2D array of integers `envelopes` where `envelopes[i] = [wi, hi]` represents the width and the height of an envelope.
>
> One envelope can fit into another if and only if both the width and height of one envelope are **greater than** the other envelope's width and height (both strict).
>
> Return the maximum number of envelopes you can Russian doll (i.e., put one inside the other).
>
> **Note:** You cannot rotate an envelope.

---

## 🧪 Examples
> [!example]
> **Input:** `envelopes = [[5,4],[6,4],[6,7],[2,3]]`
> **Output:** `3`
> **Explanation:** The maximum number of envelopes you can Russian doll is `3` (`[2,3] => [5,4] => [6,7]`).

> [!example]
> **Input:** `envelopes = [[1,1],[1,1],[1,1]]`
> **Output:** `1`
> **Explanation:** Every envelope is identical, so none can strictly fit inside another.

---

## ⚠️ Constraints
> [!warning]
> - `1 <= envelopes.length <= 10^5`
> - `envelopes[i].length == 2`
> - `1 <= wi, hi <= 10^5`

---

## 🔍 Intuition

This is Longest Increasing Subsequence wearing a disguise — the trick is entirely in how you *sort* before you ever touch LIS. If widths were strictly distinct, sorting by width would immediately reduce the problem to "find the LIS of the heights," since width order is already guaranteed increasing left-to-right. The hard part is envelopes that **tie on width**: they can never nest in each other (`w < w` is false), but a naive ascending sort by height would let LIS wrongly chain several same-width envelopes together, since LIS only looks at the height sequence and has no idea two entries share a width. The fix is to sort ties **by height descending** — this "poisons" the height sequence for same-width groups so it's strictly decreasing there, and LIS (which only extends on strictly increasing values) can never pick more than one envelope per width. Once the sort enforces that invariant, `O(n log n)` patience-sorting LIS on the height column alone gives the answer.

> 🟢 *Sort trick (asc width, desc height on ties) + Patience Sorting LIS on heights*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Sort (asc width, desc height tie-break) + LIS via Binary Search (Patience Sorting)

**Why this works:**
- Sorting by width ascending means any valid nesting chain automatically has non-decreasing width as you scan left to right — the width constraint is handled by sort order, not by LIS logic.
- Sorting same-width groups by **height descending** turns them into a strictly decreasing run in the height array. LIS can only extend on strictly increasing values, so it is structurally incapable of selecting two envelopes from the same width group — this is what makes the strict `w < w` requirement hold.
- With width fully handled by sort order, "longest chain with strictly increasing width AND height" collapses to "longest strictly increasing subsequence of the height column" — solved with the standard `O(n log n)` patience-sorting/binary-search LIS.
- The binary search finds the **lower bound** — the first index where `tail[index] >= num`. If that index equals `tail.size()`, every existing tail is smaller than `num`, so `num` extends the sequence (`append`); otherwise `num` can tighten an existing tail to a smaller value at that index (`replace`), which keeps future extensions easier without changing the LIS length found so far.

**Dry Run** (`envelopes = [[5,4],[6,4],[6,7],[2,3]]`):

Sort ascending by width, descending by height on ties:

| Envelope | Width | Height |
|---|---|---|
| `[2,3]` | 2 | 3 |
| `[5,4]` | 5 | 4 |
| `[6,7]` | 6 | 7 |
| `[6,4]` | 6 | 4 |

(Width `6` ties → height sorted descending: `7` before `4`.)

Height sequence fed to LIS: `[3, 4, 7, 4]`

| `num` | Binary search result | Action | `tail` after |
|---|---|---|---|
| `3` | `left = 0 = tail.size()` | append | `[3]` |
| `4` | `left = 1 = tail.size()` | append | `[3, 4]` |
| `7` | `left = 2 = tail.size()` | append | `[3, 4, 7]` |
| `4` | `left = 1` (first `>= 4` is `tail[1]=4`) | replace `tail[1]` with `4` (no-op) | `[3, 4, 7]` |

`tail.size() = 3` → matches the answer `3` (`[2,3] → [5,4] → [6,7]`).

```java
class Solution {
    public int maxEnvelopes(int[][] envelopes) {
        /*
        1  4
        2  2
        3  3
        4  4
        5  7
        5  6
        5  5
        6  9
        */
        Arrays.sort(envelopes, (a,b) -> {
            if (a[0]==b[0]) {
                return b[1] - a[1];
            } else {
                return a[0] - b[0];
            }
        });

        return lis(envelopes);

    }

    private int lis (int[][] nums) {
        int row = nums.length;
        int col = nums[0].length;
        List<Integer> tail = new ArrayList<>();

        for (int i=0; i<row; i++) {
            int num = nums[i][col-1];
            int left = 0;
            int right = tail.size();

            while (left < right) {
                int mid = left + (right - left)/2;
                if (tail.get(mid) < num) {
                    left = mid + 1;
                } else {
                    right = mid;
                }
            }

            if (left==tail.size()) {
                tail.add(num);
            } else {
                tail.set(left, num);
            }
        }

        return tail.size();
    }
}
```

---

## 🔑 Key Insights
- **The sort does the width work; LIS only ever sees heights.** Once sorted `(asc width, desc height on ties)`, "strictly increasing width and height" reduces to "strictly increasing height" — a pure LIS problem.
- **Descending tie-break is the whole trick.** It converts same-width groups into strictly decreasing runs, which LIS structurally cannot chain through, enforcing the strict `<` on width without LIS needing to know widths exist at all.
- **The binary search returns an insertion *position*, not a value.** `left == tail.size()` means "every current tail is smaller" → append (sequence grows). Any other `left` means "found the first tail `>= num`" → replace at that index (tighten, length unchanged).
- **`tail` is not an actual valid envelope chain** — like in plain LIS, its contents mix values from different candidate subsequences. Only its length is meaningful; reconstructing the actual chain needs parent pointers.

---

## ⚠️ Pitfalls
> [!warning]
> - **Ascending height on ties is the classic wrong answer.** It lets LIS pick multiple envelopes of the same width (e.g. heights `4,5,6` all same width look "increasing" to LIS but none can actually nest), silently inflating the result.
> - **Comparator overflow.** `a[0]-b[0]` / `b[1]-a[1]` is safe here since `wi, hi <= 10^5`, but it's a habit worth flagging — with larger constraints, prefer `Integer.compare(...)` to avoid subtraction overflow.
> - **Off-by-one on the binary search boundary.** The loop invariant is "first index where `tail[mid] >= num`" (lower bound) — using `<=` instead of `<` in the comparison would turn this into an upper bound and silently break strictness (would solve the non-decreasing variant instead).

---

## ⏱️ Complexity
- **Time:** `O(n log n)` — sorting is `O(n log n)`, and the binary-search LIS pass is `O(n log n)`.
- **Space:** `O(n)` — for the sort and the `tail` list (`O(log n)` extra for `Arrays.sort` on objects, plus `O(n)` for `tail` in the worst case).
