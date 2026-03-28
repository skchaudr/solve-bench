import heapq
from typing import List

class Solution:
    def findDiagonalOrder(self, nums: List[List[int]]) -> List[int]:
        heap = []
        for i, row in enumerate(nums):
            for j, val in enumerate(row):
                heap.append((i + j, -i, val))

        heapq.heapify(heap)

        ans = []
        while heap:
            ans.append(heapq.heappop(heap)[2])

        return ans
