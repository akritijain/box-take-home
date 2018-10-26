from minishogi import MoveType

letter_to_number = {'a' : 0, 'b' : 1, 'c' : 2, 'd' : 3, 'e' : 4}
digit_to_number = {'1' : 0, '2' : 1, '3' : 2, '4' : 3, '5' : 4}
valid_pieces = {'k', 'r', 'b', 'g', 's', 'p'}

def parse_move(input_str):
    input_words = input_str.split()
    if (len(input_words) > 4) or (len(input_words) < 3):
        return None
    if not(input_words[0] == 'move' or input_words[0] == 'drop'):
        return None
    if input_words[0] == 'move':
        start_pos = pos_from_string(input_words[1])
        end_pos = pos_from_string(input_words[2])
        if start_pos == None or end_pos == None:
            return None
        if len(input_words) == 4 and not(input_words[3] == 'promote'):
            return None
        if len(input_words) == 3:
            return MoveType.MOVE, start_pos, end_pos
        elif input_words[3] == 'promote':
            return MoveType.MOVE_AND_PROMOTE, start_pos, end_pos
    if input_words[0] == 'drop':
        if len(input_words) > 3:
            return None
        pos = pos_from_string(input_words[2])
        if pos == None or not(input_words[1] in valid_pieces):
            return None
        return MoveType.DROP, input_words[1], pos


def pos_from_string(str_pos):
    if not(len(str_pos) == 2):
        return None
    if str_pos[0] not in letter_to_number:
        return None
    if str_pos[1] not in digit_to_number:
        return None
    return (letter_to_number[str_pos[0]], digit_to_number[str_pos[1]])
