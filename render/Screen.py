
import pygame


class Screen:
    def __init__(self, size: tuple[int, int]) -> None:
        pygame.init()
        self.__screen_size = size
        self.__screen_name = 'PACMAN'
        self.__screen = pygame.display.set_mode(
            self.__screen_size
        )
        self.__clock = pygame.time.Clock()
        pygame.display.set_caption(self.__screen_name)
        self.__background = None

    def clear(self) -> None:
        if self.__background:
            self.__screen.blit(self.__background, (0, 0))
        else:
            self.__screen.fill((0, 0, 0))

    def flip(self) -> None:
        self.__clock.tick(360)
        pygame.display.flip()

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
