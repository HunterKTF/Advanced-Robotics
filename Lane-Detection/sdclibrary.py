# Import standard libraries
import numpy as np
import cv2
from time import sleep


class Sdclib:
    def __init__(self):
        self.img_color = None
        self.img_path = ""
        self.grey = None
        self.blur_img = None
        self.canny = None
        self.mask_img = None
        self.img_hough = None
        self.img_inlier = None
        self.img_lanes = None
        
        self.dimensions = ()
        self.height = 0
        self.width = 0
        self.channels = 0

        self.kernel_size = ()
        self.low_threshold = 0
        self.high_threshold = 0
        self.vertices = None

        self.rho = 0
        self.theta = 0
        self.threshold = 0
        self.min_line_len = 0
        self.max_line_gap = 0
        self.hough_transform = None

        self.x_left = []
        self.y_left = []
        self.x_right = []
        self.y_right = []
        
        self.min_lane_size = 0
        self.max_lane_size = 0

        self.BLUE = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (0, 0, 255)

    def read_image(self):
        self.img_color = cv2.imread(self.img_path, cv2.IMREAD_REDUCED_COLOR_4)
        
        # Get image dimensions
        self.dimensions = self.img_color.shape
        
        self.height = self.dimensions[0]
        self.width = self.dimensions[1]
        self.channels = self.dimensions[2]
        
        # cv2.imshow("Original Image", self.img_color)
        # cv2.waitKey(1)

    def greyscale(self):
        self.grey = cv2.cvtColor(self.img_color, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Greyscale Image", self.grey)
        # cv2.waitKey(1)

    def gaussian_blur(self):
        self.blur_img = cv2.GaussianBlur(self.grey, self.kernel_size, sigmaX=0, sigmaY=0)
        # cv2.imshow("Blured Image", self.blur_img)
        # cv2.waitKey(1)

    def canny_edge_det(self):
        self.canny = cv2.Canny(self.blur_img, self.low_threshold, self.high_threshold, apertureSize=3)
        # cv2.imshow("Canny Edge Detection", self.canny)
        # cv2.waitKey(1)

    def region_of_interest(self):
        # mask using 0
        layer = np.copy(self.canny) * 0
        cv2.fillPoly(layer, self.vertices, 255)
        self.mask_img = cv2.bitwise_and(self.canny, layer)
        # cv2.imshow("Canny edge detect with RoI", self.mask_img)
        # cv2.waitKey(1)

    def hough_function(self):
        self.img_hough = self.img_color.copy()
        self.hough_transform = cv2.HoughLinesP(self.mask_img, self.rho, self.theta,
                                          self.threshold, np.array([]),
                                          minLineLength=self.min_line_len,
                                          maxLineGap=self.max_line_gap)

        for coords in self.hough_transform:
            for x0, y0, x1, y1 in coords:
                cv2.line(self.img_hough, (x0, y0), (x1, y1), self.GREEN, 5)
        # cv2.imshow('Hough lines', self.img_hough)
        # cv2.waitKey(1)

    def inlier_lines(self):
        self.img_inlier = self.img_color.copy()

        for coords in self.hough_transform:
            for x0, y0, x1, y1 in coords:
                mx_slope = (y1 - y0) / (x1 - x0)
                if abs(mx_slope) > 0.28:
                    
                    if mx_slope <= 0:
                        if x0 <= (self.width/2) and x1 <= (self.width/2):
                            self.x_left.extend((x0, x1))
                            self.y_left.extend((y0, y1))
                            cv2.line(self.img_inlier, (x0, y0), (x1, y1), self.BLUE, 5)
                    
                    else:
                        if x0 > (self.width/2) and x1 > (self.width/2):
                            self.x_right.extend((x0, x1))
                            self.y_right.extend((y0, y1))
                            cv2.line(self.img_inlier, (x0, y0), (x1, y1), self.RED, 5)
                            
        # cv2.imshow('Lane lines', self.img_inlier)
        # cv2.waitKey(1)
        
    def lane_detect(self):
        self.img_lanes = self.img_color.copy()

        if self.x_left and self.y_left and self.x_right and self.y_right:

            left_line = np.poly1d(np.polyfit(self.y_left, self.x_left, deg=1))
            right_line = np.poly1d(np.polyfit(self.y_right, self.x_right, deg=1))
            
            right_init = int(right_line(self.max_lane_size))
            right_end = int(right_line(self.min_lane_size))
            
            left_init = int(left_line(self.max_lane_size))
            left_end = int(left_line(self.min_lane_size))
            
            lines = [[
                [left_init, self.max_lane_size, left_end, self.min_lane_size],
                [right_init, self.max_lane_size, right_end, self.min_lane_size]
            ]]
            pts = []
            for line in lines:
                for x0, y0, x1, y1 in line:
                    cv2.line(self.img_color, (x0, y0), (x1, y1), self.RED, 6)

                    if x0 <= (self.width / 2) and x1 <= (self.width / 2):
                        pts.append([x0, y0])
                        pts.append([x1, y1])
                    else:
                        pts.append([x1, y1])
                        pts.append([x0, y0])
                        
            points = np.array(pts, np.int32)
            cv2.fillPoly(self.img_lanes, pts=[points], color=self.GREEN)
            alpha = 0.4
            img_out = cv2.addWeighted(self.img_lanes, alpha, self.img_color, 1-alpha, 0)
                    
        cv2.imshow('Lane detection', img_out)
        cv2.waitKey(0)
