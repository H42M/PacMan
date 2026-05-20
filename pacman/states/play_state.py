from pygame.event import Event
# from pacman.game_config import GameConfig
from pacman.render.Screen import Screen
from pacman.render.RenderConfig import RenderConfig
from pacman.states.base_state import GameState, StateManager
from typing import Optional
from pacman.render.RenderMaze import RenderMaze
from pacman.render.Container import Container
from pacman.render.Window import Window
import pygame


class PlayState(GameState):
    def __init__(self, screen: Screen,
                 state_manager: Optional[StateManager] = None
                 ) -> None:
        super().__init__(screen, state_manager)

        # TODO: Define real maze size with GameConfig
        self.__maze = RenderMaze(screen, (300, 300))
        self.__game_ctn = self.__load_game_ctn()
        self.__menu_ctn = self.__load_menu()
        self.__menu_displayed = False

    def render(self) -> None:
        self._screen.clear()
        self.__game_ctn.render()
        self.__menu_ctn.render()
        self._screen.flip()

    def handle_events(self, events: list[Event]) -> bool:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__menu_ctn.switch_display()
                    print(f'Display Menu {self.__menu_displayed}')
        return super().handle_events(events)

    def update(self) -> None:
        pass

    def __load_game_ctn(self) -> Container:
        game_win_ctn = Container(self._screen, 'VERTICAL',
                                 (0, 0), padding=20,
                                 size=RenderConfig.screen_size)
        game_ctn = Container(self._screen, 'VERTICAL', bg_color=(0, 0, 0, 230))
        game_ctn.add_content({self.__maze: '90%'})

        game_win_ctn.add_content({game_ctn: '0%'})
        return game_win_ctn

    def __load_menu(self) -> Window:
        # TODO: Menu shouldnt be defined here
        """Generate an exemple of menu if needed"""
        from pacman.render.Container import Container
        from pacman.render.Window import Window
        from pacman.render.RenderText import RenderText
        from pacman.render.interactives.Button import Button
        from pacman.render.Divider import Divider
        from pacman.render.interactives.Input import Input

        # WINDOW MENU
        window_menu = Window(self._screen, 'VERTICAL', (200, 200), (500, 500),
                             display_default=True, padding=20)
        title_ctn = Container(self._screen, 'VERTICAL')
        title_ctn.add_content([{
            RenderText(self._screen, "Menu", font_size=40): '20%'},
            {Divider(self._screen): "1%"}])

        # INPUT CONTAINER
        input_ctn = Container(self._screen, 'HORIZONTAL', )
        input_ctn.add_content([
            {RenderText(self._screen, 'Player name'): '40%'},
            {Input(self._screen, placeholder="Ex: player_1"): '60%'},
            ])

        def on_quit():
            if self._state_manager:
                self._state_manager.set_state('MENU')

        save_quit_ctn = Container(self._screen, 'HORIZONTAL', gap=20)
        save_quit_ctn.add_content([
            {Button(self._screen, 'Save changes'): '0%'},
            {Button(self._screen, 'Quit', callback=on_quit): '0%'},
        ])

        sett_area_ctn = Container(self._screen, 'VERTICAL')
        sett_area_ctn.add_content([
            {input_ctn: '30%'},
            {Button(self._screen, 'Restart'): '30%'}
            ])

        # BTNS CONTAINER
        btn_ctn = Container(self._screen, 'VERTICAL', padding=3, gap=10)
        btn_ctn.add_content([
            {sett_area_ctn: '60%'},
            {Divider(self._screen): '1%'},
            {save_quit_ctn: '30%'}
            ])

        window_menu.add_content([
            {title_ctn: '30%'},
            {btn_ctn: '70%'},
            ])

        return window_menu
