from render.GameLoader import GameLoader

from render.Screen import Screen
from render.RenderMaze import RenderMaze
from render.buttons.Button import Button
from render.Entity import Entity


if __name__ == "__main__":
    try:

        GameLoader.init((800, 800), (15, 15))
        GameLoader.load_asset('pacman', 'assets/sprites/pacman.png')

        screen = Screen()
        maze = RenderMaze(screen)
        button = Button(screen, 'Un Bouton', (0, 0), (100, 100))
        pacman = Entity(screen, (100, 100), (50, 50))
        pacman.set_skin(GameLoader.get_asset('pacman'))
    except Exception as e:
        print(f'Error: {e}')
        exit()
    while screen.handle_events():
        maze.render()
        screen.flip()
        pacman.render()
        # button.render()
