import re
from cursor import DARK_GRAY, GREEN, DARK_GRAY, RED, RESET_CURSOR
from movement_parser import ActionParser, ParsingResult

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
        color = GREEN if res.final_score else DARK_GRAY
        print(f'   {color}     * Final score            -> {res.final_score} ')
        color = GREEN if res.rook else DARK_GRAY
        print(f'   {color}     * Rook                   -> {res.rook} ')
        color = GREEN if res.board_actions else DARK_GRAY
        print(f'   {color}     * Board Action           -> {res.board_actions} ')
        color = GREEN if res.piece else DARK_GRAY
        print(f'   {color}     * Piece                  -> {res.piece} ')
        color = GREEN if res.disambiguating_action else DARK_GRAY
        print(f'   {color}     * Disambiguating action  -> {res.disambiguating_action} ')
        color = GREEN if res.capture else DARK_GRAY
        print(f'   {color}     * Capture                -> {res.capture} ')
        color = GREEN if res.movement else DARK_GRAY
        print(f'   {color}     * Movement               -> {res.movement} ')
        color = GREEN if res.promotion else DARK_GRAY
        print(f'   {color}     * Promotion              -> {res.promotion} ')
        color = GREEN if res.checkmate else DARK_GRAY
        print(f'   {color}     * Checkmate              -> {res.checkmate} {RESET_CURSOR} ')

# for res in result:
#     res.print()
