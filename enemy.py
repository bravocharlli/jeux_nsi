import pygame
import texture
import math
from carte import *
import random

class Object:
    def __init__(self, x, y, path):
        self.pos = pygame.Vector2(x, y)
        sprite = pygame.image.load(path).convert_alpha()
        self.texture = texture.Object(sprite)

    def calcul(self, screen, param, ppos, pang):
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

            if 0 < 1200 - int(screen_x) < len(param):
                # get distance
                distance = dist(self.pos.x, self.pos.y, ppos.x, ppos.y)

                if param[1200 - int(screen_x)][4] > distance:
                    taille = ((64 * 720) / distance)

                    sprite = self.texture.get_image(taille, [255, 0, 255])
                    return [sprite, screen_x, taille]


class Enemy:
    def __init__(self, x, y, path, dead_path, numero, carte):
        self.pos = pygame.Vector2(x, y)
        sprite = pygame.image.load(path).convert_alpha()
        self.texture = texture.Object(sprite)
        sprite = pygame.image.load(dead_path).convert_alpha()
        self.texture_mort = texture.Object(sprite)
        self.pv = 3
        self.numero = numero
        self.speed = 50 * numero
        self.angle = 0
        self.carte = carte
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed

    def move(self, ppos, dt):
        if self.pv <= 0:
            return 0
        distance = dist(self.pos.x, self.pos.y, ppos.x, ppos.y)
        if distance > 320:
            return 0

        # calcul direction
        self.angle = math.atan2(ppos.y - self.pos.y, ppos.x - self.pos.x) + random.uniform(-0.4, 0.4)
        if random.randint(0, 5) == 0:
            self.dx = math.cos(self.angle) * self.speed
            self.dy = math.sin(self.angle) * self.speed

        if self.angle < 0:
            self.angle += 2 * math.pi
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi


        # move
        if 100 * self.numero < distance or self.numero == 1:
            self.pos.x += self.dx * dt
            self.pos.y += self.dy * dt

            # collision
            if self.dx < 0:
                xo = -20
            else:
                xo = 20
            if self.dy < 0:
                yo = -20
            else:
                yo = 20

            ipx = int(self.pos.x / tille)
            ipy = int(self.pos.y / tille)
            ipx_add_xo = int((self.pos.x + xo) / tille)
            ipy_add_yo = int((self.pos.y + yo) / tille)
            ipx_sub_xo = int((self.pos.x - xo) / tille)
            ipy_sub_yo = int((self.pos.y - yo) / tille)

            if self.carte[ipy][ipx_add_xo] > 0:
                self.pos.x -= self.dx * dt
            if self.carte[ipy_add_yo][ipx] > 0:
                self.pos.y -= self.dy * dt

        if 100 < distance and self.numero == 1:
            return random.randint(0, 100) == 1
        elif 200 < distance and self.numero == 2:
            a = math.tan(self.angle)
            c = self.pos.y - a * self.pos.x
            distance = abs((a * ppos.x - ppos.y + c) / math.sqrt(a ** 2 + 1))
            diff = correction_ang(self.angle - math.atan2(self.pos.y - ppos.y, self.pos.x - ppos.x))
            if abs(diff) > math.pi / 2:
                return random.randint(0, 100) == 1

        return 0

    def calcul(self, screen, param, ppos, pang):
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

            if 0 < 1200 - int(screen_x) < len(param):
                # get distance
                distance = dist(self.pos.x, self.pos.y, ppos.x, ppos.y)

                if param[1200 - int(screen_x)][4] > distance:
                    taille = ((64 * 720) / distance)
                    if self.pv > 0:
                        sprite = self.texture.get_image(taille, [255, 0, 255])
                        return [sprite, screen_x, taille]
                    else:
                        sprite = self.texture_mort.get_image(taille, [255, 0, 255])
                        return [sprite, screen_x, taille] 

    def tir(self, ppos, pang):
        a = math.tan(pang)
        c = ppos.y - a * ppos.x
        distance = abs((a * self.pos.x - self.pos.y + c) / math.sqrt(a ** 2 + 1))
        diff = correction_ang(pang - math.atan2(ppos.y - self.pos.y, ppos.x - self.pos.x))

        if abs(diff) > math.pi / 2 and self.pv > 0 and distance < 30:
            self.pv -= 1
            return True
        return False


def dist(sx, sy, ex, ey):
    return math.sqrt((ex - sx) ** 2 + (ey - sy) ** 2)


def correction_ang(ang):
    if ang < -math.pi:
        ang += 2 * math.pi
    if ang > math.pi:
        ang -= 2 * math.pi
    return ang
