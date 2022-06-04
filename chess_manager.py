from mimetypes import init
import re
from tabnanny import check
from board import Board
from chessman import *
from old.piece import Knight


class Chess_Manager:

    def __init__(self) -> None:
        self.board = Board()
        self.chessman = None
        self.disambiguating_move = None
        self.capture = None
        self.move = None
        self.promotion = None
        self.checkmate = None
        self.is_white_turn = False

    # region Rook

    def king_side_rook_white(self):
        b = self.board.board
        b[7][4] = None
        b[7][5] = Rook(7, 5, True)
        b[7][6] = King(7, 6, True)
        b[7][7] = None

    def queen_side_rook_white(self):
        b = self.board.board
        b[7][0] = None
        b[7][3] = Rook(7, 5, True)
        b[7][2] = King(7, 6, True)
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

    def CheckIfKingRook(self, movement):
        color = 'white' if self.is_white_turn else 'black'
        possible_rooks = {'o-o': 'king_side_rook_', 'o-o-o': 'queen_side_rook_'}
        king_rook_regex = re.compile(r'(o-o)(-o)?')
        rook = False
        match = re.search(king_rook_regex, movement)
        if match:
            rook = possible_rooks[match.group()] + color
            getattr(self, rook)()
        return rook

    # endregion Rook

    # region Identify Chessman
    def check_piece(self, movement):
        pieces = {'k': King, 'b': Bishop, 'q': Queen, 'n': Knight, 'r': Rook}
        piece_regex = re.compile(r'^(k|q|r|b|n)')
        match = re.search(piece_regex, movement)
        piece = Pawn
        if match:
            piece = pieces[match.group()]
        print(f'Piece                      -> {piece}')
        self.chessman = piece
        return re.sub(r'^(k|q|r|b|n)', '', movement)

    # endregion Identify Chessman

    # region Disambiguating Move

    def DisambiguatingX(self, movement):
        # Check for the file of departure before the move
        regex = re.compile(r'^([a-h])(x|[a-h])')
        match = re.search(regex, movement)
        disambiguating_move = None
        if match:
            disambiguating_move = match.group(1)
            # disambiguating_move = ord(match.group(1)) - 97
            movement = re.sub(r'^[a-h]', '', movement)
        print(f'Disambiguating X        -> {disambiguating_move}')
        return movement, disambiguating_move

    def DisambiguatingY(self, movement):
        # Check for the rank of departure before the move
        regex = re.compile(r'^([1-8])(x|[a-h])')
        match = re.search(regex, movement)
        disambiguating_move = None
        if match:
            disambiguating_move = match.group(1)
            # disambiguating_move = ord(match.group(1)) - 1
            movement = re.sub(r'^[1-8]', '', movement)
        print(f'Disambiguating Y        -> {disambiguating_move}')
        return movement, disambiguating_move

    def DisambiguatingXY(self, movement):
        # Check for both the file and rank of departure before the move
        regex = re.compile(r'^([a-h][1-8])(x|[a-h])')
        match = re.search(regex, movement)
        disambiguating_move = None
        if match:
            disambiguating_move = match.group(1)
            # disambiguating_move = []
            # disambiguating_move.append(ord(match.group(1)[0]) - 97)
            # disambiguating_move.append(int(match.group(1)[1]) - 1)

            movement = re.sub(r'^[a-h][1-8]', '', movement)
        print(f'Disambiguating XY -> {disambiguating_move}')
        return movement, disambiguating_move

    def CheckDisambiguating(self, movement):
        d = ['DisambiguatingX', 'DisambiguatingY', 'DisambiguatingXY']
        for i in d:
            movement, disambiguating_move = getattr(self, i)(movement)
            if disambiguating_move:
                self.disambiguating_move = self.translate(disambiguating_move)
        return movement

# endregion Disambiguating Move

# region Capture

    def CheckCapture(self, movement):
        match = re.search(r'^x', movement)
        capture = False
        if match:
            capture = False
            movement = re.sub(r'^x', '', movement)
        print(f'Capture                    -> {capture}')
        self.capture = capture
        return movement

# endregion Capture

