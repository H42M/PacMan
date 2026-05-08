from render.Screen import Screen

if __name__ == "__main__":
    screen = Screen((800, 800))

    while screen.handle_events():
        screen.flip()
