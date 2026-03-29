from collections import Counter

class Solution:
    def longestArithSeqLength(self, nums: list[int]) -> int:
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
