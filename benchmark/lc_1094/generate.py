import json
import random
import os

def generate_data():
    scales = [100, 1000, 10000, 100000]
    data = {}
    
    # Generate datasets that will pass the capacity check to test the algorithm's full execution path.
    # We set a very large capacity so the algorithm does not terminate early.
    for n in scales:
        trips = []
        # Max location can be 1000 as per constraints, but for n=100000, we can increase the location span
        # to make it more spread out and realistic for the heap operations.
        # Actually, let's keep constraints flexible since the algorithm time complexity doesn't strictly depend on location bounds, 
        # but spreading locations helps the heap have a non-trivial size. Let's use 0 to 1,000,000 for large n.
        max_loc = max(1000, n * 10)
        
        for _ in range(n):
            num_passengers = random.randint(1, 100)
            start = random.randint(0, max_loc - 1)
            end = random.randint(start + 1, max_loc)
            trips.append([num_passengers, start, end])
        
        # Max capacity needed to guarantee True: N * 100
        capacity = n * 100 + 1 
        
        data[str(n)] = {
            "trips": trips,
            "capacity": capacity
        }
    
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), "dataset.json"), "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    generate_data()
