import random
import sys
import os

def generate_data(n: int) -> list[int]:
    """
    Generate an array of n barcodes such that no element has a frequency
    greater than (n+1)//2.
    """
    if n <= 0:
        return []
    
    max_freq = (n + 1) // 2
    barcodes = []
    
    # We can distribute elements safely
    remaining = n
    current_barcode = 1
    
    while remaining > 0:
        # We need to make sure we don't violate max_freq
        limit = min(remaining, max_freq)
        count = random.randint(1, limit)
        barcodes.extend([current_barcode] * count)
        remaining -= count
        current_barcode += 1
        
    random.shuffle(barcodes)
    return barcodes
