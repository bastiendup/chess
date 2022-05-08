from calendar import c
import re


class chess_manager:
    def CheckIfKingRook(movement):
        possible_rooks = {'O-O': 'King side rook', 'O-O-O': 'Queen side rook'}
        king_rook_regex = re.compile(r'(O-O)(-O)?')
        match = re.search(king_rook_regex, movement)
        rook = 'No rook'
        if match:
            rook = possible_rooks[match.group()]
        print(rook)
        return re.sub(king_rook_regex, '', movement)

    def CheckPiece(movement):
        pieces = {'K': 'King', 'B': 'Bishop', 'Q': 'Queen', 'N': 'Knight', 'R': 'Rook'}
        piece_regex = re.compile(r'^(K|Q|R|B|N)')
        match = re.search(piece_regex, movement)
        piece = 'pawn'
        if match:
            piece = pieces[match.group()]
        print(f'Piece is {piece}')
        return re.sub(piece_regex, '', movement)

    def CheckCapture(movement):
        match = re.search(r'^x', movement)
        capture = 'no capture'
        if match:
            capture = 'capture'
        print(capture)
        return re.sub(r'^x', '', movement)

    if __name__ == '__main__':
        while True:
            movement = input('Movement :')
            movement = CheckIfKingRook(movement)
            movement = CheckPiece(movement)
            movement = CheckCapture(movement)
            print('')
