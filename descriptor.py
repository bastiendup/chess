
from action_parser import BoardAction
from chessman import Bishop, King, Knight, Pawn, Queen, Rook
from manager import TurnResult


class Descriptor:

    @classmethod
    def describe(cls, turn: TurnResult):
        score= turn.score
        if score:
            print(f'End of game with a result of {score}')
            return
        
        rook = turn.rook
        if rook:
            print(f'{rook}')
            return

        piece = turn.chessman
        capture = turn.captured_chessman

        promotion = turn.promotion
        if promotion:
            print(f'The {piece} has been promoted to {promotion}')
            return

        


        
        distance = cls.get_distance(turn.actions[0])
        if capture:
            print(
                f'The {piece} has moved {distance} and captured a {capture}.'
            )
        else:
            print(f'The {piece} has moved {distance}.')
        


        """
        if capture :
            ajoute capture + piece concernée
        if promotion:
            ajoute promote into + piece
        if actions > 1 => Rook
            ajoute rook + côté + color
        if actions = 1:
            ajoute has moved
        if score:
            ajoute game ended with score of
        if echec:
            ajoute met en echec le roi
        if echec et mat
            ajoute met en echec et mat
        
        """

    @classmethod
    def get_distance(cls, action: BoardAction):
        x, y = action.start_pos
        x1, y1 = action.end_pos
        piece = action.chessman
        distance = 0
        if isinstance(piece, (Pawn, Bishop)):
            distance = abs(x1 - x)
        elif isinstance(piece, (Rook, King, Queen)):
            distance = max(abs(x1 - x), abs(y1 - y))
        elif isinstance(piece, Knight):
            distance_x = abs(x1 - x)
            distance_y = abs(y1 - y)
            return f'{distance_y} square horizontally and {distance_x} squares vertically '
        return f'{distance} squares'