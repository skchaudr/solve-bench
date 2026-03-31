import json
import random

def generate_input(n):
    # Generating a complete/balanced tree structure as an array format, similar to level-order.
    # To hit a specific path sum, we'll set nodes carefully, or just random values
    # For worst case time/space, deep paths or many paths summing to targetSum.
    # We will just generate random integers between -10 and 10,
    # and a random target sum.
    # Format: {"tree": [...], "targetSum": X}
    
    # We'll build an array of length n. 
    # Use small ints so path sums might hit targetSum
    tree_vals = [random.randint(-10, 10) for _ in range(n)]
    
    # Randomly select a path and calculate its sum
    targetSum = 0
    idx = 0
    while idx < n:
        targetSum += tree_vals[idx]
        # go to left or right child randomly
        if random.choice([True, False]):
            idx = 2 * idx + 1
        else:
            idx = 2 * idx + 2
            
    # Sometimes we want nulls, but a full tree is worst-case for exploring all paths
    return {"tree": tree_vals, "targetSum": int(targetSum)}

def main():
    scales = [100, 1000, 10000, 100000]
    data = {}
    for n in scales:
        data[n] = generate_input(n)
        
    with open("benchmark/lc_113/dataset.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    main()
