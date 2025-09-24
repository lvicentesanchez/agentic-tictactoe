from flask import Flask, render_template, redirect, url_for
from game import TicTacToe
from ai import RandomAI

app = Flask(__name__)
ai_strategy = RandomAI()
game = TicTacToe(ai_strategy=ai_strategy)
game_mode = None


@app.route("/")
def index():
    if game_mode is None:
        return redirect(url_for("mode_select"))
    return redirect(url_for("game_view"))


@app.route("/mode_select")
def mode_select():
    global game_mode
    game_mode = None
    game.reset()
    return render_template("mode_select.html")


@app.route("/select_mode/<mode>")
def select_mode(mode):
    global game_mode
    game_mode = mode
    game.mode = mode
    game.reset()
    game.current_player = "X"  # Human starts first
    return redirect(url_for("game_view"))


@app.route("/game")
def game_view():
    ai_turn = (
        game_mode == "single"
        and game.current_player == "O"
        and not game.check_winner()
        and not game.is_full()
    )
    return render_template(
        "index.html",
        board=game.board,
        winner=game.check_winner(),
        full=game.is_full(),
        mode=game_mode,
        game=game,
        ai_turn=ai_turn,
        ai_thinking=False,
    )


@app.route("/move/<int:row>/<int:col>")
def move(row, col):
    if game.make_move(row, col):
        winner = game.check_winner()
        full = game.is_full()
        if game_mode == "single" and not winner and not full:
            ai_turn = True
            return render_template(
                "index.html",
                board=game.board,
                winner=winner,
                full=full,
                mode=game_mode,
                game=game,
                ai_turn=ai_turn,
                ai_thinking=True,
            )
    return redirect(url_for("game_view"))


@app.route("/reset")
def reset():
    game.reset()
    return redirect(url_for("game_view"))


@app.route("/quit")
def quit_game():
    if not game.check_winner() and not game.is_full():
        game.winner = "O" if game.current_player == "X" else "X"
    return redirect(url_for("game_view"))


@app.route("/ai_move")
def ai_move():
    game.ai_move()
    return redirect(url_for("game_view"))


if __name__ == "__main__":
    app.run(debug=True)
