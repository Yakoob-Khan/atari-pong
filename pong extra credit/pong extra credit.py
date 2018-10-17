# Author: Yakoob Khan
# Date: 01/30/2018
# Lab Assignment 1
# A program for the game of pong
# Extra credit version

from cs1lib import *
from random import randint

# GLOBAL CONSTANTS
WIDTH_PADDLE = 20
HEIGHT_PADDLE = 80
WIDTH_WINDOW = 400
HEIGHT_WINDOW = 400
PADDLE_MOVEMENT = 10    # amount by which paddles moves vertically
X_LEFT = 0              # x coordinate of left paddle
X_RIGHT = WIDTH_WINDOW - WIDTH_PADDLE     # x coordinate of right paddle
BALL_RADIUS = 9

# For loading images of left and right paddles
DARTMOUTH = load_image("Dartmouth.png")
YALE = load_image("Yale.png")

# Global variables
y_l = 150     # y coordinate of left paddle (top left corner)
y_r = 150     # y coordinate of right paddle (top left corner)
x = 200       # x coordinate of center of ball
y = 200       # y coordinate of center of ball
xd = 1        # horizontal direction component of ball
yd = 1        # vertical direction component of ball
r = 1         # red color component of ball
g = 1         # green color component of ball
b = 0         # blue color component of ball
d = 1         # for changing sign of vertical and horizontal components of the ball
ran = 1       # for randomizing initial direction of ball

z = False     # boolean for downward movement of left paddle
a = False     # boolean for upward movement of left paddle
k = False     # boolean for upward movement of right paddle
m = False     # boolean for downward movement of right paddle

dartmouth_score = 0     # Ser initial score to 0 : 0
yale_score = 0
check_goal = False      # boolean used in goal function
ball_speed = 4

# Booleans to accelerate the ball slightly if ball hits moving paddle
left_move = False
right_move = False


# Function for drawing background structures.
# Contains background color, court lines and score board
def background():
    # Set background color to black
    clear()
    set_fill_color(0, 0, 0)             # set color to black
    draw_rectangle(0, 0, WIDTH_WINDOW, HEIGHT_WINDOW)

    # Draw center and halfway line of court
    set_fill_color(1, 1, 1)             # set color to white
    draw_rectangle(200, 0, 3, 400)      # draws halfway line
    draw_circle(200, 200, 30)           # draws a big white circle in the middle
    set_fill_color(0, 0, 0)             # sets color to black

    # Draws a slightly smaller black circle to create a ring in the center
    draw_circle(200, 200, 28)

    # Text for the scores of the two players
    set_stroke_color(1, 1, 1)           # sets color to white
    enable_stroke()
    set_font_size(26)
    set_font("Times New Roman")
    draw_text("Dartmouth", 75, 30)
    draw_text("Yale", 250, 30)
    draw_text(str(dartmouth_score), 125, 60)  # score of Dartmouth
    draw_text(str(yale_score), 270, 60)       # score of Yale


# Function to draw left paddle
def left_paddle():
    disable_stroke()
    draw_image(DARTMOUTH, X_LEFT, y_l)


# Function to draw right paddle
def right_paddle():
    disable_stroke()
    draw_image(YALE, X_RIGHT, y_r)


# Function for pong ball
def ball():
    global x, y
    disable_stroke()
    set_fill_color(r, g, b)              # set color of ball
    draw_circle(x, y, BALL_RADIUS)       # draws the ball
    x = x + xd * ball_speed              # horizontal movement of ball

    # vertical movement of ball is multiplied by 2 so that ball movement
    # becomes more interesting
    y = y + yd * 2 * ball_speed


def random_bounce():
    global d, xd, yd
    d = -d
    num = randint(1, 4)     # creates unpredictable bounce

    if num == 1:            # bounces ball back to hitter (25% chance)
        yd = d * yd
        xd = d * xd
    else:
        yd = d * yd         # bounces ball normally


# Function for when ball collides with bottom wall
def collision_bottom():
    if y > HEIGHT_WINDOW - BALL_RADIUS:
        random_bounce()


# Function when ball collides with top wall
def collision_top():
    if y < BALL_RADIUS:
        random_bounce()


