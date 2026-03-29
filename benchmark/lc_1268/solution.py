from typing import List

class Solution:
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        products.sort()
        res = []
        l, r = 0, len(products) - 1
        
        for i, c in enumerate(searchWord):
            while l <= r and (len(products[l]) <= i or products[l][i] != c):
                l += 1
            while l <= r and (len(products[r]) <= i or products[r][i] != c):
                r -= 1
            
            valid_len = r - l + 1
            curr = []
            for j in range(min(3, valid_len)):
                curr.append(products[l + j])
            res.append(curr)
            
        return res
