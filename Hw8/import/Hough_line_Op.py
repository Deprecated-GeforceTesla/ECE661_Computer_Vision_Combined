import cv
import numpy as np

class Hough_Line(object):

    def __init__(self, image):
        self.image = image
        self.rho = 1
        self.theta = np.pi / 180
        self.threshold = 50

    def get_hough_line(self):
        line = cv.HoughLines2(self.image, cv.CreateMemStorage(),
                              cv.CV_HOUGH_STANDARD, self.rho, self.theta,
                              self.threshold)
        return line
