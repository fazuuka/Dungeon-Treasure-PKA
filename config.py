"""Shared configuration for Dungeon Treasure Hunt."""
CELL_SIZE = 42
GRID_WIDTH = 16
GRID_HEIGHT = 12
MAP_X, MAP_Y = 28, 104
PANEL_X = MAP_X + GRID_WIDTH * CELL_SIZE + 26
WINDOW_WIDTH, WINDOW_HEIGHT = PANEL_X + 320, 670
FPS = 60
TERRAIN_COST = {'.': 1, 'M': 3, 'L': 5, 'S': 1, 'T': 1}
COLORS = {
    'bg': (13, 18, 31), 'surface': (24, 32, 49), 'surface2': (32, 43, 64),
    'text': (237, 242, 250), 'muted': (156, 171, 190), 'outline': (69, 84, 106),
    'floor': (73, 103, 115), 'wall': (40, 49, 69), 'wall_edge': (92, 106, 132),
    'mud': (156, 108, 67), 'lava': (205, 78, 64), 'start': (43, 190, 146),
    'goal': (248, 195, 72), 'visited': (68, 139, 213), 'frontier': (98, 186, 222),
    'path': (255, 225, 104), 'accent': (111, 134, 250), 'button': (52, 66, 97),
}
