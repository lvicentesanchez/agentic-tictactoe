from hypothesis import given, strategies as st
from ai import RandomAI

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
