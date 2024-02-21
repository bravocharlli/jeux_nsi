import pygame


class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, origine, taille_de_bande, hauteur, colour=None):
        image = pygame.Surface((taille_de_bande, 225)).convert_alpha()
        image.blit(self.sheet, (0, 0), (origine*(225/64), 0, origine*(225/64)+taille_de_bande, 225))
        image = pygame.transform.scale(image, (taille_de_bande, hauteur))
        image.set_colorkey(colour)
        if taille_de_bande > 20:
            raise IndexError

        return image
