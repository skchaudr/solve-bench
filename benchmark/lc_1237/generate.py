import sys
import os

# To ensure the benchmark can find the solution interface
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1237.solution import CustomFunction

class MockCustomFunction(CustomFunction):
    def __init__(self, formula_type, z):
        self.formula_type = formula_type
        self.z = z

    def f(self, x: int, y: int) -> int:
        if self.formula_type == 1:
            return x + y
        elif self.formula_type == 2:
            return x * y
        elif self.formula_type == 3:
            return x * x + y * y
        elif self.formula_type == 4:
            return x * x + x * y + y * y
        else:
            return x + y

def generate_data(n: int):
    # Here n acts as z to stretch the scale to 100, 1000, 10000, 100000.
    # The constraints in the problem usually have x, y in [1, 1000] and z in [1, 100].
    # But to test the complexity properly as requested we test up to 100000.
    # We will use formula_type = 1 to have z length paths evaluated.
    return {
        "customfunction": MockCustomFunction(formula_type=1, z=n),
        "z": n
    }

if __name__ == "__main__":
    data = generate_data(100)
    print("z =", data["z"])
    print("f(1, z-1) =", data["customfunction"].f(1, data["z"]-1))
