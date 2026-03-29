import random
import sys

sys.setrecursionlimit(2000000)

def generate_test_case(n):
    # To test a generalized case, we generate a tree.
    # We want a balanced tree to keep depth O(log N) and avoid stack overflows
    arr = sorted(random.sample(range(1, 10**9 + 1), n))

    res = []

    def dfs(left, right):
        if left > right:
            return
        m = (left + right) // 2
        res.append(arr[m])
        dfs(left, m - 1)
        dfs(m + 1, right)

    dfs(0, len(arr) - 1)
    return res
