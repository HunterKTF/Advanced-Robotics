"""sdclibrary.py

This is the main library used to compute a lane detection workflow using edge detection.

Made by: Jorge R. Hernández Sabino
Last updated: 14 / Nov / 2022
"""

# Import standard libraries
import numpy as np
import cv2
import math


class Sdclib():
    def __init__(self):
        self.img_color = None
        self.img_path = ""
        self.grey = None
        self.blur_img = None
        self.canny = None
        self.mask_img = None
        self.img_hough = None
        self.img_inlier = None

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

        self.GREEN = (255, 0, 0)

    def read_image(self):
        self.img_color = cv2.imread(self.img_path, cv2.IMREAD_REDUCED_COLOR_4)
        cv2.imshow("Original Image", self.img_color)

    def greyscale(self):
        self.grey = cv2.cvtColor(self.img_color, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Greyscale Image", self.grey)

    def gaussian_blur(self):
        self.blur_img = cv2.GaussianBlur(self.grey, self.kernel_size, sigmaX=0, sigmaY=0)
        # cv2.imshow("Blured Image", self.blur_grey)

    def canny_edge_det(self):
        self.canny = cv2.Canny(self.blur_img, self.low_threshold, self.high_threshold, apertureSize=3)
        # cv2.imshow("Canny Edge Detection", self.canny)

    def region_of_interest(self):
        # mask using 0
        layer = np.copy(self.canny) * 0
        cv2.fillPoly(layer, self.vertices, 255)
        self.mask_img = cv2.bitwise_and(self.canny, layer)
        # cv2.imshow("Canny edge detect with RoI", self.mask_img)

    def hough_transform(self):
        self.img_hough = self.img_color.copy()
        self.hough_transform = cv2.HoughLinesP(self.mask_img, self.rho, self.theta,
                                          self.threshold, np.array([]),
                                          minLineLength=self.min_line_len,
                                          maxLineGap=self.max_line_gap)

        for coords in self.hough_transform:
            for x0, y0, x1, y1 in coords:
                cv2.line(self.img_hough, (x0, y0), (x1, y1), self.GREEN, 5)
        # cv2.imshow('Hough lines', self.img_hough)

    def inlier_lines(self):
        self.img_inlier = self.img_color.copy()



print("ok")
