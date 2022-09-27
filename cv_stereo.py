import cv2
import math

class Stereo:
    def __init__(self):
        self.line_counter = 0
        self.prev_x = 0
        self.prev_y = 0

        self.X0 = 0
        self.Y0 = 0
        self.X1 = 0
        self.Y1 = 0
        self.perimeter = 0

        self.calibration_info = {}
        self.img = None


    def set_image(self, input_image):
        self.img = cv2.imread(input_image, cv2.IMREAD_COLOR)


    def compute_XYZ(self, x, y):
        Z = self.calibration_info["Z"]
        X = Z*(x - self.calibration_info["cx"]) / self.calibration_info["f"]
        Y = Z*(y - self.calibration_info["cy"]) / self.calibration_info["f"]

        # print(f"X: {X} \t Y:{Y} \t Z:{Z}")
        return X, Y

    
    def draw_line(self, x, y):
        cv2.line(self.img, (self.prev_x, self.prev_y), (x, y), (0,0,255), 5)


    def click_event(self, event, x, y, flags, params):
        # Check for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.img, (x,y), 5, (0,0,255), -1)

            if self.line_counter > 0:
                self.draw_line(x, y)

                # Text coords
                t_x_coord = int((x + self.prev_x)/2)
                t_y_coord = int((y + self.prev_y)/2)

                self.prev_x, self.prev_y = x, y
                
                # Compute XYZ coordinates
                self.X1, self.Y1 = self.compute_XYZ(x, y)

                dist_x = self.X1 - self.X0
                dist_y = self.Y1 - self.Y0

                distance = math.sqrt(dist_x**2 + dist_y**2)
                
                self.perimeter += distance

                # Draw text
                cv2.putText(img=self.img, 
                            text=str(round(distance,2)) + "m", 
                            org=(t_x_coord,t_y_coord), 
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
                        org=(x,y), 
                        fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 
                        fontScale=0.65, 
                        color=(120, 190, 60), 
                        thickness=2)

            # Visualize the input image
            cv2.imshow("input image", self.img)

        if event == cv2.EVENT_RBUTTONDOWN:
            print("Perimeter:", round(self.perimeter,2), "m")

    def show_image(self):
        cv2.imshow("input image", self.img)


    def mouse_callback(self):
        cv2.setMouseCallback("input image", self.click_event)


    def key_wait(self):
        key = cv2.waitKey(0)


    def destroy_windows(self):
        cv2.destroyAllWindows()