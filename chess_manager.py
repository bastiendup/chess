import re
import sys
from board import Board
from chessman import *


class Chess_Manager:

    def __init__(self):
        self.board = Board()
        self.movement = None
        self.chessman = None
        self.disambiguating_move = None
        self.capture = None
        self.current_move = None
        self.promotion = None
        self.checkmate = None
        self.is_white_turn = False
        self.final_score = None
        self.rook = None

    # region Score
    def check_final_score(self, movement):
        possible_scores = {'1/2-1/2': 'DRAW', '1-0': 'WHITE WINS', '0-1': 'BLACK WINS', '*': 'INTERRUPTED GAME'}
        final_score_regex = re.compile(r'\d-\d|\*|1/2-1/2')
        match = re.search(final_score_regex, movement)
        if match:
            self.final_score = possible_scores[match.group()]

        return self.final_score
    # end region Score

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
        b[7][3] = Rook(7, 3, True)
        b[7][2] = King(7, 2, True)
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
        b[0][3] = Rook(0, 3, False)
        b[0][2] = King(0, 2, False)
        b[0][4] = None

    def CheckIfKingRook(self, movement):
        color = 'white' if self.is_white_turn else 'black'
        possible_rooks = {'O-O': 'king_side_rook_', 'O-O-O': 'queen_side_rook_'}
        king_rook_regex = re.compile(r'(O-O)(-O)?')
        match = re.search(king_rook_regex, movement)
        if match:
            rook = possible_rooks[match.group()] + color
            getattr(self, rook)()
    # endregion Rook

    # region Identify Chessman
    def check_piece(self, movement):
        pieces = {'K': King, 'B': Bishop, 'Q': Queen, 'N': Knight, 'R': Rook}
        piece_regex = re.compile(r'^(K|Q|R|B|N)')
        match = re.search(piece_regex, movement)
        piece = Pawn
        if match:
            piece = pieces[match.group()]
        # print(f'Piece                      -> {piece}')
        self.chessman = piece
        return re.sub(r'^(K|Q|R|B|N)', '', movement)
    # endregion Identify Chessman

    # region Disambiguating current_move
    def DisambiguatingX(self, movement):
        # Check for the file of departure before the current_move
        regex = re.compile(r'^([a-h])(x|[a-h])')
        match = re.search(regex, movement)
        disambiguating_move = None
        if match:
            disambiguating_move = []
            disambiguating_move.append(match.group(1))
            disambiguating_move.append(None)
            # disambiguating_move = ord(match.group(1)) - 97
            movement = re.sub(r'^[a-h]', '', movement)
        # print(f'Disambiguating X        -> {disambiguating_move}')
        return movement, disambiguating_move

    def DisambiguatingY(self, movement):
        # Check for the rank of departure before the current_move
        regex = re.compile(r'^([1-8])(x|[a-h])')
        match = re.search(regex, movement)
        disambiguating_move = None
        if match:
            disambiguating_move = [None]
            disambiguating_move.append(match.group(1))
            # disambiguating_move = ord(match.group(1)) - 1
            movement = re.sub(r'^[1-8]', '', movement)
        # print(f'Disambiguating Y        -> {disambiguating_move}')
        return movement, disambiguating_move

    def DisambiguatingXY(self, movement):
        # Check for both the file and rank of departure before the current_move
        regex = re.compile(r'^([a-h][1-8])(x|[a-h])')
        match = re.search(regex, movement)
        disambiguating_move = None
        if match:
            disambiguating_move = match.group(1)
            # disambiguating_move = []
            # disambiguating_move.append(ord(match.group(1)[0]) - 97)
            # disambiguating_move.append(int(match.group(1)[1]) - 1)

            movement = re.sub(r'^[a-h][1-8]', '', movement)
        # print(f'Disambiguating XY -> {disambiguating_move}')
        return movement, disambiguating_move

    def CheckDisambiguating(self, movement):
        d = ['DisambiguatingX', 'DisambiguatingY', 'DisambiguatingXY']
        self.disambiguating_move = None
        for i in d:
            movement, disambiguating_move = getattr(self, i)(movement)
            if disambiguating_move:
                self.disambiguating_move = self.translate(disambiguating_move)
        return movement

# endregion Disambiguating current_move

# region Capture

    def CheckCapture(self, movement):
        match = re.search(r'^x', movement)
        capture = False
        if match:
            capture = True
            movement = re.sub(r'^x', '', movement)
        # print(f'Capture                    -> {capture}')
        self.capture = capture
        return movement

