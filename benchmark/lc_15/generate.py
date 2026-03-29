import json
import random
import os

def generate_data():
    sizes = [100, 1000, 10000, 100000]
    out_dir = "benchmark/lc_15"
    os.makedirs(out_dir, exist_ok=True)
    
    for n in sizes:
        # Generate random array
        nums = [random.randint(-10**9, 10**9) for _ in range(n)]
        
        # We can sprinkle some 0s and pairs that sum to 0 to ensure
        # some triplets sum to 0
        num_sprinkles = min(n // 10, 1000)
        for _ in range(num_sprinkles):
            idx1 = random.randint(0, n - 1)
            idx2 = random.randint(0, n - 1)
            idx3 = random.randint(0, n - 1)
            
            # Make sure they are distinct
            if len({idx1, idx2, idx3}) == 3:
                val = random.randint(-10**9, 10**9)
                nums[idx1] = val
                nums[idx2] = -val // 2
                nums[idx3] = -val + (val // 2)
        
        with open(os.path.join(out_dir, f"data_{n}.json"), "w") as f:
            json.dump(nums, f)

if __name__ == "__main__":
    generate_data()
