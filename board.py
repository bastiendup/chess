import sys
from typing import List
from chessman import *
from cursor import BLACK, BUFFER, CURSOR_UP, DARK_GRAY, RESET_CURSOR, RED


class Board:

    def __init__(self) -> None:
        self.__board = []

        # Board set-up
        for i in range(8):
            self.__board.append([None] * 8)

        # White
        self.__board[7][0] = Rook(7, 0, True)
        self.__board[7][1] = Knight(7, 1, True)
        self.__board[7][2] = Bishop(7, 2, True)
        self.__board[7][3] = Queen(7, 3, True)
        self.__board[7][4] = King(7, 4, True)
        self.__board[7][5] = Bishop(7, 5, True)
        self.__board[7][6] = Knight(7, 6, True)
        self.__board[7][7] = Rook(7, 7, True)

        # Black
        for i in range(8):
            self.__board[6][i] = Pawn(6, i, True)
        self.__board[0][0] = Rook(0, 0, False)
        self.__board[0][1] = Knight(0, 1, False)
        self.__board[0][2] = Bishop(0, 2, False)
        self.__board[0][3] = Queen(0, 3, False)
        self.__board[0][4] = King(0, 4, False)
        self.__board[0][5] = Bishop(0, 5, False)
        self.__board[0][6] = Knight(0, 6, False)
        self.__board[0][7] = Rook(0, 7, False)

        for i in range(8):
            self.__board[1][i] = Pawn(1, i, False)

    def get(self, pos: tuple) -> Chessman:
        return self.__board[pos[0]][pos[1]]

    def get_chessmans(self,
                      chessman: Chessman,
                      color: bool = None) -> List[Chessman]:  # type: ignore
        chessmans = []
        for _, line in enumerate(self.__board):
            for square in line:
                if isinstance(square, chessman):  # type: ignore
                    if color is not None:
                        if square.isWhite == color:
                            chessmans.append(square)
                    else:
                        chessmans.append(square)

        return chessmans

    def move_chessman(self, from_pos: tuple, to_pos: tuple,
                      new_chessman: Chessman):
        for pawn in self.get_chessmans(Pawn):  # type: ignore
            pawn.valid_for_en_passant_move = False
        self.__board[from_pos[0]][from_pos[1]] = None
        self.__board[to_pos[0]][to_pos[1]] = new_chessman
        new_chessman.position = to_pos

    def promote(self, chessman: Pawn, into: Chessman, to: Tuple):
        x = chessman.position[0]
        y = chessman.position[1]
        promoted_x = to[0]
        promoted_y = to[1]
        if into == Queen:
            new_chessman = Queen(promoted_x, promoted_y, chessman.isWhite)
            self.__board[promoted_x][promoted_y] = new_chessman
        if into == Rook:
            new_chessman = Rook(promoted_x, promoted_y, chessman.isWhite)
            self.__board[promoted_x][promoted_y] = new_chessman
        if into == Bishop:
            new_chessman = Bishop(promoted_x, promoted_y, chessman.isWhite)
            self.__board[promoted_x][promoted_y] = new_chessman
        if into == Knight:
            new_chessman = Knight(promoted_x, promoted_y, chessman.isWhite)
            self.__board[promoted_x][promoted_y] = new_chessman
        self.__board[x][y] = None
        return new_chessman

    def print_board(self):
        ''''
         Prints the current state of the board.

         precondition : chessman should return this for __str__ : f'{colorize}{icon}{RESET_CURSOR}'
         '''

        tmp_str = '\n    '
        for j in range(len(self.__board[0])):
            tmp_str += (RED + ' ' + str(chr(j + 65)) + '  ')
        print(tmp_str)

        buffer = RESET_CURSOR + '    '
        for i in range(31):
            buffer += BUFFER
        print(buffer)

        for i in range(len(self.__board)):
            tmp_str = f' {RED}{str(len(self.__board[0])-i)}{RESET_CURSOR}' + ' |'
            for index, j in enumerate(self.__board[i]):
                if j == None:
                    j = f'{BLACK}.{RESET_CURSOR}'
                tmp_str += (' ' + str(j) + ' |')
            print(tmp_str)

        buffer = RESET_CURSOR + '    '
        for i in range(31):
            buffer += BUFFER
        print(buffer + '\n')

        # sys.stdout.write(CURSOR_UP * 14)  # Cursor up 14 lines

    def print_board_with_coordinates(self):
        '''
        Prints the current state of the board with chessman coordinates.

        precondition : chessman should return this for __str__ : f'{colorize}{icon} {self.position} {RESET_CURSOR}'
        '''

        tmp_str = '\n     '
        for j in range(len(self.__board[0])):
            tmp_str += (RED + '     ' + str(chr(j + 65)) + RESET_CURSOR +
                        '      ')
        print(tmp_str)

        buffer = '     '
        for i in range(8):
            buffer += BUFFER * 12
        print(buffer)

        for i in range(len(self.__board)):
            tmp_str = RED + f'  {str(len(self.__board[0])-i)} ' + RESET_CURSOR + ' |'
            for index, j in enumerate(self.__board[i]):
                if j == None:
                    j = f'{DARK_GRAY}  ({i}, {index}) {RESET_CURSOR}'

                tmp_str += (' ' + str(j) + ' |')

            print(tmp_str)

        buffer = '     '
        for i in range(8):
            buffer += BUFFER * 12
        print(buffer + '\n')

        # sys.stdout.write(CURSOR_UP * 14)  # Cursor up 14 lines
