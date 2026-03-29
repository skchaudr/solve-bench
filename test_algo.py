import random
from collections import defaultdict
from bisect import bisect_left
import time

def maxUncrossedLines_dp(nums1, nums2):
    if len(nums1) < len(nums2):
        nums1, nums2 = nums2, nums1
    dp = [0] * (len(nums2) + 1)
    for num1 in nums1:
        prev = 0
        for j in range(len(nums2)):
            temp = dp[j+1]
            if num1 == nums2[j]:
                dp[j+1] = prev + 1
            elif dp[j] > dp[j+1]:
                dp[j+1] = dp[j]
            prev = temp
    return dp[-1]

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

N = 10000
nums1 = [random.randint(1, 2000) for _ in range(N)]
nums2 = [random.randint(1, 2000) for _ in range(N)]

t0 = time.time()
ans1 = maxUncrossedLines_dp(nums1, nums2)
t1 = time.time()
print(f"DP: {ans1} in {t1-t0:.3f}s")

t0 = time.time()
ans2 = maxUncrossedLines_lis(nums1, nums2)
t1 = time.time()
print(f"LIS: {ans2} in {t1-t0:.3f}s")

