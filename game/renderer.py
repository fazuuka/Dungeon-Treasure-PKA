"""Draw the entire Pygame interface with built-in fonts and shapes."""
import pygame
from config import (CELL_SIZE, MAP_X, MAP_Y, PANEL_X, WINDOW_HEIGHT,
                    WINDOW_WIDTH, COLORS)
from visualization.statistics import summary


def label(surface, font, text, position, color=None):
    surface.blit(font.render(text, True, color or COLORS['text']), position)


class Renderer:
    def __init__(self):
        pygame.font.init()
        self.large = pygame.font.SysFont('segoeui', 31, bold=True)
        self.title = pygame.font.SysFont('segoeui', 21, bold=True)
        self.medium = pygame.font.SysFont('segoeui', 17, bold=True)
        self.small = pygame.font.SysFont('segoeui', 14)

    def button(self, surface, rect, text, selected=False):
        color = COLORS['accent'] if selected else COLORS['button']
        pygame.draw.rect(surface, color, rect, border_radius=10)
        label(surface, self.medium, text,
              (rect.centerx - self.medium.size(text)[0] // 2,
               rect.centery - self.medium.get_height() // 2))

    def draw(self, screen, dungeon, animation, algorithm, scenario, speed, controls):
        screen.fill(COLORS['bg'])
        label(screen, self.large, 'DUNGEON TREASURE HUNT', (28, 19))
        label(screen, self.small, 'AI pathfinding  /  find the treasure', (29, 65), COLORS['muted'])
        for y, row in enumerate(dungeon.rows):
            for x, terrain in enumerate(row):
                node = (x, y)
                rect = pygame.Rect(MAP_X + x*CELL_SIZE, MAP_Y + y*CELL_SIZE,
                                   CELL_SIZE-2, CELL_SIZE-2)
                colors = {'#': COLORS['wall'], '.': COLORS['floor'],
                          'M': COLORS['mud'], 'L': COLORS['lava'],
                          'S': COLORS['start'], 'T': COLORS['goal']}
                color = colors[terrain]
                if node in animation.visited and terrain not in 'ST#':
                    color = COLORS['visited']
                if node in animation.path and terrain not in 'ST#':
                    color = COLORS['path']
                pygame.draw.rect(screen, color, rect, border_radius=5)
                if terrain == '#':
                    pygame.draw.rect(screen, COLORS['wall_edge'], rect, width=2, border_radius=5)
                if terrain == 'M' and node not in animation.path:
                    label(screen, self.small, '3', (rect.x+15, rect.y+10))
                if terrain == 'L' and node not in animation.path:
                    label(screen, self.small, '5', (rect.x+15, rect.y+10))
                if terrain in 'ST':
                    letter = 'S' if terrain == 'S' else '$'
                    label(screen, self.title, letter, (rect.x+12, rect.y+5), COLORS['bg'])
        pygame.draw.rect(screen, COLORS['surface'],
                         pygame.Rect(PANEL_X - 13, 101, 320, 510), border_radius=15)
        label(screen, self.title, 'SEARCH CONTROL', (PANEL_X+6, 119))
        label(screen, self.small, 'Choose algorithm', (PANEL_X+6, 156), COLORS['muted'])
        for name in ('UCS', 'Greedy', 'A*'):
            self.button(screen, controls[name], name, algorithm == name)
        label(screen, self.small, 'Dungeon scenario', (PANEL_X+6, 235), COLORS['muted'])
        for name in ('Basic', 'Walls', 'Weighted'):
            self.button(screen, controls[name], name, scenario == name)
        self.button(screen, controls['SEARCH'], 'START SEARCH', True)
        self.button(screen, controls['RESET'], 'RESET')
        label(screen, self.small, f'Animation speed: {speed}x  (press +/-)',
              (PANEL_X+7, 365), COLORS['muted'])
        pygame.draw.line(screen, COLORS['outline'], (PANEL_X+6, 395),
                         (PANEL_X+290, 395), 1)
        label(screen, self.title, 'RESULTS', (PANEL_X+6, 406))
        for i, (name, value) in enumerate(summary(animation.result)):
            y = 443+i*36
            label(screen, self.small, name, (PANEL_X+6, y), COLORS['muted'])
            label(screen, self.medium, value,
                  (PANEL_X+289 - self.medium.size(value)[0], y-3))
        status = ('Searching...' if animation.result and not animation.finished
                  else 'Path found!' if animation.result and animation.result.path
                  else 'No path found' if animation.result else 'Ready to search')
        label(screen, self.small, status, (PANEL_X+7, 587), COLORS['goal'])
        label(screen, self.small,
              'Legend: floor 1  |  mud 3  |  lava 5  |  wall blocked',
              (MAP_X, 627), COLORS['muted'])
        pygame.display.flip()
