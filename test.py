import re
import sys
import time
from cursor import BLACK, BLUE, CURSOR_REWRITE_LINE, CURSOR_UP, DARK_GRAY, GREEN, DARK_GRAY, RED, RESET_CURSOR, WHITE
from action_parser import ActionParser, ParsingResult
from descriptor import Descriptor
from manager import Manager, TurnResult


def add_line(string: str, action, color_true=GREEN, color_false=DARK_GRAY, end_of_line='\n'):
    color = color_true if action else color_false
    return '{}{}     * {}{} -> {}{}{}'.format(CURSOR_REWRITE_LINE, color,
                                                    string,
                                                    " " * (23 - len(string)),
                                                    action, RESET_CURSOR, end_of_line)


def print_action(action:ParsingResult):
    string = '\n'
    string += add_line('Final score', action.final_score)
    string += add_line('Rook', action.rook)
    string += add_line('Board Action', action.board_actions)
    string += add_line('Piece', action.piece)
    string += add_line('Disambiguating action', action.disambiguating_action)
    string += add_line('Capture', action.capture)
    string += add_line('Movement', action.movement)
    string += add_line('Promotion', action.promotion)
    string += add_line('Checkmate', action.checkmate, end_of_line='')
    print(string)
    


def print_turn(turn: TurnResult):
    string = '\n'
    string += add_line('Chessman', turn.chessman)
    string += add_line('Capture', turn.captured_chessman)
    string += add_line('Actions', turn.actions, end_of_line='')
    print(string)


with open('Viswanathan Anand_vs_Garry Kasparov_2021.07.10.pgn') as f:
    pgn_game = f.read()

clean_headers = re.sub(r'(\[.*\]\n\n?)', '', pgn_game, 0)
clean_line_return = re.sub(r'\n', ' ', clean_headers, 0)

pgn_content = re.sub(r'(\d\d?\d?\. ?)', '\\n', clean_line_return, 0)

moves = re.split(r'\n', pgn_content)

# print('\n')
parsing_result = dict()
is_white_turn = True
parser = ActionParser()
for i, move in enumerate(moves):
    if move == '':
        continue
    if i == 16:
        print()
    parsing_result[i] = dict()
    for idx, movement in enumerate(move.split()):
        parsing_result[i][idx] = {
            'mvmt': movement,
            'action': parser.parse_movement(movement, is_white_turn)
        }
        is_white_turn = not is_white_turn

manager = Manager()
turn_results = dict()
for idx, turn in parsing_result.items():
    #print(f'Turn : {idx}')
    turn_results[idx] = dict()
    for i, value in turn.items():

        mvmt = value.get('mvmt')
        action = value.get('action')
        color = WHITE if action.white_turn else BLUE
        player = 'White' if action.white_turn else 'Black'

        print(
            f'{CURSOR_REWRITE_LINE}Turn : {idx} \n {color} Action : {mvmt}        \n  Player : {player}              {RESET_CURSOR}'
        )

        # print_action(action)

        res = manager.compute_parsing_result(action)
        turn_results[idx][player] = res

        # print_turn(res)

        if not manager.print_board(res):
            sys.stdout.write(CURSOR_UP * 16)  # Cursor up 14 lines
            # sys.stdout.write(CURSOR_UP * 31)  # Cursor up 14 lines

        # time.sleep(.02)

for k, v in turn_results.items():
    for kk, vv in v.items():
        Descriptor.describe(vv) 


# for res in result:
#     res.print()
