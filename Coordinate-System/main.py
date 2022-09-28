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

system = coord_sys.Transform()

system.alpha = 0
system.beta = 0
system.gamma = -90

system.tx = 0.45
system.ty = 0.25
system.tz = 0.15

system.p_L = [2.5, 5.0, -0.35]

system.compute_3d_rotation()

system.compute_3d_translation()

system.compute_3d_transformation_matrix()

system.compute_transformation()
# print("Hello World")
