import random
import time

def longestArithSeqLength(nums):
    min_val, max_val = min(nums), max(nums)
    ans = 1
    # optimize array allocation
    for diff in range(min_val - max_val, max_val - min_val + 1):
        dp = [0] * (max_val + 1)
        for x in nums:
            prev = x - diff
            if 0 <= prev <= max_val:
                dp[x] = dp[prev] + 1
            else:
                dp[x] = 1
            if dp[x] > ans:
                ans = dp[x]
    return ans

nums = [random.randint(0, 500) for _ in range(100000)]
start = time.time()
print(longestArithSeqLength(nums))
print("Time taken:", time.time() - start)
