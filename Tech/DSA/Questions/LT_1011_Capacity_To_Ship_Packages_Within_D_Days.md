---
created: 2026-08-02 11:35
tags:
  - dsa
  - binary-search
  - binary-search-on-answer
  - arrays
  - greedy
source: https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/
problem_id: "1011"
difficulty: Medium
status: Solved
review_date:
---
# LT_1011 – Capacity To Ship Packages Within D Days

**Link:** [Open Problem](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)

---

## 📝 Problem Description
> [!info]
> A conveyor belt has packages that must be shipped from one port to another within `days` days.
>
> The `i`-th package on the conveyor belt has a weight of `weights[i]`. Each day, we load the ship with packages on the conveyor belt (**in the order given by** `weights`). We may not load more weight than the maximum weight capacity of the ship.
>
> Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within `days` days.

---

## 🧪 Examples
> [!example]
> **Input:** `weights = [1,2,3,4,5,6,7,8,9,10], days = 5`
> **Output:** `15`
> **Explanation:** A ship capacity of `15` is the minimum to ship all the packages in `5` days like this:
> ```
> 1st day: 1, 2, 3, 4, 5
> 2nd day: 6, 7
> 3rd day: 8
> 4th day: 9
> 5th day: 10
> ```
> Note that the cargo must be shipped in the given order, so using a ship of capacity `14` and splitting the packages into parts like `(2,3,4,5), (1,6,7), (8), (9), (10)` is not allowed.

> [!example]
> **Input:** `weights = [3,2,2,4,1,4], days = 3`
> **Output:** `6`
> **Explanation:** A ship capacity of `6` is the minimum to ship all the packages in `3` days like this:
> ```
> 1st day: 3, 2
> 2nd day: 2, 4
> 3rd day: 1, 4
> ```

> [!example]
> **Input:** `weights = [1,2,3,1,1], days = 4`
> **Output:** `3`
> **Explanation:**
> ```
> 1st day: 1
> 2nd day: 2
> 3rd day: 3
> 4th day: 1, 1
> ```

---

## ⚠️ Constraints
> [!warning]
> - `1 <= days <= weights.length <= 5 * 10^4`
> - `1 <= weights[i] <= 500`

---

## 🔍 Intuition

This isn't a searching-an-array problem — the array is fixed and I'm searching for a **number that isn't in it**. The unlock is noticing the answer space is *monotonic*: if capacity `C` can ship everything within `days`, then so can `C + 1`, `C + 2`, and everything above. Feasibility flips from `false` to `true` exactly once as capacity increases, which means the answer space looks like `F F F F T T T T` — and finding the first `T` in a monotone boolean sequence is textbook binary search.

So I binary search over the **answer range**, not the array. The lower bound is `1` (any capacity below the heaviest package is infeasible anyway, and the validity check catches that) and the upper bound is `sum(weights)` — one giant day that carries everything, which is trivially feasible. Then the only remaining question is: given a fixed capacity, how many days do I need? That's a **greedy count**: walk the packages in order and keep loading until the next one would overflow, then start a new day. Greedy is optimal here because the order is locked — deferring a package that still fits can never reduce the day count, it can only push more work later.

Brute-forcing every capacity from `max(weights)` up to `sum(weights)` would be `O(sum · n)` — with sums up to `2.5 × 10^7` that's far too slow. Binary search cuts the capacity dimension to `log(sum)`, leaving `O(n log sum)`.

> 🟢 *Binary Search on the Answer + Greedy Feasibility Check*

---

## 🧠 Evolution of Solutions

### ✅ Solution — Binary Search on Answer with Greedy Validation

**Why this works:**

- **Monotonic predicate.** `isConditionValid(weights, C, days)` is monotone in `C`: once true, it stays true for every larger capacity. That's the *only* precondition binary search on the answer needs — no sorting of `weights` is involved or required.
- **The greedy day-count is optimal.** Since packages must ship in the given order, the best strategy for a fixed capacity is "fit as many as possible today". Any schedule that stops a day early is dominated by the greedy one, so the greedy count is the *minimum* days achievable at that capacity.
- **The bounds bracket the answer.** `hi = sum(weights)` is always feasible (`count == 1 <= days`), and `lo = 1` is at or below the true answer. So the true answer is guaranteed inside `[lo, hi]` at the start.
- **`weight > capacity` short-circuits to `false`.** This is what makes the sloppy-looking `lo = 1` safe: any capacity smaller than the heaviest single package is rejected outright, because that package could never be loaded at all. Without this line, the loop would silently spin forever creating new days for a package that never fits.

**Dry Run** (`weights = [1,2,3,4,5,6,7,8,9,10], days = 5`):

Initial: `lo = 1`, `hi = 55` (sum), `capacity = 55`

