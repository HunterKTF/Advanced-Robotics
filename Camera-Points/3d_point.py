""" 3d_point.py

Description:

Author: 
Contact: 
First created: 

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

camera = cv_stereo.Stereo()

camera.calibration_info["f"] = 500      # Focal length in pixels
camera.calibration_info["cx"] = 450     # Center in pixels
camera.calibration_info["cy"] = 450     # Center in pixels
camera.calibration_info["Z"] = 2        # Distance in meters

camera.set_image(args.input_image)

camera.show_image()

camera.mouse_callback()

camera.key_wait()

camera.destroy_windows()
