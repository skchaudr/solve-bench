import json
import random
import os

def generate_data():
    sizes = [100, 1000, 10000, 100000]
    data = {}
    for n in sizes:
        # Generate random array of stones with weights 1 to 100
        stones = [random.randint(1, 100) for _ in range(n)]
        data[n] = stones
    
    os.makedirs('benchmark/lc_1049', exist_ok=True)
    with open('benchmark/lc_1049/data.json', 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    random.seed(42)
    generate_data()
