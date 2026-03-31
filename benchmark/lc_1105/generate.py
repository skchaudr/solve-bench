import json
import random
import os

def generate():
    os.makedirs('benchmark/lc_1105', exist_ok=True)
    scales = [100, 1000, 10000, 100000]
    
    for N in scales:
        shelfWidth = 100
        # Average books per shelf will be roughly ~100/10 = 10
        books = [[random.randint(5, 15), random.randint(10, 50)] for _ in range(N)]
        
        with open(f'benchmark/lc_1105/input_{N}.json', 'w') as f:
            json.dump({'books': books, 'shelfWidth': shelfWidth}, f)

if __name__ == '__main__':
    generate()