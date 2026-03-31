class Solution:
    def makeConnected(self, n: int, connections: list[list[int]]) -> int:
        if len(connections) < n - 1:
            return -1
            
        parent = list(range(n))
        
        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]
            
        components = n
        for u, v in connections:
            pu = find(u)
            pv = find(v)
            if pu != pv:
                parent[pu] = pv
                components -= 1
                
        return components - 1
