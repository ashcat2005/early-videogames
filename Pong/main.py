'''
###############################################################################
 ______________________________________
|   ___  ___  ___  ___  ___  _____     |
|  | . || __|| | ||  _|| . ||_   _|    |
|  |   ||__ ||   || |_ |   |  | |      |
|  |_|_||___||_|_||___||_|_|  |_| 2022 |
|______________________________________|

PONG!
by Edward Larrañaga - 2022

###############################################################################

Sounds acknowledgement:

Open Treasure Chest 8 Bit.wav
Mrthenoronha. 
https://freesound.org/people/Mrthenoronha/sounds/519630/

Old Video Game 5
Enes DENİZ (sonically_sound). 
https://freesound.org/people/sonically_sound/sounds/624882/

Menu Select
pumodi. 
https://freesound.org/people/pumodi/sounds/150222/

Game Over
wolderado. 
https://freesound.org/people/wolderado/sounds/415096/

###############################################################################
'''


import pygame, sys, random

class Block(pygame.sprite.Sprite):
    '''
    General sprite class used for all objects in the game
    '''
    def __init__(self, width, height, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(light_grey)
        self.rect = self.image.get_rect(center = (pos_x, pos_y))


class Player(Block):
    '''
    Player sprite
    '''
    def __init__(self, width, height, pos_x, pos_y, speed):
        super().__init__(width, height, pos_x, pos_y)
        self.speed = speed
        self.delta_y = 0
    
    def constrains(self):
        if self.rect.top<=0:
            self.rect.top =0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    def reset(self):
        self.rect.center = (SCREEN_WIDTH -20 , SCREEN_HEIGHT//2)

    def update(self):
        self.constrains()
        self.rect.y += self.delta_y


class Opponent(Block):
    '''
    Opponent sprite
    '''
    def __init__(self, width, height, pos_x, pos_y, speed, ball):
        super().__init__(width, height, pos_x, pos_y)
        self.speed = speed
        self.delta_y = 0
        self.ball = ball
    
    def constrains(self):
        if self.rect.top<=0:
            self.rect.top =0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    def reset(self):
        self.rect.center = (20 , SCREEN_HEIGHT//2)
    
    def update(self):
        if self.ball.rect.top <= self.rect.centery:
            self.delta_y = -self.speed
        elif self.ball.rect.bottom >= self.rect.centery:
            self.delta_y = self.speed
        self.rect.y += self.delta_y


class Ball(Block):
    def __init__(self, width, height, pos_x, pos_y, speed, paddles):
        super().__init__(width, height, pos_x, pos_y)
        self.speed0 = speed
        self.speed = self.speed0
        self.delta_x = self.speed*random.choice((-1,1))
        self.delta_y = self.speed*random.choice((-1,1))
        self.paddles = paddles
    
    def collisions(self):
        if self.rect.top<=0 or self.rect.bottom >= SCREEN_HEIGHT:
            pygame.mixer.Sound.play(pong_sound)
            self.delta_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            pygame.mixer.Sound.play(pong_sound)
            paddle_col = pygame.sprite.spritecollide(self, self.paddles, False)[0]
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
        self.delta_x = self.speed*random.choice((-1,1))
        self.delta_y = self.speed*random.choice((-1,1))


class game_play():
    '''
    Game environment class. Controls the game.
    '''
    def __init__(self, ball_group, paddles_group, screen, gameplay=False):
        self.player1_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddles_group = paddles_group
        self.screen = screen
        self.ready = ready_font.render('READY', False, light_grey)
        self.ready3 = ready_font.render('3', False, light_grey)
        self.ready2 = ready_font.render('2', False, light_grey)
        self.ready1 = ready_font.render('1', False, light_grey)
        self.gameplay = gameplay

    def update(self):
        pygame.display.flip()
        self.screen.blit(background, [0,0])
        # Central line
        pygame.draw.aaline(screen, light_grey, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT))
        self.ball_group.sprite.update()
        for paddle in self.paddles_group:
            paddle.update()
        self.ball_group.draw(self.screen)
        self.paddles_group.draw(self.screen)
        self.draw_scores()
        self.goal()

    def reset(self):
        if self.opponent_score < 50 and self.player1_score < 50:
            self.ball_group.sprite.reset()
            for paddle in self.paddles_group:
                paddle.reset()
            self.ball_group.sprite.speed += 0.2
            self.count_in()
        else: 
            self.ball_group.sprite.reset()
            self.gameplay = False
    
    def new_game(self):
        self.opponent_score = 0
        self.player1_score = 0
        self.ball_group.sprite.speed = self.ball_group.sprite.speed0
        pygame.mixer.Sound.play(start_sound)
        self.goal_timer = pygame.time.get_ticks()
                
    def count_in(self):
        current_time = pygame.time.get_ticks()
        while current_time - self.goal_timer < 2700:
            self.screen.blit(background, [0,0])
            # Central line
            pygame.draw.aaline(screen, light_grey, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT))
            self.ball_group.draw(self.screen)
            self.paddles_group.draw(self.screen)
            self.draw_scores()
            self.screen.blit(self.ready, (SCREEN_WIDTH/2-85, SCREEN_HEIGHT/2-100))
            if current_time - self.goal_timer < 900:
                self.screen.blit(self.ready3, (SCREEN_WIDTH/4, SCREEN_HEIGHT/2))
                self.screen.blit(self.ready3, (3*SCREEN_WIDTH/4, SCREEN_HEIGHT/2))
            elif current_time - self.goal_timer < 1800:
                self.screen.blit(self.ready2, (SCREEN_WIDTH/4, SCREEN_HEIGHT/2))
                self.screen.blit(self.ready2, (3*SCREEN_WIDTH/4, SCREEN_HEIGHT/2))
            elif current_time - self.goal_timer < 2700:
                self.screen.blit(self.ready1, (SCREEN_WIDTH/4, SCREEN_HEIGHT/2))
                self.screen.blit(self.ready1, (3*SCREEN_WIDTH/4, SCREEN_HEIGHT/2))  
            current_time = pygame.time.get_ticks() 
            pygame.display.flip()
   
    def goal(self):
        if self.ball_group.sprite.rect.right >= SCREEN_WIDTH:
            self.opponent_score += 10
            self.goal_timer = pygame.time.get_ticks()
            pygame.mixer.Sound.play(fail_sound)
            self.reset()

        if self.ball_group.sprite.rect.left <= 0:
            self.player1_score += 10
            self.goal_timer = pygame.time.get_ticks()
            pygame.mixer.Sound.play(win_sound)
            self.reset()

    def draw_scores(self):
        opponent_text = score_font.render(f'{self.opponent_score}', False, light_grey)
        self.screen.blit(opponent_text, (SCREEN_WIDTH//4, 10))
        player1_text = score_font.render(f'{self.player1_score}', False, light_grey)
        self.screen.blit(player1_text, (3*SCREEN_WIDTH//4, 10))





class intro_screen():
    '''
    Intro environment class. Control the intro screen
    '''
    def __init__(self, screen):
        pong_font =  pygame.font.Font("freesansbold.ttf", 100)
        self.pong = ready_font.render('PONG!', False, light_grey)
        self.press_start = score_font.render('Press SPACE to start', False, light_grey)
        self.screen = screen
    
    def draw(self):
        self.screen.blit(background, [0,0])
        self.screen.blit(self.pong, (SCREEN_WIDTH/2-80, SCREEN_HEIGHT/2-100))
        self.screen.blit(self.press_start, (SCREEN_WIDTH/2-140, SCREEN_HEIGHT/2+100))
        game.draw_scores()
        pygame.display.flip()




###############################################################################

# Inizialization
pygame.init()
clock = pygame.time.Clock()

# Screen settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong!')

# Colors
bg_color = pygame.Color('gray12')
light_grey = (200,200,200)

background = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])
background.fill(bg_color)

# Sprites
paddles_group = pygame.sprite.Group()
ball_group = pygame.sprite.GroupSingle()

ball = Ball(20,20,SCREEN_WIDTH//2,SCREEN_HEIGHT//2, 8, paddles_group)
ball_group.add(ball)

player1 = Player(10,120,SCREEN_WIDTH -20 , SCREEN_HEIGHT//2, 7)
opponent = Opponent(10,120, 20 , SCREEN_HEIGHT//2, 7, ball)
paddles_group.add(player1,opponent)

# Sounds
start_sound = pygame.mixer.Sound('sounds/intro.wav')
win_sound = pygame.mixer.Sound('sounds/win.wav')
fail_sound = pygame.mixer.Sound('sounds/fail.wav')
pong_sound = pygame.mixer.Sound('sounds/pong.mp3')

# Score settings
score_font =  pygame.font.Font("freesansbold.ttf", 27)
ready_font =  pygame.font.Font("freesansbold.ttf", 48)


# Intro environment
intro = intro_screen(screen)

# Game evironment
game = game_play(ball_group, paddles_group, screen, gameplay=False)



###############################################################################

# Main loop
while True:

    while game.gameplay == False:
        # Intro Update
        intro.draw()
        game.draw_scores()
        # Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.new_game()
                    game.gameplay = True
                    game.reset()


    # Handling events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player1.delta_y = -player1.speed
            elif event.key == pygame.K_DOWN:
                player1.delta_y = player1.speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player1.delta_y = 0
    
        
    # Game Update
    game.update()
    clock.tick(60)
