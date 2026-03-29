import json
import os

def generate_data():
    scales = [100, 1000, 10000, 100000]
    
    # We will map these nominal scales to feasible string lengths
    # since the output size is 2^(n-1).
    mapping = {
        100: 12,
        1000: 14,
        10000: 16,
        100000: 18
    }
    
    dataset = []
    
    for n in scales:
        actual_length = mapping[n]
        # Worst case: all same characters
        s = "a" * actual_length
        dataset.append({
            "n": n,
            "s": s
        })
        
    out_dir = os.path.dirname(__file__)
    with open(os.path.join(out_dir, "dataset.json"), "w") as f:
        json.dump(dataset, f, indent=2)

if __name__ == "__main__":
    generate_data()
