import json
import random

def generate_data(n):
    # n is number of gardens, max 10^4 per problem description, but let's scale to 10^5
    # Max degree is 3
    paths = []
    edges = set()
    
    for u in range(1, n + 1):
        num_edges = random.randint(0, 3)
        for _ in range(num_edges):
            # Try to add up to 3 edges per node
            if random.random() < 0.5 and n - u >= 1:
                v = u + random.randint(1, min(3, n - u))
                if u != v and (u, v) not in edges and (v, u) not in edges:
                    edges.add((u, v))
                    paths.append([u, v])
            
    return {"n": n, "paths": paths}

def main():
    scales = [100, 1000, 10000, 100000]
    for scale in scales:
        data = generate_data(scale)
        with open(f"benchmark/lc_1042/data_{scale}.json", "w") as f:
            json.dump(data, f)

if __name__ == "__main__":
    main()
