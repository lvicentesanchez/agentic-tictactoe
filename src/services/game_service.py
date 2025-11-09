from typing import Optional
import uuid
from models.game import GameState, MoveResult, AIConfig
from models.ai import AIStrategy, RandomAI, MinimaxAI
from utils.game_utils import check_winner, is_board_full
from config.settings import settings


class GameService:
    """Service layer for Tic-Tac-Toe game logic."""

    def __init__(self) -> None:
        self.games: dict[str, GameState] = {}
        self.ai_strategies: dict[str, AIStrategy] = {}

    def create_new_game(
        self, mode: Optional[str], ai_config: Optional[AIConfig] = None
    ) -> str:
        """Create a new game and return its ID."""
        game_id = str(uuid.uuid4())

        # Initialize board
        board = [
            ["" for _ in range(settings.board_size)] for _ in range(settings.board_size)
        ]

        # Set up AI strategy if single player mode
        ai_strategy = None
        if mode == "single" and ai_config:
            if ai_config.strategy_type == "random":
                ai_strategy = RandomAI()
            elif ai_config.strategy_type == "minimax":
                ai_strategy = MinimaxAI(ai_config.symbol, ai_config.max_depth)

            if ai_strategy:
                self.ai_strategies[game_id] = ai_strategy

        # Create game state
        game_state = GameState(
            board=board,
            current_player="X",
            mode=mode,
            winner=None,
            is_full=False,
            ai_thinking=False,
        )

        self.games[game_id] = game_state
        return game_id

    def get_game_state(self, game_id: str) -> Optional[GameState]:
        """Get the current state of a game."""
        return self.games.get(game_id)

    def make_move(self, game_id: str, row: int, col: int) -> MoveResult:
        """Make a move in the game."""
        game_state = self.games.get(game_id)
        if not game_state:
            return MoveResult(
                success=False,
                game_state=GameState([], "", None),
                message="Game not found",
            )

        # Validate move
        if not (0 <= row < settings.board_size and 0 <= col < settings.board_size):
            return MoveResult(
                success=False, game_state=game_state, message="Invalid move coordinates"
            )

        if game_state.board[row][col] != "":
            return MoveResult(
                success=False, game_state=game_state, message="Cell already occupied"
            )

        if game_state.winner or game_state.is_full:
            return MoveResult(
                success=False, game_state=game_state, message="Game is already over"
            )

        # Make the move
        game_state.board[row][col] = game_state.current_player

        # Check for winner
        winner = check_winner(game_state.board)
        if winner:
            game_state.winner = winner
        else:
            # Check for full board
            game_state.is_full = is_board_full(game_state.board)

            # Switch player
            if not game_state.is_full:
                game_state.current_player = (
                    "O" if game_state.current_player == "X" else "X"
                )

        return MoveResult(
            success=True, game_state=game_state, message="Move successful"
        )

    def make_ai_move(self, game_id: str) -> MoveResult:
        """Make an AI move."""
        game_state = self.games.get(game_id)
        ai_strategy = self.ai_strategies.get(game_id)

        if not game_state or not ai_strategy:
            return MoveResult(
                success=False,
                game_state=game_state or GameState([], "", None),
                message="AI not available for this game",
            )

        if game_state.winner or game_state.is_full:
            return MoveResult(
                success=False, game_state=game_state, message="Game is already over"
            )

        # Get AI move
        move = ai_strategy.get_move(game_state.board)
        if not move:
            return MoveResult(
                success=False, game_state=game_state, message="No available moves"
            )

        row, col = move
        return self.make_move(game_id, row, col)

    def reset_game(self, game_id: str) -> Optional[GameState]:
        """Reset a game to its initial state."""
        game_state = self.games.get(game_id)
        if not game_state:
            return None

        mode = game_state.mode
        ai_config = None

        # Recreate AI config if needed
        if mode == "single" and game_id in self.ai_strategies:
            ai_strategy = self.ai_strategies[game_id]
            strategy_type = "random" if isinstance(ai_strategy, RandomAI) else "minimax"
            symbol = getattr(ai_strategy, "symbol", "O")
            max_depth = getattr(ai_strategy, "max_depth", settings.ai_max_depth)
            ai_config = AIConfig(strategy_type, symbol, max_depth)

        # Remove old game
        del self.games[game_id]
        if game_id in self.ai_strategies:
            del self.ai_strategies[game_id]

        # Create new game
        new_game_id = self.create_new_game(mode, ai_config)
        new_game_state = self.games[new_game_id]

        # Update the original game ID to maintain continuity
        self.games[game_id] = new_game_state
        if new_game_id in self.ai_strategies:
            self.ai_strategies[game_id] = self.ai_strategies[new_game_id]
            del self.ai_strategies[new_game_id]
        del self.games[new_game_id]

        return new_game_state

    def quit_game(self, game_id: str) -> Optional[GameState]:
        """Mark the current player as the loser and end the game."""
        game_state = self.games.get(game_id)
        if not game_state:
            return None

        if not game_state.winner and not game_state.is_full:
            # Current player quits, so the other player wins
            game_state.winner = "O" if game_state.current_player == "X" else "X"

        return game_state
