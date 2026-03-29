import random

def solve_fixed_diff(nums):
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

def solve_n2(nums):
    dp = [{} for _ in range(len(nums))]
    ans = 0
    for i in range(len(nums)):
        for j in range(i):
            diff = nums[i] - nums[j]
            dp[i][diff] = dp[j].get(diff, 1) + 1
            ans = max(ans, dp[i][diff])
    return ans if ans > 0 else 1

for _ in range(100):
    nums = [random.randint(0, 50) for _ in range(100)]
    ans1 = solve_fixed_diff(nums)
    ans2 = solve_n2(nums)
    if ans1 != ans2:
        print(f"MISMATCH! nums={nums}, ans1={ans1}, ans2={ans2}")
        break
else:
    print("ALL MATCH!")
