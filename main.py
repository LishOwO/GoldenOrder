import pygame
import sys
import math

# Variable self publique
# Variable

class Game:
    def __init__(self):

        pygame.init()


        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.run = True

        # Chargement du joueur
        self.player_image = pygame.image.load('PlayerTest.bmp').convert()
        self.player = self.player_image.get_rect(topleft=(30, 30))  # Position initiale

    def run_game(self):

        while self.run:

            self.screen.fill((0, 0, 0))  # Efface l'écran avec une couleur noire

            # Gestion de la fin de jeu (clic sur la croix)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            # Gestion des touches pour déplacer le joueur
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.player.y -= 3
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
               self.player.y += 3
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.player.x -= 3
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.player.x += 3

            # Dessine le joueur
            self.screen.blit(self.player_image, self.player.topleft)

            pygame.display.update()
            self.clock.tick(60)  # Limite à 60 FPS

        pygame.quit()

Game().run_game()
