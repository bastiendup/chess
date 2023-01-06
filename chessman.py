from typing import Tuple
from cursor import BLUE, PIECE_SET_1, PIECE_SET_2, RESET_CURSOR, WHITE


class Chessman:

    def __init__(self, x, y, isWhite) -> None:
        self.__position = (x, y)
        self.isWhite = isWhite
        self.name = ''
        self.full_name = ''
        self.possible_moves = []
        self.first_move = True
        self.valid_for_en_passant_move = False

    def __str__(self):
        colorize = BLUE
        if self.isWhite:
            colorize = WHITE
        icon = PIECE_SET_1.get(self.name)

        return f'{colorize}{icon}{RESET_CURSOR}'
        # return f'{colorize}{icon} {self.position} {RESET_CURSOR}'

    def compute_possible_move(self, board,
                              isWhiteTurn) -> list:  # type: ignore
        pass

    @property
    def position(self) -> Tuple:
        return self.__position

    @position.setter
    def position(self, to_pos: tuple):
        self.__position = to_pos


class Pawn(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        color = 'white' if isWhite else 'black'
        self.full_name = color + ' pawn'
        self.name = 'P'

    def promote(self, target: Chessman):
        pass

    @property
    def position(self):
        return super().position

    @position.setter
    def position(self, to_pos: tuple):
        if to_pos[0] - self.position[0] == 2:
            self.valid_for_en_passant_move = True
        super(Pawn, type(self)).position.fset(self, to_pos)  # type: ignore

    def compute_possible_move(self, board,
                              isWhiteTurn) -> list:  # type: ignore
        # Reset possible moves
        self.possible_moves = []

        inversor = -1 if isWhiteTurn else 1

        # If first move, pawn can move forward twice
        if self.first_move:
            possible_x = self.position[0] + 2 * inversor
            possible_y = self.position[1]
            if possible_x < 8 and possible_x >= 0:
                # Check there is no chessman in the path
                if board.get((possible_x - inversor, possible_y)) == None:
                    # self.possible_moves = []
                    self.possible_moves.append((possible_x, possible_y))

        # Else pawn can move forward once
        possible_x = self.position[0] + inversor
        possible_y = self.position[1]
        pos = (possible_x, possible_y)
        if possible_x < 8 and possible_x >= 0:
            # Check there is no chessman in the path
            if board.get(pos) == None:
                self.possible_moves.append((possible_x, possible_y))

        # Diagonal left
        possible_x = self.position[0] + inversor
        possible_y = self.position[1] - 1
        pos = (possible_x, possible_y)
        if possible_y >= 0 and possible_x < 8 and possible_x >= 0:
            possible_chessman = board.get(pos)
            if possible_chessman is not None and possible_chessman.isWhite is not isWhiteTurn:
                self.possible_moves.append((possible_x, possible_y))

        # Diagonal right
        possible_x = self.position[0] + inversor
        possible_y = self.position[1] + 1
        pos = (possible_x, possible_y)
        if possible_y < 8 and possible_x < 8 and possible_x >= 0:
            possible_chessman = board.get(pos)
            if possible_chessman is not None and possible_chessman.isWhite is not isWhiteTurn:
                # if not self.possible_moves:
                #     self.possible_moves = []
                self.possible_moves.append((possible_x, possible_y))
        """  "En passant" move :
        To execute this move, the pawn needs to be on the 5th line (line 5 if white, 4 if black)
        And if the opposite team move one of his pawn by two square,
        and position it next to the current pawn on last turn
        """
        if self.isWhite:
            valid_position = self.position[0] == 3
        else:
            valid_position = self.position[0] == 4

        if valid_position:
            # left en passant
            possible_x = self.position[0]
            possible_y = self.position[1] - 1
            pos = (possible_x, possible_y)
            if possible_y > 0:
                enemy = board.get(pos)
                if enemy and isinstance(enemy, Pawn):
                    if enemy.valid_for_en_passant_move:
                        self.possible_moves.append(
                            (possible_x + inversor, possible_y))

            # right en passant
            possible_x = self.position[0]
            possible_y = self.position[1] + 1
            pos = (possible_x, possible_y)
            if possible_y < 8:
                enemy = board.get(pos)
                if enemy and isinstance(enemy, Pawn):
                    if enemy.valid_for_en_passant_move:
                        self.possible_moves.append(
                            (possible_x + inversor, possible_y))

        # print(f'{self} -> possible_moves : {self.possible_moves}')


class Rook(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        color = 'white' if isWhite else 'black'
        self.full_name = color + ' rook'
        self.name = 'R'

    def compute_possible_move(self, board,
                              isWhiteTurn) -> list:  # type: ignore
        # Reset possible moves
        self.possible_moves = []

        # Up
        x = self.position[0]
        y = self.position[1]
        while True:
            x -= 1
            if x < 0: break
            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))

            else:
                if board.get((x, y)).isWhite is not isWhiteTurn:
                    self.possible_moves.append((x, y))
                break

        # Right
        x = self.position[0]
        y = self.position[1]
        while True:
            y += 1
            if y > 7: break
            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))

            else:
                if board.get((x, y)).isWhite is not isWhiteTurn:
                    self.possible_moves.append((x, y))
                break

        # Down
        x = self.position[0]
        y = self.position[1]
        while True:
            x += 1
            if x > 7: break
            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))

            else:
                if board.get((x, y)).isWhite is not isWhiteTurn:
                    self.possible_moves.append((x, y))
                break
        # Left
        x = self.position[0]
        y = self.position[1]
        while True:
            y -= 1
            if y < 0: break
            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))

            else:
                if board.get((x, y)).isWhite is not isWhiteTurn:
                    self.possible_moves.append((x, y))
                break

        # print(f'{self} -> possible_moves : {self.possible_moves}')


