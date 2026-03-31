import json
import random

def generate():
    scales = [100, 1000, 10000, 100000]
    data = {}
    for n in scales:
        redEdges = []
        blueEdges = []
        
        for i in range(n - 1):
            if i % 2 == 0:
                redEdges.append([i, i + 1])
            else:
                blueEdges.append([i, i + 1])
                
        for _ in range(n):
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if random.random() < 0.5:
                redEdges.append([u, v])
            else:
                blueEdges.append([u, v])
                
        data[n] = {"n": n, "redEdges": redEdges, "blueEdges": blueEdges}
        
    with open("dataset.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    generate()
