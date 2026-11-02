"""Search engine and metric definitions for fair algorithm comparisons."""
from dataclasses import dataclass
from heapq import heappush, heappop
from itertools import count
from time import perf_counter


@dataclass
class SearchResult:
    algorithm: str
    path: list
    explored_order: list
    total_cost: int | None
    path_length: int
    explored_nodes: int
    execution_ms: float


def manhattan(a, b):
    # Minimum step cost = 1, so this is admissible for A*.
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct(parents, goal):
    path = [goal]
    while path[-1] in parents:
        path.append(parents[path[-1]])
    return list(reversed(path))


def search(dungeon, mode):
    """UCS uses g, Greedy uses h, A* uses g+h.

    - explored_nodes counts UNIQUE expanded nodes (heap pop accepted).
    - execution_ms measures search only, excluding display/animation.
    - a node may be expanded again if a better g is discovered (A*).
    """
    if mode not in ('UCS', 'Greedy', 'A*'):
        raise ValueError(f'Unknown algorithm: {mode}')
    tic = perf_counter()
    start, goal = dungeon.start, dungeon.goal
    queue, serial = [], count()
    best_g = {start: 0}
    parents = {}
    expanded_g = {}
    order = []

    def priority(node, g):
        h = manhattan(node, goal)
        return g if mode == 'UCS' else h if mode == 'Greedy' else g + h

    heappush(queue, (priority(start, 0), next(serial), 0, start))
    while queue:
        _, _, g, current = heappop(queue)
        if g != best_g.get(current):
            continue  # stale heap entry
        if current in expanded_g and (mode == 'Greedy' or g >= expanded_g[current]):
            continue
        expanded_g[current] = g
        if current not in order:
            order.append(current)
        if current == goal:
            path = reconstruct(parents, goal)
            return SearchResult(mode, path, order, dungeon.cost_of_path(path),
                                len(path) - 1, len(order), (perf_counter() - tic) * 1000)
        for neighbor in dungeon.neighbors(current):
            proposed = g + dungeon.move_cost(neighbor)
            if mode == 'Greedy':
                # Greedy chooses based on h alone. The first discovery sets its parent.
                if neighbor in best_g:
                    continue
            elif proposed >= best_g.get(neighbor, float('inf')):
                continue
            best_g[neighbor] = proposed
            parents[neighbor] = current
            heappush(queue, (priority(neighbor, proposed), next(serial), proposed, neighbor))
    return SearchResult(mode, [], order, None, 0, len(order), (perf_counter() - tic) * 1000)
