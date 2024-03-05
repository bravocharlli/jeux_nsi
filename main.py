# Example file showing a circle moving on screen
import pygame

from player import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1200, 720))
clock = pygame.time.Clock()
running = True
state = 0
dt = 0

# init
player = Player()
font = pygame.font.SysFont("Arial", 18)
win = pygame.image.load('resource/win.png')
image = pygame.Surface((1200, 720)).convert_alpha()
image.blit(win, (0, 0), (0, 0, 248, 216))
image = pygame.transform.scale(image, (720, 1200))


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, True, pygame.Color("coral"))
    return fps_text

def interface(joueur):
    point = font.render(str(joueur.pv), True, pygame.Color("coral"))
    screen.blit(point, (10, 690))


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill([125, 125, 125])
    pygame.draw.rect(screen, [175, 175, 175], [0, 360, 1200, 360])

    match state:
        case 0:
           player.draw(screen)
        case 1:
            player.update(dt)
            player.draw(screen)
            # affichage fps
            screen.blit(update_fps(), (10, 0))
            interface(player)
        case 2:
            screen.blit(image, (0, 0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        state = 1
    if keys[pygame.K_ESCAPE]:
        state = 0
    if player.pv == -33:
        state = 2
    if player.pv == 0:
        state = 2

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
