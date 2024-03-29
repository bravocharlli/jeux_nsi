import pygame


class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, origine, taille_de_bande, hauteur, colour=None):
        # crée une image vide
        image = pygame.Surface((taille_de_bande, 32)).convert_alpha()
        # destine la texture
        image.blit(self.sheet, (0, 0), (origine*(32/64), 0, origine*(32/64)+taille_de_bande, 32))
        # modifie la taille de l'image
        image = pygame.transform.scale(image, (taille_de_bande, hauteur))
        # enlève une certaine couleur
        image.set_colorkey(colour)
        return image


class Object:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, taille, colour):
        # crée une image vide
        image = pygame.Surface((32, 32)).convert_alpha()
        # destine la texture
        image.blit(self.sheet, (0, 0), (0, 0, 32, 32))
        # modifie la taille de l'image
        image = pygame.transform.scale(image, (taille, taille))
        # enlève une certaine couleur
        image.set_colorkey(colour)
        return image
