from utils.enum_types import GameEnd, MoveType
from utils import io_utils
from utils import string_mappings
from pieces import Player
from minishogi import MiniShogi

def main():
    #initialize game
    board = [['k','p','','','R'],['g','','','','B'],['s','','','','S'],['b','','','','G'],['r','','','P','K']]
    capturedU = []
    capturedL = []
    new_game = MiniShogi(board, capturedL, capturedU, 0)
    #main loop
    while not(new_game.game_end):
        input_str = new_game.game_state()
        if (input_str == None):
            break
        move_type, input1, input2 = io_utils.parse_move(input_str)
        new_game.make_move(input1, input2, move_type)
    if new_game.game_end == GameEnd.TIE:
        print("Tie Game. " + string_mappings.game_end_string[GameEnd.TIE])
    else:
        print(string_mappings.player_string[new_game.winner] + " player wins. " + string_mappings.game_end_string[new_game.game_end_cause])

if __name__ == "__main__":
    main()
