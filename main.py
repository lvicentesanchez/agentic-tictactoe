from flask import Flask, render_template, redirect, url_for
from game import TicTacToe

app = Flask(__name__)
game = TicTacToe()
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
    return redirect(url_for("game_view"))


@app.route("/game")
def game_view():
    return render_template(
        "index.html",
        board=game.board,
        winner=game.check_winner(),
        full=game.is_full(),
        mode=game_mode,
    )


@app.route("/move/<int:row>/<int:col>")
def move(row, col):
    if game.make_move(row, col):
        pass
    return redirect(url_for("game_view"))


@app.route("/reset")
def reset():
    game.reset()
    return redirect(url_for("game_view"))


if __name__ == "__main__":
    app.run(debug=True)
