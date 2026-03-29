import json
import random
import os

def generate_data(n):
    # Generates synthetic data for longest arithmetic subsequence
    # The constraints dictate 0 <= nums[i] <= 500
    nums = [random.randint(0, 500) for _ in range(n)]
    
    # Let's embed a sequence to ensure we test some positive cases.
    # The sequence could have a length between 10 and min(n // 2, 500)
    diff = random.randint(1, 10)
    start = random.randint(0, 500)
    
    seq = []
    curr = start
    while 0 <= curr <= 500:
        seq.append(curr)
        curr += diff
    
    if len(seq) > 2:
        # We replace some random elements with this sequence, maintaining their order.
        indices = sorted(random.sample(range(n), len(seq)))
        for i, val in zip(indices, seq):
            nums[i] = val
            
    return nums

def main():
    sizes = [100, 1000, 10000, 100000]
    output_dir = os.path.dirname(__file__)
    
    for n in sizes:
        nums = generate_data(n)
        filepath = os.path.join(output_dir, f"data_{n}.json")
        with open(filepath, "w") as f:
            json.dump({"nums": nums}, f)
        print(f"Generated {filepath} with length {len(nums)}")

if __name__ == "__main__":
    main()
