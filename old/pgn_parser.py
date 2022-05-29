import chess

png_folder = open('Viswanathan Anand_vs_Garry Kasparov_2021.07.10.pgn')
current_game = chess.pgn.read_game(png_folder)
png_text = str(current_game.mainline_moves())