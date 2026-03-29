class Solution:
    def maxRepOpt1(self, text: str) -> int:
        if not text:
            return 0
        
        from collections import Counter
        freq = Counter(text)
        
        groups = []
        n = len(text)
        i = 0
        while i < n:
            char = text[i]
            length = 0
            while i < n and text[i] == char:
                length += 1
                i += 1
            groups.append((char, length))
            
        max_len = 0
        for i, (char, length) in enumerate(groups):
            # Case 1: Extend this group by 1 if there's another identical character elsewhere
            max_len = max(max_len, min(length + 1, freq[char]))
            
            # Case 2: Merge two groups separated by exactly one character
            if i >= 2 and groups[i-2][0] == char and groups[i-1][1] == 1:
                merged_len = groups[i-2][1] + length
                max_len = max(max_len, min(merged_len + 1, freq[char]))
                
        return max_len
