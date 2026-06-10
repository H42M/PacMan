import pygame
from typing import Optional

from pacman.game_state import GameState
from pacman.ghost import GhostMode
from pacman.render.RenderMaze import RenderMaze
from pacman.render.Screen import Screen
from pacman.render.RenderConfig import RenderConfig
from pacman.render.RenderObj import RenderOBJ


class RenderGameplay (RenderOBJ):
    """Render the current gameplay state."""

    def __init__(self, screen: Screen, game: GameState) -> None:
        super().__init__(screen)
        self.screen = screen
        self.game = game
        self.maze_renderer = RenderMaze(screen, game.level.maze)
        self._configure_maze_renderer()
        self.player_image = pygame.image.load(
            "assets/sprites/pacman.png"
        ).convert_alpha()

    def render(self) -> None:
        self.maze_renderer.render()
        self._render_pacgums()
        self._render_ghosts()
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

    def _render_ghosts(self) -> None:
        surface = self.screen.screen
        cell_width, cell_height = self.maze_renderer.cell_size
        ghost_size = min(cell_width, cell_height) - 8

        for ghost in self.game.ghosts:
            if ghost.mode is GhostMode.DEAD:
                continue
            ghost_pos = self.maze_renderer.grid_to_screen(
                ghost.position,
                (ghost_size, ghost_size),
            )
            center = (
                ghost_pos[0] + ghost_size // 2,
                ghost_pos[1] + ghost_size // 2,
            )
            pygame.draw.circle(surface, ghost.color, center, ghost_size // 2)

    def _render_pacgums(self) -> None:
        surface = self.screen.screen
        pacgum_color = (255, 220, 120)
        super_pacgum_color = (255, 255, 255)

        cell_width, cell_height = self.maze_renderer.cell_size
        dot_size = max(4, min(cell_width, cell_height) // 6)
        super_dot_size = max(12, min(cell_width, cell_height) // 2)

        for position in self.game.pacgums:
            dot_pos = self.maze_renderer.grid_to_screen(
                position,
                (dot_size, dot_size),
            )
            center = (
                dot_pos[0] + dot_size // 2,
                dot_pos[1] + dot_size // 2,
            )
            pygame.draw.circle(surface, pacgum_color, center, dot_size // 2)
        for position in self.game.super_pacgums:
            dot_pos = self.maze_renderer.grid_to_screen(
                position,
                (super_dot_size, super_dot_size),
            )
            center = (
                dot_pos[0] + super_dot_size // 2,
                dot_pos[1] + super_dot_size // 2,
            )
            pygame.draw.circle(surface, super_pacgum_color,
                               center, super_dot_size // 2)

    def _configure_maze_renderer(self) -> None:
        screen_width, screen_height = RenderConfig.screen_size
        margin = 60
        maze_size = min(screen_width, screen_height) - margin

        self.maze_renderer.size = (maze_size, maze_size)
        self.maze_renderer.pos = (
            (screen_width - maze_size) // 2,
            (screen_height - maze_size) // 2,
        )

    @property
    def size(self) -> Optional[tuple[int, int]]:
        return self._size

    @size.setter
    def size(self, value: Optional[tuple[int, int]]) -> None:
        if value is not None:
            self._size = value
            self.maze_renderer.size = value

    @property
    def w(self) -> Optional[int]:
        if self._size:
            return self._size[0]
        return None

    @w.setter
    def w(self, value: Optional[int]) -> None:
        if value is not None:
            if self._size:
                self._size = (value, self._size[1])
            else:
                self._size = (value, 0)
            self.maze_renderer.size = self._size

    @property
    def h(self) -> Optional[int]:
        if self._size is not None:
            return self._size[1]
        return None

    @h.setter
    def h(self, value: Optional[int]) -> None:
        if value is not None:
            if self._size:
                self._size = (self._size[0], value)
            else:
                self._size = (0, value)
            self.maze_renderer.size = self._size

    @property
    def pos(self) -> Optional[tuple[int, int]]:
        return self._pos

    @pos.setter
    def pos(self, value: Optional[tuple[int, int]]) -> None:
        if value is not None:
            self._pos = value
            self.maze_renderer.pos = self._pos

    @property
    def x(self) -> Optional[int]:
        if self._pos is not None:
            return self._pos[0]
        return None

    @x.setter
    def x(self, value: Optional[int]) -> None:
        if value is not None:
            if self._pos:
                self._pos = (value, self._pos[1])
            else:
                self._pos = (value, 0)
            self.maze_renderer.pos = self._pos

    @property
    def y(self) -> Optional[int]:
        if self._pos is not None:
            return self._pos[1]
        return None

    @y.setter
    def y(self, value: Optional[int]) -> None:
        if value is not None:
            if self._pos:
                self._pos = (self._pos[0], value)
            else:
                self._pos = (0, value)
            self.maze_renderer.pos = self._pos
