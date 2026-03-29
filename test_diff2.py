import random

def longestArithSeqLength(nums):
    min_val, max_val = min(nums), max(nums)
    ans = 1
    for diff in range(min_val - max_val, max_val - min_val + 1):
        dp = [0] * (max_val + 1)
        for x in nums:
            prev = x - diff
            if 0 <= prev <= max_val:
                dp[x] = max(dp[x], dp[prev] + 1)
            else:
                dp[x] = max(dp[x], 1)
            if dp[x] > ans:
                ans = dp[x]
    return ans

print(longestArithSeqLength([3,6,9,12]))
print(longestArithSeqLength([9,4,7,2,10]))
print(longestArithSeqLength([20,1,15,3,10,5,8]))

nums = [random.randint(0, 500) for _ in range(1000)]
print(longestArithSeqLength(nums))

