import time
import random
from Ida_algorithm import ida_star
import copy
import numpy as np
import csv

class OptimizedPuzzleEvaluator:
    def __init__(self, board_size, max_time):
        self.board_size = board_size
        self.max_time = max_time
        self.heuristics = ["manhattan", "misplaced", "linear_conflict", "diagonal", "euclidean", "custom"]

        self.goal_state = [[i * board_size + j + 1 for j in range(board_size)] for i in range(board_size)]
        self.goal_state[-1][-1] = None
        self.goal_serial = self.serialize(self.goal_state)

    def serialize(self, state):
        return tuple(tuple(row) for row in state)

    def shuffle_state(self, state, moves):
        r, c = self.find_blank(state)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for _ in range(moves):
            dr, dc = random.choice(directions)
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                state[r][c], state[nr][nc] = state[nr][nc], state[r][c]
                r, c = nr, nc

        return state

    def find_blank(self, state):
        for i, row in enumerate(state):
            if None in row:
                return i, row.index(None)
        return -1, -1

    def generate_solvable_states(self, count=100):
        states = []
        for _ in range(count):
            state = copy.deepcopy(self.goal_state)
            state = self.shuffle_state(state, random.randint(30, 50))
            states.append(state)
        return states

    def evaluate_heuristic(self, heuristic_name, states):
        results = []

        for state_idx, state in enumerate(states):
            print(f"Evaluating state {state_idx + 1} with {heuristic_name}...", end="\r")

            class PuzzleWrapper:
                def __init__(self, state, size, heuristic):
                    self.board_state = copy.deepcopy(state)
                    self.board_size = size
                    self.heuristic = heuristic
                    self.visited_count = 0

            puzzle = PuzzleWrapper(state, self.board_size, heuristic_name)

            start_time = time.time()
            try:
                solution_path = self.run_with_timeout(ida_star, puzzle, timeout=self.max_time)
                end_time = time.time()

                if solution_path:
                    results.append({
                        'time': end_time - start_time,
                        'steps': len(solution_path),
                        'visited': puzzle.visited_count,
                        'success': True
                    })
                else:
                    results.append({
                        'time': end_time - start_time,
                        'steps': 0,
                        'visited': puzzle.visited_count,
                        'success': False
                    })
            except TimeoutError:
                results.append({
                    'time': self.max_time,
                    'steps': 0,
                    'visited': puzzle.visited_count,
                    'success': False
                })

        return results

    def run_with_timeout(self, func, *args, timeout):
        from threading import Thread
        import queue

        result_queue = queue.Queue()

        def worker():
            try:
                result = func(*args)
                result_queue.put(result)
            except Exception as e:
                result_queue.put(e)

        thread = Thread(target=worker)
        thread.start()
        thread.join(timeout=timeout)

        if thread.is_alive():
            raise TimeoutError()

        if not result_queue.empty():
            result = result_queue.get()
            if isinstance(result, Exception):
                raise result
            return result

        raise TimeoutError()

    def calculate_stats(self, results):
        successful = [r for r in results if r['success']]

        if successful:
            avg_time = np.mean([r['time'] for r in successful])
            avg_steps = np.mean([r['steps'] for r in successful])
            avg_visited = np.mean([r['visited'] for r in successful])
        else:
            avg_time = avg_steps = avg_visited = 0

        return {
            'avg_time': avg_time,
            'avg_steps': avg_steps,
            'avg_visited': avg_visited,
            'total_tested': len(results),
        }

    def evaluate_all(self, output_file):
        test_states = self.generate_solvable_states(100)

        all_stats = {}
        for heuristic in self.heuristics:
            print(f"\nEvaluating {heuristic} heuristic...")
            results = self.evaluate_heuristic(heuristic, test_states)
            stats = self.calculate_stats(results)
            all_stats[heuristic] = stats

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)

            writer.writerow([
                'Heuristic',
                'Total Tested',
                'Avg Time (successful)',
                'Avg Solution Length',
                'Avg Visited States'
            ])

            for heuristic, stats in all_stats.items():
                writer.writerow([
                    heuristic.upper(),
                    stats['total_tested'],
                    f"{stats['avg_time']:.3f}",
                    f"{stats['avg_steps']:.1f}",
                    f"{stats['avg_visited']:.0f}"
                ])

        return all_stats


if __name__ == "__main__":
    if __name__ == "__main__":
        evaluator = OptimizedPuzzleEvaluator(board_size=4, max_time=50)
        evaluator.evaluate_all("Danhgia4.csv")