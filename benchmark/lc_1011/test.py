from solution import Solution

def test():
    sol = Solution()
    print(sol.shipWithinDays([1,2,3,4,5,6,7,8,9,10], 5) == 15)
    print(sol.shipWithinDays([3,2,2,4,1,4], 3) == 6)
    print(sol.shipWithinDays([1,2,3,1,1], 4) == 3)

if __name__ == "__main__":
    test()
