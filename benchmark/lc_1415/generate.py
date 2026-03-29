import sys
import json
import random
import os

def generate_data():
    scales = [100, 1000, 10000, 100000]
    
    # Ensure the directory exists
    os.makedirs("benchmark/lc_1415", exist_ok=True)
    
    for n in scales:
        max_k = 3 * (1 << (n - 1))
        # Random k within range
        k = random.randint(1, max_k)
        
        data = {
            "n": n,
            "k": str(k) # Store as string to avoid JSON parsing integer limit in standard setups
        }
        
        with open(f"benchmark/lc_1415/data_{n}.json", "w") as f:
            json.dump(data, f)

if __name__ == "__main__":
    # Increase the limit for integer string conversion to accommodate large k
    sys.set_int_max_str_digits(200000)
    generate_data()
