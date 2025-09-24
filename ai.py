import random
from abc import ABC, abstractmethod
from typing import Optional, Tuple, List


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
