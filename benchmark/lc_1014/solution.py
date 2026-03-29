from typing import List

class Solution:
    def maxScoreSightseeingPair(self, values: List[int]) -> int:
        max_i_val = values[0]
        max_score = 0
        
        for j in range(1, len(values)):
            score = max_i_val + values[j] - j
            if score > max_score:
                max_score = score
            
            i_val = values[j] + j
            if i_val > max_i_val:
                max_i_val = i_val
                
        return max_score
