from typing import List

class Solution:
    def maxSumTwoNoOverlap(self, nums: List[int], firstLen: int, secondLen: int) -> int:
        def helper(L: int, M: int) -> int:
            sumL = 0
            for i in range(L):
                sumL += nums[i]
                
            sumM = 0
            for i in range(L, L + M):
                sumM += nums[i]
                
            maxL = sumL
            ans = maxL + sumM
            
            for i in range(L + M, len(nums)):
                sumL += nums[i - M] - nums[i - M - L]
                maxL = max(maxL, sumL)
                
                sumM += nums[i] - nums[i - M]
                ans = max(ans, maxL + sumM)
                
            return ans

        return max(helper(firstLen, secondLen), helper(secondLen, firstLen))
