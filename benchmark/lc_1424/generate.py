import random

def generate_data(n: int) -> list[list[int]]:
    """
    Generate a 2D array representing nums, where the total number of elements
    across all rows is exactly n.
    """
    # The constraints are:
    # 1 <= nums.length <= 10^5
    # 1 <= nums[i].length <= 10^5
    # 1 <= sum(nums[i].length) <= 10^5
    # 1 <= nums[i][j] <= 10^5

    # We want to randomly partition the total elements n into k rows
    # Let's say we have k rows, where 1 <= k <= min(n, 100_000).
    # We can randomly pick k between 1 and n.

    if n == 0:
        return []

    # To create interesting test cases, let's randomly split `n` into `k` parts.
    # A simple way to do this is to generate k-1 cut points in a sequence of n.
    # However, for simplicity and variety, we can just randomly decide row sizes.

    k = random.randint(1, n)

    # Pre-allocate rows with size 1 to ensure each of the k rows has at least 1 element
    # But wait, we might not have enough elements if k > n, but k <= n.
    row_sizes = [1] * k
    remaining = n - k

    # Distribute the remaining elements randomly among the k rows
    # To do this efficiently, we can just randomly pick a row and increment its size.
    # For large n, this loop is fast enough (up to 100,000).
    if remaining > 0:
        for _ in range(remaining):
            idx = random.randint(0, k - 1)
            row_sizes[idx] += 1

    # Now generate the actual data
    nums = []
    for size in row_sizes:
        row = [random.randint(1, 100_000) for _ in range(size)]
        nums.append(row)

    return nums
