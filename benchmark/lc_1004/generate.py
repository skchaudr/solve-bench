import random
import json
import os

def generate_data():
    scales = [100, 1000, 10000, 100000]
    dataset = {}

    for n in scales:
        dataset[n] = []
        # Generate at least 3 random instances per scale for averaging
        for _ in range(3):
            # Must produce valid inputs for this specific problem
            # nums[i] is either 0 or 1.
            nums = [random.choice([0, 1]) for _ in range(n)]
            # 0 <= k <= nums.length
            k = random.randint(0, n)
            dataset[n].append({"nums": nums, "k": k})

    return dataset

if __name__ == "__main__":
    dataset = generate_data()
    # Write to a JSON file if run standalone
    file_path = os.path.join(os.path.dirname(__file__), 'dataset.json')
    with open(file_path, 'w') as f:
        json.dump(dataset, f)
    print(f"Dataset generated at {file_path}")
