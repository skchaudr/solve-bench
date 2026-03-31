class Solution:
    def watchedVideosByFriends(self, watchedVideos: list[list[str]], friends: list[list[int]], id: int, level: int) -> list[str]:
        from collections import deque, Counter
        
        n = len(friends)
        q = deque([(id, 0)])
        visited = {id}
        
        target_friends = []
        
        while q:
            node, d = q.popleft()
            if d == level:
                target_friends.append(node)
                continue
            
            for nei in friends[node]:
                if nei not in visited:
                    visited.add(nei)
                    q.append((nei, d + 1))
                    
        counts = Counter()
        for f in target_friends:
            for v in watchedVideos[f]:
                counts[v] += 1
                
        sorted_videos = sorted(counts.keys(), key=lambda x: (counts[x], x))
        
        return sorted_videos
