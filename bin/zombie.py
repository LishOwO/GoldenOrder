import sys
import math
import tools as tools
import random
import pygame

sys.path.append('../')
class Zombie:
    def __init__ (self, pos, type, rect, game):
        
        self.zombie_pos = pos
        self.zombie_type = type
        self.zombie_hitbox = rect

        #Zombies type :

        #Zombie normal
        if self.zombie_type == 1:
            self.zombie_vel = 1
            self.zombie_atk_dist = 32
            self.zombie_size = 0.5
            self.zombie_image = game.load_and_resize_image('src/images/sprite/zombie/zombie1/zombie1.png', self.zombie_size) # to fix

         #Zombie déviant
        if self.zombie_type == 2:
            self.zombie_vel = 2
            self.zombie_atk_dist = 22
            self.zombie_size = 0.5
            self.zombie_image = game.load_and_resize_image('src/images/sprite/zombie/zombie1/zombie1.png', self.zombie_size) # to fix


    def draw_zombie(self, image, screen, player_pos):
        # Determine the direction of movement and flip the image if necessary
        zombie_dx = player_pos[0] - self.zombie_pos[0]
        zombie_dy = player_pos[1] - self.zombie_pos[1]
        distance = math.sqrt(zombie_dx**2 + zombie_dy**2)

        if distance != 0:
            zombie_dx /= distance  # Normalisation
            zombie_dy /= distance  # Normalisation

        # Flip the image if the direction changes
        if zombie_dx < 0 and not getattr(self, 'flipped', False):
            self.zombie_image = pygame.transform.flip(self.zombie_image, True, False)
            self.flipped = True
        elif zombie_dx > 0 and getattr(self, 'flipped', False):
            self.zombie_image = pygame.transform.flip(self.zombie_image, True, False)
            self.flipped = False

    def update_hitbox(self):
        self.zombie_hitbox = pygame.Rect(self.zombie_pos[0]+16, self.zombie_pos[1]+16, 32, 32)


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

        
        # Store the last horizontal direction for flipping
        self.last_direction = zombie_dx
        # Collision avec le joueur -> Dégats
        if distance <= self.zombie_atk_dist:
            return True
        return False

    # Boost de vitesse 
    def speed_boost(self):
        old_speed = self.zombie_vel
        self.zombie_vel = old_speed+5

