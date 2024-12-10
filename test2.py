import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
screen = pygame.display.set_mode((128, 128))
clock = pygame.time.Clock()

# Load images
player = pygame.image.load('New-Piskel.bmp').convert()
background = pygame.image.load('New-Piskel-_1_.bmp').convert()

# Draw the background
screen.blit(background, (0, 0))

# Define GameObject class
class GameObject:
    def __init__(self, image, x, y):
        self.image = image
        self.pos = pygame.Rect(x, y, image.get_width(), image.get_height())

    def move(self):
        self.pos.x += 1
        if self.pos.x > 640:  # Wrap around the screen
            self.pos.x = 0

# Create objects
objects = []
for x in range(10):
    o = GameObject(player, x * 40, x * 40)  # Example staggered placement
    objects.append(o)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    screen.blit(background, (0, 0))

    # Update and draw objects
    for o in objects:
        o.move()
        screen.blit(o.image, o.pos.topleft)

    # Refresh display
    pygame.display.update()
    clock.tick(60)
