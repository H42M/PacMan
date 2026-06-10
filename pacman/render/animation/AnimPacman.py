from pacman.render.RenderObj import RenderOBJ
from pacman.render.Screen import Screen
from pacman.render.animation import SpriteSheet, RenderEntity, Animator

from typing import Optional

from pacman.player import Direction


class AnimPacman(RenderOBJ):
    def __init__(self, screen: Screen) -> None:
        super().__init__(screen)
        self.__last_pos = self.pos
        self.__sheet = self.__load_sheet(
            'assets/sprites/pacman-spritesheet.png')
        self._SHEET_NB_SPRITES_H = 14
        self._SHEET_NB_SPRITES_V = 15
        self._SHEET_SPRITE_W = self.__sheet.size[0] // self._SHEET_NB_SPRITES_H
        self._SHEET_SPRITE_H = self.__sheet.size[1] // self._SHEET_NB_SPRITES_V
        self.__render_pacman = self.__set_render_pacman()

        self.__cell_pos: tuple[int, int] = (0, 0)
        self.__move_progress: float = 1.0
        self.__move_speed = 0.05
        self.__tick_rate = 12

    def __set_render_pacman(self) -> RenderEntity:
        frames = []
        for i in range(3):
            w = self._SHEET_SPRITE_W
            h = self._SHEET_SPRITE_H
            x = i * w
            y = 0
            frames.append(self.__sheet.crop_rect((x, y, w, h)))

        entity = RenderEntity(self._screen)
        entity.set_animator(Animator(frames, tick_rate=self.__tick_rate))
        return entity

    def __load_sheet(self, path: str) -> SpriteSheet:
        try:
            return SpriteSheet(path)
        except Exception as e:
            raise ValueError(f'Cannot load spritesheet: {e}')

    def start_moving(self, new_pos: tuple[int, int]) -> None:
        self.__prev_pos = self.pos
        self.pos = new_pos
        self.__move_progress = 0.0

    def tick(self) -> None:
        if self.__move_progress < 1.0:
            self.__move_progress = min(
                1.0, self.__move_progress + self.__move_speed)

    def render(self):
        self.__render_pacman.pos = self.pos
        self.__render_pacman.size = self.size
        self.__render_pacman.render()

    def set_rotation(self, rotation: Optional[Direction]) -> None:
        if not rotation:
            return
        dir_mapper = {
            Direction.UP: 'N',
            Direction.DOWN: 'S',
            Direction.RIGHT: 'E',
            Direction.LEFT: 'W',
        }
        self.__render_pacman.set_rotation(dir_mapper[rotation])

    def set_progress(self, progress: float) -> None:
        self.__render_pacman.set_progress(progress)

    def tick_animator(self) -> None:
        self.__render_pacman.tick_animator()

    @property
    def pos(self) -> Optional[tuple[int, int]]:
        return self._pos

    @pos.setter
    def pos(self, value: Optional[tuple[int, int]]) -> None:
        self.__last_pos = self.pos
        self._pos = value
