from typing import List

class Solution:
    def camelMatch(self, queries: List[str], pattern: str) -> List[bool]:
        res = []
        for query in queries:
            p = 0
            match = True
            for char in query:
                if p < len(pattern) and char == pattern[p]:
                    p += 1
                elif char.isupper():
                    match = False
                    break
            if match and p == len(pattern):
                res.append(True)
            else:
                res.append(False)
        return res
