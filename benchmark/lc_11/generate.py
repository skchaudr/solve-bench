import os
import json
import random

def generate_data():
    scales = [100, 1000, 10000, 100000]
    
    # Let's generate a directory to hold the data
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Task says "values in [-10^9, 10^9]". But height constraints say "0 <= height[i] <= 104" (10^4).
    # I will stick to [0, 10^4] as realistic constraints from the problem description for height,
    # but to stress test and follow the boilerplate prompt literal text ("[-10^9, 10^9]"),
    # I will actually generate up to 10^9 just in case. However, heights can't be negative, 
    # so I'll generate [0, 10^9]. Wait, the task says "Input type: sorted or unsorted integer arrays of length n, values in [-10^9, 10^9]".
    # Negative heights don't make sense for container with most water. Let's just generate [0, 10^9].
    
    for n in scales:
        # Create a mix of random data to avoid any specific worst case being missed
        # 1. Random heights
        data = [random.randint(0, 10**9) for _ in range(n)]
        
        file_path = os.path.join(data_dir, f'input_{n}.json')
        with open(file_path, 'w') as f:
            json.dump(data, f)
            
    print("Data generated successfully.")

if __name__ == '__main__':
    generate_data()
