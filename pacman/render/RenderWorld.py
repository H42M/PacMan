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
    def __init__(self, screen: Screen,
                 world: GameWorld,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None,
                 ) -> None:
        super().__init__(screen, pos, size)
        self.__world = world
        self.__render_maze = RenderMaze(screen, world.maze)

        sheet = self.__load_sheet('assets/sprites/pacman-spritesheet.png')

        self._SHEET_NB_SPRITES_H = 14
        self._SHEET_NB_SPRITES_V = 15
        self._SHEET_SPRITE_W = sheet.size[0] // self._SHEET_NB_SPRITES_H
        self._SHEET_SPRITE_H = sheet.size[1] // self._SHEET_NB_SPRITES_V

        self.__render_player = self.__setup_player(sheet)
        self.__render_ghosts = self.__setup_ghosts(sheet)

    def __load_sheet(self, path: str) -> SpriteSheet:
        try:
            return SpriteSheet(path)
        except Exception as e:
            raise AssetsError(f'Cannot load spritesheet: {e}')

    def __setup_player(self, sheet: SpriteSheet) -> RenderEntity:
        # frames = [sheet.crop_rect(r) for r in self._PAC_FRAMES]
        frames = []
        for i in range(4):
            w = self._SHEET_SPRITE_W
            h = self._SHEET_SPRITE_H
            x = i * w
            y = 0
            frames.append(sheet.crop_rect((x, y, w, h)))

        entity = RenderEntity(self._screen, self.__world.player)
        entity.set_animator(Animator(frames))
        return entity

    def __setup_ghosts(self, sheet: SpriteSheet) -> list[RenderEntity]:
        entities: list[RenderEntity] = []
        # Ghost loop
        for ghost_i, ghost in enumerate(self.__world.ghosts):
            # Direction loop
            animators = {}
            for dir_i, dir in enumerate('EWNS'):
                frames = []
                # Frame loop
                for frame_i in range(2):
                    w = self._SHEET_SPRITE_W
                    h = self._SHEET_SPRITE_H
                    x = (frame_i * w) + (dir_i * w * 2)
                    y = h * (4 + ghost_i)
                    frames.append(sheet.crop_rect((x, y, w, h)))
                animators[dir] = Animator(frames, tick_rate=8)

            entity = RenderEntity(self._screen, ghost)
            entity.set_dir_animators(animators)
            entities.append(entity)
        return entities

    # -------------------------------------------------------------- render

    def render(self) -> None:
        cell_w, cell_h = self.__render_maze.cell_size
        entities_size = (int(cell_w * 0.6), int(cell_h * 0.6))

        self.__render_maze.render()
        self.__render_player_func(entities_size)
        self.__render_ghosts_func(entities_size)

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

    def __render_ghosts_func(self, size: tuple[int, int]) -> None:
        for ghost, entity in zip(self.__world.ghosts, self.__render_ghosts):
            entity.size = size
            entity.pos = self.__render_maze.grid_to_screen(ghost.pos, size)
            entity.set_rotation(ghost.dir_str)
            entity.tick_animator()
            entity.render()

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
