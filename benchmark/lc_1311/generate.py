import json
import random
import string

def generate():
    scales = [100, 1000, 10000, 100000]
    data = {}
    
    videos = ["".join(random.choices(string.ascii_uppercase, k=3)) for _ in range(100)]
    
    for n in scales:
        watchedVideos = []
        friends = [[] for _ in range(n)]
        
        for i in range(1, n):
            parent = random.randint(0, i - 1)
            friends[i].append(parent)
            friends[parent].append(i)
            
        for _ in range(n // 2):
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and v not in friends[u]:
                friends[u].append(v)
                friends[v].append(u)
                
        for i in range(n):
            num_vids = random.randint(1, 5)
            watchedVideos.append(random.sample(videos, num_vids))
            
        target_id = 0
        level = 5
        
        data[n] = {
            "watchedVideos": watchedVideos,
            "friends": friends,
            "id": target_id,
            "level": level,
            "n": n
        }
        
    with open("dataset.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    generate()
