from typing import List

class Solution:
    def maxSatisfied(self, customers: List[int], grumpy: List[int], minutes: int) -> int:
        n = len(customers)
        base_satisfied = 0
        current_additional = 0
        
        # Calculate base satisfied and first window additional satisfied
        for i in range(n):
            if grumpy[i] == 0:
                base_satisfied += customers[i]
            elif i < minutes:
                current_additional += customers[i]
                
        max_additional = current_additional
        
        # Slide the window
        for i in range(minutes, n):
            # If the outgoing element from the window was grumpy, subtract it
            if grumpy[i - minutes] == 1:
                current_additional -= customers[i - minutes]
            # If the incoming element into the window is grumpy, add it
            if grumpy[i] == 1:
                current_additional += customers[i]
                
            if current_additional > max_additional:
                max_additional = current_additional
                
        return base_satisfied + max_additional
