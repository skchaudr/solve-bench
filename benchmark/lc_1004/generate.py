import random

def generate_data(n: int):
    """
    Generate a random binary array of size n, and a random integer k.
    Despite the generic prompt mentioning [1, 10^4], the problem constraints
    for Max Consecutive Ones III dictate the array contains only 0 or 1, and 0 <= k <= n.
    """
    # Generate array of 0s and 1s
    # Vary the density of 0s to provide robust test cases, e.g. 10% to 50%
    density = random.uniform(0.1, 0.5)
    nums = [1 if random.random() > density else 0 for _ in range(n)]
    
    # k can be anywhere from 0 to the number of zeroes, or slightly more,
    # or even up to n. Let's make it proportional to the number of zeros
    # to make it interesting, or just random in [0, n/2]
    k = random.randint(0, int(n * density) + 1)
    # Ensure k doesn't exceed n as per constraints
    k = min(n, k)
    
    return nums, k
