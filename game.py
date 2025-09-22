class TicTacToe:
    def __init__(self, mode=None):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.mode = mode
        self.winner = None

    def make_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

    def check_winner(self):
        if self.winner:
            return self.winner
        # Check rows, columns, diagonals
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return self.board[0][2]
        return None

    def is_full(self):
        return all(cell != "" for row in self.board for cell in row)

    def reset(self):
        mode = self.mode
        self.__init__(mode)
        self.winner = None

    def ai_move(self):
        import random

        empty = [(i, j) for i in range(3) for j in range(3) if not self.board[i][j]]
        if empty:
            i, j = random.choice(empty)
            self.make_move(i, j)
