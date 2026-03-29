from collections import defaultdict
from bisect import bisect_left
from typing import List

class Solution:
    def maxUncrossedLines(self, nums1: List[int], nums2: List[int]) -> int:
        positions = defaultdict(list)
        for i, num in enumerate(nums2):
            positions[num].append(i)
        
        sub = []
        for num in nums1:
            for idx in reversed(positions[num]):
                pos = bisect_left(sub, idx)
                if pos == len(sub):
                    sub.append(idx)
                else:
                    sub[pos] = idx
        return len(sub)
