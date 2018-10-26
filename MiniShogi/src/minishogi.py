from enum import Enum
from utils import utils
from pieces import Piece, Player, PieceType

N = 5

class MoveType(Enum):
    MOVE = 1
    DROP = 2
    MOVE_AND_PROMOTE = 3
class GameEnd(Enum):
    ILLEGAL_MOVE = 1
    CHECKMATE = 2
    TIE = 3

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
        self.captured = {}
        self.captured[Player.LOWER] = captured_lower
        self.captured[Player.UPPER] = captured_UPPER
        self.turn_count = turn_count
        self.pos_to_piece = {}
        for i in range(0, N):
            for j in range(0, N):
                if not(board[i][j] == ''):
                    self.pos_to_piece[(i, j)] = Piece.piece_from_string(board[i][j])
        self.player_turn = Player.UPPER
        if turn_count % 2 == 0:
            self.player_turn = Player.LOWER
        self.game_end = False
        self.game_end_cause = None
        self.winner = None

    def display_game_state(self):
        """
        Converts the board state into string form and outputs it to the screen.
        """
        board_string = utils.stringifyBoard(self.board)
        print(board_string)
        print ("Captures UPPER:" + utils.stringifyCaptured(self.captured[Player.UPPER]))
        print ("Captures lower:" + utils.stringifyCaptured(self.captured[Player.LOWER]))
        return

    def move_piece(self, start_pos, end_pos):
        """
        Checks if move is valid (possible piece movements and exposure to check),
        moves piece to new position and updates game state.
        Returns a boolean indicating whether move was made or not
        """
        #check if the start pos has a piece on it
        if not(start_pos in self.pos_to_piece):
            return False
        #check if that piece belongs to the player who is moving
        piece = self.pos_to_piece[start_pos]
        if not(piece.player == self.player_turn):
            return False
        #check if it's a valid move
        moves = piece.possible_moves(start_pos)
        if not(end_pos in moves):
            return False
        #check if the end pos has a piece in it and which player it belongs to
        if end_pos in self.pos_to_piece:
            end_piece = self.pos_to_piece[end_pos]
            if end_piece.player == self.player_turn:
                return False
            else:
                player_captures = self.captured[self.player_turn]
                end_piece_string = self.board[end_pos[0]][end_pos[1]]
                if len(end_piece_string) == 2:
                    end_piece_string = end_piece_string[1]
                player_captures.append(utils.changeCase(end_piece_string))
                del self.pos_to_piece[end_pos]
                self.board[end_pos[0]][end_pos[1]] = ''
        #actually move the piece
        piece_string = self.board[start_pos[0]][start_pos[1]]
        self.board[start_pos[0]][start_pos[1]] = ''
        self.board[end_pos[0]][end_pos[1]] = piece_string
        self.pos_to_piece[end_pos] = piece
        del self.pos_to_piece[start_pos]
        return True

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
    def make_move(self, start_pos, end_pos, move_type):
        """
        Determines the kind of move user is trying to make, and executes it while
        performing all validity checks
        Returns a boolean to indicate success.
        """
        if move_type == MoveType.MOVE:
            if (self.move_piece(start_pos, end_pos) == True):
                print("moved")
                self.increment_turn()
                return True
            else:
                self.game_end = True
                self.game_end_cause = GameEnd.ILLEGAL_MOVE
                if self.player_turn == Player.UPPER:
                    self.winner = Player.LOWER
                else:
                    self.winner = Player.UPPER
                return False

    def increment_turn(self):
        self.turn_count += 1
        if (self.turn_count == 200):
            self.game_end = True
            self.game_end_cause = GameEnd.TIE

        if self.player_turn == Player.LOWER:
            self.player_turn = Player.UPPER
        else:
            self.player_turn = Player.LOWER
