import json

def generate_input(n):
    # This is a backtracking problem that generates O(N!) combinations
    # so we must aggressively downscale N.
    # We will map standard sizes to [3, 5, 7, 9] to make it computationally feasible.
    mapping = {
        100: 3,
        1000: 5,
        10000: 7,
        100000: 9
    }
    
    actual_n = mapping.get(n, 7)
    
    # Generate tiles using max variety of characters to hit worst-case O(N!)
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    tiles = ""
    for i in range(actual_n):
        tiles += chars[i % 26]
    return tiles

def main():
    scales = [100, 1000, 10000, 100000]
    data = {}
    for n in scales:
        data[n] = generate_input(n)
        
    with open("benchmark/lc_1079/dataset.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    main()