class Knight(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        color = 'white' if isWhite else 'black'
        self.full_name = color + ' knight'
        self.name = 'N'


    def knight_move(self, target_x, target_y, board, is_white_turn):

        x = self.position[0] + target_x
        y = self.position[1] + target_y
        if (x >= 0 and x < 8 and y >= 0 and y < 8):
            if board.get((x, y)) is None or board.get(
                (x, y)).isWhite is not is_white_turn:
                # if not self.possible_moves:
                #     self.possible_moves = []
                self.possible_moves.append((x, y))

    def compute_possible_move(self, board,
                              isWhiteTurn) -> list:  # type: ignore
        # Reset possible moves
        self.possible_moves = []

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

        # print(f'{self} -> possible_moves : {self.possible_moves}')


class Bishop(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        color = 'white' if isWhite else 'black'
        self.full_name = color + ' bishop'
        self.name = 'B'

    def compute_possible_move(self, board,
                              isWhiteTurn) -> list:  # type: ignore
        # Reset possible moves
        self.possible_moves = []

        # TopLeft
        x = self.position[0]
        y = self.position[1]
        while True:
            x -= 1
            y -= 1
            if x < 0 or y < 0:
                break

            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))

            else:
                if board.get((x, y)).isWhite is not isWhiteTurn:
                    self.possible_moves.append((x, y))
                break

        # TopRight
        x = self.position[0]
        y = self.position[1]
        while True:
            x -= 1
            y += 1
            if x < 0 or y > 7:
                break

            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))

            else:
                if board.get((x, y)).isWhite is not isWhiteTurn:
                    self.possible_moves.append((x, y))
                break

        # DownRight
        x = self.position[0]
        y = self.position[1]
        while True:
            x += 1
            y += 1
            if x > 7 or y > 7:
                break

            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))

            else:
                if board.get((x, y)).isWhite is not isWhiteTurn:
                    self.possible_moves.append((x, y))
                break

        # DownLeft
        x = self.position[0]
        y = self.position[1]
        while True:
            x += 1
            y -= 1
            if x > 7 or y < 0:
                break

            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))

            else:
                if board.get((x, y)).isWhite is not isWhiteTurn:
                    self.possible_moves.append((x, y))
                break

        # print(f'{self} -> possible_moves : {self.possible_moves}')


