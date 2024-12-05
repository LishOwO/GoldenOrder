import pygame
import sys
import math

class Game:
    def __init__(self):

        pygame.init()

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.run = True

        self.player_color = (255,0,0)
        self.player = pygame.Rect(30,30,50,50)

    def run_game(self):

        while self.run:

            pygame.draw.rect(self.screen, self.player_color, self.player)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
            
            pygame.display.update()

Game().run_game()