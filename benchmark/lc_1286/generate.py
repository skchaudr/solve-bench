import json
import os
import string

def generate_operations(n):
    ops = []
    args = []
    
    characters = string.ascii_lowercase[:15]
    # C(15, 7) = 6435 combinations
    combinationLength = 7
    
    while len(ops) < n:
        ops.append("CombinationIterator")
        args.append([characters, combinationLength])
        
        for _ in range(6435):
            if len(ops) >= n: break
            ops.append("hasNext")
            args.append([])
            
            if len(ops) >= n: break
            ops.append("next")
            args.append([])
            
    return {"ops": ops, "args": args}

def main():
    os.makedirs(os.path.join(os.path.dirname(__file__), "dataset"), exist_ok=True)
    scales = [100, 1000, 10000, 100000]
    for n in scales:
        data = generate_operations(n)
        with open(os.path.join(os.path.dirname(__file__), f"dataset/{n}.json"), "w") as f:
            json.dump(data, f)

if __name__ == "__main__":
    main()
