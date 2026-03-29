class Solution:
    def maxUniqueSplit(self, s: str) -> int:
        max_count = 0
        seen = set()

        def backtrack(start, count):
            nonlocal max_count
            if count + (len(s) - start) <= max_count:
                return
            
            if start == len(s):
                max_count = max(max_count, count)
                return
            
            for end in range(start + 1, len(s) + 1):
                sub = s[start:end]
                if sub not in seen:
                    seen.add(sub)
                    backtrack(end, count + 1)
                    seen.remove(sub)

        backtrack(0, 0)
        return max_count
