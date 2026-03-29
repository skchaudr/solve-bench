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
            print(f"DECREASE! nums={nums}, diff={diff}, x={x}, old={dp[x]}, new={new_val}")
            return False
            
        dp[x] = new_val
        if dp[x] > ans:
            ans = dp[x]
    return ans

for _ in range(10000):
    nums = [random.randint(0, 20) for _ in range(30)]
    diff = random.randint(-10, 10)
    res = solve_dp(nums, diff)
    if res is False:
        break
else:
    print("NO DECREASE EVER!")
