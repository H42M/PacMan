from pacman.states.base_state import GameState
from pacman.render.Container import Container
from pacman.render.RenderConfig import RenderConfig
from pacman.render.Screen import Screen
from typing import Optional

from pacman.states.base_state import StateManager


import pygame


class MenuState(GameState):
    def __init__(self, screen: Screen,
                 state_manager: Optional[StateManager] = None
                 ) -> None:
        super().__init__(screen, state_manager)
        self.__menu_ctn = self.__load_menu()

    def handle_events(self, events: list[pygame.event.Event]) -> bool:
        return super().handle_events(events)

    def update(self) -> None:
        # return super().update()
        pass

    def render(self) -> None:
        self._screen.clear()
        if self.__menu_ctn is not None:
            self.__menu_ctn.render()
        self._screen.flip()

    def __load_menu(self) -> Container:
        from pacman.render.RenderText import RenderText
        from pacman.render.Divider import Divider
        from pacman.render.interactives import Button

        container = Container(self._screen, 'VERTICAL',
                              size=RenderConfig.screen_size,
                              pos=(0, 0),
                              padding=130)

        menu_ctn = Container(self._screen, 'VERTICAL',
                             padding=50,
                             bg_color=(0, 0, 0, RenderConfig.menu_opacity))

        title_ctn = Container(self._screen, 'VERTICAL')
        title_ctn.add_content([{RenderText(self._screen, 'PACMAN',
                                           font_color=(255, 255, 0),
                                           font_size=60): '0%'},
                               {Divider(self._screen, (255, 255, 0)): '1%'}
                               ])
        # BUTTONS

        def on_play() -> None:
            if self._state_manager:
                print('Starting game...')
                self._state_manager.set_state('PLAYING')

        def on_settings() -> None:
            if self._state_manager:
                print('Opening settings...')
                self._state_manager.set_state('SETTINGS')

        def on_quit() -> None:
            import pygame
            pygame.quit()
            exit()

        btns_ctn = Container(self._screen, 'VERTICAL', gap=30)
        btns_ctn.add_content([
            {Button(self._screen, 'PLAY', callback=on_play): '0%'},
            {Button(self._screen, 'SETTINGS',
                    callback=on_settings): '0%'},
            {Button(self._screen, 'QUIT', callback=on_quit): '0%'},
        ])

        # FOOTER
        footer_ctn = Container(self._screen, 'VERTICAL', gap=20)
        # TODO: Implement real max score
        max_score = 3025
        footer_info = Container(self._screen, 'HORIZONTAL')
        footer_info.add_content([
            # {Divider(self.__screen): '1%'},
            {RenderText(self._screen, 'Game made by ngaubil and hgeorges',
                        font_size=20):
             '0%'},
            {RenderText(self._screen, f'Max score: {max_score}',
                        font_size=20): '0%'}
        ])
        footer_ctn.add_content([{Divider(self._screen): '2%'},
                                {footer_info: '0%'}])

        menu_ctn.add_content([{title_ctn: '20%'}, {btns_ctn: '70%'},
                              {footer_ctn: '10%'}])
        container.add_content({menu_ctn: '90%'})
        return container
