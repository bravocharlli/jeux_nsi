import pygame
import texture
import math


class Object:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        sprite = pygame.image.load('resource/murs_en_mousse.png').convert_alpha()
        self.texture = texture.Object(sprite)

    def draw(self, screen, param, ppos, pang):
        dy = ppos.y-self.pos.y
        dx = ppos.x-self.pos.x
        # get angle
        angle = math.atan(dy/dx)
        diff = pang - angle

        if diff < 0:
            diff += 2 * math.pi
        elif diff > 2 * math.pi:
            diff -= 2 * math.pi

        if diff < 0:
            render = False
        else:
            render = True

        print(diff)


        if True:
            screen_x = 0.5 * 1200 * (1-(math.tan(diff)/math.tan(math.pi/6)))

            # get distance
            distance = dist(self.pos.x, self.pos.y, ppos.x, ppos.y)
            taille = ((64 * 720) / distance)

            texture = self.texture.get_image(taille, 1)
            screen.blit(texture, (screen_x-taille/2, 360-taille/2))


def dist(sx, sy, ex, ey):
    return math.sqrt((ex - sx) ** 2 + (ey - sy) ** 2)
