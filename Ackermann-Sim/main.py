import game
import argparse
from colors import *

# Object for Ackermann simulator
car = game.Ackermann()

# Create input argument for user input
parser = argparse.ArgumentParser(description='Add simulator parameters')
parser.add_argument("--vehicle_speed", help="Max vehicle speed in sim", nargs='?', const=10, type=int)
parser.add_argument("--lf", help="Distance from vehicle's center of mass to front wheel axle")
parser.add_argument("--lb", help="Distance from vehicle's center of mass to rear wheel axle")
parser.add_argument("--x0", help="Starting position in x axis")
parser.add_argument("--y0", help="Starting position in y axis")
parser.add_argument("--phi0", help="Starting angle (should be 0)")
parser.add_argument("--df0", help="Speed increments")
parser.add_argument("--dt", help="Sampling time steps")

args = parser.parse_args()
print(args)

# Initialize main variables
car.tick = 120  # Ticks to 120 fps
car.step = 2.4  # Max degree of turning (2 left and 2 right)
car.dT = 0.1 if args.dt is None else args.dt  # Sampling time of 0.1
car.speed = 10 if args.vehicle_speed is None else args.vehicle_speed  # Vehicle speed in m/s
car.l_b = 1.2 if args.lb is None else args.lb  # Distance from vehicle's center of mass to rear wheel axle
car.l_f = 1.4 if args.lf is None else args.lf  # Distance from vehicle's center of mass to front wheel axle
car.x0 = car.size[0]/2 if args.x0 is None else args.x0  # car.size[0] / 2,  Starts in the middle of the x axis
car.y0 = car.size[1]/2 if args.y0 is None else args.y0  # car.size[1] / 2,  Starts in the middle of the y axis
car.phi = 0 if args.phi0 is None else args.phi0
car.df = 0 if args.df0 is None else args.df0

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
    car.error_tracing()
    
    # Renders parameters textbox
    car.param_textbox()
    
    # Renders coordinates on top of main object
    car.render_coord()
    
    # Draw main object in shape of triangle
    car.draw_object()
    car.draw_object_error()
    
    # Check for pygame events
    car.check_end_event()
    
    # Move main object
    car.move_object()
    # car.move_object_error()
    
    # Update display
    car.update()
    
    # Setting clock tick
    car.set_clock_tick()
