from pacman.render.RenderObj import RenderOBJ
from pacman.render.Screen import Screen
from pacman.render.RenderMaze import RenderMaze
from pacman.render.RenderEntity import RenderEntity
from pacman.render.SpriteSheet import SpriteSheet
from pacman.render.Animator import Animator
from pacman.game.GameWorld import GameWorld

from typing import Optional


class AssetsError(Exception):
    pass


class RenderWorld(RenderOBJ):

    _PAC_FRAMES = [
        (10,  11,  88,  121),   # bouche fermée
        (139, 11,  236, 121),   # mi-ouverte
        (267, 11,  372, 121),   # grande ouverte
    ]

    _GHOST_FRAME_X = [5, 135, 263, 391, 519, 647, 775, 903]
    _GHOST_FRAME_W = 114
    _GHOST_DIR_ORDER = ['E', 'E', 'W', 'W', 'N', 'N', 'S', 'S']

    _GHOST_ROWS = {
        'red':    (395, 504),
        'pink':   (519, 632),
        'cyan':   (647, 760),
        'orange': (774, 896),
    }

    def __init__(self, screen: Screen,
                 world: GameWorld,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None,
                 ) -> None:
        super().__init__(screen, pos, size)
        self.__world = world
        self.__render_maze = RenderMaze(screen, world.maze)

        sheet = self.__load_sheet('assets/sprites/pacman-spritesheet.png')
        self.__render_player = self.__setup_player(sheet)
        self.__render_ghosts = self.__setup_ghosts(sheet)

    def __load_sheet(self, path: str) -> SpriteSheet:
        try:
            return SpriteSheet(path)
        except Exception as e:
            raise AssetsError(f'Cannot load spritesheet: {e}')

    def __setup_player(self, sheet: SpriteSheet) -> RenderEntity:
        frames = [sheet.crop_rect(r) for r in self._PAC_FRAMES]
        entity = RenderEntity(self._screen, self.__world.player)
        entity.set_animator(Animator(frames))
        return entity

    def __setup_ghosts(self, sheet: SpriteSheet) -> list[RenderEntity]:
        entities: list[RenderEntity] = []
        ghost_colors = list(self._GHOST_ROWS.keys())

        for i, ghost in enumerate(self.__world.ghosts):
            # Associer une couleur selon l'index (cycle si plus de 4 fantômes)
            color = ghost_colors[i % len(ghost_colors)]
            gy0, gy1 = self._GHOST_ROWS[color]

            # Grouper les frames par direction
            dir_frames: dict[str, list] = {'E': [], 'W': [], 'N': [], 'S': []}
            for j, gx in enumerate(self._GHOST_FRAME_X):
                d = self._GHOST_DIR_ORDER[j]
                dir_frames[d].append(
                    sheet.crop_rect((gx, gy0, gx + self._GHOST_FRAME_W, gy1))
                )

            entity = RenderEntity(self._screen, ghost)
            entity.set_dir_animators(
                {d: Animator(frames) for d, frames in dir_frames.items()}
            )
            entities.append(entity)

        return entities

    # -------------------------------------------------------------- render

    def render(self) -> None:
        cell_w, cell_h = self.__render_maze.cell_size
        entities_size = (int(cell_w * 0.6), int(cell_h * 0.6))

        self.__render_maze.render()
        self.__render_player_func(entities_size)
        # self.__render_ghosts_func(entities_size)

    def __render_player_func(self, size: tuple[int, int]) -> None:
        player = self.__world.player
        prog = player.progress

        px_prev = self.__render_maze.grid_to_screen(player.prev_pos, size)
        px_next = self.__render_maze.grid_to_screen(player.pos, size)

        px = int(px_prev[0] + (px_next[0] - px_prev[0]) * prog)
        py = int(px_prev[1] + (px_next[1] - px_prev[1]) * prog)

        self.__render_player.size = size
        self.__render_player.pos = (px, py)
        self.__render_player.set_rotation(player.dir_str)
        self.__render_player.set_progress(prog)
        self.__render_player.render()

    # def __render_ghosts_func(self, size: tuple[int, int]) -> None:
    #     for ghost, entity in zip(self.__world.ghosts, self.__render_ghosts):
    #         entity.size = size
    #         entity.pos = self.__render_maze.grid_to_screen(ghost.pos, size)
    #         entity.set_rotation(ghost.dir_str)
    #         entity.tick_animator()
    #         entity.render()

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
        return self._size[0] if self._size else None

    @w.setter
    def w(self, value: Optional[int]) -> None:
        if value is not None:
            self._size = (value, self._size[1]) if self._size else (value, 0)
            self.__render_maze.w = value

    @property
    def h(self) -> Optional[int]:
        return self._size[1] if self._size else None

    @h.setter
    def h(self, value: Optional[int]) -> None:
        if value is not None:
            self._size = (self._size[0], value) if self._size else (0, value)
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
        return self._pos[0] if self._pos is not None else None

    @x.setter
    def x(self, value: Optional[int]) -> None:
        if value is not None:
            self._pos = (value, self._pos[1]) if self._pos else (value, 0)
            self.__render_maze.x = value

    @property
    def y(self) -> Optional[int]:
        return self._pos[1] if self._pos is not None else None

    @y.setter
    def y(self, value: Optional[int]) -> None:
        if value is not None:
            self._pos = (self._pos[0], value) if self._pos else (0, value)
            self.__render_maze.y = value
