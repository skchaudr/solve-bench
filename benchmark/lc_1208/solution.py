class Solution:
    def equalSubstring(self, s: str, t: str, maxCost: int) -> int:
        n = len(s)
        left = 0
        current_cost = 0
        max_len = 0
        
        for right in range(n):
            current_cost += abs(ord(s[right]) - ord(t[right]))
            
            while current_cost > maxCost and left <= right:
                current_cost -= abs(ord(s[left]) - ord(t[left]))
                left += 1
                
            if right - left + 1 > max_len:
                max_len = right - left + 1
                
        return max_len
