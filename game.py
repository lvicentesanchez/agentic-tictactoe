from typing import Optional
from ai import AIStrategy
import game_utils as gu


class TicTacToe:
    def __init__(self, mode=None, ai_strategy: Optional[AIStrategy] = None):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.mode = mode
        self.ai_strategy = ai_strategy
        self.winner = None

    def make_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

    def check_winner(self):
        if self.winner:
            return self.winner
        self.winner = gu.check_winner(self.board)
        return self.winner

    def is_full(self):
        return gu.is_board_full(self.board)

    def reset(self):
        mode = self.mode
        ai_strategy = self.ai_strategy
        self.__init__(mode, ai_strategy)
        self.winner = None

    def ai_move(self):
        if self.ai_strategy:
            move = self.ai_strategy.get_move(self.board)
            if move:
                self.make_move(*move)
