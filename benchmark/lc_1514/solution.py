from typing import List
import collections
import heapq

class Solution:
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start: int, end: int) -> float:
        graph = collections.defaultdict(list)
        for i, (u, v) in enumerate(edges):
            prob = succProb[i]
            graph[u].append((v, prob))
            graph[v].append((u, prob))
        
        # Max heap: store (-probability, node)
        pq = [(-1.0, start)]
        max_prob = [0.0] * n
        max_prob[start] = 1.0
        
        while pq:
            curr_prob, u = heapq.heappop(pq)
            curr_prob = -curr_prob
            
            # If we reached the target, we can return the probability.
            # Since it's a max-heap, the first time we reach the end node,
            # it is guaranteed to be the maximum probability path.
            if u == end:
                return curr_prob
            
            # If the current probability is less than the recorded max probability,
            # skip it.
            if curr_prob < max_prob[u]:
                continue
            
            for v, edge_prob in graph[u]:
                next_prob = curr_prob * edge_prob
                if next_prob > max_prob[v]:
                    max_prob[v] = next_prob
                    heapq.heappush(pq, (-next_prob, v))
                    
        return 0.0
