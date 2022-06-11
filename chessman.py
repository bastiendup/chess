class Chessman:

    def __init__(self, x, y, isWhite) -> None:
        self.position = (x, y)
        self.isWhite = isWhite
        self.name = ""
        self.possible_move = []
        self.first_move = True

    def __str__(self):
        colorize = '\033[94m'
        if self.isWhite:
            colorize = ''

        return f'{colorize}{self.name}\033[0m'

    def compute_possible_move(self, board, isWhiteTurn) -> list:
        pass


class Pawn(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        self.name = "P"

    def promote(target: Chessman):
        pass

    def compute_possible_move(self, board, isWhiteTurn) -> list:
        # Reset possible moves
        self.possible_move = []

        inversor = -1 if isWhiteTurn else 1

        # If first move, pawn can move forward twice
        if self.first_move:
            possible_x = self.position[0] + 2 * inversor
            possible_y = self.position[1]
            if possible_x < 8 and possible_x >= 0:
                # Check there is no chessman in the path
                if board.board[possible_x - inversor][possible_y] == None:
                    # self.possible_move = []
                    self.possible_move.append((possible_x, possible_y))

        # Else pawn can move forward once
        possible_x = self.position[0] + inversor
        possible_y = self.position[1]
        if possible_x < 8 and possible_x >= 0:
            # Check there is no chessman in the path
            if board.board[possible_x][possible_y] == None:
                # if not self.possible_move:
                #     self.possible_move = []
                self.possible_move.append((possible_x, possible_y))

        # Diagonal left
        possible_x = self.position[0] + inversor
        possible_y = self.position[1] - 1
        if possible_y >= 0 and possible_x < 8 and possible_x >= 0:
            if board.board[possible_x][possible_y] is not None and board.board[possible_x][
                    possible_y].isWhite is not isWhiteTurn:
                # if not self.possible_move:
                #     self.possible_move = []
                self.possible_move.append((possible_x, possible_y))

        # Diagonal right
        possible_x = self.position[0] + inversor
        possible_y = self.position[1] + 1
        if possible_y < 8 and possible_x < 8 and possible_x >= 0:
            if board.board[possible_x][possible_y] is not None and board.board[possible_x][
                    possible_y].isWhite is not isWhiteTurn:
                # if not self.possible_move:
                #     self.possible_move = []
                self.possible_move.append((possible_x, possible_y))

        # print(f'{self} -> possible_moves : {self.possible_move}')


class Rook(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        self.name = "R"

    def compute_possible_move(self, board, isWhiteTurn) -> list:
        # Reset possible moves
        self.possible_move = []

        # Up
        x = self.position[0]
        y = self.position[1]
        while True:
            x -= 1
            if x < 0: break
            if board.board[x][y] is None:
                self.possible_move.append((x, y))

            else:
                if board.board[x][y].isWhite is not isWhiteTurn:
                    self.possible_move.append((x, y))
                break

        # Right
        x = self.position[0]
        y = self.position[1]
        while True:
            y += 1
            if y > 7: break
            if board.board[x][y] is None:
                self.possible_move.append((x, y))

            else:
                if board.board[x][y].isWhite is not isWhiteTurn:
                    self.possible_move.append((x, y))
                break

        # Down
        x = self.position[0]
        y = self.position[1]
        while True:
            x += 1
            if x > 7: break
            if board.board[x][y] is None:
                self.possible_move.append((x, y))

            else:
                if board.board[x][y].isWhite is not isWhiteTurn:
                    self.possible_move.append((x, y))
                break
        # Left
        x = self.position[0]
        y = self.position[1]
        while True:
            y -= 1
            if y < 0: break
            if board.board[x][y] is None:
                self.possible_move.append((x, y))

            else:
                if board.board[x][y].isWhite is not isWhiteTurn:
                    self.possible_move.append((x, y))
                break

        # print(f'{self} -> possible_moves : {self.possible_move}')


class Knight(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        self.name = "N"

    def knight_move(self, target_x, target_y, board, is_white_turn):

        x = self.position[0] + target_x
        y = self.position[1] + target_y
        if (x >= 0 and x < 8 and y >= 0 and y < 8):
            if board.board[x][y] is None or board.board[x][y].isWhite is not is_white_turn:
                # if not self.possible_move:
                #     self.possible_move = []
                self.possible_move.append((x, y))

    def compute_possible_move(self, board, isWhiteTurn) -> list:
        # Reset possible moves
        self.possible_move = []

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

        # print(f'{self} -> possible_moves : {self.possible_move}')


class Bishop(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        self.name = "B"

    def compute_possible_move(self, board, isWhiteTurn) -> list:
        # Reset possible moves
        self.possible_move = []

        # TopLeft
        x = self.position[0]
        y = self.position[1]
        while True:
            x -= 1
            y -= 1
            if x < 0 or y < 0:
                break

            if board.board[x][y] is None:
                self.possible_move.append((x, y))

            else:
                if board.board[x][y].isWhite is not isWhiteTurn:
                    self.possible_move.append((x, y))
                break

        # TopRight
        x = self.position[0]
        y = self.position[1]
        while True:
            x -= 1
            y += 1
            if x < 0 or y > 7:
                break

            if board.board[x][y] is None:
                self.possible_move.append((x, y))

            else:
                if board.board[x][y].isWhite is not isWhiteTurn:
                    self.possible_move.append((x, y))
                break

        # DownRight
        x = self.position[0]
        y = self.position[1]
        while True:
            x += 1
            y += 1
            if x > 7 or y > 7:
                break

            if board.board[x][y] is None:
                self.possible_move.append((x, y))

            else:
                if board.board[x][y].isWhite is not isWhiteTurn:
                    self.possible_move.append((x, y))
                break

        # DownLeft
        x = self.position[0]
        y = self.position[1]
        while True:
            x += 1
            y -= 1
            if x > 7 or y < 0:
                break

            if board.board[x][y] is None:
                self.possible_move.append((x, y))

            else:
                if board.board[x][y].isWhite is not isWhiteTurn:
                    self.possible_move.append((x, y))
                break

        # print(f'{self} -> possible_moves : {self.possible_move}')


class Queen(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        self.name = "Q"

    def compute_possible_move(self, board, isWhiteTurn) -> list:
        # Reset possible moves
        self.possible_move = []

        # region Rook Behavior
        # Up
        x = self.position[0]
        y = self.position[1]
        while True:
            x -= 1
            if x < 0: break
            if board.board[x][y] is None:
                self.possible_move.append((x, y))

            else:
                if board.board[x][y].isWhite is not isWhiteTurn:
                    self.possible_move.append((x, y))
                break

        # Right
        x = self.position[0]
        y = self.position[1]
        while True:
            y += 1
            if y > 7: break
            if board.board[x][y] is None:
                self.possible_move.append((x, y))

            else:
                if board.board[x][y].isWhite is not isWhiteTurn:
                    self.possible_move.append((x, y))
                break

        # Down
        x = self.position[0]
        y = self.position[1]
        while True:
            x += 1
            if x > 7: break
            if board.board[x][y] is None:
                self.possible_move.append((x, y))

            else:
                if board.board[x][y].isWhite is not isWhiteTurn:
                    self.possible_move.append((x, y))
                break
        # Left
        x = self.position[0]
        y = self.position[1]
        while True:
            y -= 1
            if y < 0: break
            if board.board[x][y] is None:
                self.possible_move.append((x, y))

            else:
                if board.board[x][y].isWhite is not isWhiteTurn:
                    self.possible_move.append((x, y))
                break
        # endregion Rook Behavior

        # region Bishop Behavior
        # TopLeft
        x = self.position[0]
        y = self.position[1]
        while True:
            x -= 1
            y -= 1
            if x < 0 or y < 0:
                break

            if board.board[x][y] is None:
                self.possible_move.append((x, y))

            else:
                if board.board[x][y].isWhite is not isWhiteTurn:
                    self.possible_move.append((x, y))
                break

        # TopRight
        x = self.position[0]
        y = self.position[1]
        while True:
            x -= 1
            y += 1
            if x < 0 or y > 7:
                break

            if board.board[x][y] is None:
                self.possible_move.append((x, y))

            else:
                if board.board[x][y].isWhite is not isWhiteTurn:
                    self.possible_move.append((x, y))
                break

        # DownRight
        x = self.position[0]
        y = self.position[1]
        while True:
            x += 1
            y += 1
            if x > 7 or y > 7:
                break

            if board.board[x][y] is None:
                self.possible_move.append((x, y))

            else:
                if board.board[x][y].isWhite is not isWhiteTurn:
                    self.possible_move.append((x, y))
                break

        # DownLeft
        x = self.position[0]
        y = self.position[1]
        while True:
            x += 1
            y -= 1
            if x > 7 or y < 0:
                break

            if board.board[x][y] is None:
                self.possible_move.append((x, y))

            else:
                if board.board[x][y].isWhite is not isWhiteTurn:
                    self.possible_move.append((x, y))
                break
        # end region Bishop Behavior

        # print(f'{self} -> possible_moves : {self.possible_move}')


class King(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        self.name = "K"

    def compute_possible_move(self, board, isWhiteTurn) -> list:
        # Reset possible moves
        self.possible_move = []

        # Top Side
        x = self.position[0] - 1
        y = self.position[1] - 1
        # If we're not on top of the board
        if x >= 0:
            for k in range(3):
                # If we're not on the edge
                if y >= 0 or y < 8:
                    if board.board[x][y] is None:
                        self.possible_move.append((x, y))
                    elif board.board[x][y].isWhite is not isWhiteTurn:
                        self.possible_move.append((x, y))
                y += 1

        # Down Side
        x = self.position[0] + 1
        y = self.position[1] - 1
        # If we're not on bottom of the board
        if x < 8:
            for k in range(3):
                # If we're not on the edge
                if y >= 0 or y < 8:
                    if board.board[x][y] is None:
                        self.possible_move.append((x, y))
                    elif board.board[x][y].isWhite is not isWhiteTurn:
                        self.possible_move.append((x, y))
                y += 1

        # Middle Left
        x = self.position[0]
        y = self.position[1] - 1
        if y < 8:
            if board.board[x][y] is None:
                self.possible_move.append((x, y))
            elif board.board[x][y].isWhite is not isWhiteTurn:
                self.possible_move.append((x, y))

        # Middle Right
        x = self.position[0]
        y = self.position[1] + 1
        if y < 8:
            if board.board[x][y] is None:
                self.possible_move.append((x, y))
            elif board.board[x][y].isWhite is not isWhiteTurn:
                self.possible_move.append((x, y))

        # print(f'{self} -> possible_moves : {self.possible_move}')
