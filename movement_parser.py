import re

from chessman import *


class BoardMove:
    """
    Use to indicate to the chess_manager which board he have to apply

    ex: BoardMove((6,4), (4,4), Pawn)
    """

    def __init__(self, start_pos, end_pos, chessman: Chessman):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.chessman = chessman


class ParsingResult:
    def __init__(self):
        self.final_score: str

        self.board_moves = []
        self.disambiguating_move = None


class MovementParser:

    def __init__(self):
        self.movement = None
        self.is_white_turn = False
        self.piece = Pawn
        self.result = ParsingResult()

    def parse_movement(self, movement: str, is_white_turn: bool) -> ParsingResult:
        self.movement = movement
        self.is_white_turn = is_white_turn

        if(self.check_final_score()):
            return self.result
        if(self.check_rook()):
            return self.result
        self.check_piece()
        self.check_disambiguating()

        return self.result

    # Score
    def check_final_score(self):
        final_score_regex = re.compile(r'\d-\d|\*|1/2-1/2')
        match = re.search(final_score_regex, self.movement)
        if match:
            possible_scores = {'1/2-1/2': 'DRAW', '1-0': 'WHITE WINS',
                               '0-1': 'BLACK WINS', '*': 'INTERRUPTED GAME'}
            self.result.final_score = possible_scores[match.group()]
            return True

    # King rook
    def check_rook(self):
        king_rook_regex = re.compile(r'(O-O)(-O)?')
        match = re.search(king_rook_regex, self.movement)
        if match:
            color = 'white' if self.is_white_turn else 'black'
            possible_rooks = {'O-O': 'king_side_rook_',
                              'O-O-O': 'queen_side_rook_'}
            rook = possible_rooks[match.group()] + color
            getattr(self, rook)()
            return True

    def king_side_rook_white(self):
        board_moves = [
            BoardMove((7, 4), (7, 5), Rook(7, 5, True)),
            BoardMove((7, 7), (7, 6), King(7, 6, True))
        ]
        self.result.board_moves.extend(board_moves)

    def queen_side_rook_white(self):
        board_moves = [
            BoardMove((7, 0), (7, 3), Rook(7, 3, True)),
            BoardMove((7, 4), (7, 2), King(7, 2, True))
        ]
        self.result.board_moves.extend(board_moves)

    def king_side_rook_black(self):
        board_moves = [
            BoardMove((0, 4), (0, 5), Rook(0, 5, False)),
            BoardMove((0, 0), (0, 6), King(0, 6, False))
        ]
        self.result.board_moves.extend(board_moves)

    def queen_side_rook_black(self):
        board_moves = [
            BoardMove((0, 0), (0, 3), Rook(0, 3, False)),
            BoardMove((0, 4), (0, 2), King(0, 2, False))
        ]
        self.result.board_moves.extend(board_moves)

    # Identify piece
    def check_piece(self):
        piece_regex = re.compile(r'^(K|Q|R|B|N)')
        match = re.search(piece_regex, self.movement)
        if match:
            pieces = {'K': King, 'B': Bishop,
                      'Q': Queen, 'N': Knight, 'R': Rook}
            self.chessman = pieces[match.group()]
            self.movement = re.sub(r'^(K|Q|R|B|N)', '', self.movement)

    # Identify if there is an indication of the starting position (used when multiple chessman can do the same movement)
    def disambiguating_file(self):
        # Check for the file (a-h) of departure before the current_move
        regex = re.compile(r'^([a-h])(x|[a-h])')
        match = re.search(regex, self.movement)
        if match:
            self.movement = re.sub(r'^[a-h]', '', self.movement)
            return [match.group(1), None]

    def disambiguating_rank(self):
        # Check for the rank (1-8) of departure before the current_move
        regex = re.compile(r'^([1-8])(x|[a-h])')
        match = re.search(regex, self.movement)
        if match:
            self.movement = re.sub(r'^[1-8]', '', self.movement)
            return [None, match.group(1)]

    def disambiguating_file_and_rank(self):
        # Check for the file (a-h) and rank (1-8) of departure before the current_move
        regex = re.compile(r'^([a-h][1-8])(x|[a-h])')
        match = re.search(regex, self.movement)
        if match:
            self.movement = re.sub(r'^[a-h][1-8]', '', self.movement)
            return match.group(1)

    def check_disambiguating(self):
        disambiguating_function = [
            self.disambiguating_file,
            self.disambiguating_rank,
            self.disambiguating_file_and_rank
        ]
        for d in disambiguating_function:
            res = d()
            if(res):
                print(res)
                self.disambiguating_move = self.translate(d)
