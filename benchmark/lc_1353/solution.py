from typing import List
import heapq

class Solution:
    def maxEvents(self, events: List[List[int]]) -> int:
        events.sort(key=lambda x: x[0])
        heap = []
        n = len(events)
        idx = 0
        d = 0
        ans = 0
        
        while idx < n or heap:
            if not heap and idx < n and d < events[idx][0]:
                d = events[idx][0]
            
            while idx < n and events[idx][0] == d:
                heapq.heappush(heap, events[idx][1])
                idx += 1
                
            while heap and heap[0] < d:
                heapq.heappop(heap)
                
            if heap:
                heapq.heappop(heap)
                ans += 1
            
            d += 1
            
        return ans
