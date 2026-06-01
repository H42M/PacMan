import pygame

from pacman.game_state import GameState
from pacman.render.RenderMaze import RenderMaze
from pacman.render.Screen import Screen


class RenderGameplay:
    """Render the current gameplay state."""

    def __init__(self, screen: Screen, game: GameState) -> None:
        self.screen = screen
        self.game = game
        self.maze_renderer = RenderMaze(screen, game.level.maze)
        maze_size = 540
        self.maze_renderer.size = (maze_size, maze_size)
        self.maze_renderer.pos = ((800 - maze_size) // 2, 30)
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
