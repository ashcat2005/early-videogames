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
import pygame, sys, random

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



class Ball(Block):
    def __init__(self, width, height, pos_x, pos_y, color, speed, player_group, blocks_group):
        super().__init__(width, height, pos_x, pos_y, color)
        self.speed0 = speed
        self.speed = self.speed0
        self.delta_x = self.speed*random.choice((-1,1))
        self.delta_y = self.speed*random.choice((-1,1))
        self.player_group = player_group
        self.player_group = blocks_group
    
    def collisions(self):
        if self.rect.top<=0 or self.rect.bottom >= SCREEN_HEIGHT:
            pygame.mixer.Sound.play(pong_sound)
            self.delta_y *= -1

        if self.rect.left<=0 or self.rect.right >= SCREEN_WIDTH:
            pygame.mixer.Sound.play(pong_sound)
            self.delta_x *= -1

        if pygame.sprite.spritecollide(self, self.player_group, False):
            pygame.mixer.Sound.play(pong_sound)
            paddle_col = pygame.sprite.spritecollide(self, self.player_group, False)[0]
            if abs(self.rect.right - paddle_col.rect.left) < 10 and self.delta_x > 0:
                self.delta_x *=-1
            if abs(self.rect.left - paddle_col.rect.right) < 10 and self.delta_x < 0:
                self.delta_x *=-1
            if abs(self.rect.top - paddle_col.rect.bottom) < 10 and self.delta_y < 0:
                self.rect.top = paddle_col.rect.bottom
                self.delta_y *=-1
            if abs(self.rect.bottom - paddle_col.rect.top) < 10 and self.delta_y > 0:
                self.rect.bottom = paddle_col.rect.top
                self.delta_y *=-1

    def update(self):
        self.collisions()
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y
        
    #def reset(self):
    #    self.rect.center = [SCREEN_WIDTH//2,SCREEN_HEIGHT//2]
    #    self.delta_x = self.speed*random.choice((-1,1))
    #    self.delta_y = self.speed*random.choice((-1,1))




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
    def __init__(self, player_group, ball_group, blocks_group):
        self.player_group = player_group
        self.ball_group = ball_group
        self.blocks_group = blocks_group

    def update(self):
        # Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player_group.sprite.delta_x = -self.player_group.sprite.speed
                elif event.key == pygame.K_RIGHT:
                    self.player_group.sprite.delta_x = self.player_group.sprite.speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.player_group.sprite.delta_x = 0
        
        # Update
        self.player_group.update()
        self.ball_group.update()
        pygame.sprite.spritecollide(self.ball_group.sprite, self.blocks_group, True)
        screen.blit(background, [0,0])
        self.player_group.draw(screen)
        self.ball_group.draw(screen)
        self.blocks_group.draw(screen)
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

# Sounds
pong_sound = pygame.mixer.Sound('sounds/pong.mp3')




# Background
background = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])
background.fill(bg_color)

# Sprites
player_group = pygame.sprite.GroupSingle()
ball_group = pygame.sprite.GroupSingle()
blocks_group = pygame.sprite.Group()

ball = Ball(20,20,SCREEN_WIDTH//2,SCREEN_HEIGHT//2, light_grey, 8, player_group, blocks_group)
ball_group.add(ball)

player1 = Player(120,10,SCREEN_WIDTH//2 , SCREEN_HEIGHT - 50, light_grey, 7)
player_group.add(player1)

block = Block(80, 10, 60 , 50, pygame.Color('green'))
blocks_group.add(block)


# Game scenes
intro = IntroScene()
game = GameScene(player_group, ball_group, blocks_group)


# Main loop
while True:
    game.update()
    clock.tick(60)
