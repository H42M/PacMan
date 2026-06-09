from pacman.render.interactives.Button import Button
from pacman.render.Screen import Screen

from typing import Optional, Callable, Union, Any


class ToggleButton(Button):
    """Standar Button which color based on an variable state."""
    def __init__(
        self,
        screen: Screen,
        text: str,
        pos: Optional[tuple[int, int]] = None,
        size: Optional[tuple[int, int]] = None,
        color_on: Optional[tuple[int, int, int]] = None,
        color_off: Optional[tuple[int, int, int]] = None,
        callback: Optional[Union[Callable[..., Any],
                                 list[Callable[..., Any]]]] = None,
        state_callback: Optional[Callable[..., Any]] = None,
    ) -> None:
        """Initialize Toggle Button."""
        super().__init__(screen, text, pos, size, color=color_on,
                         callback=callback)
        self.__color_on = color_on if color_on else (0, 255, 0)
        self.__color_off = color_off if color_off else (255, 0, 0)
        self.__state_callback = state_callback

    def render(self) -> None:
        """Display button on screen."""
        if self.__state_callback and self.__state_callback():
            self._color = self.__color_on
        else:
            self._color = self.__color_off
        super().render()

    def execute(self) -> None:
        if self._color == self.__color_on:
            return super().execute()
