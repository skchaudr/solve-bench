import json
import random

def generate():
    scales = [100, 1000, 10000, 100000]
    data = {}
    
    for n in scales:
        arr = []
        num_unique = max(10, n // 10)
        
        for _ in range(n):
            arr.append(random.randint(1, num_unique))
            
        data[n] = {
            "arr": arr,
            "n": n
        }
        
    with open("dataset.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    generate()
