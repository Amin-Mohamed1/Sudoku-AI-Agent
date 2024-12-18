class ArcConsistencyService:
    @staticmethod
    def check_consistency(sudoku_grid):
        # Step 1: Convert 2D array to 3D array (domains)
        n, m = len(sudoku_grid), len(sudoku_grid[0])
        three_d_array = [[[val] if val != 0 else list(range(1, 10)) for val in row] for row in sudoku_grid]

        # Step 2: Arc Consistency Logic
        while True:
            flag = False

            for i in range(n):
                for j in range(m):
                    x = three_d_array[i][j]  # Domain of (i, j)

                    if len(x) == 0:
                        continue

                    for k in range(n):
                        for l in range(m):
                            is_neighbor = ArcConsistencyService.__is_on_same_row_or_column(i, j, k, l) or \
                                          ArcConsistencyService.__is_on_same_box(i, j, k, l)

                            if is_neighbor:
                                y = three_d_array[k][l]
                                if len(y) == 1:
                                    z = y[0]
                                    if z in x:
                                        x.remove(z)
                                        flag = True

                                        if not x:
                                            return False, None  # No solution exists

            if not flag:
                break

        # Step 3: Backtracking to solve the grid
        solved, result = ArcConsistencyService.__backtracking_solver(three_d_array)
        return solved, result

    @staticmethod
    def __backtracking_solver(grid):
        for i in range(9):
            for j in range(9):
                if len(grid[i][j]) > 1:
                    for value in grid[i][j]:
                        new_grid = [row[:] for row in grid]
                        new_grid[i][j] = [value]
                        consistent, result = ArcConsistencyService.check_consistency(
                            [[cell[0] if len(cell) == 1 else 0 for cell in row] for row in new_grid]
                        )

                        if consistent:
                            return True, result

                    return False, None
        solved_grid = [[cell[0] if len(cell) == 1 else 0 for cell in row] for row in grid]
        return True, solved_grid

    @staticmethod
    def __is_on_same_row_or_column(i, j, k, l):
        return (i == k or j == l) and (i != k or j != l)

    @staticmethod
    def __is_on_same_box(i, j, k, l):
        return (i // 3 == k // 3 and j // 3 == l // 3) and (i != k or j != l)

if __name__ == '__main__':
    normal_grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    arc = ArcConsistencyService()
    solvable, solved_grid = arc.check_consistency(normal_grid)

    print("Solvable:", solvable)
    if solved_grid is not None:
        for row in solved_grid:
            print(row)
