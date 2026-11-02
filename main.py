"""Launch with: python main.py"""
import pygame
from algorithms import ALGORITHMS
from config import (FPS, WINDOW_WIDTH, WINDOW_HEIGHT, PANEL_X)
from experiments.scenarios import load_scenario
from game.renderer import Renderer
from visualization.animation import SearchAnimation


def control_rects():
    return {
        'UCS': pygame.Rect(PANEL_X+6, 180, 87, 39),
        'Greedy': pygame.Rect(PANEL_X+103, 180, 91, 39),
        'A*': pygame.Rect(PANEL_X+204, 180, 86, 39),
        'Basic': pygame.Rect(PANEL_X+6, 258, 87, 39),
        'Walls': pygame.Rect(PANEL_X+103, 258, 91, 39),
        'Weighted': pygame.Rect(PANEL_X+204, 258, 86, 39),
        'SEARCH': pygame.Rect(PANEL_X+6, 314, 180, 39),
        'RESET': pygame.Rect(PANEL_X+196, 314, 94, 39),
    }


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Dungeon Treasure Hunt | AI Pathfinding')
    clock, renderer = pygame.time.Clock(), Renderer()
    controls = control_rects()
    scenario, algorithm, speed = 'Weighted', 'A*', 1
    dungeon = load_scenario(scenario)
    animation = SearchAnimation()
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                    speed = min(8, speed * 2)
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    speed = max(1, speed // 2)
                elif event.key == pygame.K_SPACE:
                    animation.begin(ALGORITHMS[algorithm](dungeon))
                elif event.key == pygame.K_r:
                    animation.reset()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for name, rect in controls.items():
                    if not rect.collidepoint(event.pos):
                        continue
                    if name in ALGORITHMS:
                        algorithm = name
                        animation.reset()
                    elif name in ('Basic', 'Walls', 'Weighted'):
                        scenario = name
                        dungeon = load_scenario(scenario)
                        animation.reset()
                    elif name == 'SEARCH':
                        animation.begin(ALGORITHMS[algorithm](dungeon))
                    elif name == 'RESET':
                        animation.reset()
                    break
        animation.update(dt, nodes_per_second=24*speed)
        renderer.draw(screen, dungeon, animation, algorithm, scenario, speed, controls)
    pygame.quit()


if __name__ == '__main__':
    main()
