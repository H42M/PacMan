from pacman.render.interactives import Button
from pacman.render.Screen import Screen
from typing import Optional, Union, Callable, Any


class SelectButton(Button):
    def __init__(self, screen: Screen,
                 options: list[str],
                 pos: tuple[int, int] | None = None,
                 size: tuple[int, int] | None = None,
                 color: tuple[int, int, int] | None = None,
                 callback: Optional[Union[Callable[..., Any],
                                          list[Callable[..., Any]]]] = None
                 ) -> None:
        super().__init__(screen, options[0], pos, size, color, callback)
        self.__options = options
        self.__index = 0

        # Créer les arrows une seule fois
        arrow_size = (30, size[1]) if size else (30, 30)
        self.__left_btn = Button(screen, '<',
                                 size=arrow_size,
                                 callback=self.__left_option)
        self.__right_btn = Button(screen, '>',
                                  size=arrow_size,
                                  callback=self.__right_option)

    def __left_option(self):
        self.__index = (self.__index - 1) % len(self.__options)
        self._text = self.__options[self.__index]

    def __right_option(self):
        self.__index = (self.__index + 1) % len(self.__options)
        self._text = self.__options[self.__index]

    def render(self) -> None:
        super().render()
        if self._pos and self._size:
            arrow_w = self.__left_btn.w or 30
            arrow_h = self._size[1]

            self.__left_btn.size = (arrow_w, arrow_h)
            self.__left_btn.pos = (self._pos[0] - arrow_w, self._pos[1])

            self.__right_btn.size = (arrow_w, arrow_h)
            self.__right_btn.pos = (self._pos[0] + self._size[0], self._pos[1])

            self.__left_btn.render()
            self.__right_btn.render()

    @property
    def value(self) -> str:
        """Retourne l'option actuellement sélectionnée"""
        return self.__options[self.__index]