import pygame
import sys

class Game:
    def __init__(self):

        pygame.init()

        # Var ECRAN
        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080

        # Var BACKGROUND
        self.BACKGROUND_SIZE = 1028
        self.BACKGROUND_TILESET_SIZE = (self.BACKGROUND_SIZE, self.BACKGROUND_SIZE)
        self.BACKGROUND_COLOR = (255, 0, 0) #Rouge
        self.BACKGROUND_MAP_SIZE = self.BACKGROUND_SIZE * 10 #Taille de la map -> CR2E BEACOUPS DE LAG


        #Var PLAYER
        self.PLAYER_VELOCITY = 30
        self.PLAYER_SIZE_MULTIPLIER = 0.5

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.run = True

        # Chargement du fond
        self.background_image = pygame.image.load('texture_map.png').convert()
        self.background_image = pygame.transform.scale(self.background_image, self.BACKGROUND_TILESET_SIZE)

        # Chargement du joueur
        self.player_image = pygame.image.load('BiggerPlayerTest.png').convert()
        new_player_size = (self.player_image.get_width() * self.PLAYER_SIZE_MULTIPLIER , self.player_image.get_height() * self.PLAYER_SIZE_MULTIPLIER)
        self.player_image = pygame.transform.scale(self.player_image, new_player_size)
        self.player_image.set_colorkey((0, 0, 0))

        # Aplication du mouvement du joueur
        self.player = self.player_image.get_rect(topleft=(30, 30))  # Position initiale LITTERALEMENT INUTILE WTF
        self.player_movement_x = [False, False]  # [Gauche, Droite]
        self.player_movement_y = [False, False]  # [Monter, Descendre]
        self.player_position = [0, 0] # Position de départ ?

        # Variables pour la caméra
        self.camera_position = [0, 0]

    def run_game(self):

        while self.run:  
            self.screen.fill(self.BACKGROUND_COLOR)

            # Déplace le fond pour que le joueur soit toujours centré
            for y in range(-self.BACKGROUND_MAP_SIZE, self.BACKGROUND_MAP_SIZE, self.BACKGROUND_SIZE): 
                for x in range(-self.BACKGROUND_MAP_SIZE, self.BACKGROUND_MAP_SIZE, self.BACKGROUND_SIZE):
                    self.screen.blit(self.background_image, (x - self.camera_position[0], y - self.camera_position[1]))

            # Mise à jour de la position du joueur en fonction des entrées
            self.player_position[0] += (self.player_movement_x[1] - self.player_movement_x[0]) * self.PLAYER_VELOCITY    
            self.player_position[1] += (self.player_movement_y[1] - self.player_movement_y[0]) * self.PLAYER_VELOCITY

            # Déplace la caméra pour centrer le joueur
            self.camera_position[0] = self.player_position[0] +250 - self.SCREEN_WIDTH // 2 
            self.camera_position[1] = self.player_position[1] +250 - self.SCREEN_HEIGHT // 2 


            # Dessine le joueur en fonction de la caméra
            self.screen.blit(self.player_image, (self.player_position[0] - self.camera_position[0], self.player_position[1] - self.camera_position[1]))

            # Gestion des événements
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
