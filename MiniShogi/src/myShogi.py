from minishogi import MiniShogi
import numpy as np

def main():
    board = [['r','','','','K'],['b','','','','G'],['s','','','','S'],['g','','','','B'],['k','','','','R']]
    capturedU = ['P', 'Q']
    capturedL = ['p', 'q']
    print("here")
    new_game = MiniShogi(board, capturedL, capturedU, 0)
    new_game.display_game_state()
    print(new_game.pos_to_piece)

if __name__ == "__main__":
    main()
