from typing import List

class Solution:
    def numberOfSubarrays(self, nums: List[int], k: int) -> int:
        def atMost(k: int) -> int:
            if k < 0:
                return 0
            ans = 0
            left = 0
            for right in range(len(nums)):
                k -= nums[right] % 2
                while k < 0:
                    k += nums[left] % 2
                    left += 1
                ans += right - left + 1
            return ans
        
        return atMost(k) - atMost(k - 1)
