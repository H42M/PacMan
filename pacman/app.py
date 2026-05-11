"""Main pygame application loop for Pac-Man."""

import pygame
from pacman.constants import FPS, WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from pacman.game_config import GameConfig


def run(config: GameConfig) -> int:
    """Run the Pac-Man application."""
    print(f"Starting Pac-Man with config: {config}")
    try:
        # pygame initialization
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        clock = pygame.time.Clock()
        is_running: bool = True

        # game loop
        while is_running:
            # events management
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    is_running = False

            # frame display
            screen.fill("black")
            pygame.display.flip()
            clock.tick(FPS)
    except pygame.error as e:
        print(e)
        return 1
    finally:
        pygame.quit()
    return 0
