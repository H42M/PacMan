from pacman.render.RenderObj import RenderOBJ
from pacman.render.Screen import Screen
from pacman.render.RenderMaze import RenderMaze
from pacman.render.Entity import RenderEntity

from pacman.game.GameWorld import GameWorld
from pacman.render.RenderConfig import RenderConfig

from typing import Optional


class RenderWorld(RenderOBJ):
    def __init__(self, screen: Screen,
                 world: GameWorld,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None,
                 ) -> None:
        super().__init__(screen, pos, size)
        self.__world = world
        self.__render_maze = RenderMaze(screen, world.maze)
        self.__render_player = RenderEntity(screen, world.player)
        # TODO: Meilleur moyen de load la sprite de pacman
        if not RenderConfig.get_asset('player'):
            RenderConfig.load_asset('player', 'assets/sprites/pacman.png')
        self.__render_player.set_skin(RenderConfig.get_asset('player'))

    def render(self) -> None:
        self.__render_maze.render()

        cell_x = self.__render_maze.cell_size[0]
        cell_y = self.__render_maze.cell_size[1]

        self.__render_player.size = (
            int(cell_x * 0.6),
            int(cell_y * 0.6)
        )

        self.__render_player.pos = (
            self.__render_maze.grid_to_screen(
                self.__world.player.pos, self.__render_player.size)
        )
        self.__render_player.render()

    @property
    def size(self) -> Optional[tuple[int, int]]:
        return self._size

    @size.setter
    def size(self, value: Optional[tuple[int, int]]) -> None:
        if value is not None:
            self._size = value
            self.__render_maze.size = value

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
            self.__render_maze.w = value

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
            self.__render_maze.h = value

    @property
    def pos(self) -> Optional[tuple[int, int]]:
        return self._pos

    @pos.setter
    def pos(self, value: Optional[tuple[int, int]]) -> None:
        if value is not None:
            self._pos = value
            self.__render_maze.pos = value

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
            self.__render_maze.x = value

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
            self.__render_maze.y = value
