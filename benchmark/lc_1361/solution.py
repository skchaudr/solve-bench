from collections import deque

class Solution:
    def validateBinaryTreeNodes(self, n: int, leftChild: list[int], rightChild: list[int]) -> bool:
        in_degree = [0] * n
        
        for i in range(n):
            if leftChild[i] != -1:
                in_degree[leftChild[i]] += 1
                if in_degree[leftChild[i]] > 1:
                    return False
            if rightChild[i] != -1:
                in_degree[rightChild[i]] += 1
                if in_degree[rightChild[i]] > 1:
                    return False
                    
        root = -1
        for i in range(n):
            if in_degree[i] == 0:
                if root == -1:
                    root = i
                else:
                    return False
                    
        if root == -1:
            return False
            
        visited = set()
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            if node in visited:
                return False
            visited.add(node)
            
            if leftChild[node] != -1:
                queue.append(leftChild[node])
            if rightChild[node] != -1:
                queue.append(rightChild[node])
                
        return len(visited) == n
