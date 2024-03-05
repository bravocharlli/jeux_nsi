# Example file showing a circle moving on screen
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
image = pygame.transform.scale(image, (1200, 720))


# declaration fonction
def update_fps():
    """
    Renvois le nombre de FPS
    :return:
    """
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, True, pygame.Color("coral"))
    return fps_text


def interface(joueur):
    """
    Affiche le nombre de PV
    :param joueur: Class de player.py
    :return:
    """
    point = font.render(str(joueur.pv), True, pygame.Color("coral"))
    screen.blit(point, (10, 690))


# boucle principale
while running:
    # pour pouvoir fermer la fenêtre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # dessin du fond
    screen.fill([125, 125, 125])
    pygame.draw.rect(screen, [175, 175, 175], [0, 360, 1200, 360])

    # boucle en fonction de l'état
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

    # tout afficher à l'écran
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

    # limite les FPS à 60
    dt = clock.tick(60) / 1000

pygame.quit()
