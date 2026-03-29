import json
import random
import string
import os

def generate_data():
    scales = [100, 1000, 10000, 100000]
    dataset = {}
    
    for n in scales:
        # Generate random strings s and t
        s_chars = [random.choice(string.ascii_lowercase) for _ in range(n)]
        t_chars = [random.choice(string.ascii_lowercase) for _ in range(n)]
        
        s = "".join(s_chars)
        t = "".join(t_chars)
        
        # Max distance per character is 25 ('z' - 'a').
        # An average difference is ~8.5
        # Set maxCost around n * 5 to have a decent length substring
        maxCost = random.randint(0, n * 10)
        
        dataset[str(n)] = {
            "s": s,
            "t": t,
            "maxCost": maxCost
        }
    
    # Write to dataset.json
    output_path = os.path.join(os.path.dirname(__file__), "dataset.json")
    with open(output_path, "w") as f:
        json.dump(dataset, f)
        
    print(f"Generated data for scales {scales} and saved to {output_path}")

if __name__ == "__main__":
    generate_data()
