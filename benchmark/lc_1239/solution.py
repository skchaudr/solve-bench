from typing import List

class Solution:
    def maxLength(self, arr: List[str]) -> int:
        unique_masks = set()
        for s in arr:
            mask = 0
            dupes = False
            for c in s:
                bit = 1 << (ord(c) - 97)
                if mask & bit:
                    dupes = True
                    break
                mask |= bit
            if not dupes:
                unique_masks.add(mask)
                
        # Sort masks by length descending for better pruning
        masks = sorted(list(unique_masks), key=lambda x: -x.bit_count())
        n = len(masks)
        
        # Precompute suffix bitwise ORs for pruning
        suffix_masks = [0] * n
        curr_or = 0
        for i in range(n - 1, -1, -1):
            curr_or |= masks[i]
            suffix_masks[i] = curr_or

        max_len = [0]
        
        def dfs(idx, current_mask, current_len):
            if current_len > max_len[0]:
                max_len[0] = current_len
                
            if idx == n:
                return
                
            # Pruning:
            # If the current bits we have + the best we can possibly add from here
            # is less than or equal to max_len[0], we prune.
            # The best we can add is bounded by the bits available in suffix_masks[idx] 
            # that don't conflict with current_mask.
            available_bits = suffix_masks[idx] & ~current_mask
            if current_len + available_bits.bit_count() <= max_len[0]:
                return
                
            for i in range(idx, n):
                mask = masks[i]
                if (current_mask & mask) == 0:
                    dfs(i + 1, current_mask | mask, current_len + mask.bit_count())
                    
        dfs(0, 0, 0)
        return max_len[0]
