import pygame

from pacman.game_state import GameState
from pacman.render.RenderMaze import RenderMaze
from pacman.render.Screen import Screen
from pacman.render.RenderConfig import RenderConfig


class RenderGameplay:
    """Render the current gameplay state."""

    def __init__(self, screen: Screen, game: GameState) -> None:
        self.screen = screen
        self.game = game
        self.maze_renderer = RenderMaze(screen, game.level.maze)
        self._configure_maze_renderer()
        self.player_image = pygame.image.load(
            "assets/sprites/pacman.png"
        ).convert_alpha()

    def render(self) -> None:
        self.maze_renderer.render()
        self._render_player()

    def _render_player(self) -> None:
        cell_width, cell_height = self.maze_renderer.cell_size
        player_size = min(cell_width, cell_height) - 6
        player_surface = pygame.transform.smoothscale(
                         self.player_image,
                         (player_size, player_size),)
        player_pos = self.maze_renderer.grid_to_screen(
                     self.game.player.position,
                     (player_size, player_size),)
        self.screen.screen.blit(player_surface, player_pos)

    def _configure_maze_renderer(self) -> None:
        screen_width, screen_height = RenderConfig.screen_size
        margin = 60
        maze_size = min(screen_width, screen_height) - margin

        self.maze_renderer.size = (maze_size, maze_size)
        self.maze_renderer.pos = (
            (screen_width - maze_size) // 2,
            (screen_height - maze_size) // 2,
        )
