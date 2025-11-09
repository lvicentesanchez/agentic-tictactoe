import sys
import os

# Add src to Python path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from services.game_service import GameService
from models.game import AIConfig


class TestGameService:
    """Test cases for GameService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.game_service = GameService()

    def test_create_single_player_game(self):
        """Test creating a single player game."""
        ai_config = AIConfig("minimax", "O", 9)
        game_id = self.game_service.create_new_game("single", ai_config)

        assert game_id is not None
        game_state = self.game_service.get_game_state(game_id)
        assert game_state is not None
        assert game_state.mode == "single"
        assert game_state.current_player == "X"
        assert game_state.winner is None
        assert not game_state.is_full

    def test_create_two_player_game(self):
        """Test creating a two player game."""
        game_id = self.game_service.create_new_game("two", None)

        assert game_id is not None
        game_state = self.game_service.get_game_state(game_id)
        assert game_state is not None
        assert game_state.mode == "two"
        assert game_state.current_player == "X"

    def test_make_valid_move(self):
        """Test making a valid move."""
        game_id = self.game_service.create_new_game("two", None)

        result = self.game_service.make_move(game_id, 0, 0)

        assert result.success
        assert result.message == "Move successful"
        assert result.game_state.board[0][0] == "X"
        assert result.game_state.current_player == "O"

    def test_make_invalid_move_out_of_bounds(self):
        """Test making a move out of bounds."""
        game_id = self.game_service.create_new_game("two", None)

        result = self.game_service.make_move(game_id, 3, 0)

        assert not result.success
        assert "Invalid move coordinates" in result.message

    def test_make_move_occupied_cell(self):
        """Test making a move on an occupied cell."""
        game_id = self.game_service.create_new_game("two", None)

        # First move
        self.game_service.make_move(game_id, 0, 0)

        # Second move on same cell
        result = self.game_service.make_move(game_id, 0, 0)

        assert not result.success
        assert "Cell already occupied" in result.message

    def test_ai_move(self):
        """Test AI making a move."""
        ai_config = AIConfig("random", "O", 9)
        game_id = self.game_service.create_new_game("single", ai_config)

        # Make player move first
        self.game_service.make_move(game_id, 0, 0)

        # AI move
        result = self.game_service.make_ai_move(game_id)

        assert result.success
        assert result.game_state.current_player == "X"

    def test_reset_game(self):
        """Test resetting a game."""
        game_id = self.game_service.create_new_game("two", None)

        # Make some moves
        self.game_service.make_move(game_id, 0, 0)
        self.game_service.make_move(game_id, 1, 1)

        # Reset game
        new_state = self.game_service.reset_game(game_id)

        assert new_state is not None
        assert new_state.current_player == "X"
        assert all(cell == "" for row in new_state.board for cell in row)

    def test_quit_game(self):
        """Test quitting a game."""
        game_id = self.game_service.create_new_game("two", None)

        result = self.game_service.quit_game(game_id)

        assert result is not None
        assert result.winner == "O"  # Current player X quits, O wins

    def test_get_nonexistent_game(self):
        """Test getting a non-existent game."""
        result = self.game_service.get_game_state("nonexistent")

        assert result is None
