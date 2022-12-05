
import pygame, sys

# Inizialization
pygame.init()
clock = pygame.time.Clock()

# Screen settings
SCREEN_WIDTH = 640
SCREEN_HEGIHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEGIHT))
pygame.display.set_caption('Pong!')


# Main loop
while True:
    # Handling events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Update
    pygame.display.flip()
    clock.tick(60)
