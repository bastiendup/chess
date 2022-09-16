import re
from cursor import DARK_GRAY, GREEN, DARK_GRAY, RED, RESET_CURSOR
from action_parser import ActionParser, ParsingResult

with open('Viswanathan Anand_vs_Garry Kasparov_2021.07.10.pgn') as f:
    pgn_game = f.read()

clean_headers = re.sub(r'(\[.*\]\n\n?)', '', pgn_game, 0)
clean_line_return = re.sub(r'\n', ' ', clean_headers, 0)

pgn_content = re.sub(r'(\d\d?\d?\. ?)', '\\n', clean_line_return, 0)

moves = re.split(r'\n', pgn_content)

print('\n')
result = dict()
is_white_turn = True
parser = ActionParser()
for i, move in enumerate(moves):
    if move == '':
        continue

    result[i] = dict()
    for idx, movement in enumerate(move.split()):
        is_white_turn = not is_white_turn
        result[i][movement] = parser.parse_movement(movement, is_white_turn)

for idx, turn in result.items():
    print(f'Turn : {idx}')
    for action, res in turn.items():
        print(f'    Action : {action} ')
        print(f'        * Turn                   -> {"White" if res.white_turn else "Black"} ')
        COLOR = GREEN if res.final_score else DARK_GRAY
        print(f'   {COLOR}     * Final score            -> {res.final_score} ')
        COLOR = GREEN if res.rook else DARK_GRAY
        print(f'   {COLOR}     * Rook                   -> {res.rook} ')
        COLOR = GREEN if res.board_actions else DARK_GRAY
        print(f'   {COLOR}     * Board Action           -> {res.board_actions} ')
        COLOR = GREEN if res.piece else DARK_GRAY
        print(f'   {COLOR}     * Piece                  -> {res.piece} ')
        COLOR = GREEN if res.disambiguating_action else DARK_GRAY
        print(f'   {COLOR}     * Disambiguating action  -> {res.disambiguating_action} ')
        COLOR = GREEN if res.capture else DARK_GRAY
        print(f'   {COLOR}     * Capture                -> {res.capture} ')
        COLOR = GREEN if res.movement else DARK_GRAY
        print(f'   {COLOR}     * Movement               -> {res.movement} ')
        COLOR = GREEN if res.promotion else DARK_GRAY
        print(f'   {COLOR}     * Promotion              -> {res.promotion} ')
        COLOR = GREEN if res.checkmate else DARK_GRAY
        print(f'   {COLOR}     * Checkmate              -> {res.checkmate} {RESET_CURSOR} ')

# for res in result:
#     res.print()
