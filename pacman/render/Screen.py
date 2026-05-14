
from __future__ import annotations
from typing import TYPE_CHECKING

import pygame
from pacman.render.RenderLoader import GameLoader

if TYPE_CHECKING:
    from pacman.render.Window import Window
    from pacman.render.interactives.Button import Button


class Screen:
    """Manage screen, all pygame stuff, and player interactions."""
    def __init__(self) -> None:
        """Initialize Screen."""
        pygame.init()
        pygame.key.set_repeat(400, 40)

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
        """Reset screen."""
        if self.__background:
            self.__screen.blit(self.__background, (0, 0))
        else:
            self.__screen.fill((0, 0, 0))

    def flip(self) -> None:
        """Display all elements rendered on screen."""
        self.__clock.tick(60)
        if self.__menu.display:
            self.__menu.render()
        pygame.display.flip()

    def handle_events(self) -> bool:
        """Manage players events like key pressed or mouse pressed."""
        from pacman.render.interactives.Input import Input
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.__clickables:
                    if button.is_clicked(mouse_pos):
                        button.execute()
                    elif isinstance(button, Input):
                        button.focus = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__menu.switch_display()

                for button in self.__clickables:
                    if isinstance(button, Input):
                        button.handle_key(event)

        for button in self.__clickables:
            button.update_hover(mouse_pos)
        return True

    def record_clickable(self, obj: Button) -> None:
        """Add a clickable objet to the list"""
        if obj not in self.__clickables:
            self.__clickables.append(obj)

    def delete_clickable(self, obj: Button) -> None:
        """Remove a clickable object to the list"""
        if obj in self.__clickables:
            self.__clickables.remove(obj)

    def __load_menu(self) -> Window:
        """Generate an exemple of menu if needed"""
        from pacman.render.Container import Container
        from pacman.render.Window import Window
        from pacman.render.RenderText import RenderText
        from pacman.render.interactives.Button import Button
        from pacman.render.Divider import Divider
        from pacman.render.interactives.Input import Input

        # WINDOW MENU
        window_menu = Window(self, 'VERTICAL', (200, 200), (500, 500),
                             display_default=True, padding=20)
        title_ctn = Container(self, 'VERTICAL')
        title_ctn.add_content([{
            RenderText(self, "Menu", font_size=40): '20%'},
            {Divider(self): "1%"}])

        # INPUT CONTAINER
        input_area_ctn = Container(self, 'VERTICAL')

        input_ctn = Container(self, 'HORIZONTAL', )
        input_ctn.add_content([
            {Input(self, placeholder="Ex: Joueur_1"): '70%'},
            {Button(self, 'Enregistrer'): '25%'}
            ])
        input_area_ctn.add_content([
            {RenderText(self, 'Nom du joueur'): '0%'},
            {input_ctn: '0%'}
        ])

        # BTNS CONTAINER
        btn_ctn = Container(self, 'VERTICAL', gap=20)
        btn_ctn.add_content([
            {Button(self, 'UN BOUTON'): '0%'},
            {Button(self, "Encore un bouton"): '0%'},
            {input_area_ctn: '0%'},
            ])

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
