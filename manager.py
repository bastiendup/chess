from dataclasses import dataclass
from typing import List
from action_parser import ActionParser, BoardAction, ParsingResult
from board import Board
from chessman import Bishop, Chessman, Knight, Queen, Rook


@dataclass
class TurnResult:
    chessman: Chessman = None
    captured_chessman: Chessman = None
    promotion: Chessman = None
    score: str = None
    actions: List[BoardAction] = None
    player: str = None


class Manager:
    ''' Class to handle a board result '''

    def __init__(self):
        self.board = Board()

    def compute_parsing_result(self, p_result: ParsingResult) -> TurnResult:
        """ Compute a parsing result """

        turn = p_result.white_turn
        player = 'white' if turn else 'black'

        final_score = p_result.final_score
        if final_score:
            return TurnResult(score=final_score, player=player)

        actions = p_result.board_actions
        if actions:
            return TurnResult(actions=actions, player=player)

        captured_chessman = None
        if p_result.capture:
            captured_chessman = self.board.get(p_result.movement)

        possibles_chessmans = self.board.get_chessmans(p_result.piece, turn)
        mvmt = p_result.movement
        chessman = self.identify_chesssman(possibles_chessmans,
                                           p_result.disambiguating_action,
                                           turn, mvmt)
        actions = [BoardAction(chessman.position, mvmt, chessman)]

        promotion = p_result.promotion
        if promotion:
            x = chessman.position[0]
            y = chessman.position[1]
            if promotion == Queen:
                chessman = Queen(x, y, turn)
            if promotion == Rook:
                chessman = Rook(x, y, turn)
            if promotion == Bishop:
                chessman = Bishop(x, y, turn)
            if promotion == Knight:
                chessman = Knight(x, y, turn)

        return TurnResult(chessman=chessman,
                          captured_chessman=captured_chessman,
                          promotion=promotion,
                          actions=actions,
                          player=player)

    def identify_chesssman(self, chessmans: List[Chessman], helper: tuple,
                           white_turn: bool, target: tuple) -> Chessman:
        """ Method to identify the chessman """
        for chessman in chessmans:
            chessman.compute_possible_move(self.board, white_turn)
            if self.is_valid_chessman(chessman, helper, target):
                chessman.first_move = False
                return chessman

    def is_valid_chessman(self, chessman: Chessman, helper: tuple,
                          target: tuple) -> bool:
        """ Determine if the currently selected chessman is a valid chessman """
        moves = chessman.possible_moves
        if not moves:
            return False
        for move in moves:
            if move == target:
                if not helper:
                    return True
                if helper[0] is None and chessman.position[1] == helper[1]:
                    return True
                if helper[1] is None and chessman.position[0] == helper[0]:
                    return True
                if move == helper:
                    return True
        return False

    def print_board(self, turn: TurnResult):
        for action in turn.actions:
            self.board.move_chessman(action.start_pos, action.end_pos,
                                     action.chessman)
        self.board.print_board_with_coordinates()
