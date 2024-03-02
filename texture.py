import pygame


class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, origine, taille_de_bande, hauteur, colour=None):
        # crée une image vide
        image = pygame.Surface((taille_de_bande, 16)).convert_alpha()
        # destine la texture
        image.blit(self.sheet, (0, 0), (origine*(16/64), 0, origine*(16/64)+taille_de_bande, 16))
        # modifie la taille de l'image
        image = pygame.transform.scale(image, (taille_de_bande, hauteur))
        # enlève une certaine couleur
        image.set_colorkey(colour)

        return image
