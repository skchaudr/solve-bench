import json
import random

def generate_data(n):
    ops = ["SnapshotArray"]
    args = [[n]]
    
    current_snap = 0
    for _ in range(n):
        r = random.random()
        if r < 0.6:
            ops.append("set")
            args.append([random.randint(0, n - 1), random.randint(1, 1000)])
        elif r < 0.8:
            ops.append("snap")
            args.append([])
            current_snap += 1
        else:
            ops.append("get")
            snap_id = random.randint(0, current_snap) if current_snap > 0 else 0
            args.append([random.randint(0, n - 1), snap_id])
            
    return {"ops": ops, "args": args}

def main():
    scales = [100, 1000, 10000, 100000]
    for scale in scales:
        data = generate_data(scale)
        with open(f"benchmark/lc_1146/data_{scale}.json", "w") as f:
            json.dump(data, f)

if __name__ == "__main__":
    main()
