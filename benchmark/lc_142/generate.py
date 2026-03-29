import os
import json
import random

def main():
    scales = [100, 1000, 10000, 100000]
    data = {}
    
    for n in scales:
        arr = [random.randint(-10**9, 10**9) for _ in range(n)]
        
        # 90% chance of cycle. If there's a cycle, place it randomly.
        # This gives a mix of cycle lengths to test.
        if random.random() < 0.9:
            pos = random.randint(0, n - 1)
        else:
            pos = -1
            
        data[str(n)] = {
            "arr": arr,
            "pos": pos
        }
        
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), "data.json"), "w") as f:
        json.dump(data, f)
        
if __name__ == "__main__":
    main()
