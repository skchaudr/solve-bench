from typing import List

class CustomFunction:
    # Interface only for type hinting in Solution
    def f(self, x: int, y: int) -> int:
        pass

class Solution:
    def findSolution(self, customfunction: CustomFunction, z: int) -> List[List[int]]:
        res = []
        x = 1
        y = z
        while x <= z and y >= 1:
            val = customfunction.f(x, y)
            if val == z:
                res.append([x, y])
                x += 1
                y -= 1
            elif val < z:
                x += 1
            else:
                y -= 1
        return res
