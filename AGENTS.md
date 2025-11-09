# Tic-Tac-Toe Agent Guidelines

## Commands
- **Install**: `uv sync`
- **Run**: `python main.py` or `uv run python main.py`
- **Test**: `uv run pytest` (all tests) or `uv run pytest test_ai.py::test_function_name` (single test)
- **Lint**: `uv run ruff check .` and `uv run ruff format .` (run after all changes)

**Important**: Never run the Flask app (`python main.py`) inside opencode as it will block the session.

## Code Style
- **Python**: 3.11+, Flask framework, class-based design, type hints required
- **Naming**: snake_case for functions/variables, PascalCase for classes, UPPER_CASE for constants
- **Imports**: Standard library first, then third-party, then local (alphabetical within groups)
- **Types**: Use `typing` module, `Optional[T]` for nullable types, `List[List[str]]` for boards
- **Error Handling**: Check conditions before actions (e.g., valid moves), return `False`/`None` on failure
- **Testing**: Use pytest with hypothesis for property-based testing
- **HTML**: Jinja2 templating, semantic structure
- **CSS**: CSS variables for theming, responsive design
- **JS**: Vanilla JavaScript, DOM manipulation with event listeners

## Commit Policy
- Do not commit changes until explicitly instructed by the user.
- Always run lint and format checks before committing.
- Always run tests before committing.
- Use descriptive commit messages; if multiple significant changes have been done, include a list of changes.
- Do not open pull requests unless explicitly instructed by the user.

## Project Structure
- `game.py`: Core TicTacToe class with game logic
- `main.py`: Flask routes and app setup
- `ai.py`: AI strategy implementations (RandomAI, MinimaxAI)
- `game_utils.py`: Utility functions for game logic
- `test_ai.py`: AI tests with hypothesis property-based testing
- `templates/`: Jinja2 HTML templates
- `static/`: CSS and assets