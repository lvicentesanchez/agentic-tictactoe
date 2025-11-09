# Tic-Tac-Toe Agent Guidelines

## Commands
- **Install**: `uv sync`
- **Run**: `python main_refactored.py` or `uv run python main_refactored.py`
- **Test**: `uv run pytest` (all tests) or `uv run pytest tests/test_game_service.py::TestGameService::test_create_single_player_game` (single test)
- **Lint**: `uv run ruff check .` and `uv run ruff format .` (run after all changes)
- **Type Check**: `uv run mypy src/` (static type checking)
- **Coverage**: `uv run pytest --cov=src --cov-report=html` (coverage report)
- **Pre-commit**: `uv run pre-commit run --all-files` (run all hooks)

**Important**: Never run the Flask app (`python main_refactored.py`) inside opencode as it will block the session.

## Code Style
- **Python**: 3.11+, Flask framework, class-based design, type hints required
- **Naming**: snake_case for functions/variables, PascalCase for classes, UPPER_CASE for constants
- **Imports**: Standard library first, then third-party, then local (alphabetical within groups)
- **Types**: Use `typing` module, `Optional[T]` for nullable types, `List[List[str]]` for boards
- **Error Handling**: Check conditions before actions (e.g., valid moves), return `False`/`None` on failure
- **Testing**: Use pytest with factory-boy for test data, hypothesis for property-based testing
- **Logging**: Use structlog for structured logging
- **Metrics**: Use prometheus-client for metrics collection
- **HTML**: Jinja2 templating, semantic structure
- **CSS**: CSS variables for theming, responsive design
- **JS**: Vanilla JavaScript, DOM manipulation with event listeners

## Commit Policy
- Do not commit changes until explicitly instructed by the user.
- Always run lint and format checks before committing.
- Always run tests and type checking before committing.
- Use descriptive commit messages; if multiple significant changes have been done, include a list of changes.
- Do not open pull requests unless explicitly instructed by the user.

## Project Structure
```
src/
├── api/
│   ├── routes/          # Flask route definitions
│   └── middleware/     # Request/response middleware
├── services/
│   ├── game_service.py  # Core game business logic
│   └── cache_service.py # AI move caching
├── models/
│   ├── game.py         # Game state dataclasses
│   └── ai.py           # AI strategy implementations
├── dto/
│   └── game_dto.py     # Data transfer objects
├── utils/
│   ├── game_utils.py   # Game utility functions
│   ├── logging.py      # Structured logging setup
│   └── metrics.py      # Prometheus metrics
└── config/
    └── settings.py     # Application configuration
tests/
├── factories.py        # Test data factories
└── test_game_service.py # Service layer tests
templates/              # Jinja2 HTML templates
static/                 # CSS and assets
main_refactored.py      # Refactored Flask application
```

## Development Workflow
1. Make changes to code in `src/` directory
2. Run tests: `uv run pytest`
3. Run linting: `uv run ruff check . && uv run ruff format .`
4. Run type checking: `uv run mypy src/`
5. Check coverage: `uv run pytest --cov=src`
6. Run pre-commit hooks: `uv run pre-commit run --all-files`