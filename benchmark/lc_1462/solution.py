from typing import List

class Solution:
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        adj = [[] for _ in range(numCourses)]
        in_degree = [0] * numCourses
        for u, v in prerequisites:
            adj[u].append(v)
            in_degree[v] += 1
            
        q = [i for i in range(numCourses) if in_degree[i] == 0]
        
        ancestors = [1 << i for i in range(numCourses)]
        
        head = 0
        while head < len(q):
            u = q[head]
            head += 1
            for v in adj[u]:
                ancestors[v] |= ancestors[u]
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    q.append(v)
                    
        return [(ancestors[v] & (1 << u)) != 0 for u, v in queries]
