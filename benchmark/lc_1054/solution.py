from collections import Counter
import heapq
from typing import List

class Solution:
    def rearrangeBarcodes(self, barcodes: List[int]) -> List[int]:
        if not barcodes:
            return []
        
        freq = Counter(barcodes)
        max_heap = [[-count, val] for val, count in freq.items()]
        heapq.heapify(max_heap)
        
        res = []
        while len(max_heap) >= 2:
            count1, val1 = heapq.heappop(max_heap)
            count2, val2 = heapq.heappop(max_heap)
            
            res.append(val1)
            res.append(val2)
            
            if count1 + 1 < 0:
                heapq.heappush(max_heap, [count1 + 1, val1])
            if count2 + 1 < 0:
                heapq.heappush(max_heap, [count2 + 1, val2])
                
        if max_heap:
            res.append(max_heap[0][1])
            
        return res
