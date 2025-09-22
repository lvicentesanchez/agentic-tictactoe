from flask import Flask, render_template, redirect, url_for
from game import TicTacToe

app = Flask(__name__)
game = TicTacToe()


@app.route("/")
def index():
    return render_template(
        "index.html", board=game.board, winner=game.check_winner(), full=game.is_full()
    )


@app.route("/move/<int:row>/<int:col>")
def move(row, col):
    if game.make_move(row, col):
        pass
    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    game.reset()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
