
Suppose there are three buckets
ones
twos
threes

nums[i] will go to ones if not in twos.
nums[i] will go to twos if present in ones.
nums[i] will go to threes if it is present in twos.

example nums = [2,2,2,3]

    public static int singleNumber(int[] nums) {
        int ones = 0, twos = 0;
        for (int num : nums) {
            ones = (ones ^ num) & ~twos; // 00
            twos = (twos ^ num) & ~ones; // 11
        }
        return ones;
    }


in the first iteration 2 