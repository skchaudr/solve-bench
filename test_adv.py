import random
import time
from collections import Counter

def longestArithSeqLength(nums):
    min_val, max_val = min(nums), max(nums)
    diff_max = max_val - min_val
    if diff_max == 0:
        return len(nums)
        
    counts = Counter(nums)
    ans = max(counts.values())
    
    for diff in range(-diff_max, diff_max + 1):
        if diff == 0: continue
        
        # Max possible length for this diff is diff_max // abs(diff) + 1
        if diff_max // abs(diff) + 1 <= ans:
            continue
            
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

# adversary: sequence of length n, where differences don't yield large ans early.
# Well, wait, if n=100000 and max_val <= 500, by Pigeonhole Principle, some number must appear at least 100000/501 ≈ 200 times.
# So `ans` will be initialized to >= 200 !
# If `ans` >= 200, then diff_max // abs(diff) + 1 <= 200 => 500 // abs(diff) < 200 => abs(diff) >= 3.
# So it will only check abs(diff) in [1, 2], which is 4 iterations!
# Let's test n=100000 with max_val=500, any array will have max count >= 200.
# So this O(N * D) with pruning is extremely fast!

