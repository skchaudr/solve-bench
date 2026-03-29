import random
import os

def generate_data():
    scales = [100, 1000, 10000, 100000]
    chars = ['Q', 'W', 'E', 'R']
    
    for n in scales:
        # Generate random string of length n with characters 'Q', 'W', 'E', 'R'
        s = "".join(random.choices(chars, k=n))
        
        dir_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(dir_path, f"data_{n}.txt"), "w") as f:
            f.write(s)

if __name__ == "__main__":
    generate_data()
