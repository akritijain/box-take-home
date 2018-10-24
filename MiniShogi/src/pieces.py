from enum import Enum

class Piece_Types(Enum):
    KING = 1
    ROOK = 2
    BISHOP = 3
    GOLD_GENERAL = 4
    SILVER_GENERAL = 5
    PAWN = 6

class Player(Enum):
    LOWER = 1
    UPPER = 2

# maps piece string representation to piece enum
str_to_piece = {'k' : Piece_Types.KING, 'r' : Piece_Types.ROOK, 'b' : Piece_Types.BISHOP,
'g' : Piece_Types.GOLD_GENERAL, 's' : Piece_Types.SILVER_GENERAL, 'p' : Piece_Types.PAWN}
# board size
N = 5

class Piece:
    def __init__(self, piece_type, promoted, player):
        self.piece_type = piece_type
        self.promoted = promoted
        self.player = player

    def piece_from_string(piece_str):
        piece_type = str_to_piece[piece_str[0].lower()]
        promoted = False
        if len(piece_str) == 2:
            promoted = True
        player = Player.LOWER
        if (piece_str[0].isupper()):
            player = Player.UPPER
        return Piece(piece_type, promoted, player)

    def possible_moves(self, pos):
        """
        Takes a position as a input and returns the set of values the current
        piece can move to from that position.
        """
        if self == None:
            return None
        else:
            if self.piece_type == Piece_Types.KING:
                return king_moves(pos)
            if self.piece_type == Piece_Types.ROOK:
                return rook_moves(pos)
            if self.piece_type == Piece_Types.BISHOP:
                return bishop_moves(pos)
            if self.piece_type == Piece_Types.GOLD_GENERAL:
                return gold_general_moves(pos)
            if self.piece_type == Piece_Types.SILVER_GENERAL:
                return silver_general_moves(pos)
            if self.piece_type == Piece_Types.PAWN:
                return pawn_moves(pos)
            #should never reach this point
            return None

    def in_check(pos, board):
        """
        Checks whether a certain position king is in check or not im the given
        board configuration
        """

    def moves_to_escape_check(pos, board):
        """
        Given the position of a king in check, goes through the board config
        and returns possible moves to get out of check
        """

    def king_moves(pos):
        """
        Helper function that takes a position as input and returns a set of
        all positions a king piece can move to from there
        """
        end_pos = set()
        right = pos[0] + 1
        left = pos[0] - 1
        up = pos[1] + 1
        down = pos[0] - 1
        #go one move up
        if up < N:
            end_pos.add((pos[0], up))
        #go one move down
        if down > 0:
            end_pos.add((pos[0], down))
        #go one move right and diagonal moves on the right
        if right < N:
            end_pos.add((right, pos[1]))
            if up < N:
                end_pos.add((right, up))
            if down > 0:
                end_pos.add((right, down))
        #go one move left and diagonal moves on the left
        if left > 0:
            end_pos.add((left, pos[1]))
            if up < N:
                end_pos.add((left, up))
            if down > 0:
                end_pos.add((left, down))
        return end_pos

    def rook_moves(pos):
        """
        Helper function that takes a position as input and returns a set of
        all positions a rook piece can move to from there
        """
        end_pos = set()
        #go right
        for i in range(pos[0], N):
            end_pos.add((i, pos[1]))
        #go left
        for i in range(0, pos[0]):
            end_pos.add((i, pos[1]))
        #go up
        for i in range(pos[1], N):
            end_pos.add((pos[0], i))
        #go down
        for i in range(0, pos[1]):
            end_pos.add((pos[0], i))
        return end_pos

    def bishop_moves(pos):
        """
        Helper function that takes a position as input and returns a set of
        all positions a bishop piece can move to from there
        """
        end_pos = set()
        #top right diagonal
        i = 1
        while ((pos[0] + i) < N) and ((pos[1] + i) < N):
            end_pos.add((pos[0] + i, pos[1] + i))
            i += 1
        #bottom right diagonal
        i = 1
        while ((pos[0] + i) < N) and ((pos[1] - i) >= 0):
            end_pos.add((pos[0] + i, pos[1] - i))
            i += 1
        #top left diagonal
        i = 1
        while ((pos[0] - i) < N) and ((pos[1] + i) >= 0):
            end_pos.add((pos[0] + i, pos[1] - i))
            i += 1
        #bottom left diagonal
        i = 1
        while ((pos[0] - i) >= 0) and ((pos[1] - i) >= 0):
            end_pos.add((pos[0] + i, pos[1] - i))
            i += 1
        return end_pos

    def gold_general_moves(pos):
        """
        Helper function that takes a position as input and returns a set of
        all positions a gold general piece can move to from there
        """
        end_pos = set()
        right = pos[0] + 1
        left = pos[0] - 1
        up = pos[1] + 1
        down = pos[0] - 1
        #go one move up
        if up < N:
            end_pos.add((pos[0], up))
        #go one move down
        if down > 0:
            end_pos.add((pos[0], down))
        #go one move right and top diagonal on the right
        if right < N:
            end_pos.add((right, pos[1]))
            if up < N:
                end_pos.add((right, up))
        #go one move left and top diagonal on the left
        if left > 0:
            end_pos.add((left, pos[1]))
            if up < N:
                end_pos.add((left, up))
        return end_pos

    def silver_general_moves(pos):
        """
        Helper function that takes a position as input and returns a set of
        all positions a silver general piece can move to from there
        """
        end_pos = set()
        right = pos[0] + 1
        left = pos[0] - 1
        up = pos[1] + 1
        down = pos[0] - 1
        #go one move up
        if up < N:
            end_pos.add((pos[0], up))
        #go one move right and diagonal moves on the right
        if right < N:
            if up < N:
                end_pos.add((right, up))
            if down > 0:
                end_pos.add((right, down))
        #go one move left and diagonal moves on the left
        if left > 0:
            if up < N:
                end_pos.add((left, up))
            if down > 0:
                end_pos.add((left, down))
        return end_pos

    def pawn_moves(pos):
        """
        Helper function that takes a position as input and returns a set of
        all positions a pawn piece can move to from there
        """
        end_pos = set()
        if (pos[1] + 1) < N:
            end_pos.add(pos[0], pos[1] + 1)
        return end_pos
