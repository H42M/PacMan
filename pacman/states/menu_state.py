from pacman.states.base_state import GameState
from pacman.render.Container import Container
from pacman.render.RenderLoader import RenderLoader
from pacman.render.Screen import Screen
from typing import Optional

from pacman.states.base_state import StateManager


import pygame


class MenuState(GameState):
    def __init__(self, screen: Screen,
                 state_manager: Optional[StateManager] = None
                 ) -> None:
        self.__screen = screen
        self.__state_manager = state_manager
        self.__menu_ctn = self.__load_menu()

    def set_state_manager(self, manager: StateManager) -> None:
        """Permet de définir le StateManager après la création"""
        self.__state_manager = manager

    def handle_events(self, events: list[pygame.event.Event]) -> bool:
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                for clickable in self.__screen.clickables:
                    clickable.update_hover(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONDOWN:
                for clickable in self.__screen.clickables:
                    if clickable._is_hovered:
                        clickable.execute()

        return super().handle_events(events)

    def update(self) -> None:
        pass

    def render(self, screen: Screen) -> None:
        self.__screen.clear()
        if self.__menu_ctn is not None:
            self.__menu_ctn.render()
        self.__screen.flip()

    def __load_menu(self) -> Container:
        from pacman.render.RenderText import RenderText
        from pacman.render.Divider import Divider
        from pacman.render.interactives import Button

        container = Container(self.__screen, 'VERTICAL',
                              size=RenderLoader.screen_size,
                              pos=(0, 0),
                              padding=90)

        menu_ctn = Container(self.__screen, 'VERTICAL',
                             padding=50,
                             bg_color=(0, 0, 0, 230))

        title_ctn = Container(self.__screen, 'VERTICAL')
        title_ctn.add_content([{RenderText(self.__screen, 'PACMAN',
                                           font_color=(255, 255, 0),
                                           font_size=60): '0%'},
                               {Divider(self.__screen, (255, 255, 0)): '1%'}
                               ])
        # BUTTONS

        def on_play() -> None:
            if self.__state_manager:
                print('Starting game...')

        def on_settings() -> None:
            if self.__state_manager:
                print('Opening settings...')
                self.__state_manager.set_state('SETTINGS')

        def on_quit() -> None:
            import pygame
            pygame.quit()
            exit()

        btns_ctn = Container(self.__screen, 'VERTICAL', gap=30)
        btns_ctn.add_content([
            {Button(self.__screen, 'PLAY', callback=on_play): '0%'},
            {Button(self.__screen, 'SETTINGS',
                    callback=on_settings): '0%'},
            {Button(self.__screen, 'QUIT', callback=on_quit): '0%'},
        ])

        # FOOTER
        footer_ctn = Container(self.__screen, 'VERTICAL', gap=20)
        # TODO: Implement real max score
        max_score = 3025
        footer_info = Container(self.__screen, 'HORIZONTAL')
        footer_info.add_content([
            # {Divider(self.__screen): '1%'},
            {RenderText(self.__screen, 'Game made by ngaubil and hgeorges',
                        font_size=20):
             '0%'},
            {RenderText(self.__screen, f'Max score: {max_score}',
                        font_size=20): '0%'}
        ])
        footer_ctn.add_content([{Divider(self.__screen): '2%'},
                                {footer_info: '0%'}])

        menu_ctn.add_content([{title_ctn: '20%'}, {btns_ctn: '70%'},
                              {footer_ctn: '10%'}])
        container.add_content({menu_ctn: '90%'})
        return container
