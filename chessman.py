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

    def could_have_done_the_move(movement):
        pass


class Pawn(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        self.name = "P"

    def promote(target: Chessman):
        pass


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
