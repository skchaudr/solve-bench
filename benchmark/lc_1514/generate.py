import json
import os
import random

def generate_data(n, target_edges=None):
    if target_edges is None:
        target_edges = 2 * n
        
    start = 0
    end = n - 1
    
    # We'll create a connected component from 0 to n-2.
    # Node n-1 will be completely disconnected.
    # This forces Dijkstra to fully explore the connected component,
    # maximizing time complexity (O(E log V)).
    
    edges = []
    succProb = []
    edge_set = set()
    
    # Create a spanning tree for 0 to n-2 to ensure connectivity
    for i in range(1, n - 1):
        u, v = i - 1, i
        if u > v: u, v = v, u
        edge_set.add((u, v))
        edges.append([u, v])
        succProb.append(random.uniform(0.5, 0.99))
        
    # Add random edges up to target_edges
    while len(edges) < target_edges:
        u = random.randint(0, n - 2)
        v = random.randint(0, n - 2)
        if u == v:
            continue
        if u > v: u, v = v, u
        if (u, v) not in edge_set:
            edge_set.add((u, v))
            edges.append([u, v])
            succProb.append(random.uniform(0.5, 0.99))
            
    return n, edges, succProb, start, end

def main():
    os.makedirs("benchmark/lc_1514", exist_ok=True)
    scales = [100, 1000, 10000, 100000]
    
    for n in scales:
        n_val, edges, succProb, start, end = generate_data(n)
        
        # Save to file
        with open(f"benchmark/lc_1514/data_{n}.json", "w") as f:
            json.dump({
                "n": n_val,
                "edges": edges,
                "succProb": succProb,
                "start": start,
                "end": end
            }, f)
            
if __name__ == "__main__":
    main()
