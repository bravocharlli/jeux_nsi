# Example file showing a circle moving on screen
from player import *
from carte import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# init
player = Player()


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill([125, 125, 125])

    """
    for i in range(cartey):
        for j in range(cartex):
            if carte[i][j] == 1:
                color = [255, 255, 255]
            else:
                color = [50, 50, 50]

            pygame.draw.rect(screen, color, [j * 64, i * 64, 63, 63])
    """

    player.update(dt)
    player.colision(dt)
    player.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
