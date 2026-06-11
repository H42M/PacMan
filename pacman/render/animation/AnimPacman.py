from pacman.render.RenderObj import RenderOBJ
from pacman.render.Screen import Screen
from pacman.render.animation.SpriteSheet import SpriteSheet
from pacman.render.animation.Animator import Animator
from pacman.render.animation.RenderEntity import RenderEntity


from typing import Optional
import pygame

from pacman.player import Direction


class AnimPacman(RenderOBJ):
    def __init__(self, screen: Screen) -> None:
        self.__move_progress: float = 1.0
        self.__move_speed = 1.0 / ((200 / 1000) * 60)
        self.__tick_rate = 12

        super().__init__(screen)

        self.__prev_pos = self.pos
        self.__real_pos = self.pos
        self.__target_pos = self.pos
        self.__move_progress = 0.0
        self.__move_duration_ms = 200
        self.__move_start_ms = 0

        self.__sheet = self.__load_sheet(
            'assets/sprites/pacman-spritesheet.png')
        self._SHEET_NB_SPRITES_H = 14
        self._SHEET_NB_SPRITES_V = 15
        self._SHEET_SPRITE_W = self.__sheet.size[0] // self._SHEET_NB_SPRITES_H
        self._SHEET_SPRITE_H = self.__sheet.size[1] // self._SHEET_NB_SPRITES_V
        self.__render_pacman = self.__set_render_pacman()

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

    def set_target_pos(self, target_pos: tuple[int, int]) -> None:
        if not self._pos:
            self._pos = target_pos
            self.__real_pos = target_pos
            self.__prev_pos = target_pos
            self.__target_pos = target_pos
            return
        if self.__target_pos != target_pos:
            self.__prev_pos = self.__real_pos
            self.__target_pos = target_pos
            self.__move_start_ms = pygame.time.get_ticks()
            self.__move_progress = 0.0

    def tick(self) -> None:
        self.__render_pacman.tick_animator()
        if not self.__prev_pos or not self.__target_pos:
            return

        elapsed = pygame.time.get_ticks() - self.__move_start_ms
        self.__move_progress = min(elapsed / self.__move_duration_ms, 1.0)

        x = self.__prev_pos[0] + ((self.__target_pos[0] - self.__prev_pos[0])
                                  * self.__move_progress)
        y = self.__prev_pos[1] + ((self.__target_pos[1] - self.__prev_pos[1])
                                  * self.__move_progress)
        self.__real_pos = (int(x), int(y))

        if self.__move_progress >= 1.0:
            self._pos = self.__target_pos
            self.__real_pos = self.__target_pos

    def render(self) -> None:
        self.__render_pacman.pos = self.__real_pos
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

    def set_move_delay(self, delay_ms: int, fps: int = 60) -> None:
        self.__move_duration_ms = delay_ms
