from pacman.render.animation.AnimEntity import AnimEntity
from pacman.render.Screen import Screen
from pacman.render.animation.Animator import Animator
from pacman.render.animation.RenderEntity import RenderEntity


class AnimGhost(AnimEntity):
    def __init__(self, screen: Screen, ghost_color: int = 0) -> None:
        super().__init__(screen)
        self.__ghost_color = ghost_color
        self._render_entity = self.__set_render_ghost()

    def __set_render_ghost(self) -> RenderEntity:
        animators = {}
        for dir_i, dir in enumerate('EWNS'):
            frames = []
            # Frame loop
            for frame_i in range(2):
                w = self._SHEET_SPRITE_W
                h = self._SHEET_SPRITE_H
                x = (frame_i * w) + (dir_i * w * 2)
                y = h * (4 + self.__ghost_color)
                frames.append(self._sheet.crop_rect((x, y, w, h)))
            animators[dir] = Animator(frames, tick_rate=8)

        entity = RenderEntity(self._screen)
        entity.set_dir_animators(animators)
        return entity
