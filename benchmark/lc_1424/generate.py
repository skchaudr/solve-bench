import json
import os
import random

def generate_data(n):
    # Total number of elements is n
    nums = []
    remaining = n
    
    while remaining > 0:
        # Generate row lengths that vary significantly
        if remaining > 1:
            if random.random() < 0.2:
                # 20% chance for a relatively longer row
                length = random.randint(1, min(remaining, max(10, remaining // 5)))
            else:
                length = random.randint(1, min(remaining, 50))
        else:
            length = 1
            
        row = [random.randint(1, 10**5) for _ in range(length)]
        nums.append(row)
        remaining -= length
        
    return {"nums": nums}

def main():
    scales = [100, 1000, 10000, 100000]
    out_dir = os.path.dirname(__file__)
    for n in scales:
        data = generate_data(n)
        file_path = os.path.join(out_dir, f"data_{n}.json")
        with open(file_path, "w") as f:
            json.dump(data, f)
            
if __name__ == "__main__":
    main()
