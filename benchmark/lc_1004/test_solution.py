from solution import Solution

def test_longestOnes():
    s = Solution()
    assert s.longestOnes([1,1,1,0,0,0,1,1,1,1,0], 2) == 6
    assert s.longestOnes([0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], 3) == 10
    print("All tests passed.")

if __name__ == "__main__":
    test_longestOnes()
