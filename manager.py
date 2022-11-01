import sys
from dataclasses import dataclass
from typing import List

from action_parser import BoardAction, ParsingResult
from board import Board
from chessman import Chessman
from cursor import CURSOR_DOWN
from logger import Logger


@dataclass
class TurnResult:
    chessman: Chessman = None  # type: ignore
    rook: str = None  # type: ignore
    captured_chessman: Chessman = None  # type: ignore
    promotion: Chessman = None  # type: ignore
    score: str = None  # type: ignore
    actions: List[BoardAction] = None  # type: ignore
    check: bool = None  # type: ignore
    checkmate: bool = None  # type: ignore
    player: str = None  # type: ignore


class Manager:
    ''' Class to handle a board result '''

    def __init__(self):
        self.logger = Logger()
        self.board = Board(self.logger)

    def compute_parsing_result(self, p_result: ParsingResult) -> TurnResult: 
        """ Compute a parsing result """

        turn = p_result.white_turn
        player = 'white' if turn else 'black'

        final_score = p_result.final_score
        if final_score:
            return TurnResult(score=final_score, player=player)

        rook = p_result.rook
        if rook:
            return TurnResult(actions=p_result.board_actions,
                              rook=rook,
                              player=player)

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
            promotion = self.board.promote(
                chessman,  # type: ignore
                promotion,
                mvmt)
            actions.pop()

        # TODO : ajouter la prise en compte de l'echec et echec et mat

        check, checkmate = None, None
        if p_result.checkmate:
            if p_result.checkmate == 'Check':
                check = True
            else:
                checkmate = True

        return TurnResult(
            chessman=chessman,
            captured_chessman=captured_chessman,  # type: ignore
            promotion=promotion,
            actions=actions,
            player=player,
            check=check,  # type: ignore
            checkmate=checkmate)  # type: ignore

    def identify_chesssman(self, chessmans: List[Chessman], helper: tuple,
                           white_turn: bool,
                           target: tuple) -> Chessman:  # type: ignore
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
        #TODO : peut mieux faire
        self.logger.add_log(turn)
        if turn.score:
            self.print_final_score(turn.score)
            return True
        for action in turn.actions:
            self.board.move_chessman(action.start_pos, action.end_pos,
                                     action.chessman)
        self.board.print_board()

    def print_final_score(self, score):
        sys.stdout.write(CURSOR_DOWN * 13)  # Cursor down 13 lines
        print('  ' * 7 + score)
