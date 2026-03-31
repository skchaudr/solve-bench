import json
import random

def generate_input(n):
    # To avoid returning [] immediately, we need a solvable sequence.
    # We maintain a pool of dry days.
    ans = []
    # simple valid case: interleave rain and dry days for a few lakes
    # We want to stress O(N log N) by having a long list of dry days and many searches.
    # Let's say first half is mostly dry days with some rain, second half is rain.
    # Actually, worst case for bisect is a long list of dry days.
    
    # Let's build a valid sequence.
    lakes = list(range(1, n // 3 + 2))
    events = []
    active = set()
    
    # Add n/2 dry days initially, then rain, then dry, then rain
    # A valid but difficult case:
    # 0, 0, 0, ..., 1, 2, 3, 4, ... then 1, 2, 3, 4
    # Wait, if we have [0, 0, ..., 0] followed by [1, 2, ..., k] followed by [1, 2, ..., k],
    # the first occurrences of [1..k] just fill lakes. 
    # The second occurrences require drying from the initial [0, 0..].
    # But wait, the dry days MUST be between the first and second rain.
    # So sequence: [1..k], [0..k], [1..k]
    # Length is 3k, let k = n/3.
    k = n // 3
    if k == 0:
        return [0] * n
        
    part1 = list(range(1, k + 1))
    part2 = [0] * k
    part3 = list(range(1, k + 1))
    
    seq = part1 + part2 + part3
    # pad to n
    while len(seq) < n:
        seq.append(0)
        
    return seq

def main():
    scales = [100, 1000, 10000, 100000]
    data = {}
    for n in scales:
        data[n] = generate_input(n)
        
    with open("benchmark/lc_1488/dataset.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    main()
