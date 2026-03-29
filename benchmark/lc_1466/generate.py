import random

def generate_random_tree(n):
    """
    Generate a random tree on n nodes.
    Returns the edge connections list where direction is randomly chosen.
    """
    nodes = list(range(1, n))
    random.shuffle(nodes)
    
    connections = []
    connected_nodes = [0]
    
    for i in range(len(nodes)):
        u = random.choice(connected_nodes)
        v = nodes[i]
        
        # Randomly choose direction: u -> v or v -> u
        if random.random() < 0.5:
            connections.append([u, v])
        else:
            connections.append([v, u])
            
        connected_nodes.append(v)
        
    random.shuffle(connections)
    return connections

def generate_data(n):
    return (n, generate_random_tree(n))
