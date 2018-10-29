from enum import Enum

class MoveType(Enum):
    MOVE = 1
    DROP = 2
    MOVE_AND_PROMOTE = 3

class GameEnd(Enum):
    ILLEGAL_MOVE = 1
    CHECKMATE = 2
    TIE = 3

class PieceType(Enum):
    KING = 1
    ROOK = 2
    BISHOP = 3
    GOLD_GENERAL = 4
    SILVER_GENERAL = 5
    PAWN = 6

class Player(Enum):
    LOWER = 1
    UPPER = 2
