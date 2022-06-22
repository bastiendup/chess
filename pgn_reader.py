import re
import sys
import time

from chess_manager import Chess_Manager

with open('Viswanathan Anand_vs_Garry Kasparov_2021.07.10.pgn') as f:
    pgn_game = f.read()

clean_headers = re.sub(r'(\[.*\]\n\n?)', '', pgn_game, re.MULTILINE)
clean_line_return = re.sub(r'\n', ' ', clean_headers, 0, re.MULTILINE)

regex = r'(\d\d?\d?\. ?)'
subst = '\\n'

result = re.sub(regex, subst, clean_line_return, 0, re.MULTILINE)

moves = re.split(r'\n', result)

manager = Chess_Manager()
print('\n')
for move in moves:
    if move == '':
        continue
    for movement in move.split():
        manager.reset_turn()
        time.sleep(.1)
        manager.is_white_turn = not manager.is_white_turn
        sys.stdout.write("\x1b[2K")  # Delete line before writing it : avoid having the previous move written
        color = 'white' if manager.is_white_turn else 'black'
        print(f'      MOVEMENT : {movement}, TURN : {color}')
        manager.board.print_board()

        # movement = input(f'White turn ? {manager.is_white_turn},  Movement : ')
        final_score = manager.check_final_score(movement)
        if final_score:
            sys.stdout.write('\033[B' * 14)  # Move cursor down 14 lines
            print(f'              {final_score}')
            break

        rook = manager.CheckIfKingRook(movement)
        if not rook:
            movement = manager.check_piece(movement)
            movement = manager.CheckDisambiguating(movement)
            movement = manager.CheckCapture(movement)
            movement = manager.CheckMoving(movement)
            movement = manager.CheckPromotion(movement)
            movement = manager.CheckForCheckMove(movement)
            manager.update_board()