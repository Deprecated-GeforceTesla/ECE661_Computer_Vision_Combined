import cv
import numpy as np
from math import cos, sin
from msic import get_hough_line


class Board_line(object):

    def __init__(self, image, hough_lines):
        self.image = cv.CloneMat(image)
        self.hough_lines = hough_lines
        self.height = image.rows
        self.width = image.cols
        self.find_thetas()
        self.distribute_vertical_and_horizontal()
        self.find_best_line()

    def get_bestline(self):
        return self.bestlines

    def get_dist(self):
        return self.sep_dist

    def classify_lines(self, lines, operation, sep):
        unique_lines = []
        unique_record = []
        temp_line = lines[0][1]
        unique_lines.append(temp_line)
        temp_record = lines[0][0]
        unique_record.append(temp_record)

        for i in range(1, len(lines)):
            temp_line = lines[i][1]
            temp_recprd = lines[i][0]
            line_hough = get_hough_line(temp_line)
            unique_line_hough = get_hough_line(unique_lines[-1])
            corner = np.cross(line_hough, unique_line_hough)  # l x l is pt

            if (corner[0] >= 0) and (corner[0] < self.height):
                if (corner[1] >= 0) and (corner[1] < self.width):
                    if (unique_record[-1] > temp_record):
                        unique_lines[-1] = temp_line
                        unique_record[-1] = temp_record
                    continue

            unique_dist = unique_lines[-1][0] * operation(unique_lines[-1][1])
            current_dist = temp_line[0] * operation(temp_line[1])
            difference = abs(unique_dist - current_dist)

            if (difference <= sep):
                if (unique_record[-1] > temp_record):
                    unique_lines[-1] = temp_line
                    unique_record[-1] = temp_record
                continue

            unique_lines.append(temp_line)
            unique_record.append(temp_record)
            final_dist = difference

        return unique_lines, final_dist

    def find_thetas(self):
        self.thetas = []
        for i in range(len(self.hough_lines)):
            self.thetas.append(self.hough_lines[i][1] - (np.pi / 2))

    def distribute_vertical_and_horizontal(self):
        self.horizontal_id = []
        self.vertical_id = []
        self.horizontal_lines = []
        self.vertical_lines = []
        horizontal_record = []
        vertical_record = []

        for i in range(len(self.thetas)):
            if (abs(self.thetas[i]) < np.pi / 4):
                self.horizontal_id.append(i)
            else:
                self.vertical_id.append(i)

        for i in self.horizontal_id:
            self.horizontal_lines.append(self.hough_lines[i])
            horizontal_record.append(i)

        for i in self.vertical_id:
            #print 'here try'
            self.vertical_lines.append(self.hough_lines[i])
            vertical_record.append(i)

        self.horzontal = zip(horizontal_record, self.horizontal_lines)
        self.vertical = zip(vertical_record, self.vertical_lines)

        self.horzontal = sorted(self.horzontal,
                                key=lambda elm: elm[1][0] * sin(elm[1][1]))

        self.vertical = sorted(self.vertical,
                               key=lambda elm: elm[1][0] * cos(elm[1][1]))

        #print '------------------------------------------'
        #print len(self.horzontal)
        #print '------------------------------------------'
        #print len(self.vertical)


    def find_best_line(self):
        sep = 1.0

        while True:
            (horizontal_unique_line,
             horizontal_dist) = self.classify_lines(self.horzontal, sin, sep)
            (vertical_unique_line,
             vertical_dist) = self.classify_lines(self.vertical, cos, sep)

            if len(horizontal_unique_line) < 10:
                break
            if len(vertical_unique_line) < 8:
                break

            if ((len(horizontal_unique_line) == 2 * 5) and
                (len(vertical_unique_line) == 2 * 4)):
                break
            else:
                sep += 1

        self.bestlines = horizontal_unique_line + vertical_unique_line
        self.sep_dist = int((vertical_dist + horizontal_dist) / 2.0)


    def get_image_with_hough_line(self):
        for line in self.bestlines:
            x = cos(line[1]) * line[0]
            y = sin(line[1]) * line[0]

            x1 = int(x + 1000 * sin(line[1]))
            y1 = int(y - 1000 * cos(line[1]))
            x2 = int(x - 1000 * sin(line[1]))
            y2 = int(y + 1000 * cos(line[1]))
            
            cv.Line(self.image, (x1,y1), (x2,y2), cv.RGB(255,255,255), 2)
        return self.image









        
