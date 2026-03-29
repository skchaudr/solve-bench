import random
import string

def generate_data(n: int):
    """
    Generates an array of n strings.
    The strings should realistically stress-test the algorithm.
    While max unique characters is 26, to fully exercise backtracking
    pruning, we use many short valid strings and some overlapping ones.
    """
    random.seed(42)  # For reproducibility
    arr = []
    
    for _ in range(n):
        # Generate strings of length 1 to 5.
        # This creates many unique combinations without instantly maxing out
        # the available alphabet, keeping the DFS tree deep and branchy.
        length = random.randint(1, 5)
        # Sample unique characters
        s = "".join(random.sample(string.ascii_lowercase, length))
        arr.append(s)
        
    return arr
