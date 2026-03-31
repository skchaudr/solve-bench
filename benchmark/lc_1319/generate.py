import json
import random

def generate():
    scales = [100, 1000, 10000, 100000]
    data = {}
    
    for n in scales:
        connections = []
        
        num_components = 5
        comp_size = n // num_components
        
        nodes = list(range(n))
        random.shuffle(nodes)
        
        for c in range(num_components):
            start = c * comp_size
            end = (c + 1) * comp_size if c < num_components - 1 else n
            comp_nodes = nodes[start:end]
            
            for i in range(1, len(comp_nodes)):
                u = comp_nodes[i]
                v = comp_nodes[random.randint(0, i - 1)]
                connections.append([u, v])
                
            for _ in range(len(comp_nodes) // 2):
                u = random.choice(comp_nodes)
                v = random.choice(comp_nodes)
                if u != v:
                    connections.append([u, v])
                    
        data[n] = {
            "n": n,
            "connections": connections
        }
        
    with open("dataset.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    generate()
