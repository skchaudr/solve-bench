import heapq
from typing import List

class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        # Sort trips by start location
        trips.sort(key=lambda x: x[1])
        
        # Min-heap to store the drop-off locations and passenger counts of currently active trips
        # Format: (end_location, num_passengers)
        min_heap = []
        
        current_passengers = 0
        
        for num_passengers, start, end in trips:
            # Remove all trips that have ended before or at the start of the current trip
            while min_heap and min_heap[0][0] <= start:
                current_passengers -= heapq.heappop(min_heap)[1]
            
            # Add current trip's passengers
            current_passengers += num_passengers
            
            # If current capacity exceeds maximum capacity, return False
            if current_passengers > capacity:
                return False
                
            # Add current trip to the heap
            heapq.heappush(min_heap, (end, num_passengers))
            
        return True
