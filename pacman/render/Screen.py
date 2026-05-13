
from __future__ import annotations
from typing import TYPE_CHECKING

import pygame
from pacman.render.GameLoader import GameLoader

if TYPE_CHECKING:
    from pacman.render.Window import Window
    from pacman.render.interactives.Button import Button


class Screen:
    def __init__(self) -> None:
        pygame.init()
        self.__screen_size = GameLoader.screen_size
        self.__screen_name = 'PACMAN'
        self.__screen = pygame.display.set_mode(
            self.__screen_size
        )
        self.__clock = pygame.time.Clock()
        pygame.display.set_caption(self.__screen_name)
        self.__background = None
        self.__clickables: list[Button] = []
        self.__menu = self.__load_menu()

    def clear(self) -> None:
        if self.__background:
            self.__screen.blit(self.__background, (0, 0))
        else:
            self.__screen.fill((0, 0, 0))

    def flip(self) -> None:
        self.__clock.tick(60)
        if self.__menu.display:
            self.__menu.render()
        pygame.display.flip()

    def handle_events(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.__clickables:
                    if button.is_clicked(mouse_pos):
                        button.execute()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__menu.switch_display()

        for button in self.__clickables:
            button.update_hover(mouse_pos)
        return True

    def record_clickable(self, obj: Button) -> None:
        if obj not in self.__clickables:
            self.__clickables.append(obj)

    def delete_clickable(self, obj: Button) -> None:
        if obj in self.__clickables:
            self.__clickables.remove(obj)

    def __load_menu(self) -> Window:
        from pacman.render.Container import Container
        from pacman.render.Window import Window
        from pacman.render.RenderText import RenderText
        from pacman.render.interactives.Button import Button
        from pacman.render.Divider import Divider

        # WINDOW MENU
        window_menu = Window(self, 'VERTICAL', (200, 200), (500, 500),
                             display_default=True, padding=20)
        title_ctn = Container(self, 'VERTICAL')
        title_ctn.add_content([{
            RenderText(self, "Menu", font_size=40): '20%'},
            {Divider(self): "1%"}])

        btn_ctn = Container(self, 'VERTICAL', gap=20)
        btn_ctn.add_content([
            {Button(self, 'UN BOUTON'): '0%'},
            {Button(self, "Encore un bouton"): '0%'}])

        window_menu.add_content([
            {title_ctn: '30%'},
            {btn_ctn: '70%'},])

        return window_menu

    # GETTERS / SETTERS

    @property
    def screen(self) -> pygame.Surface:
        return self.__screen

    @screen.setter
    def screen(self, value: pygame.Surface) -> None:
        self.__screen = value

    @property
    def menu(self) -> Window:
        return self.__menu

    @menu.setter
    def menu(self, value: Window) -> None:
        self.__menu = value
