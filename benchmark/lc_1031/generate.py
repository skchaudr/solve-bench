import random
from typing import Tuple, List

def generate_data(n: int) -> Tuple[List[int], int, int]:
    """
    Generate a random array of length n.
    Values are uniformly distributed between 1 and 10^4.
    Returns the array, firstLen, and secondLen such that firstLen + secondLen <= n.
    """
    nums = [random.randint(1, 10000) for _ in range(n)]
    
    # Randomly choose firstLen and secondLen such that firstLen + secondLen <= n
    # For large n, we'll choose reasonable lengths to avoid trivial boundary cases
    # but still keep it random. We'll set lengths up to min(n//2, 1000) 
    max_len = min(n // 2, 1000)
    
    firstLen = random.randint(1, max_len)
    secondLen = random.randint(1, n - firstLen)
    
    return nums, firstLen, secondLen

if __name__ == "__main__":
    nums, firstLen, secondLen = generate_data(100)
    print(f"Generated nums of length {len(nums)}, firstLen: {firstLen}, secondLen: {secondLen}")
