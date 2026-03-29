import os
import json
import random

def generate_test_data(n: int, max_val: int = 10**6):
    # According to constraints:
    # 1 <= nums.length <= 10^5
    # 1 <= nums[i] <= 10^6
    # 1 <= target <= 10^6
    
    # We will relax up to n=100,000 for standard benchmark scales
    nums = [random.randint(1, max_val) for _ in range(n)]
    
    # Let's select a target such that we have a mix of valid and invalid pairs.
    # Target can just be a random value, but picking it as median of some sort or just random
    target = random.randint(1, max_val)
    
    return {
        "nums": nums,
        "target": target
    }

def main():
    scales = [100, 1000, 10000, 100000]
    output_dir = os.path.dirname(__file__)
    os.makedirs(output_dir, exist_ok=True)
    
    for n in scales:
        data = generate_test_data(n)
        
        file_path = os.path.join(output_dir, f"data_{n}.json")
        with open(file_path, "w") as f:
            json.dump(data, f)
            
    print(f"Generated test data for scales {scales} in {output_dir}")

if __name__ == "__main__":
    main()
