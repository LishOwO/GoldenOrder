import pygame
import sys
import math
import time


class Game:
    def __init__(self):

        pygame.init()

        self.BACKGROUND_SIZE = 2048


        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080

        self.BACKGROUND_TILESET_SIZE = (self.BACKGROUND_SIZE, self.BACKGROUND_SIZE)
        self.BACKGROUND_COLOR = (14, 219, 248)
        self.PLAYER_VELOCITY = 5



        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.run = True

        # Chargement du joueur
        self.background_image = pygame.image.load('texture_map.png').convert()
        self.background_image = img = pygame.transform.scale(self.background_image, self.BACKGROUND_TILESET_SIZE)

        self.player_image = pygame.image.load('BiggerPlayerTest.png').convert()
        self.player_image.set_colorkey((0, 0, 0))

        self.player = self.player_image.get_rect(topleft=(30, 30))  # Position initiale
        self.player_movement_x = [False, False] #[Gauche, Droite]
        self.player_movement_y = [False, False] #[Monter, Descendre]
        self.player_position = [200, 200]

         

    def run_game(self):

        while self.run:  

            self.screen.fill(self.BACKGROUND_COLOR)
            
            for y in range(-2048,2048,self.BACKGROUND_SIZE): 
                for x in range(-2048,2048,self.BACKGROUND_SIZE):
                    self.screen.blit(self.background_image,(x,y)) 

            self.player_position[0] += (self.player_movement_x[1] - self.player_movement_x[0]) * self.PLAYER_VELOCITY    
            self.player_position[1] += (self.player_movement_y[1] - self.player_movement_y[0]) * self.PLAYER_VELOCITY
            

            # Dessine le joueur
            self.screen.blit(self.player_image, self.player_position)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player_movement_y[0] = True
                    if event.key == pygame.K_DOWN:
                        self.player_movement_y[1] = True

                    if event.key == pygame.K_LEFT:
                        self.player_movement_x[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.player_movement_x[1] = True


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.player_movement_y[0] = False
                    if event.key == pygame.K_DOWN:
                        self.player_movement_y[1] = False  

                    if event.key == pygame.K_LEFT:
                        self.player_movement_x[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.player_movement_x[1] = False
            
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()



Game().run_game()