| Iter | `lo` | `hi` | `mid` | Greedy split at capacity `mid` | days used | Valid? | Action |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 55 | 28 | `(1..7)=28`, `(8,9,10)=27` | 2 | ✅ `2 <= 5` | `capacity = 28`, `hi = 27` |
| 2 | 1 | 27 | 14 | `(1..4)=10`,`(5,6)=11`,`(7)`,`(8)`,`(9)`,`(10)` | 6 | ❌ `6 > 5` | `lo = 15` |
| 3 | 15 | 27 | 21 | `(1..6)=21`,`(7,8)=15`,`(9,10)=19` | 3 | ✅ | `capacity = 21`, `hi = 20` |
| 4 | 15 | 20 | 17 | `(1..5)=15`,`(6,7)=13`,`(8,9)=17`,`(10)` | 4 | ✅ | `capacity = 17`, `hi = 16` |
| 5 | 15 | 16 | 15 | `(1..5)=15`,`(6,7)=13`,`(8)`,`(9)`,`(10)` | 5 | ✅ `5 <= 5` | `capacity = 15`, `hi = 14` |
| — | 15 | 14 | — | `lo > hi` → exit | — | — | **return `15`** ✅ |

Iteration 2 is the interesting one: capacity `14` fails by exactly one day, which is precisely why the answer is `15` and not `14` — the first four packages sum to `10`, and adding `5` needs `15`.

```java
class Solution {
    public int shipWithinDays(int[] weights, int days) {
        int lo = 1;
        int hi = Arrays.stream(weights)
            .sorted()
            .sum();

        int capacity = hi;

        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            boolean isValid = isConditionValid(weights, mid, days);
            if (isValid) {
                capacity = Math.min (capacity, mid);
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        }

        return capacity;   
    }

    private boolean isConditionValid(int[] weights, int capacity, int days) {
        int currLoad = 0;
        int count = 1;
        for (int weight : weights) {
            if (weight > capacity) return false;
            if (currLoad + weight <= capacity) {
                currLoad += weight;
            } else {
                count++;
                currLoad = weight;
            }
        }
        return count <= days;
    }
}
```

> [!tip]
> **Two harmless redundancies worth trimming:**
> - `.sorted()` before `.sum()` does nothing — addition is order-independent — but it costs an `O(n log n)` sort. Just `Arrays.stream(weights).sum()`.
> - `capacity = Math.min(capacity, mid)` is belt-and-braces: since `hi = mid - 1` only moves left, every later valid `mid` is already smaller. A plain `capacity = mid` is equivalent. Keeping the `min` isn't wrong, and it makes the "record the best feasible answer so far" intent explicit — a reasonable habit for this template.

---

## 🔑 Key Insights

- **Recognise the shape: "minimum X such that a condition holds".** That phrasing — minimum capacity, minimum eating speed, minimum largest subarray sum — is the tell for binary-search-on-answer. Same skeleton every time: pick `[lo, hi]` bounds, write a monotone `isValid(x)`, search for the boundary.
- **The array is never sorted, and must not be.** Package *order* is part of the problem constraints (the example explicitly forbids reordering into `(2,3,4,5),(1,6,7)`). Sorting `weights` would change the answer entirely — the `.sorted()` in the stream is safe only because it feeds `.sum()` and never touches the actual array.
- **The tightest lower bound is `max(weights)`, not `1`.** Starting at `1` still works because of the `weight > capacity` guard, but `lo = max(weights)` is the semantically correct floor: you can't ship a package heavier than the ship. It saves a couple of iterations and states the invariant more honestly.
- **`count` starts at `1`, not `0`.** You're already on day one before loading anything. Starting at `0` under-counts by exactly one day and returns an answer that's too small.

---

## ⚠️ Pitfalls
> [!warning]
> - **Dropping the `weight > capacity` check while keeping `lo = 1`.** Then a package heavier than `capacity` never fits in the `if`, so the else-branch fires, `currLoad = weight` (still over capacity), and the count inflates on a schedule that is physically impossible — you'd get a wrong `false` for the right reason by luck, or a wrong answer if the counting is written differently. Either keep the guard or set `lo = max(weights)`.
> - **Initialising `count = 0`.** Off-by-one on the day count propagates straight into an off-by-one final answer.
> - **`currLoad = weight` vs `currLoad = 0` when starting a new day.** The overflowing package must be *carried into* the new day, not dropped. Setting `currLoad = 0` silently ships that package for free.
> - **Overflow on `hi`.** Fine here — max sum is `5×10^4 × 500 = 2.5×10^7`, well inside `int` — but on variants with larger weights, `sum` needs `long`.

---

## ⏱️ Complexity
- **Time:** `O(n log S)` where `S = sum(weights)` — `O(log S)` binary search iterations, each running an `O(n)` greedy scan. The stray `.sorted()` adds a one-off `O(n log n)`.
- **Space:** `O(1)` for the algorithm itself; `Arrays.stream(...).sorted()` allocates an `O(n)` buffer internally (another reason to drop it).

---

## 💡 Mental Model

```
Don't search the array — search the ANSWER.

Capacity:   1  2  3 ... 14 | 15 16 17 ... 55
Feasible?   F  F  F ...  F |  T  T  T ...  T
                           ↑
                     find this boundary

isValid(C): walk packages in order, greedily fill each day,
            count days, return count <= days.
            Monotone in C → binary search applies.

Valid   → this capacity works, try smaller  (hi = mid - 1, record it)
Invalid → too small, need bigger            (lo = mid + 1)
```

Same template as *Koko Eating Bananas* (`875`) and *Split Array Largest Sum* (`410`) — only `isValid` changes.
