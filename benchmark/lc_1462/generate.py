import random

def generate_data(n: int, random_seed: int = 42):
    """
    Generate synthetic data for LC 1462 (Course Schedule IV).
    Returns (numCourses, prerequisites, queries).
    """
    random.seed(random_seed)
    
    numCourses = n
    numEdges = min(n * (n - 1) // 2, 2 * n)
    
    edges_set = set()
    prerequisites = []
    
    # Try to generate a DAG with ~2n edges
    # For large n, random generation might be slow if we have many collisions, 
    # but since numEdges is 2n and max edges is n^2/2, collisions are rare.
    while len(prerequisites) < numEdges:
        u = random.randint(0, n - 2)
        v = random.randint(u + 1, n - 1)
        if (u, v) not in edges_set:
            edges_set.add((u, v))
            prerequisites.append([u, v])
            
    # Generate ~n queries
    numQueries = n
    queries = []
    for _ in range(numQueries):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        while u == v:
            v = random.randint(0, n - 1)
        queries.append([u, v])
        
    return numCourses, prerequisites, queries
