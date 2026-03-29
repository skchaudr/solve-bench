import random

def generate_test_case(n: int) -> dict:
    """
    Generates a synthetic test case for Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit.
    Constraints:
    - 1 <= nums.length <= 10^5
    - 1 <= nums[i] <= 10^9
    - 0 <= limit <= 10^9
    """
    limit = random.randint(0, 1000)
    # create chunks of small variance numbers with occasional large jumps
    nums = []
    base_val = random.randint(1, 10**9 - 2000)
    
    for _ in range(n):
        if random.random() < 0.05: # 5% chance of a jump to simulate window break
            base_val = random.randint(1, 10**9 - 2000)
        
        val = base_val + random.randint(-100, 100)
        val = max(1, min(10**9, val))
        nums.append(val)
        
    return {"nums": nums, "limit": limit}
