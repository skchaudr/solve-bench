import random
from typing import Tuple, List

def generate_data(n: int) -> Tuple[List[int], List[int], int]:
    """
    Generates synthetic input data for the Grumpy Bookstore Owner problem.
    """
    customers = [random.randint(1, 10**4) for _ in range(n)]
    grumpy = [random.randint(0, 1) for _ in range(n)]
    minutes = random.randint(1, n)
    return customers, grumpy, minutes

if __name__ == "__main__":
    n = 10
    customers, grumpy, minutes = generate_data(n)
    print(f"n = {n}")
    print(f"customers = {customers}")
    print(f"grumpy = {grumpy}")
    print(f"minutes = {minutes}")
