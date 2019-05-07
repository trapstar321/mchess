from constants import X, Y


def validate_move(position, new_position):
    vertical_diff = abs(position[X] - new_position[X])
    horizontal_diff = abs(position[Y] - new_position[Y])

    if vertical_diff == horizontal_diff:
        return True

    return False


def move_positions(position, new_position):
    vertical_diff = abs(position[X] - new_position[X])

    x_direction = 1
    y_direction = 1
    if position[X] > new_position[X]:
        x_direction = -1
    if position[Y] > new_position[Y]:
        y_direction = -1

    moves = [position]

    for i in range(1, vertical_diff):
        move = (position[X]+(x_direction*i), position[Y]+(y_direction*i))
        moves.append(move)

    moves.append(new_position)
    return tuple(moves)
