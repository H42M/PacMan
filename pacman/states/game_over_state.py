from pygame.event import Event

from pacman.render.Screen import Screen
from pacman.states.base_state import ScreenState, StateManager
from pacman.render.Container import Container
from pacman.highscores import add_highscore, load_highscores, save_highscores
from pacman.render.animation.AnimGhost import AnimGhost


class GameOverState(ScreenState):
    LOOSE_SCREEN = 'LOOSE_SCEEN'
    WIN_SCREEN = 'WIN_SCREEN'

    def __init__(
        self,
        screen: Screen,
        state_manager: StateManager | None = None,
        win_or_lose: str = LOOSE_SCREEN,
        final_score: int = 0,
        highscore_path: str = "highscores.json",
    ) -> None:
        super().__init__(screen, state_manager)
        self.__win_or_loose = win_or_lose
        self.__final_score = final_score
        self.__highscore_path = highscore_path
        self.__player_name = ""
        self.__ghosts = self.__init_ghosts()
        self.__game_over_ctn = self.__load_game_over_ctn()

        self.__ghost_speed = 20
        self.__ghost_dir = 1

    def __init_ghosts(self) -> list[AnimGhost]:
        ghosts: list[AnimGhost] = []
        for i in range(4):
            ghost = AnimGhost(self._screen, i)
            cell = (50, 50)
            ghost.size = cell
            pos = ((-300 + ((i * cell[0]) + 60 * i), 100))
            ghost.set_target_pos(pos)
            ghosts.append(ghost)
        return ghosts

    def save_and_quit(self) -> None:
        if not self._state_manager:
            return

        try:
            highscores = load_highscores(self.__highscore_path)
            highscores = add_highscore(
                highscores,
                self.__player_name,
                self.__final_score,
            )
            save_highscores(self.__highscore_path, highscores)
        except ValueError as e:
            print(e)
            return

        self._state_manager.set_state(StateManager.MENU)

    def __load_game_over_ctn(self) -> Container:
        from pacman.render.RenderConfig import RenderConfig
        from pacman.render.Container import Container
        from pacman.render.RenderText import RenderText
        from pacman.render.interactives import Input, ToggleButton, Button
        from pacman.render.Divider import Divider

        game_over_header = Container(self._screen, 'VERTICAL', gap=15)
        game_over_header.add_content([
            {RenderText(self._screen,
                        'You Win' if self.__win_or_loose == self.WIN_SCREEN
                        else 'Game Over',
                        font_size=50,
                        font_color=RenderConfig.YELLOW,
                        font_family=RenderConfig.FONT): '40%'},
            {RenderText(
                self._screen, f'Your Score: {self.__final_score}',
                font_size=15,
                font_color=RenderConfig.YELLOW): '0%'},
            {Divider(self._screen): '1%'}
        ])
        input_name_ctn = Container(self._screen, 'HORIZONTAL')
        input_name = Input(self._screen, 'ex: PacMan',
                           base_color=RenderConfig.RED,
                           focus_color=(255, 50, 50))

        input_name_ctn.add_content([
            {RenderText(self._screen, 'Player name: ',
                        font_size=18): '20%'},
            {input_name: '50%'},
        ])
        game_over_ctn = Container(self._screen, 'VERTICAL',
                                  padding=30,
                                  gap=30)

        def save_and_quit() -> None:
            self.__player_name = input_name.value
            self.save_and_quit()

        def quit() -> None:
            if self._state_manager:
                self._state_manager.set_state(StateManager.MENU)

        btns_ctn = Container(self._screen, 'HORIZONTAL', gap=20)
        btns_ctn.add_content([
            {ToggleButton(self._screen, 'SAVE AND QUIT',
                          color_on=RenderConfig.RED,
                          color_off=RenderConfig.GREY,
                          state_callback=input_name.get_value,
                          callback=save_and_quit): '45%'},
            {Button(self._screen, 'QUIT',
                    callback=quit,
                    color=RenderConfig.RED
                    ): '45%'},
        ])

        game_over_ctn.add_content([
            {game_over_header: '25%'},
            {input_name_ctn: '15%'},
            {btns_ctn: '10%'}
        ])
        window_ctn = Container(self._screen, 'VERTICAL',
                               size=RenderConfig.screen_size,
                               pos=(0, 0),
                               bg_color=RenderConfig.BLACK)
        window_ctn.add_content({game_over_ctn: '60%'})
        return window_ctn

    def render(self) -> None:
        self._screen.clear()
        self.__game_over_ctn.render()
        for ghost in self.__ghosts:
            ghost.render()
        self._screen.flip()

    def ghosts_out_window(self) -> bool:
        from pacman.render.RenderConfig import RenderConfig
        for ghost in self.__ghosts:
            if ghost.pos:
                if (0 < ghost.pos[0] < RenderConfig.screen_size[0]):
                    return False
        return True

    def update(self) -> None:
        from pacman.render.RenderConfig import RenderConfig
        from pacman.player import Direction
        screen_w, screen_h = RenderConfig.screen_size
        for _, ghost in enumerate(self.__ghosts):
            if ghost.pos and ghost.size:
                x, y = ghost.pos
                ghost_dir = ghost.direction.upper()
                if ghost_dir == 'E' and x > screen_w + 10:
                    ghost.set_rotation(Direction.LEFT)
                    x = screen_w + 10
                    y += 100
                    ghost.pos = (x, y)
                elif ghost_dir == 'W' and x < -10 - ghost.size[0]:
                    ghost.set_rotation(Direction.RIGHT)
                    x = -10 - ghost.size[0]
                    y -= 100
                    ghost.pos = (x, y)
                ghost_dir = ghost.direction.upper()

                print(y)
                if ghost_dir == 'E':
                    ghost.set_target_pos((x + (self.__ghost_dir *
                                               self.__ghost_speed), y))
                elif ghost_dir == 'W':
                    ghost.set_target_pos((x + (-1 * self.__ghost_speed), y))

            ghost.tick()

    def handle_events(self, events: list[Event]) -> bool:
        return super().handle_events(events)
