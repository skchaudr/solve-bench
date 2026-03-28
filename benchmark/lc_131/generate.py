def generate(n: int) -> str:
    """
    Generate synthetic data for palindrome partitioning.
    To stress test the backtracking approach, we want to maximize the number
    of valid palindromes. A string with all identical characters achieves this.
    For length n, there are 2^(n-1) partitions, all of which are palindromic.
    """
    # Using 'a' repeated n times
    return "a" * n
