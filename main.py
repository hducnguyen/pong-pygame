from random import randint
from re import X
import sys
from tkinter.tix import WINDOW
from turtle import left
import pygame as pg
from pygame.locals import(

    K_UP,
    K_DOWN,
    K_w,
    K_s
)


# The line below is to initiate Pygame
pg.init()

# Set up game's window
WINDOW_W = 1000
WINDOW_H = 800 

window = pg.display.set_mode((WINDOW_W, WINDOW_H)) # Window display

# Importing all the sound needed
pong_sound = pg.mixer.Sound("pong_sound.mp3")
score_sound = pg.mixer.Sound("score_sound.mp3")
victory_sound = pg.mixer.Sound("victory_sound.mp3")
sound = [pong_sound, score_sound, victory_sound]

# Name the program application tab to be Pong
pg.display.set_caption("Pong")

# Initiate the clock
clock = pg.time.Clock()

# Get the font
font = pg.font.Font(pg.font.get_default_font(), 36)

# Initiate the paddle dimension
PADDLE_WIDTH = 15 
PADDLE_HEIGHT = 60

paddle_speed = 5 # Choose the paddle speed

# Setup the spawning spot for the objects
# Left paddle
left_x = 10
left_y = WINDOW_H/2 - 10

# Right paddle
right_x = 975
right_y = WINDOW_H/2 - 10

rect_y = 20

# Ball
ballz_x = WINDOW_W/2
ballz_y = WINDOW_H/2

# Random the ball's initial trajectory
x_direction = randint(1, 1)
y_direction = randint(-1, 1)

# Set up the score system
left_score = 0
right_score = 0
left_score_text = font.render(str(left_score), True, (200, 200, 200))
right_score_text = font.render(str(right_score), True, (200, 200, 200))

# random the  ball's initial trjectory without it being straight up or fully horizontal 
while (x_direction == 0) or (y_direction == 0):
    x_direction = randint(-1, 1)
    y_direction = randint(-1, 1)

def game_quit():
    global ballz_x, ballz_y

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.KEYDOWN:

            # Set up for the players. If the ESC key is pressed, quit game
            if event.key == pg.K_ESCAPE:
                sys.exit()

def movement ():
    global right_y, left_y
    keys_pressed = pg.key.get_pressed()

    # Code for right paddle's movement based on user input
    if keys_pressed[K_DOWN]:
        if right_y < WINDOW_H - PADDLE_HEIGHT:
            right_y += paddle_speed
        elif right_y >= WINDOW_H - PADDLE_HEIGHT:
            right_y = WINDOW_H - PADDLE_HEIGHT
    if keys_pressed[K_UP]:
        if right_y > 0:
            right_y -= paddle_speed
        elif right_y < 0:
            right_y = 0
    
    # Code for left paddle's movement based on user input
    if keys_pressed[K_w]:
        if left_y > 0:
            left_y -= paddle_speed
        elif left_y < 0:
            left_y = 0
    if keys_pressed[K_s]:
        if left_y <= WINDOW_H - PADDLE_HEIGHT:
            left_y += paddle_speed
        elif left_y > WINDOW_H - PADDLE_HEIGHT:
            left_y = WINDOW_H - PADDLE_HEIGHT    
                    
def draw_and_color ():
    # Color the background with black
    window.fill((0,0,0))

    # Left paddle
    pg.draw.rect(
        window,
        (0,0,255),
        pg.Rect(left_x, left_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    )

    # Right paddle
    pg.draw.rect(
        window,
        (255,0,0),
        pg.Rect(right_x, right_y, PADDLE_WIDTH,PADDLE_HEIGHT)
    )

    # Draw the middle line seperating the two sides
    for i in range(20):
        pg.draw.rect(
            window,
            (255,255,255),
            pg.Rect(500-2.5, rect_y*i*2+10, 5, 30)
        )
    
    # Draw the ball 
    pg.draw.circle(
        window,
        (100,30,255),
        (ballz_x,ballz_y),
        10
    )

def score ():
    # Displace the score of two players
    window.blit(left_score_text, dest=(50, 40))
    window.blit(right_score_text, dest=(WINDOW_W - 80, 40))

def collision ():
    global ballz_x, ballz_y, x_direction, y_direction
    global left_score, right_score, left_score_text, right_score_text

    # Collision check with the left and right paddles
    if (ballz_x > left_x) and (ballz_x < left_x + PADDLE_WIDTH) and (ballz_y > left_y) and (ballz_y < left_y + PADDLE_HEIGHT):
        x_direction = -x_direction
        sound[0].play()

    if (ballz_x > right_x) and (ballz_x < right_x + PADDLE_WIDTH) and (ballz_y > right_y) and (ballz_y < right_y + PADDLE_HEIGHT):
        x_direction = -x_direction
        sound[0].play()

    if ballz_y < 0 or ballz_y > WINDOW_H:
        y_direction = -y_direction
        sound[0].play()
    
    ballz_x += (x_direction * 2)
    ballz_y += (y_direction * 2)

    if ballz_x >  WINDOW_W:
        left_score += 1
        # print(left_score)
        ballz_x = WINDOW_W/2
        ballz_y = WINDOW_H/2
        x_direction = -x_direction
        left_score_text = font.render(str(left_score), True, (200, 200, 200))
        score_sound.play()

    elif ballz_x < 0:
        right_score += 1
        # print(right_score)
        ballz_x = WINDOW_W/2
        ballz_y = WINDOW_H/2
        x_direction = -x_direction
        right_score_text = font.render(str(right_score), True, (200, 200, 200))
        score_sound.play()

while True:
    game_quit()

    movement()

    draw_and_color()
   
    score()

    collision()

    # Victory condition for 2 players. If the score of any player reaches 5, the game ends
    if left_score == 5 or right_score == 5:
        ballz_x = WINDOW_W / 2
        ballz_y = WINDOW_H/2
        ballz_x += 0
        ballz_y += 0
        victory_sound.play()

    # Limiting the updating rate
    clock.tick(144)
    
    # Update the frame
    pg.display.flip()