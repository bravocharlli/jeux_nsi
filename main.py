# Example file showing a circle moving on screen
import pygame

from player import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1200, 720))
clock = pygame.time.Clock()
running = True
etat = 0
dt = 0

# init
player = Player()
font = pygame.font.SysFont("Arial", 18)


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, True, pygame.Color("coral"))
    return fps_text


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill([125, 125, 125])
    pygame.draw.rect(screen, [175, 175, 175], [0, 360, 1200, 360])

    match etat:
        case 0:
            player.draw(screen)
        case 1:
            player.update(dt)
            player.draw(screen)
            # affichage fps
            screen.blit(update_fps(), (10, 0))
        case 2:
            pass

    # flip() the display to put your work on screen
    pygame.display.flip()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        etat = 1
    if keys[pygame.K_ESCAPE]:
        etat = 0

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
