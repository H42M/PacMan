from pacman.states.base_state import GameState
from pacman.render.Container import Container
from pacman.render.RenderLoader import RenderLoader
from pacman.render.Screen import Screen


import pygame


class MenuState(GameState):
    def __init__(self, screen: Screen) -> None:
        self.__screen = screen
        self.__menu_ctn = self.__load_menu()

    def handle_events(self, events: list[pygame.event.Event]) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEMOTION:
                for clickable in self.__screen.clickables:
                    clickable.update_hover(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONDOWN:
                for clickable in self.__screen.clickables:
                    if clickable._is_hovered:
                        clickable.execute()

        return True

    def update(self) -> None:
        pass

    def render(self, screen):
        self.__screen.clear()
        if self.__menu_ctn is not None:
            self.__menu_ctn.render()
        self.__screen.flip()

    def __load_menu(self):
        from pacman.render.RenderText import RenderText
        from pacman.render.Divider import Divider
        from pacman.render.interactives import Button

        menu_ctn = Container(self.__screen, 'VERTICAL',
                             size=RenderLoader.screen_size,
                             pos=(0, 0),
                             padding=100,
                             bg_color=(0, 0, 0, 200))
        menu_ctn.padding_in_bg = False

        title_ctn = Container(self.__screen, 'VERTICAL')
        title_ctn.add_content([{RenderText(self.__screen, 'PACMAN',
                                           font_color=(255, 255, 0),
                                           font_size=60): '0%'},
                               {Divider(self.__screen, (255, 255, 0)): '1%'}
                               ])
        # BUTTONS

        def print_something():
            print('Button clicked')

        btns_ctn = Container(self.__screen, 'VERTICAL', gap=50)
        btns_ctn.add_content([
            {Button(self.__screen, 'PLAY', callback=print_something): '0%'},
            {Button(self.__screen, 'SETTINGS',
                    callback=print_something): '0%'},
            {Button(self.__screen, 'QUIT', callback=print_something): '0%'},
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
        return menu_ctn
