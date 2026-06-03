"""Main pygame application loop for Pac-Man."""

import os
import pygame

from pacman.constants import WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from pacman.game_config import GameConfig
from pacman.maze_adapter import MazeGenerationError
from pacman.level import build_level
from pacman.game_state import GameState
from pacman.input import direction_from_key

from pacman.render.RenderConfig import RenderConfig
from pacman.render.RenderGameplay import RenderGameplay
from pacman.render.Screen import Screen


def run(config: GameConfig) -> int:
    """Run the Pac-Man application."""
    print()
    print(f"Starting Pac-Man with config: {config}")
    try:
        # level building and maze generation
        level = build_level(config, 0)
        game = GameState.from_level(config, level)
        print()
        print(game)
        print()

        # pygame initialization
        os.environ["SDL_VIDEO_WINDOW_POS"] = "100,100"
        RenderConfig.init(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            (game.level.maze.width, game.level.maze.height),
        )
        screen = Screen()
        pygame.display.set_caption(WINDOW_TITLE)
        renderer = RenderGameplay(screen, game)
        is_running: bool = True
        level_complete = False

        # game loop
        while is_running:
            # events management
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.KEYDOWN:
                    key_pressed = event.key
                    direction = direction_from_key(key_pressed)
                    if direction:
                        moved = game.try_move(direction)
                        if moved and not level_complete:
                            if game.has_collected_all_pacgums():
                                print("Congratulations, you won!")
                                level_complete = True

            # frame display
            screen.clear()
            renderer.render()
            screen.flip()

    # error handling
    except pygame.error as error:
        print()
        print("Error:")
        print(error)
        print()
        return 1
    except MazeGenerationError as error:
        print()
        print("Error:")
        print(error)
        print()
        return 1
    except ValueError as error:
        print()
        print("Error:")
        print(error)
        print()
        return 1
    finally:
        pygame.quit()
    return 0
