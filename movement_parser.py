from dataclasses import dataclass
import re
from typing import List

from chessman import Bishop, Chessman, King, Knight, Pawn, Queen, Rook


@dataclass
class BoardMovement:
    """ Dataclass to store a board movement """
    start_pos: tuple
    end_pos: tuple
    piece: Chessman


@dataclass
class ParsingResult:
    """ Dataclass to store a parsing result"""
    move: tuple = None
    piece: Chessman = Pawn
    checkmate: str = None
    promotion: Chessman = None
    final_score: str = None
    board_moves: BoardMovement = None
    disambiguating_move: tuple = None


class MovementParser:
    """ Class to parse a movement """

  

    @classmethod
    def parse_movement(self, movement: str,
                       is_white_turn: bool) -> ParsingResult:
        """Function that parse a movement

        Return an ParsingResult object
        """
        self.movement = movement
        self.is_white_turn = is_white_turn

        final_score = self.check_final_score()
        if final_score:
            return ParsingResult(final_score=final_score)

        board_moves = self.check_rook()
        if board_moves:
            return ParsingResult(board_moves=board_moves)

        piece = self.check_piece()
        disambiguating = self.check_disambiguating()
        move = self.check_move()
        promotion = self.check_promotion()
        checkmate = self.check_checkmate()

        return ParsingResult(piece=piece,
                             disambiguating_move=disambiguating,
                             move=move,
                             promotion=promotion,
                             checkmate=checkmate)

    def check_final_score(self):
        """ Check for a final_score pattern

        This pattern indicate the end of the game, and the final score
        """

        final_score_regex = re.compile(r'\d-\d|\*|1/2-1/2')
        match = re.search(final_score_regex, self.movement)
        if match:
            possible_scores = {
                '1/2-1/2': 'DRAW',
                '1-0': 'WHITE WINS',
                '0-1': 'BLACK WINS',
                '*': 'INTERRUPTED GAME'
            }
            return possible_scores[match.group()]
        return None

    def check_rook(self):
        """ Check for a rook pattern

        If a rook pattern is identified, call the appropriate function
        based on the rook side and color
        """
        king_rook_regex = re.compile(r'(O-O)(-O)?')
        match = re.search(king_rook_regex, self.movement)
        if match:
            color = 'white' if self.is_white_turn else 'black'
            possible_rooks = {
                'O-O': 'king_side_rook_',
                'O-O-O': 'queen_side_rook_'
            }
            rook = possible_rooks[match.group()] + color
            return getattr(self, rook)()
        return None

    def king_side_rook_white(self) -> List[BoardMovement]:
        """
            Return the board movements associated
            with a king side rook for the white player
        """
        board_moves = [
            BoardMovement((7, 4), (7, 5), Rook(7, 5, True)),
            BoardMovement((7, 7), (7, 6), King(7, 6, True))
        ]
        return board_moves

    def queen_side_rook_white(self) -> List[BoardMovement]:
        """
            Return the board movements associated
            with a queen side rook for the white player
        """
        board_moves = [
            BoardMovement((7, 0), (7, 3), Rook(7, 3, True)),
            BoardMovement((7, 4), (7, 2), King(7, 2, True))
        ]
        return board_moves

    def king_side_rook_black(self) -> List[BoardMovement]:
        """
            Return the board movements associated
            with a king side rook for the black player
        """
        board_moves = [
            BoardMovement((0, 4), (0, 5), Rook(0, 5, False)),
            BoardMovement((0, 0), (0, 6), King(0, 6, False))
        ]
        return board_moves

    def queen_side_rook_black(self) -> List[BoardMovement]:
        """
            Return the board movements associated
            with a queen side rook for the black player
        """
        board_moves = [
            BoardMovement((0, 0), (0, 3), Rook(0, 3, False)),
            BoardMovement((0, 4), (0, 2), King(0, 2, False))
        ]
        return board_moves

    def check_piece(self):
        """ Check for a piece pattern

        If no pattern is present, the piece is a Pawn
        """
        piece_regex = re.compile(r'^(K|Q|R|B|N)')
        match = re.search(piece_regex, self.movement)
        if match:
            pieces = {
                'K': King,
                'B': Bishop,
                'Q': Queen,
                'N': Knight,
                'R': Rook
            }
            self.movement = re.sub(r'^(K|Q|R|B|N)', '', self.movement)
            return pieces[match.group()]
        return Pawn

    def check_disambiguating(self):
        """ Check for a disambiguating pattern

        A disambiguating pattern is use as an indicator of the starting position for the piece,
        it's used when multiple chessman can do the same movement.
        There is three disambiguating patterns :
            file (a-h),
            rank (1-8),
            file and rank (a-h)(1-8)
        """
        disambiguating_function = [
            self.disambiguating_file, self.disambiguating_rank,
            self.disambiguating_file_and_rank
        ]
        for disambiguating in disambiguating_function:
            res = disambiguating()
            if res:
                return self.translate(res)
        return None

    def disambiguating_file(self):
        """ Check for a disambiguating pattern

        This pattern is a file pattern, it represent the file (a-h)
            of departure of the piece
        """
        regex = re.compile(r'^([a-h])(x|[a-h])')
        match = re.search(regex, self.movement)
        if match:
            self.movement = re.sub(r'^[a-h]', '', self.movement)
            return [match.group(1), None]
        return None

    def disambiguating_rank(self):
        """ Check for a disambiguating pattern

        This pattern is a rank pattern, it represent the rank (1-8)
            of departure of the piece
        """
        regex = re.compile(r'^([1-8])(x|[a-h])')
        match = re.search(regex, self.movement)
        if match:
            self.movement = re.sub(r'^[1-8]', '', self.movement)
            return [None, match.group(1)]
        return None

    def disambiguating_file_and_rank(self):
        """ Check for a disambiguating pattern

        This pattern is a file and rank pattern, it represent both the file (a-h) and the rank (1-8)
            of departure of the piece
        """
        regex = re.compile(r'^([a-h][1-8])(x|[a-h])')
        match = re.search(regex, self.movement)
        if match:
            self.movement = re.sub(r'^[a-h][1-8]', '', self.movement)
            return match.group(1)
        return None

    def translate(self, coordinates: tuple):
        """ Translate coordinates from PGN to board coordinates

        example :
            B7 -> (1, 1)
            F2 -> (6, 5)
        """
        row = int(coordinates[1]) if coordinates[1] else None
        col = coordinates[0] if coordinates[0] else None

        board_coordinates = {
            'a': 0,
            'b': 1,
            'c': 2,
            'd': 3,
            'e': 4,
            'f': 5,
            'g': 6,
            'h': 7
        }
        if row is None:
            return (None, board_coordinates[col])
        if col is None:
            return (8 - row, None)
        return (8 - row, board_coordinates[col])

    def check_move(self):
        """ Check for the piece movement pattern"""
        regex = re.compile(r'^[a-h][1-8]')
        match = re.search(regex, self.movement)
        move = match.group()
        self.movement = re.sub(r'^[a-h][1-8]', '', self.movement)
        return move

    def check_promotion(self):
        """ Check for piece promotion pattern
        This pattern indicate if there is a chessman promotion during the turn
        """
        regex = re.compile(r'^=(Q|B|N|R)')
        match = re.search(regex, self.movement)
        if match:
            promote_piece = {'B': Bishop, 'Q': Queen, 'N': Knight, 'R': Rook}
            promotion = promote_piece[match.group(1)]
            self.movement = re.sub(r'^=(Q|B|N|R)', '', self.movement)
            return promotion
        return None

    def check_checkmate(self):
        """ Check for the checkmate pattern
        This pattern indicate if there is a check or a checkmate move
        """
        regex = re.compile(r'^(\+|\#)')
        match = re.search(regex, self.movement)
        if match:
            check_ending = {'+': 'Check', '#': 'Checkmate'}
            checkmate = check_ending[match.group(1)]
            self.movement = re.sub(r'^\+|\#', '', self.movement)
            return checkmate
        return None
