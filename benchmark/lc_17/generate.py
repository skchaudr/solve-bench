import json
import os
import random

def generate_data():
    scales = [100, 1000, 10000, 100000]
    # To avoid OOM and excessive time, we intercept standard scales
    # and map them to small n values: 6, 8, 10, 12.
    # The output space is 4^n. 
    # For n=12, 4^12 = 16,777,216 items, which takes ~8 seconds.
    mapped_n = {
        100: 6,
        1000: 8,
        10000: 10,
        100000: 12
    }
    
    datasets = []
    
    for n in scales:
        real_n = mapped_n[n]
        # To hit worst case 4^n complexity, we only use '7' and '9'
        digits = "".join(random.choice(['7', '9']) for _ in range(real_n))
        datasets.append({
            "n": n,
            "real_n": real_n,
            "digits": digits
        })
        
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), "test_cases.json"), "w") as f:
        json.dump(datasets, f)
        
if __name__ == "__main__":
    generate_data()
