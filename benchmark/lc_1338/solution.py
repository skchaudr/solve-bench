class Solution:
    def minSetSize(self, arr: list[int]) -> int:
        from collections import Counter
        counts = Counter(arr)
        
        freqs = sorted(counts.values(), reverse=True)
        
        removed = 0
        set_size = 0
        half = len(arr) // 2
        
        for f in freqs:
            removed += f
            set_size += 1
            if removed >= half:
                break
                
        return set_size
