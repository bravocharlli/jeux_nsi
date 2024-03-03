import math
import matplotlib.image as mpimg
import enemy
from carte import *
from texture import *


BLACK = [0, 0, 0]


class Player:
    def __init__(self):
        self.pos = pygame.Vector2(100, 100)
        self.pos_z = 32
        self.angle = 0
        self.speed = 500
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed

        # sprite_sheet c'est la texture du mur qu'il faut redécouper
        sprite_sheet_image_mur = pygame.image.load('resource/murs.png').convert_alpha()
        sprite_sheet_image_mur_mouse = pygame.image.load('resource/murs_en_mousse.png').convert_alpha()
        self.sprite_sheet_mur = SpriteSheet(sprite_sheet_image_mur)
        self.sprite_sheet_mur_mouse = SpriteSheet(sprite_sheet_image_mur_mouse)

        # object
        self.objet = enemy.Object(250, 250, 10)

    def update(self, dt):
        self.move(dt)
        self.collision(dt)

    def move(self, dt):
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
            if carte[ipy][ipx_add_xo] > 0:
                self.pos.x -= self.dx * dt
            if carte[ipy_add_yo][ipx] > 0:
                self.pos.y -= self.dy * dt
        if keys[pygame.K_DOWN]:
            if carte[ipy][ipx_sub_xo] > 0:
                self.pos.x += self.dx * dt
            if carte[ipy_sub_yo][ipx] > 0:
                self.pos.y += self.dy * dt

    def calcul_mur(self):
        """
        Dessine se que le personnage voit
        :return:
        """

        # parcour de tout les rayon dans le champ de vision
        param = []
        for r in range(1200):
            # calcule l'angle du rayon et le borne entre 0 et 2pi
            ra = self.angle - ((r * (math.pi / 3600)) - 0.4)
            if ra < 0:
                ra += 2 * math.pi
            if ra > 2 * math.pi:
                ra -= 2 * math.pi

            # init var
            type_mur_h = 0
            type_mur_v = 0

            # ___________________________________________________________________________________________________
            # mur horizontal                                                                                      |
            # ____________________________________________________________________________________________________

            # init var
            dof = 0
            xo, yo = 0, 0
            rx, ry = 0, 0
            ch = 0

            disth = 10000
            hx = self.pos.x
            hy = self.pos.y

            # regarde en bas
            if ra > math.pi:
                ata = -1 / math.tan(ra)
                ry = (int(self.pos.y / tille)) * tille  # rx et ry sont les coordonnées de
                rx = (self.pos.y - ry) * ata + self.pos.x  # rencontre de première ligne horizontale
                ch = 1
                yo = -tille
                xo = -yo * ata

            # regarde en haut
            elif ra < math.pi:
                ata = -1 / math.tan(ra)
                ry = (int(self.pos.y / tille)) * tille + tille
                rx = (self.pos.y - ry) * ata + self.pos.x
                ch = 0
                yo = tille
                xo = -yo * ata

            elif 0 == ra or ra == math.pi:
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
                        type_mur_h = carte[my - ch][mx]
                    else:
                        rx += xo
                        ry += yo
                        dof += 1
                else:
                    dof = 12

            # ___________________________________________________________________________________________________
            # mur vertical                                                                                      |
            # ___________________________________________________________________________________________________

            distv = 10000
            vx = self.pos.x
            vy = self.pos.y
            dof = 0
            cv = 0

            # regarde à gauche
            if math.pi / 2 < ra < (3 * math.pi) / 2:
                nta = -math.tan(ra)
                rx = (int(self.pos.x / tille)) * tille
                ry = (self.pos.x - rx) * nta + self.pos.y
                cv = 1
                xo = -tille
                yo = -xo * nta

            # regarde à droite
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
                        type_mur_v = carte[my][mx - cv]
                    else:
                        rx += xo
                        ry += yo
                        dof += 1
                else:
                    dof = 10

            # garde-les valeurs du mur le plus proche
            p = 0
            if distv < disth:
                rx = vx
                ry = vy
                ofset = ry % tille if ra < math.pi / 2 or ra > (3 * math.pi) / 2 else tille - (ry % tille)
                distf = distv
                type_mur = type_mur_v
                p = 1
            else:
                rx = hx
                ry = hy
                ofset = rx % tille if ra > math.pi else tille - (rx % tille)
                distf = disth
                type_mur = type_mur_h
                p = 0

            ca = self.angle - ra
            if 2 * math.pi < ca:
                ca -= 2 * math.pi
            if 0 > ca:
                ca += 2 * math.pi

            distf = distf * math.cos(ca)
            lineh = (tille * 720) / distf
            lineo = 360 - lineh / 2

            # enregistrement des valeurs calculé
            param.append([type_mur, ofset, lineh, lineo, distf])
        return param

    def draw(self, screen):
        param = self.calcul_mur()


        for r in range(len(param)):
            type_mur = param[r][0]
            ofset = param[r][1]
            lineh = param[r][2]
            lineo = param[r][3]
            if type_mur == 1:
                texture = self.sprite_sheet_mur.get_image(ofset, 1, lineh)
            else:
                texture = self.sprite_sheet_mur_mouse.get_image(ofset, 1, lineh)
            screen.blit(texture, (1200 - r, lineo))

        self.objet.draw(screen, param, self.pos, self.angle)


def dist(sx, sy, ex, ey):
    return math.sqrt((ex - sx) ** 2 + (ey - sy) ** 2)
