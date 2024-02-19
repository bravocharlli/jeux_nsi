import pygame
import math
from carte import *


class Player:
    def __init__(self):
        self.pos = pygame.Vector2(100, 100)
        self.angle = 0
        self.speed = 500
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed

    def update(self, dt):
        """
        Modifie la position et l’angle en fonction des touches
        :param dt:
        :return:
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.pos.x += self.dx * dt
            self.pos.y += self.dy * dt
        if keys[pygame.K_DOWN]:
            self.pos.x -= self.dx * dt
            self.pos.y -= self.dy * dt
        if keys[pygame.K_LEFT]:
            self.angle -= 3 * dt
            self.dx = math.cos(self.angle) * self.speed
            self.dy = math.sin(self.angle) * self.speed
        if keys[pygame.K_RIGHT]:
            self.angle += 3 * dt
            self.dx = math.cos(self.angle) * self.speed
            self.dy = math.sin(self.angle) * self.speed
        if self.angle < 0:
            self.angle += 2 * math.pi
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi

    def collision(self, dt):
        """
        Recule ou avance le personnage en fonction de la carte
        :param dt:
        :return:
        """
        keys = pygame.key.get_pressed()
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
        if keys[pygame.K_UP]:
            if carte[ipy][ipx_add_xo] == 1:
                self.pos.x -= self.dx * dt
            if carte[ipy_add_yo][ipx] == 1:
                self.pos.y -= self.dy * dt
        if keys[pygame.K_DOWN]:
            if carte[ipy][ipx_sub_xo] == 1:
                self.pos.x += self.dx * dt
            if carte[ipy_sub_yo][ipx] == 1:
                self.pos.y += self.dy * dt

    def draw(self, screen):
        """
        Dessine le personnage et se qu'il voit
        :param screen:
        :return:
        """

        for r in range(120):
            ra = self.angle - ((r * (math.pi / 360)) - 0.4)
            if ra < 0:
                ra += 2 * math.pi
            if ra > 2 * math.pi:
                ra -= 2 * math.pi

            # ___________________________________________________________________________________________________
            # mur horizontal                                                                                      |
            # ____________________________________________________________________________________________________

            dof = 0
            xo, yo = 0, 0
            rx, ry = 0, 0
            ch = 0

            disth = 10000
            hx = self.pos.x
            hy = self.pos.y

            if ra > math.pi:
                ata = -1 / math.tan(ra)
                ry = (int(self.pos.y / tille)) * tille  # rx et ry sont les coordonnées de
                rx = (self.pos.y - ry) * ata + self.pos.x  # rencontre de première ligne horizontale
                ch = 1
                yo = -tille
                xo = -yo * ata

            if ra < math.pi:
                ata = -1 / math.tan(ra)
                ry = (int(self.pos.y / tille)) * tille + tille
                rx = (self.pos.y - ry) * ata + self.pos.x
                ch = 0
                yo = tille
                xo = -yo * ata

            if 0 == ra or ra == math.pi:
                ch = 0
                ry = self.pos.y
                rx = self.pos.x

            while dof < 10:
                mx = int(rx / tille)
                my = int(ry / tille)
                if 0 <= mx < cartex and 0 <= my < cartey:
                    if carte[my - ch][mx] > 0:
                        dof = 10
                        hx = rx
                        hy = ry
                        disth = dist(self.pos.x, self.pos.y, hx, hy)
                    else:
                        rx += xo
                        ry += yo
                        dof += 1
                else:
                    dof = 12

            # ___________________________________________________________________________________________________
            # mur vertical                                                                                      |
            # ____________________________________________________________________________________________________

            distv = 10000
            vx = self.pos.x
            vy = self.pos.y
            dof = 0
            cv = 0
            if math.pi / 2 < ra < (3 * math.pi) / 2:
                nta = -math.tan(ra)
                rx = (int(self.pos.x / tille)) * tille
                ry = (self.pos.x - rx) * nta + self.pos.y
                cv = 1
                xo = -tille
                yo = -xo * nta

            if ra < math.pi / 2 or ra > (3 * math.pi) / 2:
                nta = -math.tan(ra)
                rx = (int(self.pos.x / tille)) * tille + tille
                ry = (self.pos.x - rx) * nta + self.pos.y
                cv = 0
                xo = tille
                yo = -xo * nta

            if ra == math.pi / 2 or ra == (3 * math.pi) / 2:
                cv = 0
                rx = self.pos.x
                ry = self.pos.y

            while dof < 10:
                mx = int(rx / tille)
                my = int(ry / tille)
                if 0 <= mx < cartex and 0 <= my < cartey:
                    if carte[my][mx - cv] > 0:
                        dof = 10
                        vx = rx
                        vy = ry
                        distv = dist(self.pos.x, self.pos.y, vx, vy)
                    else:
                        rx += xo
                        ry += yo
                        dof += 1
                else:
                    dof = 10

            distf = 1
            p = 0
            if distv < disth:
                rx = vx
                ry = vy
                distf = distv
                p = 25
            elif distv >= disth:
                rx = hx
                ry = hy
                distf = disth
                p = 0

            ca = self.angle - ra
            if 2 * math.pi < ca:
                ca -= 2 * math.pi
            if 0 > ca:
                ca += 2 * math.pi

            distf = distf * math.cos(ca)
            lineh = (tille * 720) / distf

            if lineh > 720:
                lineh = 720
            lineo = 360 - lineh / 2

            for i in range(int(lineh)):
                pygame.draw.rect(screen, [75 + p, 75 + p, 75 + p], [1200 - r * 10, lineo+i, 10, 1])



def dist(sx, sy, ex, ey):
    return math.sqrt((ex - sx) ** 2 + (ey - sy) ** 2)
