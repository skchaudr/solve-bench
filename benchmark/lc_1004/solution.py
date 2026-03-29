from typing import List

class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        left = 0
        for right in range(len(nums)):
            # If we see a 0, we use one of our allowed flips
            k -= 1 - nums[right]
            
            # If we've used more flips than allowed, we need to slide the window forward
            if k < 0:
                # If the element sliding out of the window was a 0, we get a flip back
                k += 1 - nums[left]
                left += 1
                
        # The window size (right - left + 1) never shrinks, so its final size is the maximum
        return len(nums) - left
