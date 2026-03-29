import time
import random

def minScoreTriangulation(values):
    n = len(values)
    dp = [[0] * n for _ in range(n)]
    
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = min(dp[i][k] + dp[k][j] + values[i]*values[k]*values[j] for k in range(i+1, j))
            
    return dp[0][n-1]

for n in [50, 100, 150, 200, 300, 400]:
    v = [random.randint(1, 100) for _ in range(n)]
    t0 = time.time()
    minScoreTriangulation(v)
    t1 = time.time()
    print(f"N={n}, time={t1-t0:.4f}s")
