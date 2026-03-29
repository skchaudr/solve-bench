from typing import List

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
            
        phone_map = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
        }
        res = []
        path = []
        
        def backtrack(index: int):
            if index == len(digits):
                res.append("".join(path))
                return
            
            for letter in phone_map[digits[index]]:
                path.append(letter)
                backtrack(index + 1)
                path.pop()
                
        backtrack(0)
        return res
