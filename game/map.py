"""Grid representation. x is column; y is row."""
from config import TERRAIN_COST


class DungeonMap:
    def __init__(self, rows):
        if not rows or len({len(row) for row in rows}) != 1:
            raise ValueError('Map rows must have a consistent non-zero width')
        if any(char not in '#.MLST' for row in rows for char in row):
            raise ValueError('Unknown terrain symbol')
        self.rows = tuple(rows)
        self.width, self.height = len(rows[0]), len(rows)
        start = [(x, y) for y, row in enumerate(rows) for x, c in enumerate(row) if c == 'S']
        goal = [(x, y) for y, row in enumerate(rows) for x, c in enumerate(row) if c == 'T']
        if len(start) != 1 or len(goal) != 1:
            raise ValueError('Exactly one start S and goal T required')
        self.start, self.goal = start[0], goal[0]

    def at(self, node):
        x, y = node
        return self.rows[y][x]

    def neighbors(self, node):
        x, y = node
        # Fixed deterministic order for reproducible comparisons.
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and self.rows[ny][nx] != '#':
                yield (nx, ny)

    def move_cost(self, destination):
        """Cost is charged when ENTERING the destination tile."""
        return TERRAIN_COST[self.at(destination)]

    def cost_of_path(self, path):
        return sum(self.move_cost(node) for node in path[1:])
