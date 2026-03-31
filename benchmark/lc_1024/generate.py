import json
import random
import os

def generate():
    os.makedirs('benchmark/lc_1024', exist_ok=True)
    scales = [100, 1000, 10000, 100000]
    
    for N in scales:
        time = N
        clips = []
        # to guarantee an answer, add segments spanning 0 to N
        for i in range(N):
            start = max(0, i - random.randint(1, 5))
            end = min(N, i + random.randint(1, 5))
            clips.append([start, end])
        
        # shuffle them to make sort meaningful
        random.shuffle(clips)
        
        with open(f'benchmark/lc_1024/input_{N}.json', 'w') as f:
            json.dump({'clips': clips, 'time': time}, f)

if __name__ == '__main__':
    generate()