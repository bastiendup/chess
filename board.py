import sys
from chessman import *


class Board:

    def __init__(self) -> None:
        self.board = []

        # Board set-up
        for i in range(8):
            self.board.append([None] * 8)

        # White
        self.board[7][0] = Rook(7, 0, True)
        self.board[7][1] = Knight(7, 1, True)
        self.board[7][2] = Bishop(7, 2, True)
        self.board[7][3] = Queen(7, 3, True)
        self.board[7][4] = King(7, 4, True)
        self.board[7][5] = Bishop(7, 5, True)
        self.board[7][6] = Knight(7, 6, True)
        self.board[7][7] = Rook(7, 7, True)

        # Black
        for i in range(8):
            self.board[6][i] = Pawn(6, i, True)
        self.board[0][0] = Rook(0, 0, False)
        self.board[0][1] = Knight(0, 1, False)
        self.board[0][2] = Bishop(0, 2, False)
        self.board[0][3] = Queen(0, 3, False)
        self.board[0][4] = King(0, 4, False)
        self.board[0][5] = Bishop(0, 5, False)
        self.board[0][6] = Knight(0, 6, False)
        self.board[0][7] = Rook(0, 7, False)

        for i in range(8):
            self.board[1][i] = Pawn(1, i, False)

    def update_chessman(self, initial_position: tuple, new_position: tuple,
                        new_chessman: Chessman):
        self.board[initial_position[0]][initial_position[1]] = None
        self.board[new_position[0]][new_position[1]] = new_chessman

    def print_board(self):
        """
         Prints the current state of the board.

         precondition : chessman should return this for __str__ : f'{colorize}{self.name}{colorize}'
         """

        tmp_str = "\n    "
        for j in range(len(self.board[0])):
            tmp_str += ("\033[91m " + str(chr(j + 65)) + " \033[0m ")
        print(tmp_str)

        buffer = "   "
        for i in range(33):
            buffer += "*"
        print(buffer)

        for i in range(len(self.board)):
            tmp_str = "\033[91m" + f" {str(len(self.board[0])-i)}" + "\033[0m" + " |"
            for index, j in enumerate(self.board[i]):
                if j == None:
                    j = " "
                tmp_str += (" " + str(j) + " |")
            print(tmp_str)

        buffer = "   "
        for i in range(33):
            buffer += "*"
        print(buffer + "\n")

        sys.stdout.write("\033[F" * 14)  # Cursor up 14 lines

    def print_board_with_coordinates(self):
        """
        Prints the current state of the board with chessman coordinates.

        precondition : chessman should return this for __str__ : f'{colorize} {self.name} {self.position} {colorize}'
        """

        tmp_str = "\n    "
        for j in range(len(self.board[0])):
            tmp_str += ("\033[91m    " + str(chr(j + 65)) + " \033[0m     ")
        print(tmp_str)

        buffer = "   "
        for i in range(8):
            buffer += "***********"
        print(buffer)

        for i in range(len(self.board)):
            tmp_str = "\033[91m" + f"{str(len(self.board[0])-i)}" + "\033[0m" + " |"
            for index, j in enumerate(self.board[i]):
                if j == None:
                    j = f'\033[90m   ({i}, {index}) \033[0m'

                tmp_str += (str(j) + "|")  # str(j)

            print(tmp_str)

        buffer = "   "
        for i in range(8):
            buffer += "***********"
        print(buffer + "\n")

        sys.stdout.write("\033[F" * 14)  # Cursor up 14 lines
