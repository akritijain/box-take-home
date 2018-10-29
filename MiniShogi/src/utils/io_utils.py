from utils.enum_types import MoveType
from utils import string_mappings

def parse_move(input_str):
    input_words = input_str.split()
    if (len(input_words) > 4) or (len(input_words) < 3):
        return None, None, None
    if not(input_words[0] == 'move' or input_words[0] == 'drop'):
        return None, None, None
    if input_words[0] == 'move':
        start_pos = pos_from_string(input_words[1])
        end_pos = pos_from_string(input_words[2])
        if start_pos == None or end_pos == None:
            return None, None, None
        if len(input_words) == 4 and not(input_words[3] == 'promote'):
            return None, None, None
        if len(input_words) == 3:
            return MoveType.MOVE, start_pos, end_pos
        elif input_words[3] == 'promote':
            return MoveType.MOVE_AND_PROMOTE, start_pos, end_pos
    if input_words[0] == 'drop':
        if len(input_words) > 3:
            return None, None, None
        pos = pos_from_string(input_words[2])
        if pos == None or not(input_words[1] in string_mappings.valid_pieces):
            return None, None, None
        return MoveType.DROP, string_mappings.str_to_piece[input_words[1]], pos

def pos_from_string(str_pos):
    if not(len(str_pos) == 2):
        return None
    if str_pos[0] not in string_mappings.letter_to_number:
        return None
    if str_pos[1] not in string_mappings.digit_to_number:
        return None
    return (string_mappings.letter_to_number[str_pos[0]], string_mappings.digit_to_number[str_pos[1]])

def move_to_string(move_type, param1, param2):
    str_out = string_mappings.move_string[move_type]
    if move_type == MoveType.DROP:
        param1_str = string_mappings.piece_to_str[param1]
    else:
        param1_str = string_mappings.number_to_letter[param1[0]] + string_mappings.number_to_digit[param1[1]]
    param2_str = string_mappings.number_to_letter[param2[0]] + string_mappings.number_to_digit[param2[1]]

    str_out = str_out + " " + param1_str+ " " + param2_str
    if move_type == MoveType.MOVE_AND_PROMOTE:
        return  (str_out + " " + 'promote')
    return str_out
