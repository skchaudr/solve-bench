import json
import os

def generate():
    os.makedirs('benchmark/lc_1238', exist_ok=True)
    scales = [100, 1000, 10000, 100000]
    
    for N in scales:
        if N == 100:
            n = 7
        elif N == 1000:
            n = 10
        elif N == 10000:
            n = 13
        elif N == 100000:
            n = 17
        
        start = 3 # arbitrary valid start
        
        with open(f'benchmark/lc_1238/input_{N}.json', 'w') as f:
            json.dump({'n': n, 'start': start}, f)

if __name__ == '__main__':
    generate()