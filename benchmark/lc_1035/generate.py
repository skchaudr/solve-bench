import json
import random
import os

def generate_data():
    scales = [100, 1000, 10000, 100000]
    out_dir = os.path.dirname(__file__)
    
    for n in scales:
        # We want to scale the values such that there are repeating numbers but it doesn't degrade LIS performance
        # For N=100_000, to keep runtime reasonable we want an alphabet size comparable to N so that average frequency is small.
        # Let's say max_val = N.
        
        max_val = n
        
        nums1 = [random.randint(1, max_val) for _ in range(n)]
        nums2 = [random.randint(1, max_val) for _ in range(n)]
        
        data = {
            "nums1": nums1,
            "nums2": nums2
        }
        
        with open(os.path.join(out_dir, f"data_{n}.json"), "w") as f:
            json.dump(data, f)
            
if __name__ == "__main__":
    generate_data()
