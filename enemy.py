import pygame
import texture
import math


class Object:
    def __init__(self, x, y, path):
        self.pos = pygame.Vector2(x, y)
        sprite = pygame.image.load(path).convert_alpha()
        self.texture = texture.Object(sprite)

    def draw(self, screen, param, ppos, pang):
        # get angle
        angle = math.atan2(ppos.y - self.pos.y, ppos.x - self.pos.x)
        diff = pang - angle

        diff = correction_ang(diff)

        if abs(diff) > math.pi / 2:
            render = True
        else:
            render = False

        if render:
            screen_x = 0.5 * 1200 * (1 - (math.tan(diff) / math.tan(math.pi / 6)))

            if 0 < screen_x < 1200:
                # get distance
                distance = dist(self.pos.x, self.pos.y, ppos.x, ppos.y)

                if (param[1200 - int(screen_x) - 1][4] > distance or
                        param[1200 - int(screen_x)][4] > distance or
                        param[1200 - int(screen_x) + 1][4] > distance):
                    taille = ((64 * 720) / distance)

                    sprite = self.texture.get_image(taille, [255, 0, 255])
                    screen.blit(sprite, (screen_x - taille / 2, 360 - taille / 2))


class Enemy:
    def __init__(self, x, y, path, dead_path):
        self.pos = pygame.Vector2(x, y)
        sprite = pygame.image.load(path).convert_alpha()
        self.texture = texture.Object(sprite)
        sprite = pygame.image.load(dead_path).convert_alpha()
        self.texture_mort = texture.Object(sprite)
        self.state = 1

    def draw(self, screen, param, ppos, pang):
        # get angle
        angle = math.atan2(ppos.y - self.pos.y, ppos.x - self.pos.x)
        diff = pang - angle

        diff = correction_ang(diff)

        if abs(diff) > math.pi / 2:
            render = True
        else:
            render = False

        if render:
            screen_x = 0.5 * 1200 * (1 - (math.tan(diff) / math.tan(math.pi / 6)))

            if 0 < screen_x < 1200:
                # get distance
                distance = dist(self.pos.x, self.pos.y, ppos.x, ppos.y)

                if (param[1200 - int(screen_x) - 1][4] > distance or
                        param[1200 - int(screen_x)][4] > distance or
                        param[1200 - int(screen_x) + 1][4] > distance):
                    taille = ((64 * 720) / distance)
                    match self.state:
                        case 1:
                            sprite = self.texture.get_image(taille, [255, 0, 255])
                            screen.blit(sprite, (screen_x - taille / 2, 360 - taille / 2))
                        case 2:
                            sprite = self.texture_mort.get_image(taille, [255, 0, 255])
                            screen.blit(sprite, (screen_x - taille / 2, 360 - taille / 2))

    def tir(self, ppos, pang):
        a = math.tan(pang)
        c = ppos.y - a * ppos.x
        distance = abs((a * self.pos.x - self.pos.y + c)/math.sqrt(a**2+1))

        if distance < 20:
            self.state = 2


def dist(sx, sy, ex, ey):
    return math.sqrt((ex - sx) ** 2 + (ey - sy) ** 2)


def correction_ang(ang):
    if ang < -math.pi:
        ang += 2 * math.pi
    if ang > math.pi:
        ang -= 2 * math.pi
    return ang
