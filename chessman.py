from distutils.command.build_scripts import first_line_re
from shutil import move
from turtle import position


class Chessman:

    def __init__(self, x, y, isWhite) -> None:
        self.position = (x, y)
        self.isWhite = isWhite
        self.name = ""
        self.possible_move = None

    def __str__(self):
        colorize = '\033[94m'
        if self.isWhite:
            colorize = ''

        return f'{colorize} {self.name} {self.position} {colorize}'

    def compute_possible_move(self, board, isWhiteTurn) -> list:
        pass


class Pawn(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        self.name = "P"
        self.first_move = True

    def promote(target: Chessman):
        pass

    def compute_possible_move(self, board, isWhiteTurn) -> list:
        self.possible_move = None
        inversor = -1 if isWhiteTurn else 1

        # If first move, pawn can move forward twice
        if self.first_move:
            possible_x = self.position[0] + 2 * inversor
            possible_y = self.position[1]
            # Check there is no chessman in the path
            if board.board[possible_x - inversor][possible_y] == None:
                self.possible_move = []
                self.possible_move.append((possible_x, possible_y))

        # Else pawn can move forward once
        possible_x = self.position[0] + inversor
        possible_y = self.position[1]
        # Check there is no chessman in the path
        if board.board[possible_x][possible_y] == None:
            if not self.possible_move:
                self.possible_move = []
            self.possible_move.append((possible_x, possible_y))

        # Diagonal left
        possible_x = self.position[0] + inversor
        possible_y = self.position[1] - 1
        if board.board[possible_x][possible_y] != None:
            if not self.possible_move:
                self.possible_move = []
            self.possible_move.append((possible_x, possible_y))

        # Diagonal right
        possible_x = self.position[0] + inversor
        possible_y = self.position[1] - 1
        if board.board[possible_x][possible_y] != None:
            if not self.possible_move:
                self.possible_move = []
            self.possible_move.append((possible_x, possible_y))

        print(f'{self} -> possible_moves : {self.possible_move}')


class Rook(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        self.name = "R"


class Knight(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        self.name = "N"

    def knight_move(self, target_x, target_y, board, is_white_turn):

        x = self.position[0] + target_x
        y = self.position[1] + target_y
        if (x >= 0 and x < 8 and y >= 0 and y < 8):
            if board.board[x][y] is None or board.board[x][y].isWhite is not is_white_turn:
                if not self.possible_move:
                    self.possible_move = []
                self.possible_move.append((x, y))

    def compute_possible_move(self, board, isWhiteTurn) -> list:
        self.possible_move = None
        # UpLeft
        self.knight_move(-2, -1, board, isWhiteTurn)
        # UpRight
        self.knight_move(-2, 1, board, isWhiteTurn)

        # RightUp
        self.knight_move(-1, 2, board, isWhiteTurn)
        # RoghtDown
        self.knight_move(+1, 2, board, isWhiteTurn)

        # DownRight
        self.knight_move(2, 1, board, isWhiteTurn)
        # DownLeft
        self.knight_move(2, -1, board, isWhiteTurn)

        # LeftDown
        self.knight_move(-1, -2, board, isWhiteTurn)
        # LeftUp
        self.knight_move(1, -2, board, isWhiteTurn)

        print(f'{self} -> possible_moves : {self.possible_move}')


class Bishop(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        self.name = "B"


class Queen(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        self.name = "Q"


class King(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        self.name = "K"
