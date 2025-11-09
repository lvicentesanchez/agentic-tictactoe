from flask import Flask, render_template, redirect, url_for
from flask_cors import CORS
from src.services.game_service import GameService
from src.models import AIConfig
from src.config.settings import settings

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure app
app.config["DEBUG"] = settings.debug
app.config["SECRET_KEY"] = (
    "your-secret-key-here"  # In production, use environment variable
)

# Initialize services
game_service = GameService()

# Global game state for simple web interface
current_game_id = None


@app.route("/")
def index():
    """Home page - redirect to mode selection if no game is active."""
    global current_game_id
    if current_game_id is None:
        return redirect(url_for("mode_select"))
    return redirect(url_for("game_view"))


@app.route("/mode_select")
def mode_select():
    """Game mode selection page."""
    global current_game_id
    current_game_id = None
    return render_template("mode_select.html")


@app.route("/select_mode/<mode>")
def select_mode(mode):
    """Select game mode and create new game."""
    global current_game_id

    if mode not in ["single", "two"]:
        return redirect(url_for("mode_select"))

    # Create AI config for single player mode
    ai_config = None
    if mode == "single":
        ai_config = AIConfig(
            strategy_type="minimax", symbol="O", max_depth=settings.ai_max_depth
        )

    current_game_id = game_service.create_new_game(mode, ai_config)
    return redirect(url_for("game_view"))


@app.route("/game")
def game_view():
    """Main game view."""
    global current_game_id

    if current_game_id is None:
        return redirect(url_for("mode_select"))

    game_state = game_service.get_game_state(current_game_id)
    if not game_state:
        return redirect(url_for("mode_select"))

    # Check if it's AI's turn
    ai_turn = (
        game_state.mode == "single"
        and game_state.current_player == "O"
        and not game_state.winner
        and not game_state.is_full
    )

    return render_template(
        "index.html",
        game_id=current_game_id,
        board=game_state.board,
        winner=game_state.winner,
        full=game_state.is_full,
        mode=game_state.mode,
        current_player=game_state.current_player,
        ai_turn=ai_turn,
        ai_thinking=False,
    )


@app.route("/move/<int:row>/<int:col>")
def move(row, col):
    """Handle player move."""
    global current_game_id

    if current_game_id is None:
        return redirect(url_for("mode_select"))

    result = game_service.make_move(current_game_id, row, col)
    game_state = result.game_state

    if game_state.mode == "single" and not game_state.winner and not game_state.is_full:
        # AI's turn
        ai_turn = True
        return render_template(
            "index.html",
            game_id=current_game_id,
            board=game_state.board,
            winner=game_state.winner,
            full=game_state.is_full,
            mode=game_state.mode,
            current_player=game_state.current_player,
            ai_turn=ai_turn,
            ai_thinking=True,
        )

    return redirect(url_for("game_view"))


@app.route("/ai_move")
def ai_move():
    """Handle AI move."""
    global current_game_id

    if current_game_id is None:
        return redirect(url_for("mode_select"))

    game_service.make_ai_move(current_game_id)
    return redirect(url_for("game_view"))


@app.route("/reset")
def reset():
    """Reset current game."""
    global current_game_id

    if current_game_id is not None:
        game_service.reset_game(current_game_id)

    return redirect(url_for("game_view"))


@app.route("/quit")
def quit_game():
    """Quit current game."""
    global current_game_id

    if current_game_id is not None:
        game_service.quit_game(current_game_id)

    return redirect(url_for("game_view"))


@app.route("/api/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    app.run(host=settings.host, port=settings.port, debug=settings.debug)
