class Solution:
    def shortestAlternatingPaths(self, n: int, redEdges: list[list[int]], blueEdges: list[list[int]]) -> list[int]:
        from collections import defaultdict, deque
        
        red_graph = defaultdict(list)
        for u, v in redEdges:
            red_graph[u].append(v)
            
        blue_graph = defaultdict(list)
        for u, v in blueEdges:
            blue_graph[u].append(v)
            
        ans = [-1] * n
        ans[0] = 0
        
        # (node, dist, color)
        q = deque([(0, 0, 0), (0, 0, 1)])
        visited = {(0, 0), (0, 1)}
        
        while q:
            node, dist, color = q.popleft()
            
            if color == 0:
                for nei in red_graph[node]:
                    if (nei, 0) not in visited:
                        visited.add((nei, 0))
                        if ans[nei] == -1:
                            ans[nei] = dist + 1
                        q.append((nei, dist + 1, 1))
            else:
                for nei in blue_graph[node]:
                    if (nei, 1) not in visited:
                        visited.add((nei, 1))
                        if ans[nei] == -1:
                            ans[nei] = dist + 1
                        q.append((nei, dist + 1, 0))
                        
        return ans
