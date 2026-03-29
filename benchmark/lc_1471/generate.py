import json
import random
import os

def generate_data(n: int):
    # Generating an array of n integers between -10^9 and 10^9
    arr = [random.randint(-10**9, 10**9) for _ in range(n)]
    
    # Randomly select k between 1 and n
    k = random.randint(1, n)
    
    return {"arr": arr, "k": k}

def main():
    scales = [100, 1000, 10000, 100000]
    data_dir = os.path.dirname(os.path.abspath(__file__))
    
    for n in scales:
        data = generate_data(n)
        file_path = os.path.join(data_dir, f"data_{n}.json")
        with open(file_path, 'w') as f:
            json.dump(data, f)
        print(f"Generated data for n={n}")

if __name__ == "__main__":
    main()
