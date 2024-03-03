import pygame
import texture
import math


class Object:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        sprite = pygame.image.load('resource/murs.png').convert_alpha()
        self.texture = texture.Object(sprite)

    def draw(self, screen, param, ppos, pang):
        # get angle


        # get distance
        distance = dist(self.pos.x, self.pos.y, ppos.x, ppos.y)
        taille = 1/(distance * math.tan(math.pi/6)) * 720

        texture = self.texture.get_image(taille, 1)
        screen.blit(texture, (100, 100))

def dist(sx, sy, ex, ey):
    return math.sqrt((ex - sx) ** 2 + (ey - sy) ** 2)
