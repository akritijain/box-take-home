from utils.enum_types import PieceType, Player
from utils import string_mappings

# board size
N = 5

class Piece:
    def __init__(self, piece_type, promoted, player):
        self.piece_type = piece_type
        self.promoted = promoted
        self.player = player

    def piece_from_string(piece_str):
        #promoted piece
        if len(piece_str) == 2:
            player = Player.LOWER
            if (piece_str[1].isupper()):
                player = Player.UPPER
            return Piece(string_mappings.str_to_piece[piece_str[1].lower()], True, player)
        #regular piece
        else:
            player = Player.LOWER
            if(piece_str.isupper()):
                player = Player.UPPER
            return Piece(string_mappings.str_to_piece[piece_str.lower()], False, player)

    def possible_moves(self, pos, pos_to_piece):
        """
        Takes a position as a input and returns the set of values the current
        piece can move to from that position.
        """
        if self == None:
            return None
        else:
            if self.piece_type == PieceType.KING:
                return Piece.king_moves(pos)
            if self.piece_type == PieceType.ROOK:
                return Piece.rook_moves(pos, pos_to_piece)
            if self.piece_type == PieceType.BISHOP:
                return Piece.bishop_moves(pos, pos_to_piece)
            if self.piece_type == PieceType.GOLD_GENERAL:
                return Piece.gold_general_moves(pos, self.player)
            if self.piece_type == PieceType.SILVER_GENERAL:
                return Piece.silver_general_moves(pos, self.player)
            if self.piece_type == PieceType.PAWN:
                return Piece.pawn_moves(pos, self.player)
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
        down = pos[1] - 1
        #go one move up
        if up < N:
            end_pos.add((pos[0], up))
        #go one move down
        if down >= 0:
            end_pos.add((pos[0], down))
        #go one move right and diagonal moves on the right
        if right < N:
            end_pos.add((right, pos[1]))
            if up < N:
                end_pos.add((right, up))
            if down >= 0:
                end_pos.add((right, down))
        #go one move left and diagonal moves on the left
        if left >= 0:
            end_pos.add((left, pos[1]))
            if up < N:
                end_pos.add((left, up))
            if down >= 0:
                end_pos.add((left, down))
        return end_pos

    def rook_moves(pos, pos_to_piece):
        """
        Helper function that takes a position as input and returns a set of
        all positions a rook piece can move to from there
        """
        end_pos = set()
        #go right
        for i in range(pos[0]+1, N):
            end_pos.add((i, pos[1]))
            if (i, pos[1]) in pos_to_piece:
                break
        #go left
        for i in range(pos[0]-1, -1, -1):
            end_pos.add((i, pos[1]))
            if (i, pos[1]) in pos_to_piece:
                break
        #go up
        for i in range(pos[1]+1, N):
            end_pos.add((pos[0], i))
            if (pos[0], i) in pos_to_piece:
                break
        #go down
        for i in range(pos[1]-1, -1, -1):
            end_pos.add((pos[0], i))
            if (pos[0], i) in pos_to_piece:
                break
        return end_pos

    def bishop_moves(pos, pos_to_piece):
        """
        Helper function that takes a position as input and returns a set of
        all positions a bishop piece can move to from there
        """
        end_pos = set()
        #top right diagonal
        i = 1
        while ((pos[0] + i) < N) and ((pos[1] + i) < N):
            end_pos.add((pos[0] + i, pos[1] + i))
            if (pos[0] + i, pos[1] + i) in pos_to_piece:
                break
            i += 1
        #bottom right diagonal
        i = 1
        while ((pos[0] + i) < N) and ((pos[1] - i) >= 0):
            end_pos.add((pos[0] + i, pos[1] - i))
            if (pos[0] + i, pos[1] - i) in pos_to_piece:
                break
            i += 1
        #top left diagonal
        i = 1
        while ((pos[0] - i) >= 0) and ((pos[1] + i) < N):
            end_pos.add((pos[0] - i, pos[1] + i))
            if (pos[0] - i, pos[1] + i) in pos_to_piece:
                break
            i += 1
        #bottom left diagonal
        i = 1
        while ((pos[0] - i) >= 0) and ((pos[1] - i) >= 0):
            end_pos.add((pos[0] - i, pos[1] - i))
            if (pos[0] - i, pos[1] - i) in pos_to_piece:
                break
            i += 1
        return end_pos

    def gold_general_moves(pos, player):
        """
        Helper function that takes a position as input and returns a set of
        all positions a gold general piece can move to from there
        """
        end_pos = set()
        right = pos[0] + 1
        left = pos[0] - 1
        up = pos[1] + 1
        down = pos[1] - 1
        if player == Player.UPPER:
            up = pos[1] - 1
            down = pos[1] + 1
        #go one move up
        if up < N and up >= 0:
            end_pos.add((pos[0], up))
        #go one move down
        if down < N and down >= 0:
            end_pos.add((pos[0], down))
        #go one move right and top diagonal on the right
        if right < N:
            end_pos.add((right, pos[1]))
            if up < N and up >= 0:
                end_pos.add((right, up))
        #go one move left and top diagonal on the left
        if left >= 0:
            end_pos.add((left, pos[1]))
            if up < N and up >= 0:
                end_pos.add((left, up))
        return end_pos

    def silver_general_moves(pos, player):
        """
        Helper function that takes a position as input and returns a set of
        all positions a silver general piece can move to from there
        """
        end_pos = set()
        right = pos[0] + 1
        left = pos[0] - 1
        up = pos[1] + 1
        down = pos[1] - 1
        if player == Player.UPPER:
            up = pos[1] - 1
            down = pos[1] + 1
        #go one move up
        if up < N and up >= 0:
            end_pos.add((pos[0], up))
        #go one move right and diagonal moves on the right
        if right < N:
            if up < N and up >= 0:
                end_pos.add((right, up))
            if down < N and down >= 0:
                end_pos.add((right, down))
        #go one move left and diagonal moves on the left
        if left >= 0:
            if up < N and up >= 0:
                end_pos.add((left, up))
            if down < N and down >= 0:
                end_pos.add((left, down))
        return end_pos

    def pawn_moves(pos, player):
        """
        Helper function that takes a position as input and returns a set of
        all positions a pawn piece can move to from there
        """
        end_pos = set()
        up = pos[1] + 1
        if player == Player.UPPER:
            up = pos[1] - 1
        if up < N and up >= 0:
            end_pos.add((pos[0], up))
        return end_pos

    def attack_king(self, piece_pos, king_pos, pos_to_piece):
        if self.piece_type == PieceType.BISHOP:
            attack_moves = set()
            if king_pos[0] > piece_pos[0]:
                inc_0 = 1
            else:
                inc_0 = -1
            if king_pos[1] > piece_pos[1]:
                inc_1 = 1
            else:
                inc_1 = -1
            x = piece_pos[0] + inc_0
            y = piece_pos[1] + inc_1
            while not(x == king_pos[0]) and not(y == king_pos[1]):
                attack_moves.add((x, y))
                x += inc_0
                y += inc_1
            return attack_moves
        elif self.piece_type == PieceType.ROOK:
            attack_moves = set()
            if king_pos[0] == piece_pos[0]:
                inc = 1
                if king_pos[1] < piece_pos[1]:
                    inc = -1
                for y in range(piece_pos[1] + inc, king_pos[1], inc):
                    attack_moves.add((king_pos[0], y))
            if king_pos[1] == piece_pos[1]:
                inc = 1
                if king_pos[0] < piece_pos[0]:
                    inc = -1
                for x in range(piece_pos[0] + inc, king_pos[0], inc):
                    attack_moves.add((king_pos[0], x))
            return attack_moves
