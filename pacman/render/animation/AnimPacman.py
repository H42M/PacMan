from pacman.render.animation.AnimEntity import AnimEntity
from pacman.render.Screen import Screen
from pacman.render.animation.Animator import Animator
from pacman.render.animation.RenderEntity import RenderEntity


class AnimPacman(AnimEntity):
    def __init__(self, screen: Screen) -> None:
        super().__init__(screen)
        self._render_entity = self.__set_render_pacman()

    def __set_render_pacman(self) -> RenderEntity:
        frames = []
        for i in range(3):
            w = self._SHEET_SPRITE_W
            h = self._SHEET_SPRITE_H
            x = i * w
            y = 0
            frames.append(self._sheet.crop_rect((x, y, w, h)))

        entity = RenderEntity(self._screen)
        entity.set_animator(Animator(frames, tick_rate=self._tick_rate))
        return entity