class Queen(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        color = 'white' if isWhite else 'black'
        self.full_name = color + ' queen'
        self.name = 'Q'


    def compute_possible_move(self, board,
                              isWhiteTurn) -> list:  # type: ignore
        # Reset possible moves
        self.possible_moves = []

        # region Rook Behavior
        # Up
        x = self.position[0]
        y = self.position[1]
        while True:
            x -= 1
            if x < 0: break
            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))

            else:
                if board.get((x, y)).isWhite is not isWhiteTurn:
                    self.possible_moves.append((x, y))
                break

        # Right
        x = self.position[0]
        y = self.position[1]
        while True:
            y += 1
            if y > 7: break
            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))

            else:
                if board.get((x, y)).isWhite is not isWhiteTurn:
                    self.possible_moves.append((x, y))
                break

        # Down
        x = self.position[0]
        y = self.position[1]
        while True:
            x += 1
            if x > 7: break
            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))

            else:
                if board.get((x, y)).isWhite is not isWhiteTurn:
                    self.possible_moves.append((x, y))
                break
        # Left
        x = self.position[0]
        y = self.position[1]
        while True:
            y -= 1
            if y < 0: break
            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))

            else:
                if board.get((x, y)).isWhite is not isWhiteTurn:
                    self.possible_moves.append((x, y))
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

            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))

            else:
                if board.get((x, y)).isWhite is not isWhiteTurn:
                    self.possible_moves.append((x, y))
                break

        # TopRight
        x = self.position[0]
        y = self.position[1]
        while True:
            x -= 1
            y += 1
            if x < 0 or y > 7:
                break

            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))

            else:
                if board.get((x, y)).isWhite is not isWhiteTurn:
                    self.possible_moves.append((x, y))
                break

        # DownRight
        x = self.position[0]
        y = self.position[1]
        while True:
            x += 1
            y += 1
            if x > 7 or y > 7:
                break

            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))

            else:
                if board.get((x, y)).isWhite is not isWhiteTurn:
                    self.possible_moves.append((x, y))
                break

        # DownLeft
        x = self.position[0]
        y = self.position[1]
        while True:
            x += 1
            y -= 1
            if x > 7 or y < 0:
                break

            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))

            else:
                if board.get((x, y)).isWhite is not isWhiteTurn:
                    self.possible_moves.append((x, y))
                break
        # end region Bishop Behavior

        # print(f'{self} -> possible_moves : {self.possible_moves}')


class King(Chessman):

    def __init__(self, x, y, isWhite) -> None:
        super().__init__(x, y, isWhite)
        color = 'white' if isWhite else 'black'
        self.full_name = color + ' king'
        self.name = 'K'


    def compute_possible_move(self, board,
                              isWhiteTurn) -> list:  # type: ignore
        # Reset possible moves
        self.possible_moves = []

        # Top Side
        x = self.position[0] - 1
        y = self.position[1] - 1
        # If we're not on top of the board
        if x >= 0:
            for k in range(3):
                # If we're not on the edge
                if y >= 0 and y < 8:
                    if board.get((x, y)) is None:
                        self.possible_moves.append((x, y))
                    elif board.get((x, y)).isWhite is not isWhiteTurn:
                        self.possible_moves.append((x, y))
                y += 1

        # Down Side
        x = self.position[0] + 1
        y = self.position[1] - 1
        # If we're not on bottom of the board
        if x < 8:
            for k in range(3):
                # If we're not on the edge
                if y >= 0 and y < 8:
                    if board.get((x, y)) is None:
                        self.possible_moves.append((x, y))
                    elif board.get((x, y)).isWhite is not isWhiteTurn:
                        self.possible_moves.append((x, y))
                y += 1

        # Middle Left
        x = self.position[0]
        y = self.position[1] - 1
        if y < 8:
            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))
            elif board.get((x, y)).isWhite is not isWhiteTurn:
                self.possible_moves.append((x, y))

        # Middle Right
        x = self.position[0]
        y = self.position[1] + 1
        if y < 8:
            if board.get((x, y)) is None:
                self.possible_moves.append((x, y))
            elif board.get((x, y)).isWhite is not isWhiteTurn:
                self.possible_moves.append((x, y))

        # print(f'{self} -> possible_moves : {self.possible_moves}')
