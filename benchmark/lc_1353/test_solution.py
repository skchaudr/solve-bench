from solution import Solution

def test_solution():
    sol = Solution()
    # Example 1
    events1 = [[1,2],[2,3],[3,4]]
    assert sol.maxEvents(events1) == 3
    # Example 2
    events2 = [[1,2],[2,3],[3,4],[1,2]]
    assert sol.maxEvents(events2) == 4
    print("All tests passed!")

if __name__ == "__main__":
    test_solution()
