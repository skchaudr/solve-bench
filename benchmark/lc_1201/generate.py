import json
import random

def generate_data(n):
    # Scale n directly. For instance, n=100,000 is still well within 10^9 max n limit
    # We will pick random a, b, c from small primes to keep the logic somewhat stressed
    a = random.randint(2, 100)
    b = random.randint(2, 100)
    c = random.randint(2, 100)
    
    return {"n": n, "a": a, "b": b, "c": c}

def main():
    scales = [100, 1000, 10000, 100000]
    for scale in scales:
        data = generate_data(scale)
        with open(f"benchmark/lc_1201/data_{scale}.json", "w") as f:
            json.dump(data, f)

if __name__ == "__main__":
    main()
