class Solution:
    def shipWithinDays(self, weights: list[int], days: int) -> int:
        left, right = max(weights), sum(weights)
        
        while left < right:
            mid = (left + right) // 2
            
            current_weight = 0
            current_days = 1
            
            for weight in weights:
                if current_weight + weight > mid:
                    current_days += 1
                    current_weight = weight
                else:
                    current_weight += weight
            
            if current_days <= days:
                right = mid
            else:
                left = mid + 1
                
        return left
