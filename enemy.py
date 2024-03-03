import pygame
import texture
import math


class Object:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        sprite = pygame.image.load('resource/murs_en_mousse.png').convert_alpha()
        self.texture = texture.Object(sprite)

    def draw(self, screen, param, ppos, pang):
        # get angle
        angle = math.atan2(ppos.y-self.pos.y, ppos.x-self.pos.x)
        diff = pang - angle

        diff = correction_ang(diff)

        if abs(diff) > math.pi/2:
            render = True
        else:
            render = False

        if render:
            screen_x = 0.5 * 1200 * (1-(math.tan(diff)/math.tan(math.pi/6)))

            # get distance
            distance = dist(self.pos.x, self.pos.y, ppos.x, ppos.y)
            taille = ((64 * 720) / distance)

            texture = self.texture.get_image(taille, 1)
            screen.blit(texture, (screen_x-taille/2, 360-taille/2))


def dist(sx, sy, ex, ey):
    return math.sqrt((ex - sx) ** 2 + (ey - sy) ** 2)


def correction_ang(ang):
    if ang < -math.pi:
        ang += 2 * math.pi
    if ang > math.pi:
        ang -= 2 * math.pi
    return ang
