from dataclasses import dataclass
import re
from typing import List

from chessman import Bishop, Chessman, King, Knight, Pawn, Queen, Rook


@dataclass
class BoardAction:
    ''' Dataclass to store a board action '''
    start_pos: tuple
    end_pos: tuple
    piece: Chessman

    def __repr__(self) -> str:
        return f'{self.piece} : from {self.start_pos} to {self.end_pos} '


@dataclass
class ParsingResult:
    ''' Dataclass to store a parsing result '''
    white_turn: bool
    rook: bool = False
    movement: tuple = None
    capture: bool = False
    piece: Chessman = None
    checkmate: str = None
    promotion: Chessman = None
    final_score: str = None
    board_actions: BoardAction = None
    disambiguating_action: tuple = None


class ActionParser:
    ''' Class to parse a movement '''

    FINAL_SCORE_REGEX =                     re.compile(r'\d-\d|\*|1/2-1/2')
    ROOK_REGEX =                            re.compile(r'(O-O)(-O)?')
    PIECE_REGEX =                           re.compile(r'^(K|Q|R|B|N)')
    DISAMBIGUATING_FILE_REGEX =             re.compile(r'^([a-h])(x|[a-h])')
    DISAMBIGUATING_RANK_REGEX =             re.compile(r'^([1-8])(x|[a-h])')
    DISAMBIGUATING_FILE_AND_RANK_REGEX =    re.compile(r'^([a-h][1-8])(x|[a-h])')
    CAPTURE_REGEX =                         re.compile(r'^x')
    MOVE_REGEX =                            re.compile(r'^[a-h][1-8]')
    PROMOTION_REGEX =                       re.compile(r'^=(Q|B|N|R)')
    CHECKMATE_REGEX =                       re.compile(r'^(\+|\#)')

    def __init__(self) -> None:
        self.action = None
        self.is_white_turn = None

    def parse_movement(self, action: str, is_white_turn: bool) -> ParsingResult:
        ''' Function that parse a action

        Return an ParsingResult object
        '''
        self.action = action
        self.is_white_turn = is_white_turn

        final_score = self.check_final_score()
        if final_score:
            return ParsingResult(white_turn=is_white_turn, final_score=final_score)

        board_moves = self.check_rook()
        if board_moves:
            return ParsingResult(white_turn=is_white_turn, rook=True, board_actions=board_moves)

        piece = self.check_piece()
        disambiguating = self.check_disambiguating()
        capture = self.check_capture()
        move = self.check_move()
        promotion = self.check_promotion()
        checkmate = self.check_checkmate()

        return ParsingResult(white_turn=is_white_turn,
                             piece=piece,
                             disambiguating_action=disambiguating,
                             capture=capture,
                             movement=move,
                             promotion=promotion,
                             checkmate=checkmate)

    def check_final_score(self):
        ''' Check for a final_score pattern

        This pattern indicate the end of the game, and the final score
        '''

        match = re.search(self.FINAL_SCORE_REGEX, self.action)
        if match:
            possible_scores = {'1/2-1/2': 'DRAW', '1-0': 'WHITE WINS', '0-1': 'BLACK WINS', '*': 'INTERRUPTED GAME'}
            return possible_scores[match.group()]
        return None

    def check_rook(self):
        ''' Check for a rook pattern

        If a rook pattern is identified, call the appropriate function
        based on the rook side and color
        '''

        match = re.search(self.ROOK_REGEX, self.action)
        if match:
            color = 'white' if self.is_white_turn else 'black'
            possible_rooks = {'O-O': 'king_side_rook_', 'O-O-O': 'queen_side_rook_'}
            rook = possible_rooks[match.group()] + color
            return getattr(self, rook)()
        return None

    def king_side_rook_white(self) -> List[BoardAction]:
        '''
            Return the board movements associated
            with a king side rook for the white player
        '''
        board_moves = [BoardAction((7, 4), (7, 5), Rook(7, 5, True)), BoardAction((7, 7), (7, 6), King(7, 6, True))]
        return board_moves

    def queen_side_rook_white(self) -> List[BoardAction]:
        '''
            Return the board movements associated
            with a queen side rook for the white player
        '''
        board_moves = [BoardAction((7, 0), (7, 3), Rook(7, 3, True)), BoardAction((7, 4), (7, 2), King(7, 2, True))]
        return board_moves

    def king_side_rook_black(self) -> List[BoardAction]:
        '''
            Return the board movements associated
            with a king side rook for the black player
        '''
        board_moves = [BoardAction((0, 4), (0, 5), Rook(0, 5, False)), BoardAction((0, 0), (0, 6), King(0, 6, False))]
        return board_moves

    def queen_side_rook_black(self) -> List[BoardAction]:
        '''
            Return the board movements associated
            with a queen side rook for the black player
        '''
        board_moves = [BoardAction((0, 0), (0, 3), Rook(0, 3, False)), BoardAction((0, 4), (0, 2), King(0, 2, False))]
        return board_moves

    def check_piece(self):
        ''' Check for a piece pattern

        If no pattern is present, the piece is a Pawn
        '''

        match = re.search(self.PIECE_REGEX, self.action)
        if match:
            pieces = {'K': King, 'B': Bishop, 'Q': Queen, 'N': Knight, 'R': Rook}
            self.action = re.sub(self.PIECE_REGEX, '', self.action)
            return pieces[match.group()]
        return Pawn

    def check_disambiguating(self):
        ''' Check for a disambiguating pattern

        A disambiguating pattern is use as an indicator of the starting position for the piece,
        it's used when multiple chessman can do the same movement.
        There is three disambiguating patterns :
            file (a-h),
            rank (1-8),
            file and rank (a-h)(1-8)
        '''
        disambiguating_function = [
            self.disambiguating_file, self.disambiguating_rank, self.disambiguating_file_and_rank
        ]
        for disambiguating in disambiguating_function:
            res = disambiguating()
            if res:
                return self.translate(res)
        return None

    def disambiguating_file(self):
        ''' Check for a disambiguating pattern

        This pattern is a file pattern, it represent the file (a-h)
            of departure of the piece
        '''

        match = re.search(self.DISAMBIGUATING_FILE_REGEX, self.action)
        if match:
            self.action = re.sub(self.DISAMBIGUATING_FILE_REGEX, r'\g<2>', self.action)
            return [match.group(1), None]
        return None

    def disambiguating_rank(self):
        ''' Check for a disambiguating pattern

        This pattern is a rank pattern, it represent the rank (1-8)
            of departure of the piece
        '''

        match = re.search(self.DISAMBIGUATING_RANK_REGEX, self.action)
        if match:
            self.action = re.sub(self.DISAMBIGUATING_RANK_REGEX, r'\g<2>', self.action)
            return [None, match.group(1)]
        return None

    def disambiguating_file_and_rank(self):
        ''' Check for a disambiguating pattern

        This pattern is a file and rank pattern, it represent both the file (a-h) and the rank (1-8)
            of departure of the piece
        '''

        match = re.search(self.DISAMBIGUATING_FILE_AND_RANK_REGEX, self.action)
        if match:
            self.action = re.sub(self.DISAMBIGUATING_FILE_AND_RANK_REGEX, r'\g<2>', self.action)
            return match.group(1)
        return None

    def translate(self, coordinates: tuple):
        ''' Translate coordinates from PGN to board coordinates

        example :
            B7 -> (1, 1)
            F2 -> (6, 5)
        '''

        row = int(coordinates[1]) if coordinates[1] else None
        col = coordinates[0] if coordinates[0] else None

        board_coordinates = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        if row is None:
            return (None, board_coordinates[col])
        if col is None:
            return (8 - row, None)
        return (8 - row, board_coordinates[col])

    def check_capture(self):
        match = re.search(self.CAPTURE_REGEX, self.action)
        if match:
            self.action = re.sub(self.CAPTURE_REGEX, '', self.action)
            return True
        return None

    def check_move(self):
        ''' Check for the piece movement pattern'''

        match = re.search(self.MOVE_REGEX, self.action)
        move = match.group()
        self.action = re.sub(self.MOVE_REGEX, '', self.action)
        return move

    def check_promotion(self):
        ''' Check for piece promotion pattern
        This pattern indicate if there is a chessman promotion during the turn
        '''

        match = re.search(self.PROMOTION_REGEX, self.action)
        if match:
            promote_piece = {'B': Bishop, 'Q': Queen, 'N': Knight, 'R': Rook}
            promotion = promote_piece[match.group(1)]
            self.action = re.sub(self.PROMOTION_REGEX, '', self.action)
            return promotion
        return None

    def check_checkmate(self):
        ''' Check for the checkmate pattern
        This pattern indicate if there is a check or a checkmate move
        '''

        match = re.search(self.CHECKMATE_REGEX, self.action)
        if match:
            check_ending = {'+': 'Check', '#': 'Checkmate'}
            checkmate = check_ending[match.group(1)]
            self.action = re.sub(self.CHECKMATE_REGEX, '', self.action)
            return checkmate
        return None
