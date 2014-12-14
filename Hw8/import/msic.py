import numpy as np
from math import sin, cos

def get_hough_line(houghLine):
    rho = houghLine[0]
    theta = houghLine[1]
    pt0 = np.array([rho * cos(theta), rho * sin(theta), 1.0])
    pt1 = np.array([pt0[0] + 100 * sin(theta), pt0[1] - 100 * cos(theta), 1.0])
    line = np.cross(pt0, pt1)
    return line
