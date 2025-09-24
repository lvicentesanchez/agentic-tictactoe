from hypothesis import given, strategies as st
from ai import RandomAI, MinimaxAI

board_strategy = st.lists(
    st.lists(st.sampled_from(["", "X", "O"]), min_size=3, max_size=3),
    min_size=3,
    max_size=3,
)


@given(board=board_strategy)
def test_random_ai_never_picks_occupied(board):
    ai = RandomAI()
    move = ai.get_move(board)
    if move is not None:
        row, col = move
        assert board[row][col] == "", f"AI picked occupied cell at {row},{col}"


@given(board=board_strategy)
def test_minimax_ai_never_picks_occupied(board):
    ai = MinimaxAI()
    move = ai.get_move(board)
    if move is not None:
        row, col = move
        assert board[row][col] == "", f"AI picked occupied cell at {row},{col}"


def test_minimax_ai_wins_when_possible():
    ai = MinimaxAI("O")
    board = [["O", "O", ""], ["", "", ""], ["", "", ""]]
    move = ai.get_move(board)
    assert move == (0, 2)


def test_minimax_ai_blocks_opponent_win():
    ai = MinimaxAI("O")
    board = [["X", "X", ""], ["", "", ""], ["", "", ""]]
    move = ai.get_move(board)
    assert move == (0, 2)