# Function for when ball collides with right paddle
def collision_right():
    global x, xd, yd, ball_speed, r, g, b, d, dartmouth_score, check_goal
    # If paddle misses, stop ball when it hits the right wall
    if x > WIDTH_WINDOW - BALL_RADIUS:
        xd = 0
        yd = 0
        dartmouth_score += 1                    # Update score of Dartmouth
        check_goal = True                       # boolean to flash GOAL!
        x = WIDTH_WINDOW - BALL_RADIUS          # Makes if condition False

    # If ball collides with the paddle,
    # we want to change ball direction when ball just touches
    # the right paddle and is within the vertical range of the paddle.
    #  Vertical range of y is within 3 times ball radius to enable ball
    # to bounce off paddle corners well.

    if x > (X_RIGHT - BALL_RADIUS) \
            and (y_r - 3 * BALL_RADIUS < y < y_r + HEIGHT_PADDLE + 3 * BALL_RADIUS):
        d = -d
        xd = d * xd

        # If paddles moves when hitting ball, accelerate ball slightly
        if right_move:
            ball_speed += 0.2

        # Changes ball color to green every time paddle hits
        r = 0
        g = 1
        b = 0


# Function when ball collides with left paddle
def collision_left():
    global x, xd, yd, ball_speed, r, g, b, d, yale_score, check_goal
    # If paddle misses, stop ball when it hits the left wall
    if x < BALL_RADIUS:
        xd = 0
        yd = 0
        yale_score = yale_score + 1         # Update score of Yale
        check_goal = True                   # boolean to flash GOAL!
        x = BALL_RADIUS                     # Makes if condition False

    # If ball collides with the paddle,
    # we want to change ball direction when ball just touches
    # the right paddle and is within the vertical range of the paddle.
    # Vertical range of y is within 3 times ball radius to enable ball
    # to bounce off paddle corners well.

    if x < (WIDTH_PADDLE + BALL_RADIUS) \
            and (y_l - 3 * BALL_RADIUS < y < y_l + HEIGHT_PADDLE + 3 * BALL_RADIUS):
        d = -d
        xd = d * xd

        # If paddles moves when hitting ball, accelerate ball slightly
        if left_move:
            ball_speed += 0.2

        # Changes ball color to red every time it hits the paddle
        r = 1
        g = 0
        b = 0


# Function for when keys are pressed. Returns booleans.
def press(key):
    global x, y, xd, yd, z, a, k, m,\
        ball_speed, d, check_goal, ran, left_move, right_move

    if is_key_pressed("z"):
        z = True
        left_move = True

    if is_key_pressed("a"):
        a = True
        left_move = True

    if is_key_pressed("k"):
        k = True
        right_move = True

    if is_key_pressed("m"):
        m = True
        right_move = True

    # To start a new game
    if key == " ":
        x = 200                 # Resets position of ball at the center of window
        y = 200
        check_goal = False      # boolean for goal function
        d = 1
        ball_speed = 4          # Resets ball speed
        left_move = False
        right_move = False

        # Randomize the initial direction of the ball
        ran = randint(1, 4)
        # Ball goes towards bottom right-hand corner of window
        if ran == 1:
            xd = d * 1
            yd = d * 1
        # Ball goes towards upper left-hand corner of window
        if ran == 2:
            xd = -d * 1
            yd = -d * 1
        # Ball goes towards upper right-hand corner of window
        if ran == 3:
            xd = d * 1
            yd = -d * 1
        # Ball goes towards bottom left-hand corner of window
        if ran == 4:
            xd = -d * 1
            yd = d * 1

    # To quit the program
    if key == "q":
        cs1_quit()


# Function for when keys are released. Sets booleans to False.
def release(key):
    global a, z, k, m, left_move, right_move

    if not is_key_pressed("a"):
        a = False
        left_move = False

    if not is_key_pressed("z"):
        z = False
        left_move = False

    if not is_key_pressed("k"):
        k = False
        right_move = False

    if not is_key_pressed("m"):
        m = False
        right_move = False


# Function for flashing the word GOAL! whenever a Team scores
def goal():
    global check_goal

    if check_goal:
        enable_stroke()
        set_stroke_color(1, 0, 0)           # Sets stroke color to red
        set_font("Times New Roman")
        set_font_size(52)
        # Flashes GOAL! in the center of the window
        draw_text("GOAL!", 120, 220)


# Main draw function that calls the above functions
def draw():
    global y_l, y_r

    background()        # Set background color
    left_paddle()       # Draw left paddle
    right_paddle()      # Draw right paddle

    # If conditions to move the paddles.
    # Second part of if condition prevents the paddle
    # from leaving the window.
    if z and y_l < 320:
        y_l += PADDLE_MOVEMENT

    if a and y_l > 0:
        y_l -= PADDLE_MOVEMENT

    if k and y_r > 0:
        y_r -= PADDLE_MOVEMENT

    if m and y_r < 320:
        y_r += PADDLE_MOVEMENT

    # Draw ball
    ball()

    # Check for collisions with the four walls,
    # adjusting ball movement accordingly.
    collision_bottom()
    collision_top()
    collision_right()
    collision_left()

    # Check if goal has occurred
    goal()


start_graphics(draw, key_press=press, key_release=release)
