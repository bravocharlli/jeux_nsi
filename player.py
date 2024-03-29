import math

import enemy
from carte import *
from texture import *

BLACK = [0, 0, 0]


# class player qui s'occupe de tout
class Player:
    def __init__(self):
        # déclaration des variables
        self.end = False
        self.object = []
        self.mechants = []
        self.carte_objet = []
        self.carte = []
        self.pos = pygame.Vector2(100, 100)
        self.pos_z = 32
        self.angle = 0
        self.speed = 300
        self.pv = 30
        self.tirer = 0
        self.mouse_x = get_mouse_delta()
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        self.strafe_dx = math.cos(self.angle + (math.pi / 2)) * self.speed * 0.75
        self.strafe_dy = math.sin(self.angle + (math.pi / 2)) * self.speed * 0.75

        self.niveau_actuel = 0
        self.changer_niv(self.niveau_actuel)

        # chargement des textures du personnage
        sprite_sheet_image_mur = pygame.image.load('resource/mur.png').convert_alpha()
        sprite_sheet_image_mur_mouse = pygame.image.load('resource/mur_mousse.png').convert_alpha()
        self.sprite_sheet_mur = SpriteSheet(sprite_sheet_image_mur)
        self.sprite_sheet_mur_mouse = SpriteSheet(sprite_sheet_image_mur_mouse)

        sprite_sheet_pistolet_1 = pygame.image.load('resource/pistolet_1.png').convert_alpha()
        sprite_sheet_pistolet_1_fire = pygame.image.load('resource/pistolet_1_fire.png').convert_alpha()
        self.sprite_sheet_pistolet_1 = Object(sprite_sheet_pistolet_1)
        self.sprite_sheet_pistolet_1_fire = Object(sprite_sheet_pistolet_1_fire)

    def changer_niv(self, level):
        """+
        Permet de basculer d'un niveau à l'autre
        :param level: niveau à choisir
        :return: renvois True ou False en fonction de si le niveau existe
        """
        # reinitialisation du pers
        self.angle = math.pi / 2
        self.pos = pygame.Vector2(100, 100)
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        if level > 1:
            return True
        self.niveau_actuel = level
        self.carte = niveau[self.niveau_actuel][0]
        self.niveau_actuel = level
        self.carte_objet = niveau[self.niveau_actuel][1]

        self.mechants = []
        self.object = []
        # load object + enemy
        for i in range(cartey):
            for j in range(cartex):
                match self.carte_objet[i][j]:
                    case 1:
                        self.mechants.append(enemy.Enemy(j * 64 + 32, i * 64 + 32, 'resource/monstre1.png',
                                                         'resource/monstre1_mort.png', 1, self.carte))
                    case 2:
                        self.mechants.append(enemy.Enemy(j * 64 + 32, i * 64 + 32, 'resource/monstre2.png',
                                                         'resource/monstre2_mort.png', 2, self.carte))
                    case 3:
                        self.object.append(enemy.Object(j * 64 + 32, i * 64 + 32, 'resource/piller.png'))

        return False

    def update(self, dt):
        """
        Déplace le joueur et les ennemis
        :param dt:
        :return:
        """
        # self.mouse_x = get_mouse_delta()
        self.move(dt)
        self.collision(dt)

        if self.tirer <= 10:
            self.tirer += dt * 30

        # tri les merchant dans l'ordre pour optimiser les jeux
        temp = []
        for i in self.mechants:
            temp.append(dist_pygame(self.pos, i.pos))

        for i in range(len(temp)):
            for j in range(len(temp) - 1):
                if temp[j] > temp[j + 1]:
                    self.mechants[j], self.mechants[j + 1] = self.mechants[j + 1], self.mechants[j]

    def move(self, dt):
        """
        Modifie la position et l’angle en fonction des touches
        :param dt:
        :return:
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_z]:
            self.pos.x += self.dx * dt
            self.pos.y += self.dy * dt
        if keys[pygame.K_s]:
            self.pos.x -= self.dx * dt
            self.pos.y -= self.dy * dt
        if keys[pygame.K_d]:
            self.pos.x += self.strafe_dx * dt
            self.pos.y += self.strafe_dy * dt
        if keys[pygame.K_q]:
            self.pos.x -= self.strafe_dx * dt
            self.pos.y -= self.strafe_dy * dt
        """
        if self.mouse_x != 0:
            self.angle += self.mouse_x * dt
            self.dx = math.cos(self.angle) * self.speed
            self.dy = math.sin(self.angle) * self.speed
            self.strafe_dx = math.cos(self.angle + (math.pi / 2)) * self.speed * 0.75
            self.strafe_dy = math.sin(self.angle + (math.pi / 2)) * self.speed * 0.75
        """
        if keys[pygame.K_LEFT]:
            self.angle -= 2 * dt
            self.dx = math.cos(self.angle) * self.speed
            self.dy = math.sin(self.angle) * self.speed
            self.strafe_dx = math.cos(self.angle + (math.pi / 2)) * self.speed * 0.75
            self.strafe_dy = math.sin(self.angle + (math.pi / 2)) * self.speed * 0.75

        if keys[pygame.K_RIGHT]:
            self.angle += 2 * dt
            self.dx = math.cos(self.angle) * self.speed
            self.dy = math.sin(self.angle) * self.speed
            self.strafe_dx = math.cos(self.angle + (math.pi / 2)) * self.speed * 0.75
            self.strafe_dy = math.sin(self.angle + (math.pi / 2)) * self.speed * 0.75

        if self.angle < 0:
            self.angle += 2 * math.pi
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi

        for mechant in self.mechants:
            self.pv -= mechant.move(self.pos, dt)

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
        if self.strafe_dx < 0:
            strafe_xo = -20
        else:
            strafe_xo = 20
        if self.strafe_dy < 0:
            strafe_yo = -20
        else:
            strafe_yo = 20

        ipx = int(self.pos.x / tille)
        ipy = int(self.pos.y / tille)
        ipx_add_xo = int((self.pos.x + xo) / tille)
        ipy_add_yo = int((self.pos.y + yo) / tille)
        ipx_sub_xo = int((self.pos.x - xo) / tille)
        ipy_sub_yo = int((self.pos.y - yo) / tille)
        ipx_add_strafe_xo = int((self.pos.x + strafe_xo) / tille)
        ipy_add_strafe_yo = int((self.pos.y + strafe_yo) / tille)
        ipx_sub_strafe_xo = int((self.pos.x - strafe_xo) / tille)
        ipy_sub_strafe_yo = int((self.pos.y - strafe_yo) / tille)

        if keys[pygame.K_z]:
            if self.carte[ipy][ipx_add_xo] > 0:
                self.pos.x -= self.dx * dt
            if self.carte[ipy_add_yo][ipx] > 0:
                self.pos.y -= self.dy * dt
        if keys[pygame.K_s]:
            if self.carte[ipy][ipx_sub_xo] > 0:
                self.pos.x += self.dx * dt
            if self.carte[ipy_sub_yo][ipx] > 0:
                self.pos.y += self.dy * dt

        if keys[pygame.K_q]:
            if self.carte[ipy][ipx_sub_strafe_xo] > 0:
                self.pos.x += self.strafe_dx * dt
            if self.carte[ipy_sub_strafe_yo][ipx] > 0:
                self.pos.y += self.strafe_dy * dt

        if keys[pygame.K_d]:
            if self.carte[ipy][ipx_add_strafe_xo] > 0:
                self.pos.x -= self.strafe_dx * dt
            if self.carte[ipy_add_strafe_yo][ipx] > 0:
                self.pos.y -= self.strafe_dy * dt

        temp = 0
        if keys[pygame.K_SPACE] and self.tirer > 10:
            self.tirer = 0
            for mechant in self.mechants:
                tir = mechant.tir(self.pos, self.angle)
                if tir:
                    temp += 1
                    if temp == 3:
                        break

    def calcul_mur(self):
        """
        Calcule les paramètres pour pouvoirs afficher les murs
        :return array: [type_mur, ofset, lineh, lineo, distf]
        """

        # Parcoure de tout le rayon dans le champ de vision
        param = []
        for r in range(1200):
            # calcule l'angle du rayon et le borne entre 0 et 2pi
            ra = self.angle - ((r * (math.pi / 3600)) - math.pi / 6)
            if ra < 0:
                ra += 2 * math.pi
            if ra > 2 * math.pi:
                ra -= 2 * math.pi

            # init var
            type_mur_h = 0
            type_mur_v = 0

            # _____________________________________________________________________________________________________
            # mur horizontal                                                                                      |
            # _____________________________________________________________________________________________________

            # init var
            dof = 0
            xo, yo = 0, 0
            rx, ry = 0, 0
            ch = 0

            disth = 10000
            hx = self.pos.x

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

            while dof < 100:
                mx = int(rx / tille)
                my = int(ry / tille)
                if 0 <= mx < cartex and 0 <= my < cartey:
                    if self.carte[my - ch][mx] > 0:
                        dof = 100
                        hx = rx
                        hy = ry
                        disth = dist(self.pos.x, self.pos.y, hx, hy)
                        type_mur_h = self.carte[my - ch][mx]
                    else:
                        rx += xo
                        ry += yo
                        dof += 1
                else:
                    dof = 100

            # ___________________________________________________________________________________________________
            # mur vertical                                                                                      |
            # ___________________________________________________________________________________________________

            distv = 10000
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

            while dof < 100:
                mx = int(rx / tille)
                my = int(ry / tille)
                if 0 <= mx < cartex and 0 <= my < cartey:
                    if self.carte[my][mx - cv] > 0:
                        dof = 100
                        vx = rx
                        vy = ry
                        distv = dist(self.pos.x, self.pos.y, vx, vy)
                        type_mur_v = self.carte[my][mx - cv]
                    else:
                        rx += xo
                        ry += yo
                        dof += 1
                else:
                    dof = 100

            # garde-les valeurs du mur le plus proche
            if distv < disth:
                ry = vy
                ofset = ry % tille if ra < math.pi / 2 or ra > (3 * math.pi) / 2 else tille - (ry % tille)
                distf = distv
                type_mur = type_mur_v
            else:
                rx = hx
                ofset = rx % tille if ra > math.pi else tille - (rx % tille)
                distf = disth
                type_mur = type_mur_h

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
        """
        Dessine tous les éléments du plus loin
        :param screen:
        :return:
        """
        # dessine les murs
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

        # récupère les paramètres des sprites
        param_sprite = []
        for mech in self.mechants:
            param_sprite.append(mech.calcul(param, self.pos, self.angle))
        for obj in self.object:
            param_sprite.append(obj.calcul(param, self.pos, self.angle))

        # enlève-les sprites qui ne sont pas déssiner
        temp = []
        for i in range(len(param_sprite)):
            if param_sprite[i] is not None:
                temp.append(param_sprite[i])
        param_sprite = temp

        # try en fonction de la distance
        for i in range(len(param_sprite)):
            for j in range(len(param_sprite) - 1):
                if param_sprite[j][2] > param_sprite[j + 1][2]:
                    param_sprite[j], param_sprite[j + 1] = param_sprite[j + 1], param_sprite[j]

        # dessine-les sprite
        for i in param_sprite:
            sprite = i[0]
            screen_x = i[1]
            taille = i[2]
            screen.blit(sprite, (screen_x - taille / 2, 360 - taille / 2))

        # dessine l'interface du personnage
        pygame.draw.rect(screen, [0, 0, 0], [590, 350, 10, 10])
        if self.tirer < 3:
            image = self.sprite_sheet_pistolet_1_fire.get_image(120, [255, 0, 255])
        else:
            image = self.sprite_sheet_pistolet_1.get_image(120, [255, 0, 255])
        screen.blit(image, (540, 560))

        pygame.draw.rect(screen, [33, 59, 188], [0, 680, 1200, 40])

        # permet l'évolution du niveau et du passage de niveau
        total = 0
        for m in self.mechants:
            if m.pv > 0:
                total += 1
        if total == 0:
            self.end = self.changer_niv(self.niveau_actuel + 1)
            if self.end:
                self.pv = -33
            else:
                self.pv = 30
        elif total <= 7:
            self.carte[5][8] = 0


def dist(sx, sy, ex, ey):
    """
    Donne la distance entre deux points
    :param sx:
    :param sy:
    :param ex:
    :param ey:
    :return:
    """
    return math.sqrt((ex - sx) ** 2 + (ey - sy) ** 2)


def dist_pygame(vec1, vec2):
    """
    Donne la distance entre deux vecteurs 2
    :param vec1:
    :param vec2:
    :return:
    """
    return math.sqrt((vec1.x - vec2.x) ** 2 + (vec1.y - vec2.y) ** 2)


def get_mouse_delta():
    """
    Donne le décalage en x de la souris
    :return x: valeur entre -60 et 60
    """
    x, y = pygame.mouse.get_pos()
    pygame.mouse.set_pos(600, 360)
    x = (x - 600) / 10
    return x
