from minishogi import MiniShogi, GameEnd
from utils import input_parser
from pieces import Player
import numpy as np

player_string = {Player.UPPER: 'UPPER', Player.LOWER : 'lower'}
game_end_string = {GameEnd.ILLEGAL_MOVE : 'Illegal move.', GameEnd.CHECKMATE : "Checkmate.", GameEnd.TIE: "Too Many Moves."}

def main():
    #initialize game
    board = [['r','','','','K'],['b','','','','G'],['s','','','','S'],['g','','','','B'],['k','','','','R']]
    capturedU = ['P', 'Q']
    capturedL = ['p', 'q']
    new_game = MiniShogi(board, capturedL, capturedU, 0)
    #main loop
    while not(new_game.game_end):
        new_game.display_game_state()
        input_str = input(player_string[new_game.player_turn] + "> ")
        move_type, input1, input2 = input_parser.parse_move(input_str)
        new_game.make_move(input1, input2, move_type)
    if new_game.winner == None:
        print("Tie Game. " + game_end_string[GameEnd.TIE])
    else:
        print(player_string[new_game.winner] + " player wins. " + game_end_string[new_game.game_end_cause])

if __name__ == "__main__":
    main()
