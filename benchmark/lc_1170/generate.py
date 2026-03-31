import json
import random
import string

def generate_data(n):
    # Total length of words and queries combined ~ N
    # Let's say length of each string is 10 to keep it manageable
    num_strings = n // 10
    if num_strings == 0:
        num_strings = 1
        
    num_queries = max(1, num_strings // 2)
    num_words = max(1, num_strings - num_queries)
    
    queries = []
    for _ in range(num_queries):
        # Generate random string of length 10
        s = "".join(random.choices(string.ascii_lowercase, k=10))
        queries.append(s)
        
    words = []
    for _ in range(num_words):
        s = "".join(random.choices(string.ascii_lowercase, k=10))
        words.append(s)
        
    return {"queries": queries, "words": words}

def main():
    scales = [100, 1000, 10000, 100000]
    for scale in scales:
        data = generate_data(scale)
        with open(f"benchmark/lc_1170/data_{scale}.json", "w") as f:
            json.dump(data, f)

if __name__ == "__main__":
    main()
