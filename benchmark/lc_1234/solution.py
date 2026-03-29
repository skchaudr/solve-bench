import collections

class Solution:
    def balancedString(self, s: str) -> int:
        n = len(s)
        target = n // 4
        counts = collections.Counter(s)
        
        if all(counts[c] <= target for c in "QWER"):
            return 0
            
        ans = n
        left = 0
        for right, char in enumerate(s):
            counts[char] -= 1
            while left <= right and all(counts[c] <= target for c in "QWER"):
                ans = min(ans, right - left + 1)
                counts[s[left]] += 1
                left += 1
                
        return ans
