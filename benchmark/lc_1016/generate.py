import sys
import random

def generate_data(n: int):
    """
    Generates a string `s` of length exactly `n` and an integer `m`.
    To construct a worst-case string, we concatenate the binary representation of integers:
    1, 2, 3, ... until the length reaches `n`.
    """
    s_parts = []
    current_len = 0
    m = 1
    
    while current_len < n:
        b = bin(m)[2:]
        s_parts.append(b)
        current_len += len(b)
        m += 1
        
    s = "".join(s_parts)[:n]
    target_n = m - 2 if m > 2 else 1
    
    return s, target_n

if __name__ == "__main__":
    s, target_n = generate_data(100)
    print(f"n=100 -> len(s)={len(s)}, target_n={target_n}")
