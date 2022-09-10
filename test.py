import re
from movement_parser import MovementParser

with open('Viswanathan Anand_vs_Garry Kasparov_2021.07.10.pgn') as f:
    pgn_game = f.read()

clean_headers = re.sub(r'(\[.*\]\n\n?)', '', pgn_game, 0)
clean_line_return = re.sub(r'\n', ' ', clean_headers, 0)


pgn_content = re.sub(r'(\d\d?\d?\. ?)', '\\n', clean_line_return, 0)

moves = re.split(r'\n', pgn_content)

print('\n')
result = dict
is_white_turn = True
for move in moves:
    if move == '':
        continue
    for idx, movement in enumerate(move.split()):
        is_white_turn = not is_white_turn
      
        result[idx] = MovementParser.parse_movement(movement, is_white_turn)


# for res in result:
#     res.print()

# result = []
# result.append(parser.parse_movement("Baa3", True))
# parser = MovementParser()
# result.append(parser.parse_movement("O-O", True))
