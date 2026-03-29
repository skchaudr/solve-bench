class Solution:
    def queryString(self, s: str, n: int) -> bool:
        if n == 0:
            return True
        if not s:
            return False

        # If n is larger than the number of substrings we can form, we can early exit.
        # But this is handled correctly by checking the set size.
        
        seen = set()
        
        # Max length of binary string representing integers up to n is n.bit_length()
        max_len = n.bit_length()
        
        # Min length of binary string representing integers >= n // 2 is (n // 2 + 1).bit_length()
        # This gives a tighter bound, but checking all up to max_len is fast enough.
        # However, checking substrings of lengths from 1 to max_len is O(len(s) * max_len)
        
        for i in range(len(s)):
            if s[i] == '0':
                continue # integer representations don't have leading zeros, except '0' itself but range is [1, n]
            
            val = 0
            # Check substrings starting at i, up to max_len characters long
            for j in range(i, min(len(s), i + max_len)):
                val = (val << 1) | int(s[j])
                if 1 <= val <= n:
                    seen.add(val)
                if val > n:
                    break
                    
        return len(seen) == n
