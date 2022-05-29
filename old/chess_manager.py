import re
from board import Board


class chess_manager:

    def __init__(self) -> None:
        self.Piece = ""

    def CheckIfKingRook(self, movement):
        possible_rooks = {'O-O': 'King side', 'O-O-O': 'Queen side'}
        king_rook_regex = re.compile(r'(O-O)(-O)?')
        match = re.search(king_rook_regex, movement)
        rook = 'No'
        if match:
            rook = possible_rooks[match.group()]
        print(f'Rook                       -> {rook}')
        return re.sub(king_rook_regex, '', movement)

    def CheckPiece(self, movement):
        pieces = {
            'K': 'King',
            'B': 'Bishop',
            'Q': 'Queen',
            'N': 'Knight',
            'R': 'Rook'
        }
        piece_regex = re.compile(r'^(K|Q|R|B|N)')
        match = re.search(piece_regex, movement)
        piece = 'Pawn'
        if match:
            piece = pieces[match.group()]
        print(f'Piece                      -> {piece}')
        self.Piece = piece
        return re.sub(r'^(K|Q|R|B|N)', '', movement)

    def CheckCapture(self, movement):
        match = re.search(r'^x', movement)
        capture = 'No'
        if match:
            capture = 'Yes'
            movement = re.sub(r'^x', '', movement)
        print(f'Capture                    -> {capture}')
        return movement

    def DisambiguatingFile(self, movement):
        # Check for the file of departure before the move
        regex = re.compile(r'^([a-h])(x|[a-h])')
        match = re.search(regex, movement)
        disambiguating_file = 'No'
        if match:
            disambiguating_file = match.group(1)
            movement = re.sub(r'^[a-h]', '', movement)
        print(f'Disambiguating File        -> {disambiguating_file}')
        return movement, match

    def DisambiguatingRank(self, movement):
        # Check for the rank of departure before the move
        regex = re.compile(r'^([1-8])(x|[a-h])')
        match = re.search(regex, movement)
        disambiguating_file = 'No'
        if match:
            disambiguating_file = match.group(1)
            movement = re.sub(r'^[1-8]', '', movement)
        print(f'Disambiguating Rank        -> {disambiguating_file}')
        return movement, match

    def DisambiguatingFileAndRank(self, movement):
        # Check for both the file and rank of departure before the move
        regex = re.compile(r'^([a-h][1-8])(x|[a-h])')
        match = re.search(regex, movement)
        disambiguating_file = 'No'
        if match:
            disambiguating_file = match.group(1)
            movement = re.sub(r'^[a-h][1-8]', '', movement)
        print(f'Disambiguating File & Rank -> {disambiguating_file}')
        return movement

    def CheckMoving(self, movement):
        # Check for move
        regex = re.compile(r'^[a-h][1-8]')
        match = re.search(regex, movement)
        move = 'No'
        if match:
            move = match.group()
            movement = re.sub(r'^[a-h][1-8]', '', movement)
        print(f'Moving                     -> {move}')
        return movement

    def CheckPromotion(self, movement):
        # Check for pawn promote
        promote_piece = {
            'K': 'King',
            'B': 'Bishop',
            'Q': 'Queen',
            'N': 'Knight',
            'R': 'Rook'
        }
        regex = re.compile(r'^=(Q|B|N|R)')
        match = re.search(regex, movement)
        promotion = 'No'
        if match:
            promotion = promote_piece[match.group(1)]
            movement = re.sub(r'^=(Q|B|N|R)', '', movement)
        print(f'Promotion                  -> {promotion}')
        return movement

    def CheckForCheckMove(self, movement):
        # Check for checkmate
        check_ending = {'+': 'Check', '#': 'Checkmate'}
        regex = re.compile(r'^(\+|\#)')
        match = re.search(regex, movement)
        checkmate = 'No'
        if match:
            checkmate = check_ending[match.group(1)]
            movement = re.sub(r'^\+|\#', '', movement)
        print(f'Checkmate                  -> {checkmate}')
        return movement

    def CheckDisambiguating(self, movement):
        movement, match = self.DisambiguatingFile(movement)
        if match:
            return movement

        movement, match = self.DisambiguatingRank(movement)
        if match:
            return movement

        movement = self.DisambiguatingFileAndRank(movement)
        return movement


board = Board()
manager = chess_manager()
while True:
    board.print_board()
    movement = input('Movement : ')
    movement = manager.CheckIfKingRook(movement)
    movement = manager.CheckPiece(movement)
    movement = manager.CheckDisambiguating(movement)
    movement = manager.CheckCapture(movement)
    movement = manager.CheckMoving(movement)
    movement = manager.CheckPromotion(movement)
    movement = manager.CheckForCheckMove(movement)
    print(manager.Piece)
    print('')
