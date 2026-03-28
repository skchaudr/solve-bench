import random

def generate(n: int) -> list[int]:
    # Constraints: 3 <= n <= 50 (Leetcode problem)
    # But for scaling, we generate up to 100,000.
    # 1 <= values[i] <= 100
    random.seed(42)
    return [random.randint(1, 100) for _ in range(n)]
