# Import standard libraries
import argparse
import os
import numpy as np
from time import process_time

# Import local libraries
from sdclibrary import Sdclib


# Pipeline to read
def pipeline():
    # 1. Read image with path provided
    sdc_lanes.read_image()
    
    # 2. Convert input image to greyscale
    sdc_lanes.greyscale()
    
    # 3. Apply Gaussian smoothing
    sdc_lanes.kernel_size = (9, 9)
    sdc_lanes.gaussian_blur()
    
    # 4. Apply Canny Edge detection
    sdc_lanes.low_threshold = 70
    sdc_lanes.high_threshold = 100
    sdc_lanes.canny_edge_det()
    
    # 5. Define Region of Interest
    # Define points for vertices
    p1, p2, p3, p4, p5, p6, p7, p8 = (3, 438), (3, 296), (325, 237), (610, 237), \
                                     (910, 320), (910, 438), (590, 290), (340, 290)
    
    sdc_lanes.vertices = np.array([[p1, p2, p3, p4, p5, p6, p7, p8]], dtype=np.int32)
    sdc_lanes.region_of_interest()
    
    # 6. Use Hough Transform to trace lane lines
    sdc_lanes.rho = 2
    sdc_lanes.theta = np.pi/180
    sdc_lanes.threshold = 100
    sdc_lanes.min_line_len = 10
    sdc_lanes.max_line_gap = 30
    
    sdc_lanes.hough_function()
    
    # 7. Get the inlier of left and right lane lines
    sdc_lanes.inlier_lines()
    
    # 8. Draw lines for each lane
    sdc_lanes.min_lane_size = 240
    sdc_lanes.max_lane_size = 500
    
    sdc_lanes.lane_detect()
    

# Read user input for image path
parser = argparse.ArgumentParser()
parser.add_argument("--img_path", help="Image path")
args = parser.parse_args()

# Dataset path
ds_path = args.img_path

# Image dataset
dataset = sorted(os.listdir(ds_path))

for img_name in dataset:
    # Create lane detection object
    sdc_lanes = Sdclib()
    
    # Get image path
    sdc_lanes.img_path = ds_path + img_name

    # Begin execution time
    begin_time = process_time()
    
    # Run pipeline workflow
    pipeline()
    
    # Print the FPS of computed image
    print(f"Processing image:{sdc_lanes.img_path}",
          f"\tCPU execution time:{1 / (process_time() - begin_time):0.4f} FPS")
