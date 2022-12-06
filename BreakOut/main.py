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

###############################################################################
# Sprites

class Block(pygame.sprite.Sprite):
    '''
    General sprite class used for all objects in the game
    '''
    def __init__(self, width, height, pos_x, pos_y, color):
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect(center = (pos_x, pos_y))

class Player(Block):
    '''
    Player sprite
    '''
    def __init__(self, width, height, pos_x, pos_y, color, speed):
        super().__init__(width, height, pos_x, pos_y, color)
        self.speed = speed
        self.delta_x = 0
        self.posx = pos_x
        self.posy = pos_y
    
    def constrains(self):
        if self.rect.left<=0:
            self.rect.left =0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    
    def reset(self):
        self.rect.center = (self.posx , self.posy)

    def update(self):
        self.constrains()
        self.rect.x += self.delta_x




###############################################################################
# Scenes

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


class GameScene():
    def __init__(self):
        pass

    def update(self):
        # Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Update
        pygame.display.flip()






###############################################################################

# Inizialization
pygame.init()
clock = pygame.time.Clock()

# Screen settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('BreakOut!')

# Colors
bg_color = pygame.Color('gray12')
light_grey = (200,200,200)

# Background
background = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])
background.fill(bg_color)

# Sprites
paddles_group = pygame.sprite.Group()
ball_group = pygame.sprite.GroupSingle()

#ball = Ball(20,20,SCREEN_WIDTH//2,SCREEN_HEIGHT//2, 8, paddles_group)
#ball_group.add(ball)

player1 = Player(120,10,SCREEN_WIDTH//2 , SCREEN_HEIGHT - 50, light_grey,7)
paddles_group.add(player1)

# Game scenes
intro = IntroScene()
game = GameScene()


# Main loop
while True:
    game.update()
    clock.tick(60)
