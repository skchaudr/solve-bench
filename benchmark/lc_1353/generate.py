import json
import random
import os

def generate_data():
    sizes = [100, 1000, 10000, 100000]
    out_dir = os.path.dirname(__file__)

    for n in sizes:
        events = []
        # Max start day up to 10^5, max end day up to 10^5
        for _ in range(n):
            start = random.randint(1, 10**5)
            # End is from start to up to max
            # To ensure varied durations, we add a random duration from 0 up to 1000
            end = min(10**5, start + random.randint(0, 1000))
            events.append([start, end])
            
        out_path = os.path.join(out_dir, f"data_{n}.json")
        with open(out_path, "w") as f:
            json.dump(events, f)
            
    print("Data generated.")

if __name__ == "__main__":
    generate_data()
