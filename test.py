import re
import sys
import time
from cursor import BLACK, BLUE, CURSOR_REWRITE_LINE, CURSOR_UP, DARK_GRAY, GREEN, DARK_GRAY, RED, RESET_CURSOR, WHITE
from action_parser import ActionParser, ParsingResult
from manager import Manager, TurnResult


def print_action(action):
    print('\n')
    print(
        f'        * Turn                   -> {"White" if action.white_turn else "Black"} '
    )
    COLOR = GREEN if action.final_score else DARK_GRAY
    print(
        f'{CURSOR_REWRITE_LINE}   {COLOR}     * Final score            -> {action.final_score} '
    )
    COLOR = GREEN if action.rook else DARK_GRAY
    print(
        f'{CURSOR_REWRITE_LINE}   {COLOR}     * Rook                   -> {action.rook} '
    )
    COLOR = GREEN if action.board_actions else DARK_GRAY
    print(
        f'{CURSOR_REWRITE_LINE}   {COLOR}     * Board Action           -> {action.board_actions} '
    )
    COLOR = GREEN if action.piece else DARK_GRAY
    print(
        f'{CURSOR_REWRITE_LINE}   {COLOR}     * Piece                  -> {action.piece} '
    )
    COLOR = GREEN if action.disambiguating_action else DARK_GRAY
    print(
        f'{CURSOR_REWRITE_LINE}   {COLOR}     * Disambiguating action  -> {action.disambiguating_action} '
    )
    COLOR = GREEN if action.capture else DARK_GRAY
    print(
        f'{CURSOR_REWRITE_LINE}   {COLOR}     * Capture                -> {action.capture} '
    )
    COLOR = GREEN if action.movement else DARK_GRAY
    print(
        f'{CURSOR_REWRITE_LINE}   {COLOR}     * Movement               -> {action.movement} '
    )
    COLOR = GREEN if action.promotion else DARK_GRAY
    print(
        f'{CURSOR_REWRITE_LINE}   {COLOR}     * Promotion              -> {action.promotion} '
    )
    COLOR = GREEN if action.checkmate else DARK_GRAY
    print(
        f'{CURSOR_REWRITE_LINE}   {COLOR}     * Checkmate              -> {action.checkmate} {RESET_CURSOR} '
    )


def print_turn(turn: TurnResult):
    print('\n')
    # COLOR = WHITE if turn.player == 'white' else BLUE
    # print(f'   {COLOR}     * Player                 -> {turn.player} {RESET_CURSOR}')
    COLOR = GREEN if turn.chessman else DARK_GRAY
    print(
        f'{CURSOR_REWRITE_LINE}   {COLOR}     * Chessman               -> {turn.chessman} {RESET_CURSOR}'
    )
    COLOR = GREEN if turn.captured_chessman else DARK_GRAY
    print(
        f'{CURSOR_REWRITE_LINE}   {COLOR}     * Capture                -> {turn.captured_chessman} {RESET_CURSOR}'
    )
    COLOR = GREEN if turn.actions else DARK_GRAY
    print(
        f'{CURSOR_REWRITE_LINE}   {COLOR}     * Actions                -> {RESET_CURSOR}{turn.actions} '
    )


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
        player = f'{WHITE}White{RESET_CURSOR}' if action.white_turn else f'{BLUE}Black{RESET_CURSOR}'

        print(
            f'{CURSOR_REWRITE_LINE}Turn : {idx} \n  Action : {mvmt}        \n  Player : {player}              '
        )

        # print_action(action)

        res = manager.compute_parsing_result(action)
        turn_results[idx][mvmt] = res

        # print_turn(res)

        if not manager.print_board(res):
            sys.stdout.write(CURSOR_UP * 16)  # Cursor up 14 lines
            # sys.stdout.write(CURSOR_UP * 31)  # Cursor up 14 lines

        time.sleep(.02)

# for res in result:
#     res.print()
