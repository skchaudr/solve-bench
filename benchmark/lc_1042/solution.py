from typing import List

class Solution:
    def gardenNoAdj(self, n: int, paths: List[List[int]]) -> List[int]:
        graph = [[] for _ in range(n)]
        for u, v in paths:
            graph[u - 1].append(v - 1)
            graph[v - 1].append(u - 1)
            
        ans = [0] * n
        for i in range(n):
            used_colors = set(ans[neighbor] for neighbor in graph[i] if ans[neighbor] != 0)
            for color in range(1, 5):
                if color not in used_colors:
                    ans[i] = color
                    break
                    
        return ans
