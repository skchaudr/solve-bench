import json
import random
import os

def generate_data():
    scales = [100, 1000, 10000, 100000]
    os.makedirs("benchmark/lc_1014", exist_ok=True)
    
    for n in scales:
        values = [random.randint(1, 1000) for _ in range(n)]
        
        with open(f"benchmark/lc_1014/data_{n}.json", "w") as f:
            json.dump(values, f)

if __name__ == "__main__":
    generate_data()