# region Movement

    def translate(self, s):
        try:
            row = int(s[1])
            col = s[0]
            if row < 1 or row > 8:
                print(s[0] + "is not in the range from 1 - 8")
                return None
            if col < 'a' or col > 'h':
                print(s[1] + "is not in the range from a - h")
                return None
            dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
            return (8 - row, dict[col])
        except:
            print(s + "is not in the format '[number][letter]'")
            return None

    def CheckMoving(self, movement):
        # Check for move
        regex = re.compile(r'^[a-h][1-8]')
        match = re.search(regex, movement)
        move = None
        if match:
            move = match.group()
            # move.append(ord(match.group()[0]) - 97)
            # move.append(int(match.group()[1]) - 1)
            movement = re.sub(r'^[a-h][1-8]', '', movement)
        print(f'Moving                     -> {move}')

        self.move = self.translate(move)
        return movement

# endregion Movement

# region Promotion

    def CheckPromotion(self, movement):
        # Check for pawn promote
        promote_piece = {'K': King, 'B': Bishop, 'Q': Queen, 'N': Knight, 'R': Rook}
        regex = re.compile(r'^=(q|b|n|r)')
        match = re.search(regex, movement)
        promotion = False
        if match:
            promotion = promote_piece[match.group(1)]
            movement = re.sub(r'^=(q|b|n|r)', '', movement)
        print(f'Promotion                  -> {promotion}')
        self.promotion = promotion
        return movement

# endregion Promotion

# region Checkmate

    def CheckForCheckMove(self, movement):
        # Check for checkmate
        check_ending = {'+': 'Check', '#': 'Checkmate'}
        regex = re.compile(r'^(\+|\#)')
        match = re.search(regex, movement)
        checkmate = False
        if match:
            checkmate = check_ending[match.group(1)]
            movement = re.sub(r'^\+|\#', '', movement)
        print(f'Checkmate                  -> {checkmate}')
        self.checkmate = checkmate
        return movement

# endregion Checkmate

# region UpdateBoard

    def find_possible_chessman(self):
        # Find all chessmans
        chessmans = []
        for i in range(len(self.board.board)):
            for j in self.board.board[i]:
                if j.__class__ == self.chessman:
                    chessmans.append(j)

        # Only keep chessmans with right color
        tmp = []
        for i in chessmans:
            if i.isWhite == self.is_white_turn:
                tmp.append(i)
        chessmans = tmp

        print(f'chessmans : {chessmans}')
        return chessmans

    def identify_chessman(self, chessmans) -> Chessman:
        for chessman in chessmans:
            moves = chessman.possible_move(self.is_white_turn, self.move)
            if moves:
                if not self.disambiguating_move:
                    initial_position = chessman.position
                    chessman.position = moves[0]
                    return chessman, initial_position

                else:
                    if self.disambiguating_move[0] is None:
                        for move in moves:
                            if move[1] == self.disambiguating_move[1]:
                                initial_position = chessman.position

                                chessman.position = move
                                return chessman, initial_position
                    elif self.disambiguating_move[1] is None:
                        for move in moves:
                            if move[0] == self.disambiguating_move[0]:
                                initial_position = chessman.position

                                chessman.position = move
                                return chessman, initial_position
                    else:
                        for move in moves:
                            if move[0] == self.disambiguating_move[0] and move[1] == self.disambiguating_move[1]:
                                initial_position = chessman.position

                                chessman.position = move
                                return chessman, initial_position
        return None, None

    def update_board(self):
        chessmans = self.find_possible_chessman()
        chessman, initial_position = self.identify_chessman(chessmans)
        self.board.update_chessman(initial_position[0], initial_position[1], None)
        self.board.update_chessman(self.move[0], self.move[1], chessman)

        print(f'chess man : {chessman.name}, pos : {chessman.position}')


# endregion UpdateBoard

manager = Chess_Manager()
while True:
    manager.is_white_turn = not manager.is_white_turn
    manager.board.print_board()
    movement = input(f'White turn ? {manager.is_white_turn},  Movement : ').lower()
    print(movement)
    rook = manager.CheckIfKingRook(movement)
    if rook: continue
    movement = manager.check_piece(movement)
    movement = manager.CheckDisambiguating(movement)
    movement = manager.CheckCapture(movement)
    movement = manager.CheckMoving(movement)
    movement = manager.CheckPromotion(movement)
    movement = manager.CheckForCheckMove(movement)

    manager.update_board()
