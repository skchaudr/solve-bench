import json
import random
import os

def generate_data():
    # Because O(N^3) DP is very slow, we map the benchmark scales to reasonable values
    # N=100 -> 50
    # N=1000 -> 100
    # N=10000 -> 200
    # N=100000 -> 400
    scales = {
        100: 50,
        1000: 100,
        10000: 200,
        100000: 400
    }
    
    datasets = []
    for scale, mapped_scale in scales.items():
        # Vertex values can be 1 to 100 based on LeetCode constraints
        # Max output could be around 100^3 * N, which easily fits in integer limits
        values = [random.randint(1, 100) for _ in range(mapped_scale)]
        
        datasets.append({
            "n": scale,
            "mapped_n": mapped_scale,
            "values": values
        })
        
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), "test_data.json"), "w") as f:
        json.dump(datasets, f)

if __name__ == "__main__":
    generate_data()
