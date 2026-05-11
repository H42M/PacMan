from render.GameLoader import GameLoader

from render.Screen import Screen
from render.RenderMaze import RenderMaze
from render.buttons.Button import Button
from render.Entity import Entity


if __name__ == "__main__":
    try:

        GameLoader.init((800, 800), (15, 15))
        GameLoader.load_asset('pacman', 'assets/sprites/pacman.png')
        GameLoader.load_asset('ghost-blue',
                              'assets/sprites/ghost-blue.png')

        screen = Screen()
        maze = RenderMaze(screen)
        button = Button(screen, 'Un Bouton', (0, 0), (100, 100))

        pacman = Entity(screen, (100, 100), GameLoader.cell_size)
        pacman.set_skin(GameLoader.get_asset('pacman'))
        ghost = Entity(screen, (300, 300), GameLoader.cell_size)
        ghost.set_skin(GameLoader.get_asset('ghost-blue'))
    except Exception as e:
        print(f'Error: {e}')
        exit()
    while screen.handle_events():
        screen.clear()
        ghost.x = (ghost.x + 1 if ghost.x is not None and
                   ghost.x <= GameLoader.screen_size[0] else 1)
        print(f'ghost.x: {ghost.x}, width: {GameLoader.screen_size[0]}')
        pacman.set_rotation('W')
        maze.render()
        pacman.render()
        ghost.render()
        button.render()

        screen.flip()
