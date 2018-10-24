from utils import utils
from pieces import Piece

N = 5

class MiniShogi:
    """ A MiniShogi game board storing all the information used to represent
    the current state of the game with the following properties:

    Attributes:
    board: A 2d list describing the location and type of pieces currently in play.
    captured_lower: A list of the pieces captured by the lower player.
    captured_UPPER: A list of the pieces captured by the UPPER player.
    turn_count: An integer representing the number of turns already been played.
    """

    def __init__(self, board, captured_lower, captured_UPPER, turn_count):
        self.board = board
        self.captured_lower = captured_lower
        self.captured_UPPER = captured_UPPER
        self.turn_count = turn_count
        self.pos_to_piece = {}
        for i in range(0, N):
            for j in range(0, N):
                if not(board[i][j] == ''):
                    self.pos_to_piece[(i, j)] = Piece.piece_from_string(board[i][j])

    def display_game_state(self):
        """
        Converts the board state into string form and outputs it to the screen.
        """
        board_string = utils.stringifyBoard(self.board)
        print(board_string)
        print ("Captures UPPER:" + utils.stringifyCaptured(self.captured_UPPER))
        print ("Captures UPPER:" + utils.stringifyCaptured(self.captured_lower))
        return

    def move_piece(self, start_pos, end_pos):
        """
        Checks if move is valid (possible piece movements and exposure to check),
        moves piece to new position and updates game state.
        Returns a boolean indicating whether move was made or not
        """
        pass

    def drop_piece(self, drop_pos):
        """
        Checks if drop position is valid, drops piece on the board and updates the
        board state.
        Returns a boolean to indicate whether piece was dropped or not.
        """
        pass

    def promote_piece(self, start_pos, end_pos):
        """
        Checks if piece is eligible to be promoted and promotes it accordingly.
        Returns a boolean to indicate success.
        """
        pass
    def make_move(self, start_pos, end_pos, player, move_type):
        """
        Determines the kind of move user is trying to make, and executes it while
        performing all validity checks
        Returns a boolean to indicate success.
        """
        pass
