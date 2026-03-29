import json
import os
import random

def generate_data():
    ns = [100, 1000, 10000, 100000]
    benchmarks = []
    
    for n in ns:
        weights = [random.randint(1, 500) for _ in range(n)]
        days = random.randint(1, n)
        benchmarks.append({
            "n": n,
            "weights": weights,
            "days": days
        })
        
    data = {
        "problem_id": "lc_1011",
        "benchmarks": benchmarks
    }
    
    with open("benchmark/lc_1011/data.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    generate_data()
