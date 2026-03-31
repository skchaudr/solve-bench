import json
import random

def generate_tree_array(n):
    # Generates a valid complete binary tree representation using array format
    if n == 0:
        return []
    return [random.randint(0, 100000) for _ in range(n)]

def main():
    scales = [100, 1000, 10000, 100000]
    for n in scales:
        arr = generate_tree_array(n)
        with open(f"data_{n}.json", "w") as f:
            json.dump({"arr": arr}, f)

if __name__ == "__main__":
    main()
