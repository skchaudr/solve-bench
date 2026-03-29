from typing import List
from collections import deque

class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        adj = [[] for _ in range(n)]
        for u, v in connections:
            adj[u].append((v, 1))
            adj[v].append((u, 0))
            
        changes = 0
        queue = deque([0])
        visited = [False] * n
        visited[0] = True
        
        while queue:
            u = queue.popleft()
            for v, cost in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    changes += cost
                    queue.append(v)
                    
        return changes
