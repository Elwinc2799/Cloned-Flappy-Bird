from time import sleep
import pygame
import random

pygame.init()
pygame.font.init()

# set game display size
WIDTH = 500
HEIGHT = 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# set background image
background = pygame.image.load('assets/background.jpg')

# set game title
pygame.display.set_caption("Flappy Bird")

# load bird image and set initial position
bird = pygame.image.load('assets/bird1.png')
bird_X = 50
bird_Y = 400
bird_Y_change = 0

# create obstacles
obstacles_width = 70
obstacles_height = random.randint(100,120)
obstacles_colour = (211,253,117)

obstacles_X_change = -2   # obstacles move from right to left on X-axis
obstacles_X = 500
obstacles_gap = 150

# load sound files
score_sound = pygame.mixer.Sound("assets/score.mp3")
game_over_sound = pygame.mixer.Sound("assets/gameover.mp3")

# define text colour profile
white = (255, 255, 255)
black = (0, 0, 0)

def display_score(score):
    font = pygame.font.Font('assets/Flappy-Bird.ttf', 40)
    score_text = "Total: " + str(score)
    text = font.render(score_text, False, black)
    screen.blit(text, (190, 200))

def display_bird(x,y):
    # create bird image
    screen.blit(bird, (x,y))

def display_obstacles(height):
    # create top obstacle
    pygame.draw.rect(screen, obstacles_colour, (obstacles_X, 0, obstacles_width, height))

    # find remaining height and create bottom obstacle
    bottom_obstacle_height = height + obstacles_gap
    pygame.draw.rect(screen, obstacles_colour, (obstacles_X, bottom_obstacle_height, obstacles_width, 550 - bottom_obstacle_height))

def detect_collision(x, height, bird_y, bottom_obstacle_height):
    # check whether the bird collides with the obstacle
    # bird starts at x-coord = 50 with a width of 85
    if x <= (50 + 85):
        # bird current height fall within the gap
        if bird_y <= height or bird_y >= (bottom_obstacle_height - 64):
            return True
    return False

run = True
score = 0
get_score = True

while run:
    screen.fill((0, 0, 0))

    # display the background image
    screen.blit(background, (0, 0))
    display_score(score)

    # detect for keyboard event
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_Y_change = -3
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                bird_Y_change = 3
    
    bird_Y += bird_Y_change

    if bird_Y <= 0:
        bird_Y = 0
    if bird_Y >= 484:
        bird_Y = 484

    # calculate new obstacle x-value
    obstacles_X += obstacles_X_change
    
    if obstacles_X <= -10:
        get_score = True
        obstacles_X = 500
        obstacles_height = random.randint(150, 350)

    display_obstacles(obstacles_height)

    collision = detect_collision(obstacles_X, obstacles_height, bird_Y, obstacles_height + obstacles_gap)
    
    if collision:
        pygame.mixer.Sound.play(game_over_sound)
        sleep(1)
        pygame.quit()
        break
    if obstacles_X <= bird_X and get_score:
        score += 1
        pygame.mixer.Sound.play(score_sound)
        get_score = False
    
    display_bird(bird_X, bird_Y)

    # render the game frame after each loop 
    pygame.display.update()

