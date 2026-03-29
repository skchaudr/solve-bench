import json
import os
import random

def generate_data():
    scales = [100, 1000, 10000, 100000]
    data = {}
    
    # Values bounded by typical int32/constraint limits
    # However, the problem specifies values up to 10^5 in constraints, 
    # but the task description mentioned [-10^9, 10^9].
    # So I'll just use [-10**9, 10**9] to follow the description
    min_val = -10**9
    max_val = 10**9
    
    for n in scales:
        arr = [random.randint(min_val, max_val) for _ in range(n)]
        data[str(n)] = arr
        
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), 'data.json'), 'w') as f:
        json.dump(data, f)
        
if __name__ == '__main__':
    generate_data()
