from typing import List

class Solution:
    def getMaximumGold(self, grid: List[List[int]]) -> int:
        R, C = len(grid), len(grid[0])
        max_gold = 0
        
        # Pre-compute degrees to optimize start positions
        degrees = [[0] * C for _ in range(R)]
        for r in range(R):
            for c in range(C):
                if grid[r][c] > 0:
                    deg = 0
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] > 0:
                            deg += 1
                    degrees[r][c] = deg
                    
        def dfs(r, c, current_gold):
            nonlocal max_gold
            gold = grid[r][c]
            grid[r][c] = 0
            current_gold += gold
            if current_gold > max_gold:
                max_gold = current_gold
                
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] > 0:
                    dfs(nr, nc, current_gold)
                    
            grid[r][c] = gold

        visited_comp = [[False] * C for _ in range(R)]
        
        for r in range(R):
            for c in range(C):
                if grid[r][c] > 0 and not visited_comp[r][c]:
                    # Find all nodes in this connected component
                    comp = []
                    q = [(r, c)]
                    visited_comp[r][c] = True
                    head = 0
                    while head < len(q):
                        cr, cc = q[head]
                        head += 1
                        comp.append((cr, cc))
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nr, nc = cr + dr, cc + dc
                            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] > 0 and not visited_comp[nr][nc]:
                                visited_comp[nr][nc] = True
                                q.append((nr, nc))
                    
                    # Start DFS only from nodes that are endpoints or branching nodes
                    starts = [(cr, cc) for cr, cc in comp if degrees[cr][cc] != 2]
                    
                    # If the component is a closed cycle, all degrees are 2
                    if not starts:
                        starts = [comp[0]]
                        
                    # Also, standard backtracking from all valid starts
                    # but if all nodes are valid (degree 1 or >2), we start from all of them.
                    # This drastically reduces O(N^2) DFS starts on long paths of degree 2.
                    for sr, sc in starts:
                        dfs(sr, sc, 0)
                        
        return max_gold
