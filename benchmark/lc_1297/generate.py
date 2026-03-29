import json
import random
import os
import string

def generate_data():
    scales = [100, 1000, 10000, 100000]
    data = {}
    
    random.seed(42)
    
    for n in scales:
        # Generates a string of length n
        # maxLetters: 1 to min(26, minSize)
        # minSize: 1 to min(26, n)
        # We can just set minSize = random.randint(1, min(10, n)) for some realistic sliding window testing
        # and maxLetters = random.randint(1, minSize)
        # maxSize >= minSize
        
        # In actual practice, it's best to keep minSize relatively small to mimic typical use cases,
        # let's pick minSize randomly between 3 and 10
        minSize = random.randint(3, min(10, n))
        maxSize = random.randint(minSize, minSize + 5) # Doesn't actually affect logic but need it for args
        maxLetters = random.randint(1, min(26, minSize))
        
        # The string needs to contain lowercase English letters.
        # If we just pick totally random letters, maxLetters might severely restrict matches.
        # Better to pick from a smaller alphabet sometimes to ensure there are many valid substrings
        # that will actually repeat.
        alphabet_size = random.randint(1, 10)
        alphabet = string.ascii_lowercase[:alphabet_size]
        
        s = "".join(random.choices(alphabet, k=n))
        
        data[n] = {
            "s": s,
            "maxLetters": maxLetters,
            "minSize": minSize,
            "maxSize": maxSize
        }
        
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), "data.json"), "w") as f:
        json.dump(data, f)
        
if __name__ == "__main__":
    generate_data()
