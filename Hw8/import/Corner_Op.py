import cv
import numpy as np
from msic import get_hough_line

class Board_corner(object):

    def __init__(self, image, bestlines, dist):
        self.image = cv.CloneMat(image)
        self.bestlines = bestlines
        self.dist = dist
        self.group_lines()
        self.find_corners()
        self.mark_corners_image()

    def get_corners(self):
        return self.corner

    def get_image(self):
        return self.image

    def group_lines(self):
        self.thetas = []
        self.horizontal_lines = []
        self.vertical_lines = []

        for line in self.bestlines:
            if abs(line[1] - (np.pi / 2)) < np.pi / 4:
                self.horizontal_lines.append(line)
            else:
                self.vertical_lines.append(line)

    #horzLines = sorted(horzLines, key=lambda elm: elm[0] * sin(elm[1]), reverse=True)
    #vertLines = sorted(vertLines, key=lambda elm: elm[0] * cos(elm[1]), reverse=False)

    def find_corners(self):
        self.corner = []
        
        for i in range(len(self.horizontal_lines)):
            temp = []
            for n in range(len(self.vertical_lines)):
                temp.append(())
            self.corner.append(temp)



        for i in range(len(self.horizontal_lines)):
            horizontal = get_hough_line(self.horizontal_lines[i])
            for n in range(len(self.vertical_lines)):
                vertical = get_hough_line(self.vertical_lines[n])
                pt = np.cross(horizontal, vertical)
                pt[0] /= pt[2]
                pt[1] /= pt[2]
                pt[2] = 1
                self.corner[i][n] = (pt[0],pt[1])

    def mark_corners_image(self):
        count = 0
        for i in self.corner:
            for n in i:
                x = int(n[0])
                y = int(n[1])
                cv.Circle(self.image, (x,y), 20, (0,0,255), -1)
                font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 3, 3 , thickness=2)
                cv.PutText(self.image, str(count), (x,y), font, (0,0,255))
                count += 1
        return self.image
            
                

        
