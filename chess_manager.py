import re


class chess_manager():


    def CheckIfKingRook(movement):
        king_rook_regex = re.compile(r'(O-O)(-O)?')
        match = re.match(king_rook_regex, movement)
        if match:
            k,q = re.match(king_rook_regex, movement).groups()
            if(q is None):
                print("King side rook")
            else:
                print("Queen side rook")
        else:
            print("No rook")

    if __name__ == "__main__":
        while True:
            movement = input("Movement :")
            CheckIfKingRook(movement)
