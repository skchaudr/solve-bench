class Solution:
    def longestDiverseString(self, a: int, b: int, c: int) -> str:
        import heapq
        pq = []
        if a > 0: heapq.heappush(pq, (-a, 'a'))
        if b > 0: heapq.heappush(pq, (-b, 'b'))
        if c > 0: heapq.heappush(pq, (-c, 'c'))
        
        res = []
        while pq:
            cnt, char = heapq.heappop(pq)
            if len(res) >= 2 and res[-1] == char and res[-2] == char:
                if not pq:
                    break
                cnt2, char2 = heapq.heappop(pq)
                res.append(char2)
                cnt2 += 1
                if cnt2 < 0:
                    heapq.heappush(pq, (cnt2, char2))
                heapq.heappush(pq, (cnt, char))
            else:
                res.append(char)
                cnt += 1
                if cnt < 0:
                    heapq.heappush(pq, (cnt, char))
        return "".join(res)
