from utils.enum_types import PieceType, Player, GameEnd, MoveType

letter_to_number = {'a' : 0, 'b' : 1, 'c' : 2, 'd' : 3, 'e' : 4}
digit_to_number = {'1' : 0, '2' : 1, '3' : 2, '4' : 3, '5' : 4}
number_to_letter= {0 : 'a', 1 : 'b', 2 : 'c', 3 : 'd', 4 : 'e'}
number_to_digit = {0 : '1', 1 : '2', 2 : '3', 3 : '4', 4 : '5'}
valid_pieces = {'k', 'r', 'b', 'g', 's', 'p'}
# maps piece string representation to piece enum
str_to_piece = {'k' : PieceType.KING, 'r' : PieceType.ROOK, 'b' : PieceType.BISHOP, 'g' : PieceType.GOLD_GENERAL, 's' : PieceType.SILVER_GENERAL, 'p' : PieceType.PAWN}
piece_to_str = {PieceType.KING : 'k', PieceType.ROOK : 'r', PieceType.BISHOP : 'b', PieceType.GOLD_GENERAL : 'g', PieceType.SILVER_GENERAL : 's', PieceType.PAWN : 'p'}
player_string = {Player.UPPER: 'UPPER', Player.LOWER : 'lower'}
game_end_string = {GameEnd.ILLEGAL_MOVE : 'Illegal move.', GameEnd.CHECKMATE : "Checkmate.", GameEnd.TIE: "Too Many Moves."}
move_string = {MoveType.MOVE : 'move', MoveType.DROP: 'drop', MoveType.MOVE_AND_PROMOTE : 'move'}
