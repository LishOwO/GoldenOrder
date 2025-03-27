import sys
import math
import tools as tools
import random
import pygame
import os


class Zombie:
    def __init__ (self, pos, type):
        
        self.zombie_pos = pos
        self.zombie_type = type

        #Zombies type :

        #Zombie normal
        base_path = os.path.join("src", "images", "sprite", "zombie")
        if self.zombie_type == 'normal':

            self.zombie_vel = 1
            self.zombie_atk_dist = 32
            self.zombie_image = self.load_and_resize_image(os.path.join(base_path, "zombie1.png"), 0.5)
            self.zombie_size = (32,32)
            self.zombie_hp = 100
            # pygame.image.load(os.path.join(base_path, "zombie1", "zombie1.png")).convert_alpha()

         #Zombie déviant
        elif self.zombie_type == 'deviant':
            self.zombie_vel = 2
            self.zombie_atk_dist = 22
            self.zombie_image = self.load_and_resize_image(os.path.join(base_path, "zombie2.png"), 0.5)
            self.zombie_size = (32,32)
            self.zombie_hp = 150

        elif self.zombie_type == 'boss1':
            self.zombie_vel = 3
            self.zombie_atk_dist = 128
            self.zombie_image = self.load_and_resize_image(os.path.join(base_path, "boss1.png"), 2, (0, 0, 0))
            self.zombie_size = (128,128)
            self.zombie_hp = 6400

        self.zombie_hitbox = self.zombie_image.get_rect(center=(pos[0], pos[1]))
    def load_and_resize_image(self, filepath, size_multiplier, colorkey=(0, 0, 0)):
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
        
    def update_hitbox(self):
        self.zombie_hitbox = pygame.Rect(int(self.zombie_pos[0]) + 16, int(self.zombie_pos[1]) + 16, *self.zombie_size)
    def draw_zombie(self, screen):
        # Use the loaded image to draw the zombie
        screen.blit(self.zombie_image, self.zombie_pos)

        #deplace les zombie
    def move_zombies(self, player_pos):
        # Déplace chaque zombie vers le joueur
        zombie_dx = player_pos[0] - self.zombie_pos[0]
        zombie_dy = player_pos[1] - self.zombie_pos[1]
        distance = math.sqrt(zombie_dx**2 + zombie_dy**2)

        if distance != 0:
            zombie_dx /= distance  # Normalisation
            zombie_dy /= distance  # Normalisation

        self.zombie_pos[0] += zombie_dx * self.zombie_vel
        self.zombie_pos[1] += zombie_dy * self.zombie_vel

        # Met à jour la hitbox
        self.update_hitbox()
        # Collision avec le joueur -> Dégats
        if distance <= self.zombie_atk_dist:
            return True
        return False

    # Boost de vitesse 
    def speed_boost(self):
        old_speed = self.zombie_vel
        self.zombie_vel = old_speed+5

