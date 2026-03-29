import json
import os
import random
import string

def generate_data():
    scales = [100, 1000, 10000, 100000]
    out_dir = os.path.dirname(__file__)
    
    # We will generate a base pattern
    pattern = "HelloWorld"
    
    for n in scales:
        queries = []
        for _ in range(n):
            # 50% chance to match the pattern
            if random.random() < 0.5:
                # generate a matching query
                query = ""
                for char in pattern:
                    # Insert some random lowercase letters before the uppercase
                    num_lower = random.randint(1, 5)
                    query += ''.join(random.choices(string.ascii_lowercase, k=num_lower))
                    query += char
                # Add trailing lowercase
                num_lower = random.randint(1, 5)
                query += ''.join(random.choices(string.ascii_lowercase, k=num_lower))
                queries.append(query)
            else:
                # generate a non-matching query
                query = ""
                # maybe missing a pattern char, or has an extra uppercase
                if random.random() < 0.5:
                    # Extra uppercase
                    for char in pattern:
                        num_lower = random.randint(1, 5)
                        query += ''.join(random.choices(string.ascii_lowercase, k=num_lower))
                        query += char
                    query += random.choice(string.ascii_uppercase)
                else:
                    # Missing a pattern char
                    for char in pattern[:-1]:
                        num_lower = random.randint(1, 5)
                        query += ''.join(random.choices(string.ascii_lowercase, k=num_lower))
                        query += char
                queries.append(query)
                
        out_file = os.path.join(out_dir, f"data_{n}.json")
        with open(out_file, "w") as f:
            json.dump({"queries": queries, "pattern": pattern}, f)

if __name__ == "__main__":
    generate_data()
