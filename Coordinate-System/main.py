"""
Python code that gets the coordinates of a sensor using transformation matrices. The user must input the values
for the position of each object.

Author: Jorge Ricardo Hernández Sabino
Contact: jorge.hernandezs@udem.edu
Last Updated: 28/09/2022
"""

# Import libraries
import argparse

# Import user defined libraries
import coord_sys

# Declare the argparse for user input
parser = argparse.ArgumentParser(description='User input values')
parser.add_argument("--alpha", help="angle of yaw movement")
parser.add_argument("--beta", help="angle of pitch movement")
parser.add_argument("--gamma", help="angle of roll movement")
parser.add_argument("--tx", help="x translation position")
parser.add_argument("--ty", help="y translation position")
parser.add_argument("--tz", help="z translation position")
parser.add_argument("--pL", help="L position array", nargs='+')

args = parser.parse_args()

# Create object to access the Transform class
system = coord_sys.Transform()

# Example tested with the following values:
""" Example tested with the following values:
alpha   = 0
beta    = 0
gamma   = -90
tx      = 0.45
ty      = 0.25
tz      = 0.15
pL      = [2.5, 5.0, -0.35]
"""

system.alpha = float(args.alpha)        # angle for yaw rotation
system.beta = float(args.beta)          # angle for pitch rotation
system.gamma = float(args.gamma)        # angle for roll rotation

system.tx = float(args.tx)              # x coord in translation vector
system.ty = float(args.ty)              # y coord in translation vector
system.tz = float(args.tz)              # z coord in translation vector

str_p_L = args.pL                       # coordinates of lidar beam to object
map_p_L = map(float, str_p_L)
system.p_L = list(map_p_L)

# Show the coordinates of P_L
system.show_coord()

# Compute the 3D rotational matrix of the yaw, pitch and roll movements
system.compute_3d_rotation()

# Compute the 3D translation vector t
system.compute_3d_translation()

# Compute the 3D transformation matrix using the rotational matrix R and vector t
system.compute_3d_transformation_matrix()

# Get the position of the GPS sensor as a vector in meters
system.compute_transformation()
