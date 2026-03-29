from typing import List
import heapq

class Solution:
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
            
        def dijkstra(start: int) -> int:
            dist = {start: 0}
            pq = [(0, start)]
            
            while pq:
                d, u = heapq.heappop(pq)
                if d > dist.get(u, float('inf')):
                    continue
                
                for v, w in adj[u]:
                    new_dist = d + w
                    if new_dist <= distanceThreshold:
                        if new_dist < dist.get(v, float('inf')):
                            dist[v] = new_dist
                            heapq.heappush(pq, (new_dist, v))
            
            return len(dist) - 1

        min_reachable = float('inf')
        best_city = -1
        
        for i in range(n):
            reachable = dijkstra(i)
            if reachable <= min_reachable:
                min_reachable = reachable
                best_city = i
                
        return best_city
