""" 3d_point.py

Description: Main file to compute image analysis. The user will interact with the code
by left-clicking the points on image to generate coordinate points. Coordinate points
will then generate lines connecting the points to generate a perimeter. The code will
finally display upon right-clicking the image analytics.

Author: Jorge Ricardo Hernández Sabino
Contact: jorge.hernandezs@udem.edu
First created: 26 / 09 / 2022

"""

# Import standard libraries
import argparse

# Import local libraries
import cv_stereo


# Ask the user to enter the required information
parser = argparse.ArgumentParser()
parser.add_argument("--input_image", 
                    help="Input image from which the 3D measurements will be obtained")
args = parser.parse_args()

camera = cv_stereo.Stereo()             # Create stereo camera object

camera.calibration_info["f"] = 500      # Focal length in pixels
camera.calibration_info["cx"] = 450     # Center in pixels
camera.calibration_info["cy"] = 450     # Center in pixels
camera.calibration_info["Z"] = 2        # Distance in meters

camera.set_image(args.input_image)      # Set the image chose by the user

camera.show_image()                     # Display image

camera.mouse_callback()                 # Trigger functions with user input

camera.key_wait()                       # Wait for user input

camera.destroy_windows()                # Function to close previous windows
