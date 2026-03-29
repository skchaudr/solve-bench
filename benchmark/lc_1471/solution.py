from typing import List

class Solution:
    def getStrongest(self, arr: List[int], k: int) -> List[int]:
        # Sort the array to find the median
        arr.sort()
        n = len(arr)
        median = arr[(n - 1) // 2]
        
        # Use two pointers to find the strongest values
        left = 0
        right = n - 1
        result = []
        
        for _ in range(k):
            # Compare the elements at left and right pointers
            left_diff = abs(arr[left] - median)
            right_diff = abs(arr[right] - median)
            
            if right_diff > left_diff:
                result.append(arr[right])
                right -= 1
            elif left_diff > right_diff:
                result.append(arr[left])
                left += 1
            else:
                # If absolute differences are equal, the larger element is stronger
                # Since the array is sorted, arr[right] is always >= arr[left]
                result.append(arr[right])
                right -= 1
                
        return result
