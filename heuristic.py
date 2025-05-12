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

def misplaced_tiles(state):
    """Heuristic đếm số ô sai vị trí."""
    count = 0
    size = len(state)
    for i in range(size):
        for j in range(size):
            val = state[i][j]
            goal = i * size + j + 1
            if val is None:
                continue
            if val != goal:
                count += 1
    return count


def linear_conflict(state):
    """Heuristic: Manhattan + xung đột tuyến tính (Linear Conflict)."""
    size = len(state)
    manh = manhattan(state)
    conflict = 0

    # Xung đột theo hàng
    for i in range(size):
        current_row = state[i]
        for j in range(size):
            for k in range(j + 1, size):
                a, b = current_row[j], current_row[k]
                if (
                    a is not None and b is not None
                    and (a - 1) // size == i and (b - 1) // size == i
                    and a > b
                ):
                    conflict += 1

    # Xung đột theo cột
    for j in range(size):
        col = [state[i][j] for i in range(size)]
        for i in range(size):
            for k in range(i + 1, size):
                a, b = col[i], col[k]
                if (
                    a is not None and b is not None
                    and (a - 1) % size == j and (b - 1) % size == j
                    and a > b
                ):
                    conflict += 1

    return manh + 2 * conflict


def diagonal_distance(state):
    """Heuristic: Khoảng cách chéo (Diagonal Distance)."""
    size = len(state)
    distance = 0
    for i in range(size):
        for j in range(size):
            val = state[i][j]
            if val is None:
                continue
            gi, gj = divmod(val - 1, size)
            distance += max(abs(gi - i), abs(gj - j))
    return distance


def euclidean_distance(state):
    """Heuristic: Khoảng cách Euclid."""
    size = len(state)
    distance = 0
    for i in range(size):
        for j in range(size):
            val = state[i][j]
            if val is None:
                continue
            gi, gj = divmod(val - 1, size)
            distance += ((gi - i) ** 2 + (gj - j) ** 2) ** 0.5
    return distance


def custom_heuristic(state):
    """Heuristic: Kết hợp giữa Manhattan và Misplaced Tiles."""
    return manhattan(state) + misplaced_tiles(state)

def choose_heuristic(heuristic_name, state):
    """Chọn heuristic dựa trên tên."""
    if heuristic_name == "manhattan":
        return manhattan(state)
    elif heuristic_name == "misplaced":
        return misplaced_tiles(state)
    elif heuristic_name == "linear_conflict":
        return linear_conflict(state)
    elif heuristic_name == "diagonal":
        return diagonal_distance(state)
    elif heuristic_name == "euclidean":
        return euclidean_distance(state)
    elif heuristic_name == "custom":
        return custom_heuristic(state)
    else:
        raise ValueError("Unknown heuristic name.")


def get_blank_pos(state):
    for i, row in enumerate(state):
        for j, val in enumerate(row):
            if val is None:
                return i, j
    return -1, -1