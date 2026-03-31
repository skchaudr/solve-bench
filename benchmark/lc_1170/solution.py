from typing import List
import bisect

class Solution:
    def numSmallerByFrequency(self, queries: List[str], words: List[str]) -> List[int]:
        def f(s: str) -> int:
            if not s:
                return 0
            min_char = min(s)
            return s.count(min_char)

        word_freqs = [f(w) for w in words]
        word_freqs.sort()
        
        ans = []
        n = len(word_freqs)
        for q in queries:
            freq = f(q)
            # Find the number of words with frequency strictly greater than `freq`
            idx = bisect.bisect_right(word_freqs, freq)
            ans.append(n - idx)
            
        return ans
