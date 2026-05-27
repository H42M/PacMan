from pacman.render.RenderObj import RenderOBJ
from pacman.render.Screen import Screen
from pacman.render.RenderMaze import RenderMaze
from pacman.render.Entity import RenderEntity

from pacman.game.GameWorld import GameWorld
from pacman.render.RenderConfig import RenderConfig

from typing import Optional


class AssetsError(Exception):

    pass


class RenderWorld(RenderOBJ):
    def __init__(self, screen: Screen,
                 world: GameWorld,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None,
                 ) -> None:
        super().__init__(screen, pos, size)
        self.__world = world
        self.__render_maze = RenderMaze(screen, world.maze)
        self.__load_assets()
        self.__render_player = RenderEntity(screen, world.player)
        self.__render_player.set_skin(RenderConfig.get_asset('player'))
        self.__render_ghosts: list[RenderEntity] = []
        for ghost in self.__world.ghosts:
            self.__render_ghosts.append(RenderEntity(self._screen, ghost))
            self.__render_ghosts[-1].set_skin(RenderConfig.get_asset('ghost'))

    def __render_player_func(self, player_size: tuple[int, int]
                             ) -> None:
        self.__render_player.size = player_size

        player = self.__world.player
        prog = player.progress

        px_prev = self.__render_maze.grid_to_screen(player.prev_pos,
                                                    player_size)
        px_next = self.__render_maze.grid_to_screen(player.pos, player_size)

        px = int(px_prev[0] + (px_next[0] - px_prev[0]) * prog)
        py = int(px_prev[1] + (px_next[1] - px_prev[1]) * prog)

        self.__render_player.pos = (px, py)
        self.__render_player.set_rotation(player.dir_str)

    def __render_ghosts_func(self, ghost_size: tuple[int, int]) -> None:
        for (ghost, render_ghost) in zip(self.__world.ghosts,
                                         self.__render_ghosts):
            # ghost.pos = (i + 1, i + 1)
            render_ghost.size = ghost_size
            render_ghost.pos = self.__render_maze.grid_to_screen(ghost.pos,
                                                                 ghost_size)
            render_ghost.render()

    def render(self) -> None:
        cell_w, cell_h = self.__render_maze.cell_size
        entities_size = (int(cell_w * 0.6), int(cell_h * 0.6))

        self.__render_maze.render()
        self.__render_player_func(entities_size)
        self.__render_ghosts_func(entities_size)

        self.__render_player.render()

    def __load_assets(self) -> None:
        try:
            if not RenderConfig.get_asset('player'):
                RenderConfig.load_asset('player', 'assets/sprites/pacman.png')
        except Exception:
            raise AssetsError('Render World unable to load player asset')

        try:
            if not RenderConfig.get_asset('ghost'):
                RenderConfig.load_asset('ghost',
                                        'assets/sprites/ghost-blue.png')
        except Exception:
            raise AssetsError('Render World unable to load ghost asset')

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
