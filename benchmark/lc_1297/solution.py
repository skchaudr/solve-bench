class Solution:
    def maxFreq(self, s: str, maxLetters: int, minSize: int, maxSize: int) -> int:
        counts = {}
        max_freq = 0
        
        for i in range(len(s) - minSize + 1):
            sub = s[i:i+minSize]
            if len(set(sub)) <= maxLetters:
                counts[sub] = counts.get(sub, 0) + 1
                if counts[sub] > max_freq:
                    max_freq = counts[sub]
                    
        return max_freq
