def adapt_map_to_2d_list(board_map: dict) -> list[list[int]]:
    return [
        [int(board_map[f"R{r + 1}C{c + 1}"])
         if board_map[f"R{r + 1}C{c + 1}"] != " "
         else 0 for c in range(9)]
        for r in range(9)]

def adapt_2d_list_to_map(board: list[list[int]]) -> dict:
    return {f"R{r + 1}C{c + 1}": str(board[r][c])
            for r in range(9) for c in range(9)}