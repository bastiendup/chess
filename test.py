import re
from movement_parser import MovementParser

with open('Viswanathan Anand_vs_Garry Kasparov_2021.07.10.pgn') as f:
    pgn_game = f.read()

clean_headers = re.sub(r'(\[.*\]\n\n?)', '', pgn_game, 0)
clean_line_return = re.sub(r'\n', ' ', clean_headers, 0)

regex = r'(\d\d?\d?\. ?)'
subst = '\\n'

result = re.sub(regex, subst, clean_line_return, 0)

moves = re.split(r'\n', result)

print('\n')
result = []
is_white_turn = True
for move in moves:
    if move == '':
        continue
    for movement in move.split():
        is_white_turn = not is_white_turn
        parser = MovementParser()
        result.append(parser.parse_movement(movement, is_white_turn))
for res in result:
    res.print()

# result = []
# result.append(parser.parse_movement("Baa3", True))
# parser = MovementParser()
# result.append(parser.parse_movement("O-O", True))
