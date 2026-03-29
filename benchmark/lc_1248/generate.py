import random
import os

def generate_data(n: int, seed: int = 42):
    random.seed(seed)
    
    # Generate array of random integers in [1, 10000]
    nums = [random.randint(1, 10000) for _ in range(n)]
    
    # Calculate how many odd numbers are actually in the array
    # to randomly pick a sensible k
    odd_count = sum(1 for x in nums if x % 2 == 1)
    
    if odd_count > 0:
        k = random.randint(1, odd_count)
    else:
        # edge case, if no odd numbers, picking k=1 is fine
        k = 1
        
    return nums, k

if __name__ == "__main__":
    scales = [100, 1000, 10000, 100000]
    for n in scales:
        nums, k = generate_data(n)
        print(f"n={n}, k={k}, len(nums)={len(nums)}")
