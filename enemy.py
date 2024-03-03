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
        sx = self.pos.x - ppos.x
        sy = self.pos.y - ppos.y
        sz = 0
        CS = math.cos(pang)
        SN = math.sin(pang)
        a = sy*CS+sx*SN
        b = sx*CS-sy*SN
        sx = a
        sy = b
        sx = (sx*(180/sy))+1200/2
        sy = (sz*(180/sy))+720/2

        # get distance
        distance = dist(self.pos.x, self.pos.y, ppos.x, ppos.y)
        taille = 1/(distance * math.tan(math.pi/6)) * 720

        texture = self.texture.get_image(100, 1)
        screen.blit(texture, (sx, sy))

def dist(sx, sy, ex, ey):
    return math.sqrt((ex - sx) ** 2 + (ey - sy) ** 2)
