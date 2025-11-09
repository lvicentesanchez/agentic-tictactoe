import pytest
import factory
from factory import fuzzy
from src.models.game import GameState, AIConfig


class GameStateFactory(factory.Factory):
    """Factory for creating GameState instances."""

    class Meta:
        model = GameState

    board = factory.LazyAttribute(lambda _: [["", "", ""], ["", "", ""], ["", "", ""]])
    current_player = fuzzy.FuzzyChoice(["X", "O"])
    mode = fuzzy.FuzzyChoice([None, "single", "two"])
    winner = None
    is_full = False
    ai_thinking = False


class AIConfigFactory(factory.Factory):
    """Factory for creating AIConfig instances."""

    class Meta:
        model = AIConfig

    strategy_type = fuzzy.FuzzyChoice(["random", "minimax"])
    symbol = fuzzy.FuzzyChoice(["X", "O"])
    max_depth = fuzzy.FuzzyInteger(1, 20)


@pytest.fixture
def game_state():
    """Provide a fresh GameState for testing."""
    return GameStateFactory()


@pytest.fixture
def ai_config():
    """Provide a fresh AIConfig for testing."""
    return AIConfigFactory()
