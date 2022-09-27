import game
import getopt, sys
from colors import *

# Object for Ackermann simulator
car = game.Ackermann()

# Argument list initialize
argumentList = sys.argv[1:]

# Options
options = "hmo:"

# Long options
long_options = ["vehicle_speed", "lf", "lb", "x0", "y0", "phi0", "df0", "dt"]

# Initialize main variables
car.tick  = 120  # Ticks to 60 fps
car.step  = 6    # Max degree of turning (3 left and 3 right)
car.dT    = 0.1  # Sampling time of 0.1
car.speed = 10   # Vehicle speed in m/s
car.l_b   = 1.2  # Distance from vehicle's center of mass to rear wheel axle
car.l_f   = 1.4  # Distance from vehicle's center of mass to front wheel axle
car.x0    = car.size[0] / 2 # Starts in the middle of the x axis
car.y0    = car.size[1] / 2 # Starts in the middle of the y axis
car.phi   = 0
car.df    = 0

# Initialize simulation parameters
car.init_sim_params()

# Set text fonts
car.set_fonts()

# Initialize objects in map
car.init_object()

# Map controller input to ackermann scale
car.xbox_controller_mapping()

# Update display
car.update()

# Main cycle
while True:
    # Set background color to black
    car.screen.fill(BLACK)

    # Draw tracing line
    car.tracing()

    # Renders parameters textbox
    car.param_textbox()

    # Renders coordinates on top of main object
    car.render_coord()

    # Draw main object in shape of triangle
    car.draw_object()

    # Check for pygame events
    car.check_end_event()

    # Move main object
    car.move_object()

    # Update display
    car.update()

    # Setting clock tick
    car.set_clock_tick()

