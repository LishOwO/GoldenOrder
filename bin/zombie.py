import sys
import math
import tools as tools
import random
import pygame
import os


class Zombie:
    def __init__ (self, pos, type, rect):
        
        self.zombie_pos = pos
        self.zombie_type = type
        self.zombie_hitbox = rect

        #Zombies type :

        #Zombie normal
        if self.zombie_type == 1:
            self.zombie_vel = 1
            self.zombie_atk_dist = 32
            self.zombie_image = pygame.image.load("src/images/sprite/zombie/zombie1/zombie1.png") # to fix


    def update_hitbox(self):
        self.zombie_hitbox = pygame.Rect(self.zombie_pos[0]+16, self.zombie_pos[1]+16, 32, 32)

    def draw(self, screen):
        screen.blit(self.zombie_type, self.zombie_pos)


        #deplace les zombie
    def move_zombies(self, playserpos):
        # Déplace chaque zombie vers le joueur
        zombie_dx = playserpos[0] - self.zombie_pos[0]
        zombie_dy = playserpos[1] - self.zombie_pos[1]
        distance = math.sqrt(zombie_dx**2 + zombie_dy**2)

        if distance != 0:
            zombie_dx /= distance  # Normalisation
            zombie_dy /= distance  # Normalisation

        self.zombie_pos[0] += zombie_dx * self.zombie_vel
        self.zombie_pos[1] += zombie_dy * self.zombie_vel

        # Collision avec le joueur -> Dégats
        if distance <= self.zombie_atk_dist:
            return True
        return False
            

