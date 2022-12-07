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
    def __init__(self, width, height, pos_x, pos_y, color, speed=8):
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
        self.delta_y = -self.speed
        self.player_group = player_group
        self.blocks_group = blocks_group
    
    def collisions(self):
        if self.rect.top<=0:
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
        
    def reset(self):
        self.rect.center = [SCREEN_WIDTH//2,SCREEN_HEIGHT//2]
        self.speed = self.speed0
        self.delta_x = self.speed*random.choice((-1,1))
        self.delta_y = -self.speed


###############################################################################
# Game Control

class Game_play():
    '''
    Controls the game.
    '''
    def __init__(self, player_group, ball_group, blocks_group, play=False):
        self.lifes = 2
        self.player1_score = 0
        self.player_group = player_group
        self.ball_group = ball_group
        self.blocks_group = blocks_group
        self.ready = ready_font.render('READY', False, light_grey)
        self.ready3 = ready_font.render('3', False, light_grey)
        self.ready2 = ready_font.render('2', False, light_grey)
        self.ready1 = ready_font.render('1', False, light_grey)
        self.screen = screen
        self.play = play
    
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
        screen.blit(background, [0,0])
        self.player_group.draw(screen)
        self.ball_group.draw(screen)
        self.blocks_group.draw(screen)
        self.collisions()
        self.draw_scores()
        pygame.display.flip()
        self.fail()
    
    def collisions(self):
        if pygame.sprite.spritecollide(self.ball_group.sprite, self.blocks_group, True):
            pygame.mixer.Sound.play(explosion_sound)
            #self.ball_group.sprite.delta_y *=-1
            self.player1_score += 10
            self.ball_group.sprite.delta_x *= 1.005
            self.ball_group.sprite.delta_y *= -1.005
            if len(blocks_group) <= 0:
                self.next_level()

    def reset(self):
        if self.lifes >=0:
            self.ball_group.sprite.reset()
            self.player_group.sprite.reset()
            self.count_in()
        else:
            self.lifes = 0
            self.play = False
    
    def next_level(self):
        build_blocks()
        self.restart_timer = pygame.time.get_ticks()
        self.lifes += 1
        pygame.mixer.Sound.play(start_sound)
        self.reset()

    def new_game(self):
        build_blocks()
        self.restart_timer = pygame.time.get_ticks()
        self.player1_score = 0
        self.lifes = 2
        pygame.mixer.Sound.play(start_sound)
        self.reset()
                
    def count_in(self):
        current_time = pygame.time.get_ticks()
        while current_time - self.restart_timer < 2700:
            screen.blit(background, [0,0])
            self.blocks_group.draw(self.screen)
            self.player_group.draw(self.screen)
            self.draw_scores()
            self.screen.blit(self.ready, (SCREEN_WIDTH/2-85, SCREEN_HEIGHT/2-100))
            if current_time - self.restart_timer < 900:
                self.screen.blit(self.ready3, (SCREEN_WIDTH/2-10, SCREEN_HEIGHT/2))
            elif current_time - self.restart_timer < 1800:
                self.screen.blit(self.ready2, (SCREEN_WIDTH/2-10, SCREEN_HEIGHT/2))
            elif current_time - self.restart_timer < 2700:
                self.screen.blit(self.ready1, (SCREEN_WIDTH/2-10, SCREEN_HEIGHT/2))
            current_time = pygame.time.get_ticks() 
            pygame.display.flip()
   
    def fail(self):
        if self.ball_group.sprite.rect.top >= SCREEN_HEIGHT:
            self.restart_timer = pygame.time.get_ticks()
            pygame.mixer.Sound.play(fail_sound)
            self.lifes -= 1
            self.reset()

    def draw_scores(self):
        player1_text = score_font.render(f'{self.player1_score}', False, light_grey)
        self.screen.blit(player1_text, (50, 10))
        lifes_text = score_font.render(f'{self.lifes}', False, light_grey)
        self.screen.blit(lifes_text, (SCREEN_WIDTH-75, 10))



class IntroScene():
    def __init__(self):
        pong_font =  pygame.font.Font("freesansbold.ttf", 100)
        self.title = ready_font.render('BREAKOUT!', False, light_grey)
        self.press_start = score_font.render('Press SPACE to start', False, light_grey)
        self.screen = screen

    def update(self):
        # Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.new_game()
                    game.play = True
        
        # Update
        self.screen.blit(background, [0,0])
        self.screen.blit(self.title, (SCREEN_WIDTH/2-150, SCREEN_HEIGHT/2-100))
        self.screen.blit(self.press_start, (SCREEN_WIDTH/2-140, SCREEN_HEIGHT/2+100))
        game.draw_scores()
        pygame.display.flip()

###############################################################################

def build_blocks():
    N = 16
    colors = ['red', 'red', 'orange', 'orange', 'green', 'green', 'yellow', 'yellow']
    px = 39

    for i in range(N):
        py = 50
        for c in colors:
            block = Block(40, 10, px , py, pygame.Color(c))
            blocks_group.add(block)
            py += 25
        px += 59
        

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

# Score settings
score_font =  pygame.font.Font("freesansbold.ttf", 27)
ready_font =  pygame.font.Font("freesansbold.ttf", 48)

# Sounds
pong_sound = pygame.mixer.Sound('sounds/pong.mp3')
explosion_sound = pygame.mixer.Sound('sounds/pong.mp3')
fail_sound = pygame.mixer.Sound('sounds/fail.wav')
start_sound = pygame.mixer.Sound('sounds/intro.wav')



# Background
background = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])
background.fill(bg_color)

# Sprites
player_group = pygame.sprite.GroupSingle()
ball_group = pygame.sprite.GroupSingle()
blocks_group = pygame.sprite.Group()

ball = Ball(20,20,SCREEN_WIDTH//2,SCREEN_HEIGHT//2, light_grey, 6, player_group, blocks_group)
ball_group.add(ball)

player1 = Player(120,10,SCREEN_WIDTH//2 , SCREEN_HEIGHT - 50, light_grey, speed=8)
player_group.add(player1)


# Game scenes
intro = IntroScene()
game = Game_play(player_group, ball_group, blocks_group)


# Main loop
while True:
    while game.play == False:
        intro.update()
       
    game.update()
    clock.tick(60)
