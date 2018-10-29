from utils.enum_types import GameEnd, MoveType, Player, PieceType
from utils import utils, io_utils, string_mappings
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
        self.captured = {}
        self.captured[Player.LOWER] = captured_lower
        self.captured[Player.UPPER] = captured_UPPER
        self.turn_count = turn_count
        self.pos_to_piece = {}
        self.player_to_pieces = {Player.UPPER: set(), Player.LOWER: set()}
        for i in range(0, N):
            for j in range(0, N):
                if not(board[i][j] == ''):
                    piece = Piece.piece_from_string(board[i][j])
                    self.pos_to_piece[(i, j)] = piece
                    self.player_to_pieces[piece.player].add((i, j))
        self.player_turn = Player.UPPER
        if turn_count % 2 == 0:
            self.player_turn = Player.LOWER
        self.game_end = False
        self.game_end_cause = None
        self.winner = None

    def game_state(self):
        """
        Converts the board state into string form and outputs it to the screen.
        Also prints the player whose turn it is and returns user input
        """
        board_string = utils.stringifyBoard(self.board)
        print(board_string)
        print ("Captures UPPER:" + utils.stringifyCaptured(self.captured[Player.UPPER]))
        print ("Captures lower:" + utils.stringifyCaptured(self.captured[Player.LOWER]))
        threatening_pieces = self.in_check(self.player_turn)
        if len(threatening_pieces) > 0:
            possible_escape_moves = self.moves_to_escape_check(self.player_turn, threatening_pieces)
            if len(possible_escape_moves) == 0:
                self.game_end = True
                self.game_end_cause = GameEnd.CHECKMATE
                self.winner = self.get_opposing_player(self.player_turn)
                return None
            print("Player " + string_mappings.player_string[self.player_turn] + " is in check")
            for move in possible_escape_moves:
                print(io_utils.move_to_string(move[0], move[1], move[2]))
        input_str = input(string_mappings.player_string[self.player_turn] + "> ")
        return input_str

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
        moves = piece.possible_moves(start_pos, self.pos_to_piece)
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
                self.player_to_pieces[end_piece.player].remove(end_pos)
                self.board[end_pos[0]][end_pos[1]] = ''
        #actually move the piece
        piece_string = self.board[start_pos[0]][start_pos[1]]
        self.board[start_pos[0]][start_pos[1]] = ''
        self.board[end_pos[0]][end_pos[1]] = piece_string
        self.pos_to_piece[end_pos] = piece
        del self.pos_to_piece[start_pos]
        self.player_to_pieces[self.player_turn].remove(start_pos)
        self.player_to_pieces[self.player_turn].add(end_pos)
        return True

    def drop_piece(self, piece_type, drop_pos):
        """
        Checks if drop position is valid, drops piece on the board and updates the
        board state.
        Returns a boolean to indicate whether piece was dropped or not.
        """
        if drop_pos in self.pos_to_piece:
            self.illegal_move_by(self.player_turn)
            return False

        captured_pieces = self.captured[self.player_turn]
        for piece_str in captured_pieces:
            piece = Piece.piece_from_string(piece_str)
            if piece.piece_type == piece_type:
                self.pos_to_piece[drop_pos] = piece
                self.player_to_pieces[self.player_turn].add(drop_pos)
                self.board[drop_pos[0]][drop_pos[1]] = piece_str
                captured_pieces.remove(piece_str)
                #check if dropping a pawn causes check mate
                if piece.piece_type == PieceType.PAWN:
                    other_player = self.get_opposing_player(self.player_turn)
                    threatening_pieces =  self.in_check(other_player)
                    if len(threatening_pieces) > 0 and len(self.moves_to_escape_check(other_player, threatening_pieces)) == 0:
                         self.illegal_move_by(self.player_turn)
                         return False
                return True
        #piece does not exist in player's captured
        self.illegal_move_by(self.player_turn)
        return False

    def promote_piece(self, start_pos, end_pos):
        """
        Checks if piece is eligible to be promoted and promotes it accordingly.
        Returns a boolean to indicate success.
        """
        pass
    def make_move(self, param1, param2, move_type):
        """
        Determines the kind of move user is trying to make, and executes it while
        performing all validity checks
        Returns a boolean to indicate success.
        """
        if move_type == MoveType.MOVE:
            if self.move_piece(param1, param2):
                if self.in_check(self.player_turn):
                    self.illegal_move_by(self.player_turn)
                self.increment_turn()
                return True
            else:
                self.illegal_move_by(self.player_turn)
                return False
        if move_type == MoveType.DROP:
            if self.drop_piece(param1, param2):
                if self.in_check(self.player_turn):
                    self.illegal_move_by(self.player_turn)
                self.increment_turn()
                return True
            else:
                self.illegal_move_by(self.player_turn)
                return False

    def in_check(self, player):
        king_pos = self.get_king_pos(player)
        pieces = set()
        player_other = self.get_opposing_player(player)
        pieces = self.player_to_pieces[player_other]
        threatening_pieces = set()
        for piece_pos in pieces:
            piece = self.pos_to_piece[piece_pos]
            if king_pos in piece.possible_moves(piece_pos, self.pos_to_piece):
                threatening_pieces.add(piece_pos)
        return threatening_pieces

    def moves_to_escape_check(self, player, threatening_pieces):
        king_pos = self.get_king_pos(player)
        moves_list = []
        player_other = self.get_opposing_player(player)
        #moves where the king moves
        king_moves_set = Piece.king_moves(king_pos)
        del self.pos_to_piece[king_pos]
        opposite_player_moves = self.get_all_moves(player_other)
        self.pos_to_piece[king_pos] = Piece(PieceType.KING, False, player)
        for move in king_moves_set:
            saves_from_check = move not in opposite_player_moves
            valid_move = move not in self.player_to_pieces[player]
            if saves_from_check and valid_move:
                moves_list.append((MoveType.MOVE, king_pos, move))
        #moves where other pieces block or capture the attacking pieces
        pos_to_moves = self.pos_to_moves_mapping(player)
        if len(threatening_pieces) <= 1:
            for piece_pos in threatening_pieces:
                piece = self.pos_to_piece[piece_pos]
                if (piece.piece_type == PieceType.BISHOP) or (piece.piece_type == PieceType.ROOK):
                    moves_pos = piece.attack_king(piece_pos, king_pos, self.pos_to_piece)
                    for move_pos in moves_pos:
                        if move_pos in self.player_to_pieces[player]:
                            continue
                        for pos in pos_to_moves:
                            if move_pos in pos_to_moves[pos]:
                                moves_list.append((MoveType.MOVE, pos, move_pos))
                        #generate drop possibilities
                        captured_pieces = self.captured[player]
                        for cap_pc in captured_pieces:
                            pc_type = string_mappings.str_to_piece[cap_pc.lower()]
                            moves_list.append((MoveType.DROP, pc_type, move_pos))
                for pos in pos_to_moves:
                    if piece_pos in pos_to_moves[pos]:
                        moves_list.append((MoveType.MOVE, pos, piece_pos))

        return moves_list


    def get_all_moves(self, player):
        pieces = self.player_to_pieces[player]
        moves = set()
        for piece_pos in pieces:
            piece = self.pos_to_piece[piece_pos]
            moves = moves.union(piece.possible_moves(piece_pos, self.pos_to_piece))
        return moves

    def pos_to_moves_mapping(self, player):
        """
        Returns the positions of all the pieces on board (except king) for a given
        player mapped to the corresponding set of positions on the board they can
        move to in the next turn.
        """
        piece_to_moves = {}
        pieces_pos = self.player_to_pieces[player]
        for piece_pos in pieces_pos:
            piece = self.pos_to_piece[piece_pos]
            if piece.piece_type == PieceType.KING:
                continue
            piece_to_moves[piece_pos] = piece.possible_moves(piece_pos, self.pos_to_piece)
        return piece_to_moves

    def get_king_pos(self, player):
        pieces = self.player_to_pieces[player]
        for piece_pos in pieces:
            piece = self.pos_to_piece[piece_pos]
            if piece.piece_type == PieceType.KING:
                return piece_pos
        return None

    def get_opposing_player(self, player):
        if player == Player.UPPER:
            return Player.LOWER
        else:
            return Player.UPPER

    def increment_turn(self):
        self.turn_count += 1
        if (self.turn_count == 200):
            self.game_end = True
            self.game_end_cause = GameEnd.TIE

        if self.player_turn == Player.LOWER:
            self.player_turn = Player.UPPER
        else:
            self.player_turn = Player.LOWER

    def illegal_move_by(self, player):
        self.game_end = True
        self.game_end_cause = GameEnd.ILLEGAL_MOVE
        self.winner = self.get_opposing_player(player)
