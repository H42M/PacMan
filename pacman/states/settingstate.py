from pacman.states.base_state import GameState
from typing import Optional
from pacman.states.base_state import StateManager
from pacman.render.Screen import Screen
from pacman.render.Container import Container
import pygame


class SettingsState(GameState):
    def __init__(self, screen: Screen,
                 state_manager: Optional[StateManager] = None
                 ) -> None:
        self.__screen = screen
        self.__menu_ctn = self.__load_settings()

    def handle_events(self, events) -> bool:
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
        return

    def render(self, screen) -> None:
        self.__screen.clear()
        self.__menu_ctn.render()
        self.__screen.flip()

    def __load_settings(self) -> Container:
        from pacman.render import RenderLoader
        from pacman.render.RenderText import RenderText
        from pacman.render.Divider import Divider
        from pacman.render.interactives import ToggleButton
        from pacman.render.interactives import SelectButton
        from pacman.render.interactives import Button

        container = Container(self.__screen, 'VERTICAL',
                              size=RenderLoader.screen_size,
                              pos=(0, 0),
                              padding=90)
        settings_ctn = Container(self.__screen, 'VERTICAL',
                                 bg_color=(0, 0, 0, 200))

        # TITLE:
        title_ctn = Container(self.__screen, 'VERTICAL')
        title_ctn.add_content([
            {RenderText(self.__screen, 'SETTINGS', font_size=40): '0%'},
            {Divider(self.__screen): '1%'}])

        # BUTTONS:
        btns_ctn = Container(self.__screen, 'VERTICAL')

        godmod_ctn = Container(self.__screen, 'HORIZONTAL')
        godmod_ctn.add_content([
            {RenderText(self.__screen, 'God mode: '): '50%'},
            {ToggleButton(self.__screen, 'Disabled'): '50%'},
        ])

        difficulty_ctn = Container(self.__screen, 'HORIZONTAL')
        difficulty_ctn.add_content([
            {RenderText(self.__screen, 'Difficulty: '): '50%'},
            {SelectButton(self.__screen, ['Easy', 'Normal', 'Hard']): '50%'},
        ])

        win_size_ctn = Container(self.__screen, 'HORIZONTAL')
        win_size_ctn.add_content([
            {RenderText(self.__screen, 'Window Size: '): '50%'},
            {ToggleButton(self.__screen, '800 x 800'): '50%'},
        ])
        btns_ctn.add_content([
                {godmod_ctn: '20%'},
                {difficulty_ctn: '20%'},
                {win_size_ctn: '20%'}
            ])

        # FOOTER
        footer_ctn = Container(self.__screen, 'HORIZONTAL')
        footer_ctn.add_content([
            {Button(self.__screen, 'SAVE CHANGES'): '45%'},
            {Button(self.__screen, 'CANCEL'): '45%'}
        ])

        settings_ctn.add_content([{title_ctn: '20%'}, {btns_ctn: '60%'},
                                  {footer_ctn: '10%'}])
        container.add_content({settings_ctn: '90%'})
        return container
