import math

class Solution:
    def nthUglyNumber(self, n: int, a: int, b: int, c: int) -> int:
        ab = a * b // math.gcd(a, b)
        ac = a * c // math.gcd(a, c)
        bc = b * c // math.gcd(b, c)
        abc = ab * c // math.gcd(ab, c)
        
        left, right = 1, 2 * 10**9
        
        while left < right:
            mid = left + (right - left) // 2
            
            # Number of ugly numbers <= mid
            count = (mid // a) + (mid // b) + (mid // c) \
                  - (mid // ab) - (mid // ac) - (mid // bc) \
                  + (mid // abc)
                  
            if count >= n:
                right = mid
            else:
                left = mid + 1
                
        return left
