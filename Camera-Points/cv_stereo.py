""" cv_stereo.py

Description: 3D point mapping library for uncalibrated RGB cameras

Author: Jorge R. Hernández Sabino
Contact: jorge.hernandezs@udem.edu
First created: 26 / 09 / 2022

"""

# Import stsandard libraries
import cv2
import math


class Stereo:
    def __init__(self):
        self.line_counter = 0       # Counts lines in map
        self.segment_count = {}     # Stores segment info
        self.prev_x = 0             # Stores previous x coordinates
        self.prev_y = 0             # Stores previous y coordinates

        self.X0 = 0                 # Saves X distance coordinate of previous point
        self.Y0 = 0                 # Saves Y distance coordinate of previous point
        self.X1 = 0                 # Saves current X distance
        self.Y1 = 0                 # Saves current Y distance
        self.perimeter = 0          # Saves calculated perimeter

        self.calibration_info = {}  # Saves camera calibration info
        self.img = None             # Stores image object

    # Function to set image object to the desired image
    def set_image(self, input_image):
        self.img = cv2.imread(input_image, cv2.IMREAD_COLOR)

    # Function to compute X Y Z distance
    def compute_XYZ(self, x, y):
        Z = self.calibration_info["Z"]
        X = Z * (x - self.calibration_info["cx"]) / self.calibration_info["f"]
        Y = Z * (y - self.calibration_info["cy"]) / self.calibration_info["f"]

        print(f"Point {self.line_counter} \t X: {X} \t Y:{Y} \t Z:{Z}")
        return X, Y

    # Function to draw a line using coordinates on image
    def draw_line(self, x, y):
        cv2.line(self.img, (self.prev_x, self.prev_y), (x, y), (0, 0, 255), 5)

    # Function to detect event and make 
    def click_event(self, event, x, y, flags, params):
        # Check for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.img, (x, y), 5, (0, 0, 255), -1)

            if self.line_counter > 0:
                self.draw_line(x, y)

                # Text coords
                t_x_coord = int((x + self.prev_x) / 2)
                t_y_coord = int((y + self.prev_y) / 2)

                self.prev_x, self.prev_y = x, y

                # Compute XYZ coordinates
                self.X1, self.Y1 = self.compute_XYZ(x, y)

                dist_x = self.X1 - self.X0
                dist_y = self.Y1 - self.Y0

                distance = math.sqrt(dist_x ** 2 + dist_y ** 2)

                key = "Segment" + str(self.line_counter)
                self.segment_count[key] = distance

                self.perimeter += distance

                # Draw text
                cv2.putText(img=self.img,
                            text=str(round(distance, 2)) + "m",
                            org=(t_x_coord, t_y_coord),
                            fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                            fontScale=0.60,
                            color=(120, 190, 60),
                            thickness=2)

                self.X0 = self.X1
                self.Y0 = self.Y1
                self.line_counter += 1
            else:
                self.prev_x = x
                self.prev_y = y

                # Compute XYZ coordinates
                self.X0, self.Y0 = self.compute_XYZ(x, y)

                self.line_counter += 1

            # Draw text
            cv2.putText(img=self.img,
                        text=str(x) + ',' + str(y),
                        org=(x, y),
                        fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                        fontScale=0.65,
                        color=(120, 190, 60),
                        thickness=2)

            # Visualize the input image
            cv2.imshow("input image", self.img)

        if event == cv2.EVENT_RBUTTONDOWN:
            print()

            sort_segments = sorted(self.segment_count.items(), key=lambda y: y[1], reverse=True)
            print("Sorted order: ")
            for i in sort_segments:
                print(i[0], "\t", i[1])

            print()
            print("Perimeter:", round(self.perimeter, 2), "m")

    def show_image(self):
        cv2.imshow("input image", self.img)

    def mouse_callback(self):
        cv2.setMouseCallback("input image", self.click_event)

    def key_wait(self):
        key = cv2.waitKey(0)

    def destroy_windows(self):
        cv2.destroyAllWindows()
