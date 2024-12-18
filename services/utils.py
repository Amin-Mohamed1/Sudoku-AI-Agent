def generate_variables():
    # R1C1, R1C2, ..., R1C9, R2C1, R2C2, ..., R2C9, ..., R9C9
    variables = []
    for row in range(1, 10):
        for col in range(1, 10):
            variables.append(f'R{row}C{col}')
    return variables

def generate_domains(initial_board):
    domains = {}
    for row in range(1, 10):
        for col in range(1, 10):
            var = f'R{row}C{col}'
            value = initial_board[row - 1][col - 1]
            if value != 0:
                # if already assigned
                domains[var] = [str(value)]
            else:
                # add the whole domain as it's empty
                domains[var] = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    return domains


def generate_neighbors():
    # R1C1 : {R1C2, R1C3, ..., R1C9, R2C1, R3C1, ..., R9C1, ... R2C2, R2C3, R3C2, R3C3}
    neighbors = {}
    def get_subgrid_neighbors(row_index, col_index):
        subgrid_neighbors3x3 = []
        subgrid_row_start = (row_index - 1) // 3 * 3 + 1
        subgrid_col_start = (col_index - 1) // 3 * 3 + 1
        for r in range(subgrid_row_start, subgrid_row_start + 3):
            for c in range(subgrid_col_start, subgrid_col_start + 3):
                if r != row_index or c != col_index:
                    subgrid_neighbors3x3.append(f'R{r}C{c}')
        return subgrid_neighbors3x3

    for row in range(1, 10):
        for col in range(1, 10):
            var = f'R{row}C{col}'
            row_neighbors = [f'R{row}C{i}' for i in range(1, 10) if i != col]
            col_neighbors = [f'R{i}C{col}' for i in range(1, 10) if i != row]
            subgrid_neighbors = get_subgrid_neighbors(row, col)
            # to remove the repeated neighbours
            all_neighbors = set(row_neighbors + col_neighbors + subgrid_neighbors)
            neighbors[var] = list(all_neighbors)
    return neighbors
