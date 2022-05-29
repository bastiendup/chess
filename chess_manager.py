import re
from board import Board
from chessman import *
from old.piece import Knight


class Chess_Manager:

    def __init__(self) -> None:
        self.board = Board()

    # region Rook

    def king_side_rook_white(self):
        b = self.board.board
        b[7][4] = None
        b[7][5] = Rook(0, 5, True)
        b[7][6] = King(0, 6, True)
        b[7][7] = None

    def queen_side_rook_white(self):
        b = self.board.board
        b[7][0] = None
        b[7][3] = Rook(0, 5, True)
        b[7][2] = King(0, 6, True)
        b[7][4] = None

    def king_side_rook_black(self):
        b = self.board.board
        b[0][4] = None
        b[0][5] = Rook(0, 5, False)
        b[0][6] = King(0, 6, False)
        b[0][7] = None

    def queen_side_rook_black(self):
        b = self.board.board
        b[0][0] = None
        b[0][3] = Rook(0, 5, False)
        b[0][2] = King(0, 6, False)
        b[0][4] = None

    def CheckIfKingRook(self, movement, isWhiteTurn):
        color = 'white' if isWhiteTurn else 'black'
        possible_rooks = {
            'O-O': 'king_side_rook_',
            'O-O-O': 'queen_side_rook_'
        }
        king_rook_regex = re.compile(r'(O-O)(-O)?')
        match = re.search(king_rook_regex, movement)
        if match:
            rook = possible_rooks[match.group()] + color
            getattr(self, rook)()

    # endregion Rook

    # region Identify Chessman
    def CheckPiece(self, movement):
        pieces = {'k': King, 'b': Bishop, 'q': Queen, 'n': Knight, 'r': Rook}
        piece_regex = re.compile(r'^(k|q|r|b|n)')
        match = re.search(piece_regex, movement)
        piece = Pawn
        if match:
            piece = pieces[match.group()]
        print(f'Piece                      -> {piece}')
        return re.sub(r'^(k|q|r|b|n)', '', movement), piece

    # endregion Identify Chessman

    # region Disambiguating Move

    def DisambiguatingX(self, movement):
        # Check for the file of departure before the move
        regex = re.compile(r'^([a-h])(x|[a-h])')
        match = re.search(regex, movement)
        disambiguating_move = None
        if match:
            disambiguating_move = ord(match.group(1)) - 96
            movement = re.sub(r'^[a-h]', '', movement)
        print(f'Disambiguating X        -> {disambiguating_move}')
        return movement, disambiguating_move

    def DisambiguatingY(self, movement):
        # Check for the rank of departure before the move
        regex = re.compile(r'^([1-8])(x|[a-h])')
        match = re.search(regex, movement)
        disambiguating_move = None
        if match:
            disambiguating_move = ord(match.group(1))
            movement = re.sub(r'^[1-8]', '', movement)
        print(f'Disambiguating Y        -> {disambiguating_move}')
        return movement, disambiguating_move

    def DisambiguatingXY(self, movement):
        # Check for both the file and rank of departure before the move
        regex = re.compile(r'^([a-h][1-8])(x|[a-h])')
        match = re.search(regex, movement)
        disambiguating_move = None
        if match:
            disambiguating_move = []
            disambiguating_move.append(ord(match.group(1)[0]) - 96)
            disambiguating_move.append(int(match.group(1)[1]))

            movement = re.sub(r'^[a-h][1-8]', '', movement)
        print(f'Disambiguating XY -> {disambiguating_move}')
        return movement, disambiguating_move

    def CheckDisambiguating(self, movement):
        d = ['DisambiguatingX', 'DisambiguatingY', 'DisambiguatingXY']
        for i in d:
            movement, disambiguating_move = getattr(self, i)(movement)
            if disambiguating_move:
                return movement, disambiguating_move


# endregion Disambiguating Move

manager = Chess_Manager()
isWhiteTurn = True
while True:
    manager.board.print_board()
    movement = input(f'White turn ? {isWhiteTurn},  Movement : ').lower()
    print(movement)
    manager.CheckIfKingRook(movement, isWhiteTurn)
    movement, piece = manager.CheckPiece(movement)
    movement = manager.CheckDisambiguating(movement)

    isWhiteTurn = not isWhiteTurn
