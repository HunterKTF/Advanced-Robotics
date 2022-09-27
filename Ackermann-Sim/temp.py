import pygame
import math
import sys

from colors import *
from pygame.locals import *


# Initialize game
pygame.init()

# Initialize joysticks
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# Set fonts
title = pygame.font.SysFont("consolas", 15)
speed = pygame.font.SysFont("consolas", 15)
delta_t = pygame.font.SysFont("consolas", 15)
delta_f_incr = pygame.font.SysFont("consolas", 15)
lb = pygame.font.SysFont("consolas", 15)
lf = pygame.font.SysFont("consolas", 15)
coord = pygame.font.SysFont("consolas", 12)

# Set window size (x, y)
size = (1000, 700)

# Set pygame screen
screen = pygame.display.set_mode(size, 0, 32)
clock = pygame.time.Clock()
pygame.display.set_caption('Ackerman Simulation')

# Movement test
my_square = pygame.Rect(15, 15, 15, 15)
my_square_color = 0
colors = [RED, GREEN, BLUE]
motion = [500, 350]
dis = [[500, 350]]

# Polygon test
my_triangle = ((motion[0],motion[1]+7),(motion[0],motion[1]-7),(motion[0]+11,motion[1]))

# Square starting position
my_square.x = motion[0]
my_square.y = motion[1]

# Initialize variables
const = 0 # Linear momentum
constRot = 0 # Angular momentum
prevRot = 0
rev_x = 0
rev_y = 0

# Mapping values (right trigger)
leftMax = 1
leftMin = -1.000030518509476
rightMax = 10
rightMin = 0

# Mapping values (left joystick)
leftMaxJ = 1
leftMinJ = -1.000030518509476
delta_f = 6
rightMaxJ = math.radians(delta_f)
rightMinJ = math.radians(-delta_f)

# Upload settings
pygame.display.update()


# Initialize screen
while True:

    screen.fill(BLACK)

    # Draws tracing line
    if [my_triangle[0][0], my_triangle[0][1]-7] not in dis:
        dis.append([my_triangle[0][0], my_triangle[0][1]-7])
    
    for x in dis:
        pygame.draw.rect(screen,GREEN,[x[0], x[1], 5, 5])
        # print(dis)

    # Font box
    value = title.render("CONFIG PARAMS:", True, RED)
    screen.blit(value, [10, 10])

    value = speed.render("Speed: " + str(const) + " km/h", True, RED)
    screen.blit(value, [10, 30])

    value = speed.render("Delta T: " + str(0.05), True, RED)
    screen.blit(value, [10, 50])

    value = speed.render("Delta f increment: " + str(delta_f) + " deg", True, RED)
    screen.blit(value, [10, 70])

    value = speed.render("Lb: " + str(1.2) + " m", True, RED)
    screen.blit(value, [10, 90])

    value = speed.render("Lf: " + str(1.4) + " m", True, RED)
    screen.blit(value, [10, 110])

    #########################################################
    # Lets text be fixed to correct degrees
    if math.degrees(prevRot) < 0:
        value = speed.render("(" + str(round(my_triangle[0][0], 2)) + " m, " + str(round(my_triangle[0][1]-7, 2)) + " m, " + str(round(abs(math.degrees(prevRot)), 2)) + " deg)", True, RED)
        screen.blit(value, [my_triangle[0][0] - 100, my_triangle[0][1] - 32])
    else:
        value = speed.render("(" + str(round(my_triangle[0][0], 2)) + " m, " + str(round(my_triangle[0][1]-7, 2)) + " m, " + str(round(360 - math.degrees(prevRot), 2)) + " deg)", True, RED)
        screen.blit(value, [my_triangle[0][0] - 100, my_triangle[0][1] - 32])
    #########################################################

    # print(rev_x, ",", rev_y)

    # Draws figures
    pygame.draw.rect(screen, BLUE, my_square)
    pygame.draw.polygon(screen, YELLOW, my_triangle)

    # Check end event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == JOYBUTTONDOWN:
            # print(event)
            if event.button == 0:
                my_square.x = 500
                my_square.y = 350
        if event.type == JOYBUTTONUP:
            print(event)
        if event.type == JOYAXISMOTION:
            # print(event)
            if event.axis == 5:
                leftSpan = leftMax - leftMin
                rightSpan = rightMax - rightMin
                valueScaled = float(event.value - leftMin) / float(leftSpan)
                const = int(rightMin + (valueScaled * rightSpan))
            if event.axis == 4:
                leftSpan = leftMax - leftMin
                rightSpan = rightMax - rightMin
                valueScaled = float(event.value - leftMin) / float(leftSpan)
                const = rightMin + (valueScaled * rightSpan)
                const = -const
            if event.axis == 0:
                leftSpanJ = leftMaxJ - leftMinJ
                rightSpanJ = rightMaxJ - rightMinJ
                valueScaledJ = float(event.value - leftMinJ) / float(leftSpanJ)
                constRot = rightMinJ + (valueScaledJ * rightSpanJ)
                # print(constRot), event.value)
        if event.type == JOYHATMOTION:
            print(event)

    #########################################################
    if const > 0:
        # Avoid degree overflow
        if prevRot >= math.radians(360):
            prevRot = math.radians(0)
        elif prevRot <= math.radians(-360):
            prevRot = math.radians(0)
        else:
            prevRot += constRot

        if prevRot > 0:
            # print("algo")
            rev_x = const * math.cos(prevRot)
            rev_y = const * math.sin(prevRot)
        elif prevRot < 0:
            # print("algo x2")
            rev_x = const * math.cos(-prevRot)
            rev_y = const * math.sin(prevRot)

        my_triangle = ((my_triangle[0][0]+rev_x, my_triangle[0][1]+rev_y), (my_triangle[1][0]+rev_x, my_triangle[1][1]+rev_y), (my_triangle[2][0]+rev_x, my_triangle[2][1]+rev_y))


    elif const < 0:
        # Avoid degree overflow
        if prevRot >= math.radians(360):
            prevRot = math.radians(0)
        elif prevRot <= math.radians(-360):
            prevRot = math.radians(0)
        else:
            prevRot += constRot

        if prevRot > 0:
            # print("algo")
            rev_x = const * math.cos(prevRot)
            rev_y = const * math.sin(prevRot)
        elif prevRot < 0:
            # print("algo x2")
            rev_x = const * math.cos(-prevRot)
            rev_y = const * math.sin(prevRot)

        my_triangle = ((my_triangle[0][0]+rev_x, my_triangle[0][1]+rev_y), (my_triangle[1][0]+rev_x, my_triangle[1][1]+rev_y), (my_triangle[2][0]+rev_x, my_triangle[2][1]+rev_y))
        #########################################################

    pygame.display.update()
    clock.tick(20)
