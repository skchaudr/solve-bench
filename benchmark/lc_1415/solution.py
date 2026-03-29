class Solution:
    def getHappyString(self, n: int, k: int) -> str:
        # Total number of happy strings of length n is 3 * 2^(n-1)
        # Using shift to compute powers of 2 for n >= 1
        leaves = 1 << (n - 1)
        
        if k > 3 * leaves:
            return ""
        
        # Make k 0-indexed
        k -= 1
        
        res = []
        
        # First character choice among 'a', 'b', 'c'
        first_idx = k // leaves
        k %= leaves
        
        choices = ['a', 'b', 'c']
        res.append(choices[first_idx])
        
        if n == 1:
            return res[0]
        
        # For the remaining n - 1 characters, each has exactly 2 choices
        # We can extract the choice directly from the binary representation of k
        # which is now strictly < 2^(n-1). We pad it to exactly n-1 bits.
        
        # To handle very large k efficiently without python string formatting limit issues
        # we can format k directly to a binary string of length n-1.
        # Although bin(k) might be large, it's efficient.
        bin_k = bin(k)[2:].zfill(n - 1)
        
        for bit in bin_k:
            prev = res[-1]
            if prev == 'a':
                next_choices = ['b', 'c']
            elif prev == 'b':
                next_choices = ['a', 'c']
            else:
                next_choices = ['a', 'b']
            
            res.append(next_choices[int(bit)])
            
        return "".join(res)
