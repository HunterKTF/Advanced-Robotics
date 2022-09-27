"""
    Ackermann Simulator
    Made by: Jorge Ricardo Hernández Sabino
    Revision date: 05/09/2022
"""

# Import libraries
import pygame
import math
import sys

from colors import *
from pygame.locals import *


class Ackermann:
    def __init__(self):
        self.beta  = 0    # slip angle of vehicle center of mass
        self.x     = 0    # coordinate of vehicle along 'x' axis
        self.x0    = 0    # starting coordinate in 'x' axis
        self.y     = 0    # coordinate of vehicle along 'y' axis
        self.y0    = 0    # starting coordinate in 'y' axis
        self.phi   = 0    # instantiates the global heading angle
        self.df    = 0    # rotation angle of the front wheel bycicle
        self.l_f   = 0    # distance from vehicle's center of mass to front wheel axle
        self.l_b   = 0    # distance from vehicle's center of mass to rear wheel axle
        self.v     = 0    # vehicle speed
        self.dT    = 0    # sampling time interval
        self.speed = 0    # vehicle initial speed
        self.step  = 0    # maximum degree angle for car steering

        self.size      = (1000, 700) # Changes the window pixel size
        self.joysticks = None        # Joysticks detected
        self.screen    = None        # Pygame screen
        self.clock     = None        # Pygame clock
        self.tick      = 0           # Game tick fps

        self.my_triangle = ()        # Moving object
        self.trail       = []        # Trail left by moving object

        self.param_text = None       # Saves parameters font
        self.coord_text = None       # Saves coordinates font
        
    # Initiates game and controllers
    def init_sim_params(self):
        # Initialize game
        pygame.init()

        # Initialize joysticks
        pygame.joystick.init()                          # If none, ignored
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        
        # Pygame screen
        self.screen = pygame.display.set_mode(self.size, 0, 32) # Sets the screen
        self.clock = pygame.time.Clock()                # Sets the screen's fps
        pygame.display.set_caption('Ackermann Simulator')

    # Select fonts for text
    def set_fonts(self):
        # Font for the parameters data screen
        self.param_text = pygame.font.SysFont("consolas", 15)

        # Font for coordinates moving with the figure
        self.coord_text = pygame.font.SysFont("consolas", 13)

    # Initiates object and trail
    def init_object(self):
        # Object's starting position
        coord = [self.x0, self.y0]                             # Starts in center of screen

        self.starting_pos =  ((coord[0], coord[1]+7),          # Draws triangle in given coord.
                             (coord[0], coord[1]-7),
                             (coord[0]+11, coord[1]))

        self.my_triangle = self.starting_pos

        # Initializes trail in starting position
        self.trail = [coord]                                   # Object's trail

    # Maps xbox controller limits
    def xbox_controller_mapping(self):
        # Mapping values (right trigger)
        self.left_max_T = 1                                    # Trigger fully pressed
        self.left_min_T = -1.000030518509476                   # Trigger released
        self.right_max_T = 10                                  # Max value for fully pressed
        self.right_min_T = 0                                   # Min value for fully released

        # Mapping values (left joystick)
        self.left_max_J = 1                                    # Left joystick fully right
        self.left_min_J = -1.000030518509476                   # Left joystick fully left
        self.right_max_J = math.radians(self.step/2)           # Max value for fully right joystick
        self.right_min_J = math.radians(-self.step/2)          # Min value for fully left joystick

    # Updates screen
    def update(self):
        pygame.display.update()

    # Drawing trail of the main object
    def tracing(self):
        if [self.my_triangle[0][0], self.my_triangle[0][1]-7] not in self.trail:
            self.trail.append([self.my_triangle[0][0], self.my_triangle[0][1]-7])

        for n in self.trail:
            pygame.draw.rect(self.screen, GREEN, [n[0], n[1], 5, 5])

    # Render parameters box
    def param_textbox(self):
        render = self.param_text.render("CONFIG PARAMS:", True, RED)
        self.screen.blit(render, [10, 10])

        render = self.param_text.render("Speed: " + str(self.v * 3.6) + " km/h", True, RED)
        self.screen.blit(render, [10, 30])

        render = self.param_text.render("Delta T: " + str(self.dT), True, RED)
        self.screen.blit(render, [10, 50])

        render = self.param_text.render("Delta f increment: " + str(math.degrees(self.df)) + " deg", True, RED)
        self.screen.blit(render, [10, 70])

        render = self.param_text.render("Lb: " + str(self.l_b) + " m", True, RED)
        self.screen.blit(render, [10, 90])

        render = self.param_text.render("Lf: " + str(self.l_f) + " m", True, RED)
        self.screen.blit(render, [10, 110])

    # Render object's coordinates
    def render_coord(self):
        x_coord = str(round(self.x, 2))
        y_coord = str(round(self.y, 2))

        if math.degrees(self.phi) > 0:
            degrees = str(round(abs(360 - math.degrees(self.phi)), 2))
        elif math.degrees(self.phi) == 360:
            degrees = str(0)
        else:
            degrees = str(round(abs(math.degrees(self.phi)), 2))

        coord_string = "(" + x_coord + " m, " + y_coord + " m, " + degrees + " deg)"

        render = self.coord_text.render(coord_string, True, RED)
        self.screen.blit(render, [self.my_triangle[0][0] - 100, self.my_triangle[0][1] - 32])

    # Render object on screen
    def draw_object(self):
        pygame.draw.polygon(self.screen, YELLOW, self.my_triangle)

    # Controller value mapping
    def mapping(self, left_max, left_min, right_max, right_min, value):
        left_span = left_max - left_min
        right_span = right_max - right_min
        value_scaled = float(value - left_min) / float(left_span)
        return right_min + value_scaled * right_span

    # Check end event
    def check_end_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == JOYBUTTONDOWN: # XBox controller buttons
                if event.button == 0:       # A Button
                    self.my_triangle = (self.size[0]/2, self.size[1]/2, 
                                        self.size[0]/2, self.size[1]/2,
                                        self.size[0]/2, self.size[1]/2)

            if event.type == JOYAXISMOTION: # XBox Controller axis
                if event.axis == 5:         # Speed up
                    self.v = int(self.mapping(self.left_max_T, self.left_min_T, self.right_max_T, self.right_min_T, event.value))
                if event.axis == 4:         # Speed down
                    speed = int(self.mapping(self.left_max_T, self.left_min_T, self.right_max_T, self.right_min_T, event.value))
                    self.v = -speed
                if event.axis == 0:         # Steering
                    self.df = self.mapping(self.left_max_J, self.left_min_J, self.right_max_J, self.right_min_J, event.value)

    # Sets moving parameters
    def move_object(self):
        self.beta = math.atan(self.l_b * math.tan(self.df) / (self.l_f + self.l_b))
        self.phi += self.v * self.dT * (math.cos(self.beta) * math.tan(self.df) / (self.l_f + self.l_b))
        self.x += self.v * self.dT * math.cos(self.phi + self.beta)
        self.y += self.v * self.dT * math.sin(self.phi + self.beta)

        if math.degrees(self.phi) >= 360:
            self.phi = math.radians(0)
        if math.degrees(self.phi) <= -360:
            self.phi = math.radians(0)

        print(math.degrees(self.beta), math.degrees(self.phi), self.x, self.y)

        self.my_triangle = ((self.starting_pos[0][0]+self.x, self.starting_pos[0][1]+self.y),
                            (self.starting_pos[1][0]+self.x, self.starting_pos[1][1]+self.y),
                            (self.starting_pos[2][0]+self.x, self.starting_pos[2][1]+self.y))

    # Sets clock timer
    def set_clock_tick(self):
        self.clock.tick(self.tick)
