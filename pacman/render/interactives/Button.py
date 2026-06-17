from pacman.render.RenderObj import RenderOBJ
from pacman.render.RenderConfig import RenderConfig
from pacman.render.Screen import Screen
import pygame

from typing import Optional, Union, Callable, Any


class Button(RenderOBJ):
    """Render an interactive button."""

    BORDER_RADIUS = 8
    BORDER_WIDTH = 2
    # DEFAULT_COLOR = (100, 150, 200)
    DEFAULT_COLOR = (255, 0, 0)

    SHADOW_COLOR = (40, 40, 40)
    HOVER_BRIGHTNESS = 40
    BORDER_DARKEN = 80

    def __init__(
        self,
        screen: Screen,
        text: str,
        pos: Optional[tuple[int, int]] = None,
        size: Optional[tuple[int, int]] = None,
        color: Optional[tuple[int, int, int]] = None,
        callback: Optional[Union[Callable[..., Any],
                                 list[Callable[..., Any]]]] = None,
        font_family: Optional[str] = RenderConfig.FONT,
        font_size: int = 28
    ) -> None:
        """Initialize the button."""
        super().__init__(screen, size=size, pos=pos)
        self._color = color

        self._text = text
        self._callback = callback
        self._is_hovered = False
        self._hover_color: tuple[int, int, int] | None = None
        self._font = pygame.font.Font(font_family, font_size)
        self._text_color = (255, 255, 255)
        if self._pos and self._size:
            self._surface = pygame.Surface(self._size)
        else:
            self._surface = None
        screen.record_clickable(self)

    # ------------------------------------------------------------------ #
    #  Helpers partagés                                                    #
    # ------------------------------------------------------------------ #

    def _brighten(self, color: tuple[int, int, int], amount: int
                  ) -> tuple[int, int, int]:
        """Return a brighter RGB color."""
        r, g, b = color
        return (min(255, r + amount), min(255, g + amount),
                min(255, b + amount))

    def _darken(self, color: tuple[int, int, int], amount: int
                ) -> tuple[int, int, int]:
        """Return a darker RGB color."""
        r, g, b = color
        return (max(0, r - amount), max(0, g - amount), max(0, b - amount))

    def _apply_hover(self, color: tuple[int, int, int]
                     ) -> tuple[int, int, int]:
        """Apply the hover effect to a color."""
        return (self._brighten(color, self.HOVER_BRIGHTNESS)
                if self._is_hovered else color)

    def _get_border_color(self, base_color: tuple[int, int, int]
                          ) -> tuple[int, int, int]:
        """Return the button border color."""
        return self._darken(base_color, self.BORDER_DARKEN)

    def _draw_shadow(self, screen: pygame.Surface) -> None:
        """Draw the button shadow."""
        if self._size and self._pos:
            offset = 4 if self._is_hovered else 2
            pygame.draw.rect(
                screen,
                self.SHADOW_COLOR,
                (int(self._pos[0]) + offset, int(self._pos[1]) + offset,
                 *self._size),
                border_radius=self.BORDER_RADIUS,
            )

    def _draw_rounded_rect(
        self,
        surface: pygame.Surface,
        fill_color: tuple[int, int, int],
        border_color: tuple[int, int, int],
    ) -> None:
        """Draw the button body."""
        if self._size and self._pos:
            rect = (0, 0, *self._size)

            pygame.draw.rect(surface, fill_color, rect,
                             border_radius=self.BORDER_RADIUS)
            pygame.draw.rect(
                surface, border_color, rect, self.BORDER_WIDTH,
                border_radius=self.BORDER_RADIUS
            )

    def _blit_centered_text(
        self,
        surface: pygame.Surface,
        text: str,
        font: pygame.font.Font | None = None,
    ) -> None:
        """Draw centered text."""
        if self._size and self._pos:
            font = font or self._font
            text_surf = font.render(text, True, self._text_color)
            surface.blit(
                text_surf,
                text_surf.get_rect(center=(self._size[0] // 2,
                                           self._size[1] // 2)),
            )

    def _resolve_color(self) -> tuple[int, int, int]:
        """Return the current button color."""
        base = (self._hover_color if self._is_hovered and self._hover_color
                else self._color)
        if not base:
            base = (255, 0, 0)
        return self._apply_hover(base)

    def _blit_to_screen(self, screen: pygame.Surface) -> None:
        """Blit the button surface to the screen."""
        if self._surface and self._pos:
            screen.blit(self._surface, (int(self._pos[0]), int(self._pos[1])))

    # ------------------------------------------------------------------ #
    #  Rendu                                                               #
    # ------------------------------------------------------------------ #

    def render(self) -> None:
        """Render the button."""
        if not self._size or not self._pos:
            return

        if not self._surface or self._surface.get_size() != self._size:
            self._surface = pygame.Surface(self._size)

        color = self._resolve_color()
        self._draw_shadow(self._screen.screen)
        self._draw_rounded_rect(self._surface, color,
                                self._get_border_color(color))
        self._blit_centered_text(self._surface, self._text)
        self._blit_to_screen(self._screen.screen)

    # ------------------------------------------------------------------ #
    #  Interactions                                                        #
    # ------------------------------------------------------------------ #

    def _get_rect(self) -> Optional[pygame.Rect]:
        """Return the button bounds."""
        if self._size and self._pos:
            return pygame.Rect(int(self._pos[0]),
                               int(self._pos[1]), *self._size)
        return None

    def is_clicked(self, mouse_pos: tuple[int, int]) -> Optional[bool]:
        """Return whether the mouse position clicks the button."""
        rect = self._get_rect()
        if rect:
            return rect.collidepoint(mouse_pos)
        return None

    def update_hover(self, mouse_pos: tuple[int, int]) -> None:
        """Update the hover state."""
        rect = self._get_rect()
        if rect:
            self._is_hovered = rect.collidepoint(mouse_pos)

    def execute(self) -> None:
        """Run the button callback."""
        if not self._callback:
            return
        callbacks = (self._callback if isinstance(self._callback, list)
                     else [self._callback])
        for cb in callbacks:
            cb()

    # ------------------------------------------------------------------ #
    #  Setters                                                             #
    # ------------------------------------------------------------------ #

    def set_callback(self, callback: Callable[..., Any]) -> None:
        """Set the button callback."""
        self._callback = callback

    def set_hover_color(self, color: tuple[int, int, int]) -> None:
        """Set the hover color."""
        self._hover_color = color

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

    @property
    def size(self) -> Optional[tuple[int, int]]:
        return self._size

    @size.setter
    def size(self, value: Optional[tuple[int, int]]) -> None:
        if value:
            self._size = value

    @property
    def w(self) -> Optional[int]:
        if self._size:
            return self._size[0]
        return None

    @w.setter
    def w(self, value: Optional[int]) -> None:
        if value:
            if self._size:
                self._size = (value, self._size[1])
            else:
                self._size = (value, 0)

    @property
    def h(self) -> Optional[int]:
        if self._size:
            return self._size[1]
        return None

    @h.setter
    def h(self, value: Optional[int]) -> None:
        if value:
            if self._size:
                self._size = (self._size[0], value)
            else:
                self._size = (0, value)

    @property
    def is_hovered(self) -> bool:
        return self._is_hovered

    @is_hovered.setter
    def is_hovered(self, value: bool) -> None:
        self._is_hovered = value
