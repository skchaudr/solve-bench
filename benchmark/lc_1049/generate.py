import random

def generate_data(n: int) -> list[int]:
    """
    Generates an array of stones of length n.
    According to constraints, stones[i] is between 1 and 100.
    """
    return [random.randint(1, 100) for _ in range(n)]
