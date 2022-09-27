""" stereo.py

Description:

Author: 
Contact: 
First created: 

"""

import argparse

import cv_stereo


# Ask the user to enter the required information
parser = argparse.ArgumentParser()
parser.add_argument("--input_image", 
                    help="Input image from which the 3D measurements will be obtained")
args = parser.parse_args()

stereo = cv_stereo.Stereo()

stereo.calibration_info["f"] = 500      # Focal length in pixels
stereo.calibration_info["cx"] = 450     # Center in pixels
stereo.calibration_info["cy"] = 450     # Center in pixels
stereo.calibration_info["Z"] = 2        # Distance in meters

stereo.set_image(args.input_image)

stereo.show_image()

stereo.mouse_callback()

stereo.key_wait()

stereo.destroy_windows()
