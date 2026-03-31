import json
import random

def generate_input(n):
    # n is the total number of characters a+b+c.
    # distribute n randomly among a, b, c.
    # To maximize the string size, make them as balanced as possible or heavily skewed.
    # E.g., heavily skewed but valid.
    
    a = random.randint(0, n)
    rem = n - a
    b = random.randint(0, rem)
    c = rem - b
    
    # Shuffle to avoid a being always largest
    arr = [a, b, c]
    random.shuffle(arr)
    return arr

def main():
    scales = [100, 1000, 10000, 100000]
    data = {}
    for n in scales:
        data[n] = generate_input(n)
        
    with open("benchmark/lc_1405/dataset.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    main()
