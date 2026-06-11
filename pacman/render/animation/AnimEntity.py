from typing import Optional

import pygame

from pacman.render.RenderObj import RenderOBJ
from pacman.render.Screen import Screen
from pacman.render.animation.RenderEntity import RenderEntity
from pacman.render.animation.SpriteSheet import SpriteSheet
from pacman.player import Direction


class AnimEntity(RenderOBJ):
    def __init__(self, screen: Screen) -> None:
        self._move_progress: float = 1.0
        self._move_speed = 1.0 / ((200 / 1000) * 60)
        self._tick_rate = 12

        super().__init__(screen)

        self._prev_pos = self.pos
        self._real_pos = self.pos
        self._target_pos = self.pos
        self._move_progress = 0.0
        self._move_duration_ms = 200
        self._move_start_ms = 0

        self._sheet = self._load_sheet(
            'assets/sprites/pacman-spritesheet.png')
        self._SHEET_NB_SPRITES_H = 14
        self._SHEET_NB_SPRITES_V = 15
        self._SHEET_SPRITE_W = self._sheet.size[0] // self._SHEET_NB_SPRITES_H
        self._SHEET_SPRITE_H = self._sheet.size[1] // self._SHEET_NB_SPRITES_V

        self._render_entity = RenderEntity(screen)

    def _load_sheet(self, path: str) -> SpriteSheet:
        try:
            return SpriteSheet(path)
        except Exception as e:
            raise ValueError(f'Cannot load spritesheet: {e}')

    def set_target_pos(self, target_pos: tuple[int, int]) -> None:
        if not self._pos:
            self._pos = target_pos

            self._real_pos = target_pos
            self._prev_pos = target_pos
            self._target_pos = target_pos
            self._move_start_ms = pygame.time.get_ticks()
            return
        if self._target_pos != target_pos:
            self._prev_pos = self._real_pos
            self._target_pos = target_pos
            self._move_start_ms = pygame.time.get_ticks()
            self._move_progress = 0.0

    def tick(self) -> None:
        self._render_entity.tick_animator()
        if not self._prev_pos or not self._target_pos:
            print('ghost pos not set')
            return

        elapsed = pygame.time.get_ticks() - self._move_start_ms
        self._move_progress = min(elapsed / self._move_duration_ms, 1.0)

        x = self._prev_pos[0] + ((self._target_pos[0] - self._prev_pos[0])
                                 * self._move_progress)
        y = self._prev_pos[1] + ((self._target_pos[1] - self._prev_pos[1])
                                 * self._move_progress)
        self._real_pos = (int(x), int(y))

        if self._move_progress >= 1.0:
            self._pos = self._target_pos
            self._real_pos = self._target_pos

    def set_move_delay(self, delay_ms: int) -> None:
        self._move_duration_ms = delay_ms

    def render(self) -> None:
        self._render_entity.pos = self._real_pos
        self._render_entity.size = self.size
        self._render_entity.render()

    def set_rotation(self, rotation: Optional[Direction]) -> None:
        if not rotation:
            return
        dir_mapper = {
            Direction.UP: 'N',
            Direction.DOWN: 'S',
            Direction.RIGHT: 'E',
            Direction.LEFT: 'W',
        }
        self._render_entity.set_rotation(dir_mapper[rotation])

    def is_anim_over(self, nb_frames: Optional[int] = None):
        animator = self._render_entity.animator
        if not animator:
            return
        if nb_frames is None:
            nb_frames = len(animator.frames)

        return True if animator.frame_index >= nb_frames else False
