import random

from adapter import board_adapter
from modules.CSP import CSP


def solve_sudoku(grid: list[list[int]]) -> list[list[int]]:
    csp = CSP(grid)
    if csp.ac3():
        solution = csp.backtracking_search()
        if solution:
            print("Solution found:\n")
            return board_adapter.adapt_map_to_2d_list(solution)
        else:
            print("No solution found")
    else:
        print("No solution found")

def generate_random_unique_sudoku(difficulty: str) -> list[list[int]]:
    board: list[list[int]] = [[0 for _ in range(9)] for _ in range(9)]
    csp = CSP(board)
    return __remove_cells(
        board_adapter.adapt_map_to_2d_list(csp.backtracking_search()),
        difficulty)

def is_board_solvable(grid: list[list[int]]) -> bool:
    validator: CSP = CSP(grid)
    return True if validator.backtracking_search() else False

def is_board_uniquely_solvable(grid: list[list[int]]) -> bool:
    validator: CSP = CSP(grid)
    return True if len(validator.find_all_solutions()) == 1 else False

def __remove_cells(board: list[list[int]], difficulty: str) -> list[list[int]]:
    difficulty_cells_to_remove = {
        "Easy": 40,
        "Medium": 50,
        "Hard": 60
    }
    cells_to_remove = difficulty_cells_to_remove[difficulty]
    puzzle = board_adapter.adapt_2d_list_to_map(board)

    removal_order = list(puzzle.keys())
    random.shuffle(removal_order)

    for cell in removal_order:
        if cells_to_remove == 0:
            break

        original_value = puzzle[cell]
        puzzle[cell] = " "

        board = board_adapter.adapt_map_to_2d_list(puzzle)
        csp = CSP(board)
        solutions = csp.find_all_solutions()

        if len(solutions) > 1:
            puzzle[cell] = original_value
        else:
            cells_to_remove -= 1

    return board_adapter.adapt_map_to_2d_list(puzzle)