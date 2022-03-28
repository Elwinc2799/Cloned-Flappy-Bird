# Cloned-Flappy-Bird

Flappy bird is a mobile game developed by Vietnamese video game artist and programmer, Dong Nguyenm, under his game development company, Gears. The cloned flappy bird game starts with a bird floating in the air, and the user can control the bird by clicking spacebar to elevate and releasing the space bar to descent. The target of the game is to score as high as possible without colliding with the upcoming green bar.

- built using Python with [Pygame](https://www.pygame.org/news).

### Initialize library

```python
from time import sleep
import pygame
import random
```

Pygame contains the core library to build this cloned flappy bird game, together with Time to set some time delay and Random to randomly generate the heights for the upcoming green bars.

### Set display size, background image and game title

```python
# set game display size
WIDTH = 500
HEIGHT = 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# set background image
background = pygame.image.load('background.jpg')

# set game title
pygame.display.set_caption("Flappy Bird")
```

### Load bird image and set initial position

```python
bird = pygame.image.load('bird1.png')
bird_X = 50
bird_Y = 400
bird_Y_change = 0
```

`bird_X` and `bird_Y` are initialized to the initial floating x-value and y-value of the bird.
✨ Note that y-value starts from top to bottom.

### Set the width, random height and colour of obstacles

```python
obstacles_width = 70
obstacles_height = random.randint(100,120)
obstacles_colour = (211,253,117)

obstacles_X_change = -2 # obstacles move from right to left on X-axis
obstacles_X = 500
obstacles_gap = 150
```

### Display the score of the game

```python
def display_score(score):
	font = pygame.font.Font('Flappy-Bird.ttf', 40)
	score_text = "Total: " + str(score)
	text = font.render(score_text, False, black)
	screen.blit(text, (190, 200))
```

`Flappy-Bird.ttf` font file is used for the score text.

### Display the obstacles

```python
def display_obstacles(height):
	# create top obstacle
	pygame.draw.rect(screen, obstacles_colour, (obstacles_X, 0, obstacles_width, height))

	# find remaining height and create bottom obstacle
	bottom_obstacle_height = height + obstacles_gap
	pygame.draw.rect(screen, obstacles_colour, (obstacles_X, bottom_obstacle_height, obstacles_width, 550 - bottom_obstacle_height))
```

To calculate the height of the bottom obstacle, we can compute `height + obstacles_gap` where `height` = top obstacle's height.

### Detect collision function

```python
def detect_collision(x, height, bird_y, bottom_obstacle_height):
	# check whether the bird collides with the obstacle
	# bird starts at x-coord = 50 with a width of 85
	if x <= (50 + 85):
		# bird current height fall within the gap
		if bird_y <= height or bird_y >= (bottom_obstacle_height - 64):
				return True
	return False
```

A nested if-else statement is used, with the 1st if statement checking on obstacle's x-value <= the bird's rigthmost tip, and the 2nd if statement checking on `bird_y` <= `height` (top obstacle's height) or >= `bottom_obstacle_height - 64` (bottom obstacle's height + obstacle's gap size). If both statement are true, collision is detected and the function will return `True`.

### Rendering of the gameplay

A while-loop is used to initiate the rendering of the gameplay. Some key aspects inside the while-loop are:

1. detect keyboard event

```python
# detect for keyboard event
for event in pygame.event.get():
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_SPACE:
			bird_Y_change = -3

	if event.type == pygame.KEYUP:
		if event.key == pygame.K_SPACE:
			bird_Y_change = 3
```

`pygame.KEYDOWN` and `pygame.KEYUP` are used to detect the click down and release of the spacebar event, changing the `bird_Y_change` value respectively.

2. calculate location of obstacles

```python
# calculate new obstacle x-value
obstacles_X += obstacles_X_change
if obstacles_X <= -10:
	get_score = True
	obstacles_X = 500
	obstacles_height = random.randint(150, 350)
```

If `obstacles_X <= -10`, meaning it exceeds the limit of the leftmost of the screen, a new obstacle is generated with a random height.

3. detect collision

```python
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
```

If the `collision` is true, the game will play the loaded game over sound and quit the game. For each `obstacles_X <= bird_X` and `get_score` is true (indicating the obstacle reaches the leftmost of the screen, `score` is increment and a score sound is played.
