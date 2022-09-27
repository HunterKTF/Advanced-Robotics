

# import standard libraries
import cv2
import argparse


# Compute X, Y and Z for each point selected on the input image
def compute_XYZ(x, y, calibration_info):
    Z = calibration_info["Z"]
    X = Z*(x - calibration_info["cx"]) / calibration_info["f"]
    Y = Z*(y - calibration_info["cy"]) / calibration_info["f"]

    print(f"X: {X} \t Y:{Y} \t Z:{Z}")


def draw_line(x, y, prev_x, prev_y):
    cv2.line(img, (prev_x,prev_y), (x,y), (0,255,0), 1) 


# Display the coordinates of points clicked on the input image
def click_event(event, x, y, flags, params):

    # Check for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # Add your code here
        # x, y
        cv2.circle(img, (x,y), 5, (0,255,0), -1)

        if line_counter > 0:
            draw_line(x, y, prevX, prevY)
            prevX, prevY = x, y
            line_counter += 1
        else:
            prevX, prevY = x, y
            line_counter += 1

        # Draw text
        cv2.putText(img, str(x) + ',' + str(y), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)

        # Compute XYZ coordinates
        compute_XYZ(x, y, calibration_info)

        # Visualize the input image
        cv2.imshow("input image", img)


# Save coordinates in variables
global line_counter
global prevX
global prevY

line_counter = 0
prevX = 0
prevY = 0

# Camera calibration parameters
calibration_info = dict()
calibration_info["f"] = 500 # Focal length in pixels
calibration_info["cx"] = 450 # Center in pixels
calibration_info["cy"] = 450 # Center in pixels
calibration_info["Z"] = 2

# Ask the user to enter the required information
parser = argparse.ArgumentParser()
parser.add_argument("--input_image", help="Input image from which the 3D measurements will be obtained")
args = parser.parse_args()

# Read in input image as color image
img = cv2.imread(args.input_image, cv2.IMREAD_COLOR)

# Visualize input image
cv2.imshow("input image", img)

# Call MouseCallback
cv2.setMouseCallback("input image", click_event)

# Wait for the user to press a key
key = cv2.waitKey(0)

# Destroy windows to free memory
cv2.destroyAllWindows()


