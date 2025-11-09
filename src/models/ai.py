import random
from abc import ABC, abstractmethod
from typing import Optional, Tuple, List
from ..utils.game_utils import check_winner, is_board_full
from ..services.cache_service import ai_cache


class AIStrategy(ABC):
    @abstractmethod
    def get_move(self, board: List[List[str]]) -> Optional[Tuple[int, int]]:
        """Return a (row, col) tuple for the next move given the current board state."""
        pass


class RandomAI(AIStrategy):
    def get_move(self, board: List[List[str]]) -> Optional[Tuple[int, int]]:
        """Choose a random empty cell."""
        empty = [(i, j) for i in range(3) for j in range(3) if not board[i][j]]
        if empty:
            return random.choice(empty)
        return None


class MinimaxAI(AIStrategy):
    def __init__(self, symbol: str = "O", max_depth: int = 9):
        self.symbol = symbol
        self.max_depth = max_depth

    def get_move(self, board: List[List[str]]) -> Optional[Tuple[int, int]]:
        """Choose the best move using minimax with alpha-beta pruning."""
        # Check cache first
        cached_move = ai_cache.get_move(board, self.symbol)
        if cached_move:
            return cached_move

        best_score = -1000
        best_move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = self.symbol
                    score = self._minimax(board, 0, False, -1000, 1000)
                    board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        # Cache the result
        if best_move:
            ai_cache.store_move(board, self.symbol, best_move)

        return best_move

    def _minimax(
        self,
        board: List[List[str]],
        depth: int,
        is_maximizing: bool,
        alpha: int,
        beta: int,
    ) -> int:
        winner = check_winner(board)
        if winner:
            return 1 if winner == self.symbol else -1
        if is_board_full(board):
            return 0

        if is_maximizing:
            max_eval = -1000
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = self.symbol
                        eval_score = self._minimax(board, depth + 1, False, alpha, beta)
                        board[i][j] = ""
                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = 1000
            opponent = "X" if self.symbol == "O" else "O"
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = opponent
                        eval_score = self._minimax(board, depth + 1, True, alpha, beta)
                        board[i][j] = ""
                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break
            return min_eval
