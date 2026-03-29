import random

def solve_dp(nums, diff):
    dp = {}
    ans = 0
    for x in nums:
        if x - diff in dp:
            new_val = dp[x - diff] + 1
        else:
            new_val = 1
        
        if x in dp and new_val < dp[x]:
            pass
            
        # We can just use max to be safe!
        dp[x] = max(dp.get(x, 0), new_val)
        if dp[x] > ans:
            ans = dp[x]
    return ans

def solve_n2(nums, diff):
    dp = [{} for _ in range(len(nums))]
    ans = 0
    for i in range(len(nums)):
        dp[i][diff] = 1
        for j in range(i):
            if nums[i] - nums[j] == diff:
                dp[i][diff] = max(dp[i][diff], dp[j][diff] + 1)
        ans = max(ans, dp[i][diff])
    return ans

for _ in range(10000):
    nums = [random.randint(0, 20) for _ in range(30)]
    diff = random.randint(-10, 10)
    ans1 = solve_dp(nums, diff)
    ans2 = solve_n2(nums, diff)
    if ans1 != ans2:
        print(f"MISMATCH! nums={nums}, diff={diff}, ans1={ans1}, ans2={ans2}")
        break
else:
    print("ALL MATCH WITH MAX!")
