import sys
from math import sqrt
import pygame


def distance_squared(target_pos, self):
    return (target_pos[0] - self[0])**2 + (target_pos[1] - self[1])**2

# load les images et les resize
@staticmethod
def load_and_resize_image(filepath, size_multiplier, colorkey=(0, 0, 0)):
    """
    Charge une image, redimensionne et applique un colorkey.
    :param filepath: Chemin vers l'image.
    :param size_multiplier: Multiplicateur pour redimensionner l'image.
    :param colorkey: Couleur à rendre transparente.
    :return:Image redim
    """
    image = pygame.image.load(filepath).convert()
    new_size = (int(image.get_width() * size_multiplier), int(image.get_height() * size_multiplier))
    image = pygame.transform.scale(image, new_size)
    image.set_colorkey(colorkey)
    return image