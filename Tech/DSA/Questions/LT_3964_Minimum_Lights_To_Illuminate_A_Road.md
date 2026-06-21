---
created: 2026-06-21 00:00
tags:
  - dsa
  - array
  - greedy
  - prefix-sum
  - difference-array
source: https://leetcode.com/problems/minimum-lights-to-illuminate-a-road/
problem_id: "3964"
difficulty: Medium
status: Solved
review_date:
---
# LT_3964 – Minimum Lights To Illuminate A Road

**Link:** [Open Problem](https://leetcode.com/problems/minimum-lights-to-illuminate-a-road/)

---

## 📝 Problem Description
> [!info]
> You are given a 0-indexed integer array `lights` of length `n`. If `lights[i] != 0`, a working bulb exists at position `i` that illuminates every position in `[max(0, i - lights[i]), min(n-1, i + lights[i])]`, inclusive. A position is **visible** if illuminated by at least one working bulb.
>
> You may install additional bulbs at any positions. Each additional bulb installed at position `j` illuminates `[max(0, j-1), min(n-1, j+1)]` (range = 1), inclusive.
>
> Return the **minimum number of additional bulbs** required to make every position on the road visible.

---

## 🧪 Examples
> [!example]
> **Input:** `lights = [0, 0, 0, 0]`
> **Output:** `2`
> **Explanation:** Place a bulb at index 1 (covers [0,2]) and index 3 (covers [2,3]). All 4 positions lit with 2 extra bulbs.

> [!example]
> **Input:** `lights = [0, 0, 0, 2, 0]`
> **Output:** `1`
> **Explanation:** Existing bulb at index 3 with range 2 covers [1,4]. Only index 0 is dark — one extra bulb at index 0 covers [0,1].

---

## ⚠️ Constraints
> [!warning]
> - `1 <= lights.length <= 10^5`
> - `0 <= lights[i] <= 10^5`

---

## 🔍 Intuition

The problem splits cleanly into two phases: first figure out which cells are already lit by existing bulbs, then greedily plug the dark gaps with minimum extra bulbs. For phase 1, naively marking each cell in `[i-val, i+val]` costs O(val) per bulb — O(n²) in the worst case when ranges are large. The fix is a **difference array**: record only the range boundaries (`diff[start]++`, `diff[end+1]--`) in O(1) per bulb, then a single prefix-sum sweep reconstructs full coverage in O(n) total. For phase 2, whenever I hit a dark cell at index `i`, I place the new bulb as far right as possible — at `i+1` if that's also dark (covering `[i, i+2]`), otherwise at `i` (covering `[i-1, i+1]`) — the classic greedy "jump as far as you can" trick that minimises the number of bulbs needed.

> 🟢 *Difference Array + Greedy Gap Filling*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Difference Array + Greedy Gap Filling

**Why this works:**
- Difference array turns O(n·val) range marking into O(n) total — a prefix sum at a single index represents "number of overlapping ranges covering this cell"
- `running` (the prefix sum) can never go negative because every `diff[end+1]--` is preceded by a `diff[start]++` at an earlier index, so the books always balance
- Greedy placement at the rightmost possible position when a gap starts maximises the number of future cells covered by each new unit-range bulb

**Dry Run** (`lights = [0, 0, 0, 2, 0]`):

**Phase 1 — Difference Array:**

| i | val | start | end | diff update |
|---|-----|-------|-----|-------------|
| 0 | 0   | —     | —   | skip        |
| 1 | 0   | —     | —   | skip        |
| 2 | 0   | —     | —   | skip        |
| 3 | 2   | 1     | 4   | `diff[1]++, diff[5]--` |
| 4 | 0   | —     | —   | skip        |

`diff = [0, 1, 0, 0, 0, -1]`

**Prefix sum → illuminated:**

| i | diff[i] | running | illuminated[i] |
|---|---------|---------|----------------|
| 0 | 0       | 0       | 0 (dark)       |
| 1 | 1       | 1       | 1              |
| 2 | 0       | 1       | 1              |
| 3 | 0       | 1       | 1              |
| 4 | 0       | 1       | 1              |

`illuminated = [0, 1, 1, 1, 1]`

**Phase 2 — Greedy:**

- `i=0`: dark, next cell `illuminated[1]=1` → place at `i=0`, `updateIlluminated(illuminated, 0, 1)` marks [0,1]; `bulbs=1`
- `i=1..4`: all lit, skip

**Return 1** ✓

```java
class Solution {
    public int minLights(int[] lights) {
        int len = lights.length;
        int[] diff = new int[len + 1];

        // O(1) per light instead of O(val) per light
        for (int i = 0; i < len; i++) {
            int val = lights[i];
            if (val > 0) {
                int start = Math.max(0, i - val);
                int end = Math.min(len - 1, i + val);
                diff[start]++;
                diff[end + 1]--;
            }
        }

        // prefix sum -> O(n) total to build the illuminated array
        int[] illuminated = new int[len];
        int running = 0;
        for (int i = 0; i < len; i++) {
            running += diff[i];
            illuminated[i] = running > 0 ? 1 : 0;
        }

        // unchanged: already O(n), since val is always 1 here
        int bulbs = 0;
        int i = 0;
        while (i < len) {
            int val = illuminated[i];
            if (val == 0) {
                if (i + 1 < len && illuminated[i + 1] == 0) {
                    updateIlluminated(illuminated, i + 1, 1);
                } else {
                    updateIlluminated(illuminated, i, 1);
                }
                bulbs++;
            }
            i++;
        }

        return bulbs;
    }

    private void updateIlluminated(int[] illuminated, int idx, int val) {
        int len = illuminated.length;
        for (int j = idx - val; j <= idx + val; j++) {
            if (j >= 0 && j < len) {
                illuminated[j] = 1;
            }
        }
    }
}
```

---

## 🔑 Key Insights
- `diff[i]` can be arbitrarily negative (e.g. `-n`) when many ranges end at the same boundary — that is intentional; `running` (the prefix sum) is always ≥ 0 because every decrement has a prior matching increment
- `diff` must be of size `len+1`, not `len` — `diff[end+1]` is written when `end = len-1`, accessing index `len`
- `updateIlluminated` with `val=1` always touches exactly 3 indices (O(1)) — no inner-loop explosion despite looking like nested iteration
- The greedy "look one ahead" rule: placing at `i+1` when both `i` and `i+1` are dark extends coverage one extra cell forward compared to placing at `i`

---

## ⚠️ Pitfalls
> [!warning]
> - Forgetting to clamp `start = max(0, i-val)` and `end = min(len-1, i+val)` — raw indices go out of bounds for bulbs near the array edges
> - Allocating `diff` with size `len` instead of `len+1` — causes `ArrayIndexOutOfBoundsException` when writing `diff[end+1]` at the last position
> - Skipping the "look ahead" check in the greedy: always placing at `i` (not `i+1` when the next cell is also dark) wastes coverage and can yield a non-minimal answer

---

## ⏱️ Complexity
- **Time:** `O(n)` — O(n) difference array setup + O(n) prefix sum + O(n) greedy scan with O(1) updates
- **Space:** `O(n)` — `diff[n+1]` and `illuminated[n]` auxiliary arrays
