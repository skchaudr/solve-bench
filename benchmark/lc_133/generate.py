import random
import os
import json

def generate_graph(n, edges_count):
    if n == 0:
        return []
        
    adj = {i: [] for i in range(1, n + 1)}
    
    # Create a spanning path to ensure graph is connected
    nodes = list(range(1, n + 1))
    random.shuffle(nodes)
    
    edges = set()
    for i in range(n - 1):
        u, v = nodes[i], nodes[i+1]
        if u > v:
            u, v = v, u
        edges.add((u, v))
        
    # Add random edges up to edges_count
    attempts = 0
    max_attempts = edges_count * 5
    while len(edges) < edges_count and attempts < max_attempts:
        attempts += 1
        u = random.randint(1, n)
        v = random.randint(1, n)
        if u != v:
            if u > v:
                u, v = v, u
            edges.add((u, v))
            
    # Populate adjacency list
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        
    # Convert to array of arrays
    adjList = []
    for i in range(1, n + 1):
        adjList.append(adj[i])
        
    return adjList

def generate_data():
    scales = [100, 1000, 10000, 100000]
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    
    for n in scales:
        edges_count = min(n * 2, n * (n - 1) // 2)
        adjList = generate_graph(n, edges_count)
        
        # Save adjacency list
        filename = os.path.join(os.path.dirname(__file__), f"data_{n}.json")
        with open(filename, "w") as f:
            json.dump(adjList, f)

if __name__ == "__main__":
    generate_data()
