def serialize(state):
    return tuple(num for row in state for num in row)


def manhattan(state):
    distance = 0
    size = len(state)
    for i in range(size):
        for j in range(size):
            val = state[i][j]
            if val is None:
                continue
            gi, gj = divmod(val - 1, size)
            distance += abs(gi - i) + abs(gj - j)
    return distance


def get_blank_pos(state):
    for i, row in enumerate(state):
        for j, val in enumerate(row):
            if val is None:
                return i, j
    return -1, -1