# Tic-Tac-Toe Agent Guidelines

## Commands
- **Install**: `uv sync`
- **Run**: `python main.py` or `uv run python main.py`
- **Test**: No tests configured - add pytest to pyproject.toml for testing
- **Lint**: `uv run ruff check .` and `uv run ruff format .` (run after all changes)

## Code Style
- **Python**: 3.11+, Flask framework, class-based design
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Imports**: Standard library first, then third-party, then local
- **Error Handling**: Check conditions before actions (e.g., valid moves)
- **HTML**: Jinja2 templating, semantic structure
- **CSS**: CSS variables for theming, responsive design
- **JS**: Vanilla JavaScript, DOM manipulation with event listeners

## Commit Policy
- Do not commit changes until explicitly instructed by the user.
- Always run lint and format checks before committing.
- Use descriptive commit messages; if multiple significant changes have been done, include a list of changes.

## Project Structure
- `game.py`: Core TicTacToe class with game logic
- `main.py`: Flask routes and app setup
- `templates/`: Jinja2 HTML templates
- `static/`: CSS and assets