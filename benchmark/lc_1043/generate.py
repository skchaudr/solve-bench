import json
import random
import os

def generate():
    os.makedirs('benchmark/lc_1043', exist_ok=True)
    scales = [100, 1000, 10000, 100000]
    
    for N in scales:
        arr = [random.randint(0, 10**9) for _ in range(N)]
        k = 50 # Keep k constant to test O(N) linear time with respect to N
        with open(f'benchmark/lc_1043/input_{N}.json', 'w') as f:
            json.dump({'arr': arr, 'k': k}, f)

if __name__ == '__main__':
    generate()