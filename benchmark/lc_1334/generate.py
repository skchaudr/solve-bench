import random
from typing import List, Tuple

def generate_test_case(n: int, seed: int = 42) -> Tuple[int, List[List[int]], int]:
    """
    Generates a synthetic undirected graph with `n` nodes and `~2n` edges.
    Ensures connectivity by first creating a spanning tree, then adding random edges.
    """
    random.seed(seed)
    
    # We want roughly 2n edges, or max possible if n is small
    num_edges = min(2 * n, n * (n - 1) // 2)
    
    unique_edges = {}
    
    # Ensure connectivity: spanning tree
    for i in range(1, n):
        u = random.randint(0, i - 1)
        w = random.randint(1, 1000) # smaller weights to make more nodes reachable
        unique_edges[(u, i)] = w
        
    attempts = 0
    max_attempts = n * 10
    while len(unique_edges) < num_edges and attempts < max_attempts:
        attempts += 1
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            u, v = min(u, v), max(u, v)
            if (u, v) not in unique_edges:
                w = random.randint(1, 1000)
                unique_edges[(u, v)] = w
                
    edges = [[u, v, w] for (u, v), w in unique_edges.items()]
    
    # distanceThreshold around the cost of a path of length 10
    distanceThreshold = random.randint(3000, 10000)
    
    return n, edges, distanceThreshold
