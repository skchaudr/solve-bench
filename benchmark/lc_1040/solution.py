from typing import List

class Solution:
    def numMovesStonesII(self, stones: List[int]) -> List[int]:
        stones.sort()
        n = len(stones)
        
        # Max moves:
        # We can either leave the gap between stones[0] and stones[1],
        # or between stones[n-2] and stones[n-1], and then shift stones 
        # inward one by one. The total number of unoccupied positions 
        # in the chosen segment gives the max moves.
        max_moves = max(stones[n-1] - stones[1] - n + 2, stones[n-2] - stones[0] - n + 2)
        
        min_moves = n
        i = 0
        
        # Min moves:
        # Use a sliding window to find a window of length up to n.
        # Window represents a contiguous block of length up to n containing some stones.
        for j in range(n):
            # Window length is stones[j] - stones[i] + 1
            # We want window length <= n
            while stones[j] - stones[i] >= n:
                i += 1
                
            # If the window has n - 1 stones and the window length is exactly n - 1
            # This is a special edge case. Like 1, 2, 3, 4, 7 -> need 2 moves (7 -> 5, 1 -> 6)
            # Cannot do 1 move because endpoint stone cannot be moved to an endpoint
            if j - i + 1 == n - 1 and stones[j] - stones[i] == n - 2:
                min_moves = min(min_moves, 2)
            else:
                # Normal case: we just move all stones outside the window into the window
                min_moves = min(min_moves, n - (j - i + 1))
                
        return [min_moves, max_moves]

