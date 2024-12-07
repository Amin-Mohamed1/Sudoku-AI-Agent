class ArcConsistencyService:
    @staticmethod
    def check_consistency(sudoko_grid):
        # Step 1: Convert 2D array to 3D array
        n, m = len(sudoko_grid), len(sudoko_grid[0])
        three_d_array = [[[val] if val != 0 else list(range(1, 10)) for val in row] for row in sudoko_grid]

        # Step 2: Start consistency logic
        while True:
            flag = False  # Flag to track if any changes were made

            # Double loop to iterate over the 2D array
            for i in range(n):
                for j in range(m):
                    x = three_d_array[i][j]  # Current list for (i, j)

                    # Double loop to iterate over the 2D array for neighbors
                    for k in range(n):
                        for l in range(m):
                            # Check if (k, l) is a neighbor of (i, j)


                            is_on_same_row_or_column = ArcConsistencyService.__is_on_same_row_or_column(i, j, k, l)
                            is_on_same_box = ArcConsistencyService.__is_on_same_box(i, j, k, l)
                            if is_on_same_row_or_column or is_on_same_box :
                                y = three_d_array[k][l]  # Neighbor list for (k, l)

                                # If the neighbor has only one value, remove it from the current list
                                if len(y) == 1:
                                    z = y[0]
                                    if z in x:
                                        x.remove(z)
                                        # if len(x) == 1:
                                        flag = True  # A change was made

                                        # If the current list becomes empty, return False
                                        if not x:
                                            print(i, j, k, l)
                                            return False, None

            # If no changes were made in this iteration, break the loop
            if not flag:
                break

        # Step 3: Reconstruct the 2D array from the 3D array
        result_2d = [[cell[0] if len(cell) == 1 else 0 for cell in row] for row in three_d_array]

        return True, result_2d

    @staticmethod
    def __is_on_same_row_or_column(i, j, k, l):
        is_not_same_element = ArcConsistencyService.__is_not_same_element(i, j, k, l)
        return (i == k or j == l) and is_not_same_element

    @staticmethod
    def __is_on_same_box(i, j, k, l):
        is_not_same_element = ArcConsistencyService.__is_not_same_element(i, j , k, l)
        i = i/3
        j = j/3
        k = k/3
        l = l/3
        return i == k and j == l and is_not_same_element

    @staticmethod
    def __is_not_same_element(i, j, k, l):
        return not(i == k and j == l)

if __name__ =='__main__':
    grid = [
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

    hi, bro = arc.check_consistency(grid)
    for row in bro:
        print(row)