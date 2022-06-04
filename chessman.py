from distutils.command.build_scripts import first_line_re
from shutil import move
from turtle import position


class Chessman:

    def __init__(self, x, y, isWhite) -> None:
        self.position = (x, y)
        self.isWhite = isWhite
        self.name = ""

    def __str__(self):
        if self.isWhite:
            return self.name
        else:
            return '\033[94m' + self.name + '\033[0m'

    def possible_move(self, isWhiteTurn, target_position) -> list:
        pass


class Pawn(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        self.name = "P"
        self.first_move = True

    def promote(target: Chessman):
        pass

    def possible_move(self, isWhiteTurn, target_position) -> list:
        moves = None
        inversor = 1 if isWhiteTurn else -1

        # If first move, pawn can move forward twice
        if self.first_move:
            possible_x = target_position[0] + 2 * inversor
            possible_y = target_position[1]
            if self.position[0] == possible_x and self.position[1] == possible_y:
                moves = []
                moves.append((possible_x, possible_y))

        # Else pawn can move forward once
        possible_x = target_position[0] + 1 * inversor
        possible_y = target_position[1]
        if self.position[0] == possible_x and self.position[1] == possible_y:
            if not moves:
                moves = []
            moves.append((possible_x, possible_y))
        print(f'{self} -> possible_moves : {moves}')
        return moves


class Rook(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        self.name = "R"


class Knigth(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        self.name = "N"


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
