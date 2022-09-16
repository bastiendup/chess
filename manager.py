from action_parser import ParsingResult
from board import Board


class Manager:
    ''' Class to handle a board result '''
    def __init__(self):
        self.board = Board()

    def compute_parsing_result(self, p_result:ParsingResult):
        if p_result.capture:
            captured_chessman = 
