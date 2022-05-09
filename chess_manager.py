from calendar import c
import re


class chess_manager:
    def CheckIfKingRook(movement):
        possible_rooks = {'O-O': 'King side', 'O-O-O': 'Queen side'}
        king_rook_regex = re.compile(r'(O-O)(-O)?')
        match = re.search(king_rook_regex, movement)
        rook = 'No'
        if match:
            rook = possible_rooks[match.group()]
        print(f'Rook -> {rook}')
        return re.sub(king_rook_regex, '', movement)

    def CheckPiece(movement):
        pieces = {'K': 'King', 'B': 'Bishop', 'Q': 'Queen', 'N': 'Knight', 'R': 'Rook'}
        piece_regex = re.compile(r'^(K|Q|R|B|N)')
        match = re.search(piece_regex, movement)
        piece = 'Pawn'
        if match:
            piece = pieces[match.group()]
        print(f'Piece -> {piece}')
        return re.sub(piece_regex, '', movement)

    def CheckCapture(movement):
        match = re.search(r'^x', movement)
        capture = 'No'
        if match:
            capture = 'Yes'
            print(f'Capture -> {capture}')
            return re.sub(r'^x', '', movement) 
        print(f'Capture -> {capture}')
        return movement

    def DisambiguatingFile(movement):
        # Check for the file of departure before the move
        regex = re.compile(r'^[a-h](x|[a-h])')
        match = re.search(regex, movement)
        disambiguating_file = 'No'
        if match:
            disambiguating_file = match.group()
            print(f'Disambiguating File -> {disambiguating_file}')
            return re.sub(r'^[a-h]', '', movement) 
        print(f'Disambiguating File -> {disambiguating_file}')
        return movement

    def DisambiguatingRank(movement):
        # Check for the rank of departure before the move
        regex = re.compile(r'^[1-8](x|[a-h])')
        match = re.search(regex, movement)
        disambiguating_file = 'No'
        if match:
            disambiguating_file = match.group()
            print(f'Disambiguating Rank -> {disambiguating_file}')
            return re.sub(r'^[1-8]', '', movement) 
        print(f'Disambiguating Rank -> {disambiguating_file}')
        return movement

    def DisambiguatingFileAndRank(movement):
        # Check for both the file and rank of departure before the move
        regex = re.compile(r'^[a-h][1-8](x|[a-h])')
        match = re.search(regex, movement)
        disambiguating_file = 'No'
        if match:
            disambiguating_file = match.group()
            print(f'Disambiguating File & Rank -> {disambiguating_file}')
            return re.sub(r'^[a-h][1-8]', '', movement) 
        print(f'Disambiguating File & Rank -> {disambiguating_file}')
        return movement


    if __name__ == '__main__':
        while True:
            movement = input('Movement :')
            movement = CheckIfKingRook(movement)
            movement = CheckPiece(movement)
            movement = DisambiguatingFile(movement)
            movement = DisambiguatingRank(movement)
            movement = DisambiguatingFileAndRank(movement)
            movement = CheckCapture(movement)
            print(f'Movement is now : {movement}')
            print('')