import copy
from heuristic import *

def ida_star(self):
    def heuristic(state):
        return choose_heuristic(self.heuristic,state)

    def neighbors(state):
        result = []
        r, c = get_blank_pos(state)
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size:
                new_state = copy.deepcopy(state)
                new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
                result.append((new_state, (nr, nc)))
        return result

    def dfs(path, g, threshold):
        state = path[-1]
        f = g + heuristic(state)
        if f > threshold:
            return f
        if serialize(state) == goal_serial:
            return path
        min_cost = float("inf")
        for neighbor, _ in neighbors(state):
            if serialize(neighbor) in visited:
                continue
            visited.add(serialize(neighbor))
            res = dfs(path + [neighbor], g + 1, threshold)
            if isinstance(res, list):
                return res
            if res < min_cost:
                min_cost = res
            visited.remove(serialize(neighbor))
        return min_cost

    start_state = copy.deepcopy(self.board_state)
    goal = [[i * self.board_size + j + 1 for j in range(self.board_size)] for i in range(self.board_size)]
    goal[-1][-1] = None
    goal_serial = serialize(goal)
    size = self.board_size

    threshold = heuristic(start_state)
    path = [start_state]
    visited = set()
    visited.add(serialize(start_state))

    while True:
        temp = dfs(path, 0, threshold)
        if isinstance(temp, list):
            return temp[1:]
        if temp == float("inf"):
            return None
        threshold = temp


