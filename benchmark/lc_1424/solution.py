class Solution:
    def findDiagonalOrder(self, nums: list[list[int]]) -> list[int]:
        groups = []
        for r in range(len(nums)):
            row = nums[r]
            for c in range(len(row)):
                idx = r + c
                if idx == len(groups):
                    groups.append([])
                groups[idx].append(row[c])
        
        res = []
        for g in groups:
            res.extend(reversed(g))
        return res
