import math

def generate_snake_grid(n):
    """
    Generates an R x C grid where exactly n cells contain gold (value=1).
    The cells form a single long non-branching path (snake) to prevent 
    combinatorial explosion and keep the benchmark focused on maximum 
    single-path depth.
    """
    if n == 0:
        return [[0]]
    
    # Calculate a nice bounding box for the snake
    C = max(3, int(math.sqrt(n)))
    R = (n // C + 2) * 2
    grid = [[0] * C for _ in range(R)]
    
    r, c = 0, 0
    direction = 1 # 1 for right, -1 for left
    count = 0
    
    while count < n:
        grid[r][c] = 1
        count += 1
        
        if count == n:
            break
            
        nc = c + direction
        if 0 <= nc < C:
            c = nc
        else:
            # Drop down one row, move over one step, and reverse direction
            r += 1
            grid[r][c] = 1
            count += 1
            if count == n:
                break
            r += 1
            direction *= -1
            
    # Crop empty rows at the bottom
    while len(grid) > 1 and sum(grid[-1]) == 0:
        grid.pop()
            
    return grid
