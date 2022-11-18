# Import standard libraries
import argparse
import os
import numpy as np
from time import process_time

# Import local libraries
from sdclibrary import Sdclib


# Pipeline to read
def pipeline(sdc_img):
    # 1. Read image with path provided
    sdc_img.read_image()
    
    # 2. Convert input image to greyscale
    sdc_img.greyscale()
    
    # 3. Apply Gaussian smoothing
    sdc_img.kernel_size = (9, 9)
    sdc_img.gaussian_blur()
    
    # 4. Apply Canny Edge detection
    sdc_img.low_threshold = 70
    sdc_img.high_threshold = 100
    sdc_img.canny_edge_det()
    
    # 5. Define Region of Interest
    # Define points for vertices
    p1, p2, p3, p4, p5, p6, p7, p8 = (3, 438), (3, 296), (325, 237), (610, 237), \
                                     (910, 320), (910, 438), (590, 290), (340, 290)
    
    sdc_img.vertices = np.array([[p1, p2, p3, p4, p5, p6, p7, p8]], dtype=np.int32)
    sdc_img.region_of_interest()
    
    # 6. Use Hough Transform to trace lane lines
    sdc_img.rho = 2                 # Distance resolution in pixels on Hough grid
    sdc_img.theta = np.pi/180       # Angular resolution in radians on Hough grid
    sdc_img.threshold = 100         # Minimum number of intersections on Hough grid
    sdc_img.min_line_len = 10       # Minimum number of pixels making a line
    sdc_img.max_line_gap = 30       # Maximum gap in pixels between connectable line segments
    
    sdc_img.hough_function()
    
    # 7. Get the inlier of left and right lane lines
    sdc_img.inlier_lines()
    
    # 8. Draw lines for each lane
    sdc_img.min_lane_size = 240     # Minimum final lane size
    sdc_img.max_lane_size = 500     # Maximum final lane size
    
    sdc_img.lane_detect()


# Run the main function to execute the pipeline
def main(dataset_list):
    for img_name in dataset_list:
        # Create lane detection object
        sdc_lanes = Sdclib()

        # Get image path
        sdc_lanes.img_path = ds_path + img_name

        # Begin execution time
        begin_time = process_time()

        # Run pipeline workflow
        pipeline(sdc_lanes)

        # Print the FPS of computed image
        fps = process_time() - begin_time
        if fps <= 0:
            fps = 0.001
        print(f"Processing image:{sdc_lanes.img_path}",
              f"\tCPU execution time:{1 / fps:0.4f} FPS")


if __name__ == "__main__":
    try:
        # Read user input for image path
        parser = argparse.ArgumentParser()
        parser.add_argument("--img_path", help="Image path")
        args = parser.parse_args()

        # Dataset path
        ds_path = args.img_path

        # Image dataset
        dataset = sorted(os.listdir(ds_path))

        main(dataset)
    except Exception as e:
        # Prints error message with error arguments
        print(e.message, e.args)
