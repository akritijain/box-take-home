import sys
from utils.enum_types import GameEnd, MoveType
from utils import io_utils
from utils import string_mappings
from utils import utils
from pieces import Player
from minishogi import MiniShogi

N = 5

def file_mode(filename):
    contents = utils.parseTestCase(filename)
    pieces = contents['initialPieces']
    board = [['']*N for i in range(N)]
    for pair in pieces:
        pos = io_utils.pos_from_string(pair['position'])
        board[pos[0]][pos[1]] = pair['piece']
    game = MiniShogi(board, contents['lowerCaptures'],contents['upperCaptures'], 0, False)
    moves = contents['moves']
    for move in moves:
        game.game_state()
        if game.game_end:
            break
        move_type, input1, input2 = io_utils.parse_move(move)
        game.make_move(input1, input2, move_type)
    prev_turn = MiniShogi.get_opposing_player(game.player_turn)
    print(string_mappings.player_string[prev_turn] + " player action: " + move)
    game.interactive = True
    game.game_state()
    if game.game_end == GameEnd.TIE:
        print("Tie Game. " + string_mappings.game_end_string[GameEnd.TIE])
    elif game.winner == None:
        return
    else:
        print(string_mappings.player_string[game.winner] + " player wins. " + string_mappings.game_end_string[game.game_end_cause])


def interactive_mode():
    #initialize game
    board = [['k','p','','','R'],['g','','','','B'],['s','','','','S'],['b','','','','G'],['r','','','P','K']]
    capturedU = []
    capturedL = []
    new_game = MiniShogi(board, capturedL, capturedU, 0, True)
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
    if len(sys.argv) > 3:
        print("Too many arguments")
        exit(1)
    if len(sys.argv) < 2:
        print("Too few arguments")
        exit(1)
    if (sys.argv[1] == '-f') and len(sys.argv) < 3:
        print("Too few arguments")
        exit(1)
    if (sys.argv[1] == '-f'):
        filename = sys.argv[2]
        file_mode(filename)
    if (sys.argv[1] == '-i'):
        interactive_mode()
