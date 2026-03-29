import json
import random
import os

def generate_data():
    scales = [100, 1000, 10000, 100000]
    data = {}
    
    for n in scales:
        # Values in [-10^9, 10^9] according to instructions for data generation,
        # although problem constraints say 1 <= Node.val <= 1000.
        # We will follow the boilerplate instruction: "values in [-10^9, 10^9]"
        arr = [random.randint(-10**9, 10**9) for _ in range(n)]
        data[str(n)] = arr
        
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), 'data.json'), 'w') as f:
        json.dump(data, f)
        
    print(f"Generated synthetic data for Reorder List up to N={scales[-1]}")

if __name__ == "__main__":
    generate_data()
