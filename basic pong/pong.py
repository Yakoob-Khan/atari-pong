# Author: Yakoob Khan
# Date: 01/30/2018
# Lab Assignment 1
# A program for the basic game of pong

from cs1lib import *

# GLOBAL CONSTANTS
WIDTH_PADDLE = 20
HEIGHT_PADDLE = 80
WIDTH_WINDOW = 400
HEIGHT_WINDOW = 400
PADDLE_MOVEMENT = 10    # amount by which paddles moves vertically
X_LEFT = 0              # x coordinate of left paddle
X_RIGHT = WIDTH_WINDOW - WIDTH_PADDLE     # x coordinate of right paddle
BALL_RADIUS = 9
BALL_SPEED = 4


# Global variables
y_l = 150     # y coordinate of left paddle (top left corner)
y_r = 150     # y coordinate of right paddle (top left corner)
x = 200       # x coordinate of center of ball
y = 200       # y coordinate of center of ball
xd = 1        # horizontal direction component of ball
yd = 1        # vertical direction component of ball


z = False     # boolean for downward movement of left paddle
a = False     # boolean for upward movement of left paddle
k = False     # boolean for upward movement of right paddle
m = False     # boolean for downward movement of right paddle


# Function for background color
def background_color():
    # Set background color to black
    clear()
    set_fill_color(0, 0, 0)     # sets color to black
    draw_rectangle(0, 0, WIDTH_WINDOW, HEIGHT_WINDOW)


# Function to draw left paddle
def left_paddle():
    disable_stroke()
    set_fill_color(0, 0.8, 1)     # set paddle color to light blue
    draw_rectangle(X_LEFT, y_l, WIDTH_PADDLE, HEIGHT_PADDLE)


# Function to draw right paddle
def right_paddle():
    disable_stroke()
    set_fill_color(0, 0.8, 1)     # set paddle color to light blue
    draw_rectangle(X_RIGHT, y_r, WIDTH_PADDLE, HEIGHT_PADDLE)


# Function for pong ball
def ball():
    global x, y
    disable_stroke()
    set_fill_color(0, 1, 0)             # set ball color to green
    draw_circle(x, y, BALL_RADIUS)

    x = x + xd * BALL_SPEED             # horizontal movement of ball

    # Vertical movement of ball is multiplied by 2
    # to make ball movement more interesting
    y = y + yd * 2 * BALL_SPEED


# Function when ball collides with bottom wall
def collision_bottom():
    global yd
    if y > HEIGHT_WINDOW - BALL_RADIUS:
        yd = - yd           # changes vertical direction of ball


# Function when ball collides with top wall
def collision_top():
    global yd
    if y < BALL_RADIUS:
        yd = - yd          # changes vertical direction of ball


# Function when ball collides with the right paddle
def collision_right():
    global xd, yd
    # If paddle misses, stop when ball hits the right wall
    if x > WIDTH_WINDOW - BALL_RADIUS:
        xd = 0                          # stops ball
        yd = 0

    # When ball collides with the paddle,
    # we want to change ball direction when ball just touches
    # the right paddle and is within the vertical range of the paddle.
    # Vertical range of y is within 3 times ball radius to enable ball
    # to bounce off paddle corners well.

    if x > (X_RIGHT - BALL_RADIUS) and \
            (y_r - 3 * BALL_RADIUS < y < y_r + HEIGHT_PADDLE + 3 * BALL_RADIUS):
        xd = - xd                        # changes horizontal direction of ball


# Function when ball collides with left paddle
def collision_left():
    global xd, yd
    # If paddle misses, stop when ball hits the left wall
    if x < BALL_RADIUS:
        xd = 0                          # stops ball if it hits left wall
        yd = 0

    # If ball collides with the paddle,
    # we want to change ball direction when ball just touches
    # the right paddle and is within the vertical range of the paddle.
    # Vertical range of y is within 3 times ball radius to enable ball
    # to bounce off paddle corners well.

    if x < (WIDTH_PADDLE + BALL_RADIUS) and \
            (y_l - 3 * BALL_RADIUS < y < y_l + HEIGHT_PADDLE + 3 * BALL_RADIUS):
        xd = - xd                       # changes horizontal direction of ball


# Function for when keys are pressed. Returns booleans.
def press(key):
    global y_l, y_r, z, a, k, m, x, y, xd, yd

    if is_key_pressed("z"):
        z = True

    if is_key_pressed("a"):
        a = True

    if is_key_pressed("k"):
        k = True

    if is_key_pressed("m"):
        m = True

    # To start a new game
    if key == " ":
        x = 200                   # Reposition ball at center of window
        y = 200
        xd = 1                    # Reset initial direction of ball
        yd = 1

    if key == "q":                # to quit the program
        cs1_quit()


# Function for when keys are released
def release(key):
    global a, z, k, m

    # Allows both paddles to move at the same time
    if not is_key_pressed("a"):
        a = False

    if not is_key_pressed("z"):
        z = False

    if not is_key_pressed("k"):
        k = False

    if not is_key_pressed("m"):
        m = False


# Main draw function that calls the above functions
def draw():
    global y_l, y_r 

    background_color()      # Set background color
    left_paddle()           # Draw left paddle
    right_paddle()          # Draw right paddle

    # Use booleans and if conditions to control movement of paddles
    # Second part of if condition prevents paddle from leaving the window.
    if z and y_l < (HEIGHT_WINDOW - HEIGHT_PADDLE):
        y_l += PADDLE_MOVEMENT

    if a and y_l > 0:
        y_l -= PADDLE_MOVEMENT

    if k and y_r > 0:
        y_r -= PADDLE_MOVEMENT

    if m and y_r < (HEIGHT_WINDOW - HEIGHT_PADDLE):
        y_r += PADDLE_MOVEMENT

    # Draw ball
    ball()

    # Check for collisions with the four walls,
    # adjusting ball movement accordingly.
    collision_bottom()
    collision_top()
    collision_right()
    collision_left()

start_graphics(draw, key_press=press, key_release=release)
