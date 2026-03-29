import random
from collections import defaultdict
from bisect import bisect_left
import time

def maxUncrossedLines_lis(nums1, nums2):
    positions = defaultdict(list)
    for i, num in enumerate(nums2):
        positions[num].append(i)
    
    sub = []
    for num in nums1:
        for idx in reversed(positions[num]):
            pos = bisect_left(sub, idx)
            if pos == len(sub):
                sub.append(idx)
            else:
                sub[pos] = idx
    return len(sub)

for N in [100, 1000, 10000, 100000]:
    nums1 = [random.randint(1, 2000) for _ in range(N)]
    nums2 = [random.randint(1, 2000) for _ in range(N)]
    
    t0 = time.time()
    ans2 = maxUncrossedLines_lis(nums1, nums2)
    t1 = time.time()
    print(f"N={N}: LIS {ans2} in {t1-t0:.4f}s")
