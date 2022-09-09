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

    def __str__(self) -> str:
        return f'Move {self.chessman} from {self.start_pos} to {self.end_pos}'


class ParsingResult:

    def __init__(self,
                 final_score=None,
                 piece=None,
                 board_moves=None,
                 disambiguating_moves=None,
                 move=None,
                 promotion=None,
                 checkmate=None):
        self.final_score = final_score
        self.piece = Pawn if not piece else piece
        self.board_moves = board_moves
        self.disambiguating_move = disambiguating_moves
        self.move = move
        self.promotion = promotion
        self.checkmate = checkmate

    def print(self):
        print(
            "\n Final score          : ",
            self.final_score,
            "\n Chessman             : ",
            self.piece,
            "\n Board movements      : ",
            [str(m) for m in self.board_moves] if self.board_moves else None,
            "\n Disambiguating moves : ",
            self.disambiguating_move,
            "\n Move                 : ",
            self.move,
            "\n Promotion            : ",
            self.promotion,
            "\n Checkmate            : ",
            self.checkmate,
        )


class MovementParser:

    def __init__(self):
        self.movement = None
        self.is_white_turn = True

    def parse_movement(self, movement: str, is_white_turn: bool) -> ParsingResult:
        self.movement = movement
        self.is_white_turn = is_white_turn

        final_score = self.check_final_score()
        if (final_score):
            return ParsingResult(final_score=final_score)

        board_moves = self.check_rook()
        if (board_moves):
            return ParsingResult(board_moves=board_moves)

        piece = self.check_piece()
        disambiguating = self.check_disambiguating()
        move = self.check_move()
        promotion = self.check_promotion()
        checkmate = self.check_checkmate()

        return ParsingResult(piece=piece,
                             disambiguating_moves=disambiguating,
                             move=move,
                             promotion=promotion,
                             checkmate=checkmate)

    # Score
    def check_final_score(self):
        final_score_regex = re.compile(r'\d-\d|\*|1/2-1/2')
        match = re.search(final_score_regex, self.movement)
        if match:
            possible_scores = {'1/2-1/2': 'DRAW', '1-0': 'WHITE WINS', '0-1': 'BLACK WINS', '*': 'INTERRUPTED GAME'}
            return possible_scores[match.group()]

    # King rook
    def check_rook(self):
        king_rook_regex = re.compile(r'(O-O)(-O)?')
        match = re.search(king_rook_regex, self.movement)
        if match:
            color = 'white' if self.is_white_turn else 'black'
            possible_rooks = {'O-O': 'king_side_rook_', 'O-O-O': 'queen_side_rook_'}
            rook = possible_rooks[match.group()] + color
            return getattr(self, rook)()

    def king_side_rook_white(self):
        board_moves = [BoardMove((7, 4), (7, 5), Rook(7, 5, True)), BoardMove((7, 7), (7, 6), King(7, 6, True))]
        return board_moves

    def queen_side_rook_white(self):
        board_moves = [BoardMove((7, 0), (7, 3), Rook(7, 3, True)), BoardMove((7, 4), (7, 2), King(7, 2, True))]
        return board_moves

    def king_side_rook_black(self):
        board_moves = [BoardMove((0, 4), (0, 5), Rook(0, 5, False)), BoardMove((0, 0), (0, 6), King(0, 6, False))]
        return board_moves

    def queen_side_rook_black(self):
        board_moves = [BoardMove((0, 0), (0, 3), Rook(0, 3, False)), BoardMove((0, 4), (0, 2), King(0, 2, False))]
        return board_moves

    # Identify piece
    def check_piece(self):
        piece_regex = re.compile(r'^(K|Q|R|B|N)')
        match = re.search(piece_regex, self.movement)
        if match:
            pieces = {'K': King, 'B': Bishop, 'Q': Queen, 'N': Knight, 'R': Rook}
            self.movement = re.sub(r'^(K|Q|R|B|N)', '', self.movement)
            return pieces[match.group()]

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
            self.disambiguating_file, self.disambiguating_rank, self.disambiguating_file_and_rank
        ]
        for d in disambiguating_function:
            res = d()
            if (res):
                return self.translate(res)

    def translate(self, s):
        '''
        translate coordinates from pgn to board 
        ex: B7 -> (1, 1)
            F2 -> (6, 5)
        '''
        row = int(s[1]) if s[1] is not None else None
        col = s[0] if s[0] is not None else None

        dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        if row is None:
            return (None, dict[col])
        if col is None:
            return (8 - row, None)
        return (8 - row, dict[col])

    def check_move(self):
        regex = re.compile(r'^[a-h][1-8]')
        match = re.search(regex, self.movement)
        if match:
            move = match.group()
            self.movement = re.sub(r'^[a-h][1-8]', '', self.movement)
            return move

    def check_promotion(self):
        # Check for pawn promote
        regex = re.compile(r'^=(Q|B|N|R)')
        match = re.search(regex, self.movement)
        if match:
            promote_piece = {'B': Bishop, 'Q': Queen, 'N': Knight, 'R': Rook}
            promotion = promote_piece[match.group(1)]
            self.movement = re.sub(r'^=(Q|B|N|R)', '', self.movement)
            return promotion

    def check_checkmate(self):
        # Check for checkmate
        regex = re.compile(r'^(\+|\#)')
        match = re.search(regex, self.movement)
        if match:
            check_ending = {'+': 'Check', '#': 'Checkmate'}
            checkmate = check_ending[match.group(1)]
            self.movement = re.sub(r'^\+|\#', '', self.movement)
            return checkmate
