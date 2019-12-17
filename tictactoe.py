from dataclasses import dataclass

winPatterns = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


@dataclass
class GameState():
    board: tuple = (0, 0, 0, 0, 0, 0, 0, 0, 0)

    def nextStates(self):
        if self.winner() is not None:
            return []
        return [
            GameState(board=tuple(
                self.board[i] if x != i else self.turn()
                for i in range(9)
            ))
            for x in range(9)
            if self.board[x] == 0
        ]

    def turn(self):
        if sum(x != 0 for x in self.board) % 2 == 0:
            return 1
        else:
            return -1

    def winner(self):
        for l in winPatterns:
            a, b, c = l
            if (self.board[a]
                    == self.board[b]
                    == self.board[c]
                    and self.board[a] != 0):
                return self.board[a]  # some player wins
        if sum(x != 0 for x in self.board) == 9:
            return 0  # DRAW
        # no one wins
        return None

    def __hash__(self):
        return hash(self.board)
    
    def print(self):
        d = {0 : '.', 1: 'X', -1: 'O'}
        print(" ".join(d[x] for x in self.board[0:3]))
        print(" ".join(d[x] for x in self.board[3:6]))
        print(" ".join(d[x] for x in self.board[6:9]))
        print()

    def playBotMove(self, bot_eval):
        f = [min, max][self.turn() == 1]
        nxt = self.nextStates()
        n = f(nxt, key=bot_eval)
        return n
    
    def playHumanMove(self):
        self.print()
        x = int(input("Enter move(1-9): "))
        if self.board[x] != 0:
            raise RuntimeError("Invalid move.")
        return GameState(board=tuple(
            self.board[i] if x != i else self.turn()
            for i in range(9)
        ))
