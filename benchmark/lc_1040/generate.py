import random
import json
import os
import sys

# Ensure the parent directory is in the path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def generate_data():
    scales = [100, 1000, 10000, 100000]
    os.makedirs("benchmark/lc_1040", exist_ok=True)
    
    for n in scales:
        # Constraints:
        # 3 <= stones.length <= 10^4 (we scale up to 10^5)
        # 1 <= stones[i] <= 10^9
        # All values unique
        
        # Use random.sample which returns unique elements
        # Since n <= 100000 and range is up to 10^9, it's efficient enough.
        stones = random.sample(range(1, 10**9 + 1), n)
        
        with open(f"benchmark/lc_1040/input_{n}.json", "w") as f:
            json.dump(stones, f)

if __name__ == "__main__":
    generate_data()
