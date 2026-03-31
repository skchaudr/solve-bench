import json
import random

def main():
    scales = [100, 1000, 10000, 100000]
    for n in scales:
        arr = sorted(random.sample(range(0, 1000000), n))
        with open(f"data_{n}.json", "w") as f:
            json.dump({"arr": arr}, f)

if __name__ == "__main__":
    main()
