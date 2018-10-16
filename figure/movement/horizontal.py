from constants import X, Y


def validate_move(position, new_position):
    # on of two axis must be equal to original position
    if position[X] == new_position[X] or position[Y] == new_position[Y]:
        return True

    return False


def move_positions(position, new_position):
    vertical_diff = abs(position[X] - new_position[X])
    horizontal_diff = abs(position[Y] - new_position[Y])

    moves = [position]
    axis = X if vertical_diff > 0 else Y

    direction = 1
    if position[axis] > new_position[axis]:
        direction = -1

    difference = vertical_diff if vertical_diff > 0 else horizontal_diff

    for i in range(1, difference):
        move = [position[X], position[Y]]
        move[axis] += (direction * i)
        moves.append(tuple(move))

    moves.append(new_position)
    return tuple(moves)