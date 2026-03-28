class Solution:
    def lastStoneWeightII(self, stones: list[int]) -> int:
        dp = 1
        for stone in stones:
            dp |= dp << stone

        total_sum = sum(stones)
        target = total_sum // 2

        for i in range(target, -1, -1):
            if (dp >> i) & 1:
                return total_sum - 2 * i

        return 0
