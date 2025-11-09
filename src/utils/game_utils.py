from typing import List, Optional


def check_winner(board: List[List[str]]) -> Optional[str]:
    """Check if there is a winner on the board."""
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
    # Check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    return None


def is_board_full(board: List[List[str]]) -> bool:
    """Check if the board is full."""
    return all(cell != "" for row in board for cell in row)
