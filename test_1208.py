from benchmark.lc_1208.solution import Solution

def run_tests():
    sol = Solution()
    assert sol.equalSubstring("abcd", "bcdf", 3) == 3
    assert sol.equalSubstring("abcd", "cdef", 3) == 1
    assert sol.equalSubstring("abcd", "acde", 0) == 1
    print("All tests passed.")

if __name__ == "__main__":
    run_tests()
