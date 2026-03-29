import json
import os
import random

def generate_data():
    scales = [100, 1000, 10000, 100000]
    # Map exponential scales to feasible string lengths
    # The actual algorithm scales O(2^N) and N <= 16 according to constraints.
    # We map 100->10, 1000->12, 10000->14, 100000->16.
    mapped_n = {
        100: 10,
        1000: 12,
        10000: 14,
        100000: 16
    }
    
    random.seed(42)
    os.makedirs('benchmark/lc_1593', exist_ok=True)
    
    for scale in scales:
        n = mapped_n[scale]
        # We tested and 'a's and 'b's generate more recursive paths
        s = "".join(random.choice(['a', 'b']) for _ in range(n))
        
        with open(f'benchmark/lc_1593/data_{scale}.json', 'w') as f:
            json.dump({"s": s}, f)

if __name__ == "__main__":
    generate_data()
