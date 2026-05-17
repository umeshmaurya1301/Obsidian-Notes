---
created: 2026-05-07 00:36
tags:
  - Arrays
  - HashMap
  - TwoSumPattern
  - Counting
source: https://leetcode.com/problems/count-good-meals/
problem_id: "1711"
difficulty: Medium
status: Completed
review_date:
---

# LT_1711 – Count Good Meals

**Link:** [Open Problem](https://leetcode.com/problems/count-good-meals/)

---

## 📝 Problem Description
> [!info]
> A **good meal** is a pair of food items whose deliciousness values sum to a power of two.
>
> Given an array `deliciousness`, return the number of different good meals.
>
> Since the answer can be very large, return it modulo `10^9 + 7`.

---

## 🧪 Examples
> [!example]
> **Input:** `[1,3,5,7,9]`  
> **Output:** `4`
>
> **Explanation:**  
> Good pairs are:
>
> - `(1,3)` → `4`
> - `(1,7)` → `8`
> - `(3,5)` → `8`
> - `(7,9)` → `16`

---

## ⚠️ Constraints
> [!warning]
> - `1 ≤ deliciousness.length ≤ 10^5`
> - `0 ≤ deliciousness[i] ≤ 2^20`

---

# 💡 Solutions

## 🟢 Approach 1: HashMap + Power of Two Enumeration

### 🔍 Intuition

Brute force would try every pair:

```java
for(i)
   for(j)
```

which becomes:

```text
O(N²)
```

Too slow for `10^5`.

---

Instead of checking:

```text
a + b == powerOfTwo
```

we reverse the thinking.

For every number `n`:
- try every possible power of two
- calculate which number is needed

Formula:

```text
required = power - n
```

If `required` already exists,
then we found valid pairs.

We use a `HashMap`:

```text
number -> frequency
```

to quickly know:
- how many times `required` appeared earlier.

---

## 🧠 Why Only Till 2^21 ?

Constraint says:

```text
deliciousness[i] ≤ 2^20
```

Maximum possible sum:

```text
2^20 + 2^20 = 2^21
```

So only these sums matter:

```text
1,2,4,8,16,...,2^21
```

Only 22 values.

---

# 🪟 Dry Run

## Input

```text
[1,3,5,7,9]
```

---

## Initial State

```text
map = {}
count = 0
```

---

## Step 1 → n = 1

Try all powers:

| power | required |
|---|---|
| 1 | 0 |
| 2 | 1 |
| 4 | 3 |
| 8 | 7 |

Nothing exists yet.

Insert current number:

```text
map = {1:1}
count = 0
```

---

## Step 2 → n = 3

Check powers.

For power = 4:

```text
required = 4 - 3 = 1
```

`1` already exists.

Valid pair:

```text
(1,3)
```

```text
count = 1
```

Insert:

```text
map = {1:1, 3:1}
```

---

## Step 3 → n = 5

For power = 8:

```text
required = 8 - 5 = 3
```

Found.

```text
(3,5)
count = 2
```

Insert:

```text
map = {1:1, 3:1, 5:1}
```

---

## Step 4 → n = 7

For power = 8:

```text
required = 1
```

Found.

```text
(1,7)
count = 3
```

Insert:

```text
map = {1:1, 3:1, 5:1, 7:1}
```

---

## Step 5 → n = 9

For power = 16:

```text
required = 7
```

Found.

```text
(7,9)
count = 4
```

Final Answer:

```text
4
```

---

# ⚡ Important Observation

This line happens AFTER checking:

```java
map.put(n, map.getOrDefault(n, 0) + 1);
```

Why?

Because:
- we only want previous elements
- avoids double counting
- prevents invalid self pairing

---

# ✅ Java Implementation

```java
class Solution {

    public int countPairs(int[] deliciousness) {

        long count = 0;

        int MOD = 1_000_000_007;

        Map<Integer, Integer> map = new HashMap<>();

        for (int n : deliciousness) {

            int power = 1;

            for (int i = 0; i <= 21; i++) {

                int required = power - n;

                count += map.getOrDefault(required, 0);

                power = power << 1;
            }

            map.put(n, map.getOrDefault(n, 0) + 1);
        }

        return (int)(count % MOD);
    }
}
```

---

# 🔬 Code Walkthrough

## Step 1

```java
long count = 0;
```

Total valid pairs.

Using `long` because count can become large.

---

## Step 2

```java
Map<Integer, Integer> map = new HashMap<>();
```

Stores:

```text
number -> frequency
```

Example:

```text
{1=2, 3=1}
```

means:
- `1` appeared twice
- `3` appeared once

---

## Step 3

```java
for (int n : deliciousness)
```

Process every number.

---

## Step 4

```java
int power = 1;
```

Start with:

```text
2^0 = 1
```

---

## Step 5

```java
for (int i = 0; i <= 21; i++)
```

Try all powers:

```text
1,2,4,8,16...
```

---

## Step 6

```java
int required = power - n;
```

Example:

```text
n = 5
power = 8

required = 3
```

Meaning:

```text
5 + 3 = 8
```

---

## Step 7

```java
count += map.getOrDefault(required, 0);
```

If `required` already appeared:
- add all its frequencies.

Example:

```text
map = {3=2}
```

Then:

```text
5 can form 8 with both 3s
```

So:

```text
count += 2
```

---

## Step 8

```java
power = power << 1;
```

Left shift means:

```text
multiply by 2
```

Sequence becomes:

```text
1
2
4
8
16
32
...
```

Equivalent to:

```java
power *= 2;
```

---

## Step 9

```java
map.put(n, map.getOrDefault(n, 0) + 1);
```

Store current number frequency.

---

# ⏱ Complexity Analysis

## Time Complexity

Outer loop:

```text
O(N)
```

Inner loop:

```text
22 iterations
```

Total:

```text
O(N × 22)
≈ O(N)
```

---

## Space Complexity

```text
O(N)
```

for HashMap.

---

# 🧩 Pattern Recognition

This problem is a variation of:

- Two Sum
- Pair Counting
- Frequency Map

Classic Two Sum:

```text
a + b = target
```

This problem:

```text
a + b ∈ {1,2,4,8,16...}
```

So instead of one target,
we iterate over all valid targets.

---

# ⚠️ Common Pitfalls

## ❌ Using int for count

Answer can exceed integer range.

Correct:

```java
long count
```

---

## ❌ Updating map before checking

Wrong order may:
- double count
- self pair incorrectly

---

## ❌ Forgetting modulo

Return:

```java
count % MOD
```

---

# 🚀 Optimization Insight

Even though there is a nested loop,
inner loop runs only 22 times.

So runtime behaves nearly linear.

Efficient for:

```text
N = 100000
```

---

# 🧠 Mental Model

For every number:

```text
"How many previously seen numbers
can combine with me
to form a power of two?"
```

HashMap answers that instantly.