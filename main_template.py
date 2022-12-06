'''
###############################################################################
 ______________________________________
|   ___  ___  ___  ___  ___  _____     |
|  | . || __|| | ||  _|| . ||_   _|    |
|  |   ||__ ||   || |_ |   |  | |      |
|  |_|_||___||_|_||___||_|_|  |_| 2022 |
|______________________________________|

BreakOut!
by Edward Larrañaga - 2022

###############################################################################

Sounds acknowledgement:



###############################################################################
'''
import pygame, sys

class IntroScene():
    def __init__(self):
        pass

    def main(self):
        # Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Update
        pygame.display.flip()










# Inizialization
pygame.init()
clock = pygame.time.Clock()

# Screen settings
SCREEN_WIDTH = 640
SCREEN_HEGIHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEGIHT))
pygame.display.set_caption('BreakOut!')

# Game scenes
intro = IntroScene()


# Main loop
while True:
    intro.main()
    clock.tick(60)
