import json
import random
import os

def generate_test_cases():
    scales = [100, 1000, 10000, 100000]
    os.makedirs("benchmark/lc_103", exist_ok=True)
    
    for n in scales:
        values = [random.randint(-100, 100) for _ in range(n)]
        
        with open(f"benchmark/lc_103/data_{n}.json", "w") as f:
            json.dump({"n": n, "values": values}, f)

if __name__ == "__main__":
    generate_test_cases()