# endregion Capture

# region Movement

    def translate(self, s):
        row = int(s[1]) if s[1] is not None else None
        col = s[0] if s[0] is not None else None

        dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        if row is None:
            return (None, dict[col])
        if col is None:
            return (8 - row, None)
        return (8 - row, dict[col])

    def CheckMoving(self, movement):
        # Check for current_move
        regex = re.compile(r'^[a-h][1-8]')
        match = re.search(regex, movement)
        current_move = None
        if match:
            current_move = match.group()
            # current_move.append(ord(match.group()[0]) - 97)
            # current_move.append(int(match.group()[1]) - 1)
            movement = re.sub(r'^[a-h][1-8]', '', movement)
        # print(f'Moving                     -> {current_move}')

        self.current_move = self.translate(current_move)
        return movement

# endregion Movement

# region Promotion

    def CheckPromotion(self, movement):
        # Check for pawn promote
        promote_piece = {'B': Bishop, 'Q': Queen, 'N': Knight, 'R': Rook}
        regex = re.compile(r'^=(Q|B|N|R)')
        match = re.search(regex, movement)
        promotion = False
        if match:
            promotion = promote_piece[match.group(1)]
            movement = re.sub(r'^=(Q|B|N|R)', '', movement)
        # print(f'Promotion                  -> {promotion}')
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
        # print(f'Checkmate                  -> {checkmate}')
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

        # print(f'chessmans : {chessmans}')
        return chessmans

    def identify_chessman(self, chessmans) -> Chessman:
        possible_chessmans = []
        for chessman in chessmans:
            chessman.compute_possible_move(self.board, self.is_white_turn)
            if chessman.possible_move:
                for current_move in chessman.possible_move:
                    if current_move == self.current_move:

                        # Un peu tordu : si on a pas de disambiguating current_move, alors le premier chessman qui match c'est forcément lui
                        if not self.disambiguating_move:
                            initial_position = chessman.position
                            chessman.position = self.current_move
                            return chessman, initial_position

                        possible_chessmans.append(chessman)
                        continue

        if self.disambiguating_move[0] is None:
            for chessman in possible_chessmans:
                if chessman.position[1] == self.disambiguating_move[1]:
                    initial_position = chessman.position
                    chessman.position = self.current_move
                    return chessman, initial_position

        if self.disambiguating_move[1] is None:
            for chessman in possible_chessmans:
                if chessman.position[0] == self.disambiguating_move[0]:
                    initial_position = chessman.position
                    chessman.position = self.current_move
                    return chessman, initial_position

        for chessman in possible_chessmans:
            if chessman.position == self.disambiguating_move:
                initial_position = chessman.position
                chessman.position = self.current_move
                return chessman, initial_position

    def identify_captured_chessman(self):
        if not self.capture: return None
        return self.board.board[self.current_move[0]][self.current_move[1]]

    def update_board(self):

        captured_chessman = self.identify_captured_chessman()
        chessmans = self.find_possible_chessman()
        chessman, initial_position = self.identify_chessman(chessmans)
        chessman.first_move = False

        # Promotion
        if self.promotion:
            if self.promotion == Queen:
                promoted_chessman = Queen(chessman.position[0], chessman.position[1], chessman.isWhite)
                chessman = promoted_chessman
            if self.promotion == Rook:
                promoted_chessman = Rook(chessman.position[0], chessman.position[1], chessman.isWhite)
                chessman = promoted_chessman
            if self.promotion == Bishop:
                promoted_chessman = Bishop(chessman.position[0], chessman.position[1], chessman.isWhite)
                chessman = promoted_chessman
            if self.promotion == Knight:
                promoted_chessman = Knight(chessman.position[0], chessman.position[1], chessman.isWhite)
                chessman = promoted_chessman

        # Reset chessman initial position on board, and set is new position
        self.board.update_chessman(initial_position, self.current_move, chessman)

        # print(f'Chessman : {chessman.name}, at position {chessman.position}')
        # print(f'Capture : {captured_chessman}')

        # Print if check or checkmate
        #if self.checkmate:
        # print(f'{self.checkmate}')


# endregion UpdateBoard

    def reset_turn(self):
        self.chessman = None
        self.disambiguating_move = None
        self.capture = None
        self.current_move = None
        self.promotion = None
        self.checkmate = None
        self.final_score_turn = False
