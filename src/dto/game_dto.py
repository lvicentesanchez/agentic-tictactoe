from typing import List, Optional
from dataclasses import dataclass


@dataclass
class MoveRequest:
    """Request model for making a move."""

    row: int
    col: int


@dataclass
class MoveResponse:
    """Response model for move results."""

    success: bool
    game_state: "GameStateResponse"
    message: Optional[str] = None


@dataclass
class GameStateResponse:
    """Response model for game state."""

    board: List[List[str]]
    current_player: str
    mode: Optional[str]
    winner: Optional[str]
    is_full: bool
    ai_thinking: bool = False


@dataclass
class GameModeRequest:
    """Request model for selecting game mode."""

    mode: str


@dataclass
class AIConfigRequest:
    """Request model for AI configuration."""

    strategy_type: str
    symbol: str
    max_depth: int


@dataclass
class ErrorResponse:
    """Standard error response model."""

    error: str
    message: Optional[str] = None
