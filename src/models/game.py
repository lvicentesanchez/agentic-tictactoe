from typing import List, Optional
from dataclasses import dataclass


@dataclass
class GameState:
    """Represents the current state of a Tic-Tac-Toe game."""

    board: List[List[str]]
    current_player: str
    mode: Optional[str]
    winner: Optional[str] = None
    is_full: bool = False
    ai_thinking: bool = False


@dataclass
class MoveResult:
    """Represents the result of a move attempt."""

    success: bool
    game_state: GameState
    message: Optional[str] = None


@dataclass
class AIConfig:
    """Configuration for AI players."""

    strategy_type: str
    symbol: str = "O"
    max_depth: int = 9
    cache_enabled: bool = True
