class Solution:
    def numTilePossibilities(self, tiles: str) -> int:
        from collections import Counter
        
        counts = Counter(tiles)
        
        def backtrack():
            total = 0
            for char in counts:
                if counts[char] > 0:
                    total += 1
                    counts[char] -= 1
                    total += backtrack()
                    counts[char] += 1
            return total
            
        return backtrack()
