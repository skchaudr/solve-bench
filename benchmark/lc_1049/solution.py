from collections import Counter

class Solution:
    def lastStoneWeightII(self, stones: list[int]) -> int:
        total_sum = sum(stones)
        target = total_sum // 2
        
        counts = Counter(stones)
        
        items = []
        for weight, count in counts.items():
            k = 1
            while count >= k:
                items.append(weight * k)
                count -= k
                k *= 2
            if count > 0:
                items.append(weight * count)
                
        dp = 1
        
        for item in items:
            dp |= (dp << item)
            
        # The largest reachable sum <= target is the highest bit set
        # in dp up to the target-th bit.
        # Mask out bits higher than target:
        mask = (1 << (target + 1)) - 1
        valid_dp = dp & mask
        
        best_sum = valid_dp.bit_length() - 1
        return total_sum - 2 * best_sum

