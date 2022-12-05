
import pygame, sys
from numpy.random import choice

def ball_motion():
    global ball_speed_x, ball_speed_y
    global player1_score, player2_score
    global goal_timer

    # Motion
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Collisions
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    if ball.left <= 0:
        player2_score +=10
        pygame.mixer.Sound.play(fail_sound)
        goal_timer = pygame.time.get_ticks()

    if ball.right>= SCREEN_WIDTH:
        player1_score +=10
        pygame.mixer.Sound.play(win_sound)
        goal_timer = pygame.time.get_ticks()
    
    if ball.colliderect(player1) and ball_speed_x < 0: 
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_x *= -1
    
    if ball.colliderect(player2) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_x *= -1


def player1_motion():
    player1.y += player1_speed   
    if player1.top <= 0: player1.top = 0
    if player1.bottom >= SCREEN_HEIGHT: player1.bottom = SCREEN_HEIGHT


def AI_player_motion():
    global player2_speed
    if ball.top <= player2.centery:
        player2_speed = -6
    elif ball.bottom >= player2.centery:
        player2_speed = 6
    
    player2.y += player2_speed
    player2_speed = 0
    if player2.top <= 0: player2.top = 0
    if player2.bottom >= SCREEN_HEIGHT: player2.bottom = SCREEN_HEIGHT


def reset_game():
    global ball_speed_x, ball_speed_y, v_max
    global goal_timer
    player1.centery = SCREEN_HEIGHT/2 
    player2.centery = SCREEN_HEIGHT/2
    ball.center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
    current_time = pygame.time.get_ticks()
    ready = ready_font.render('READY', False, light_grey)
    ready3 = ready_font.render('3', False, light_grey)
    ready2 = ready_font.render('2', False, light_grey)
    ready1 = ready_font.render('1', False, light_grey)
    if current_time - goal_timer < 900:
        screen.blit(ready, (SCREEN_WIDTH/2-85, SCREEN_HEIGHT/2-100))
        screen.blit(ready3, (SCREEN_WIDTH/4, SCREEN_HEIGHT/2))
        screen.blit(ready3, (3*SCREEN_WIDTH/4, SCREEN_HEIGHT/2))
    elif current_time - goal_timer < 1800:
        screen.blit(ready, (SCREEN_WIDTH/2-85, SCREEN_HEIGHT/2-100))
        screen.blit(ready2, (SCREEN_WIDTH/4, SCREEN_HEIGHT/2))
        screen.blit(ready2, (3*SCREEN_WIDTH/4, SCREEN_HEIGHT/2))
    elif current_time - goal_timer < 2700:
        screen.blit(ready, (SCREEN_WIDTH/2-85, SCREEN_HEIGHT/2-100))
        screen.blit(ready1, (SCREEN_WIDTH/4, SCREEN_HEIGHT/2))
        screen.blit(ready1, (3*SCREEN_WIDTH/4, SCREEN_HEIGHT/2))

    if current_time - goal_timer < 2700:
        ball_speed_x = 0
        ball_speed_y = 0
    else:
        v_max += 0.2
        ball_speed_x = v_max*choice([1.1,-1.1])
        ball_speed_y = v_max*choice([1.1,-1.1])
        goal_timer = None

# Inizialization
pygame.mixer.pre_init()
pygame.init()
clock = pygame.time.Clock()

# Screen settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong!')

# Score settings
player1_score = 0
player2_score = 0
score_font =  pygame.font.Font("freesansbold.ttf", 24)
ready_font =  pygame.font.Font("freesansbold.ttf", 48)

# Setup
ball = pygame.Rect(SCREEN_WIDTH/2 -10, SCREEN_HEIGHT/2 -10, 20, 20)
player1 = pygame.Rect(10, SCREEN_HEIGHT/2 - 60, 10, 120)
player2 = pygame.Rect(SCREEN_WIDTH -20, SCREEN_HEIGHT/2 - 60, 10, 120)

# Game variables
v_max = 6
ball_speed_x = v_max *choice([1,-1])
ball_speed_y = v_max *choice([1,-1])
player1_speed = 0
player2_speed = 0

# Colors
bg_color = pygame.Color('gray12')
light_grey = (200,200,200)

# Time variables
goal_timer = True

# Sounds
start_sound = pygame.mixer.Sound('intro.wav')
win_sound = pygame.mixer.Sound('win.wav')
fail_sound = pygame.mixer.Sound('fail.wav')
pong_sound = pygame.mixer.Sound('pong.mp3')

# Intro - play
intro = True

def play_intro():
    global intro, player1_score, player2_score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.mixer.Sound.play(start_sound)  
                player1_score = 0
                player2_score = 0  
                intro = False
      
    # Visuals
    screen.fill(bg_color)
    pygame.draw.aaline(screen, light_grey, (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT))
    pygame.draw.rect(screen, light_grey, player1)
    pygame.draw.rect(screen, light_grey, player2)
    pygame.draw.rect(screen, light_grey, ball)
    player1_text = score_font.render(f'{player1_score}', False,light_grey)
    screen.blit(player1_text, (SCREEN_WIDTH/4, 10))

    player2_text = score_font.render(f'{player2_score}', False,light_grey)
    screen.blit(player2_text, (3*SCREEN_WIDTH/4, 10))
    # Update
    pygame.display.flip()
    clock.tick(60)
    

# Main loop
while True:
    while intro:
        play_intro()

    # Handling events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player1_speed = -6
            elif event.key == pygame.K_DOWN:
                player1_speed = +6

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player1_speed = 0
    
    # All Motion
    ball_motion()
    player1_motion()
    AI_player_motion()


    # Visuals
    screen.fill(bg_color)
    pygame.draw.aaline(screen, light_grey, (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT))
    
    pygame.draw.rect(screen, light_grey, player1)
    pygame.draw.rect(screen, light_grey, player2)
    pygame.draw.rect(screen, light_grey, ball)
    
    player1_text = score_font.render(f'{player1_score}', False,light_grey)
    screen.blit(player1_text, (SCREEN_WIDTH/4, 10))

    player2_text = score_font.render(f'{player2_score}', False,light_grey)
    screen.blit(player2_text, (3*SCREEN_WIDTH/4, 10))

    if goal_timer:
        reset_game()
    
    if player1_score > 50 or player2_score > 50:
        intro = True

    # Update
    pygame.display.flip()
    clock.tick(60)
