import json
import random
import string
import os

def generate_chain(length):
    word = ""
    chain = []
    for _ in range(length):
        pos = random.randint(0, len(word))
        char = random.choice(string.ascii_lowercase)
        word = word[:pos] + char + word[pos:]
        chain.append(word)
    return chain

def generate_data(n):
    words = set()
    
    # Generate some guaranteed chains
    for _ in range(n // 16 + 1):
        chain = generate_chain(random.randint(1, 16))
        for w in chain:
            words.add(w)
            if len(words) >= n:
                break
        if len(words) >= n:
            break
            
    # Fill the rest with random variations if needed
    while len(words) < n:
        l = random.randint(1, 16)
        w = "".join(random.choices(string.ascii_lowercase, k=l))
        words.add(w)
        
    words_list = list(words)
    random.shuffle(words_list)
    return words_list

def main():
    os.makedirs("benchmark/lc_1048", exist_ok=True)
    
    sizes = [100, 1000, 10000, 100000]
    for n in sizes:
        print(f"Generating data for n={n}...")
        data = generate_data(n)
        with open(f"benchmark/lc_1048/data_{n}.json", "w") as f:
            json.dump(data, f)
    print("Data generation complete.")

if __name__ == "__main__":
    main()
