from typing import List

class Solution:
    def minScoreTriangulation(self, values: List[int]) -> int:
        n = len(values)
        dp = [[0] * n for _ in range(n)]
        
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                # Initialize with infinity
                min_score = float('inf')
                for k in range(i + 1, j):
                    score = dp[i][k] + dp[k][j] + values[i] * values[k] * values[j]
                    if score < min_score:
                        min_score = score
                dp[i][j] = min_score
                
        return dp[0][n - 1]
