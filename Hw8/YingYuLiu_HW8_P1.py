import sys
import cv
sys.path.append("import/")
from Hough_line_Op import Hough_Line
from Canny_Op import Canny
from Line_Op import Board_line
from Corner_Op import Board_corner
from Homography_Op import Homography
from Cam_Calibration_Op import Cam_Calibration
from Reprojection import Reprojection
import optimization as opt

class HW_problem1(object):

    def __init__(self):
        pick = raw_input("1. For given data set, 2. For my data set : ")
        self.choice = raw_input('use optimization? 1:Y, 2:N : ')
        if int(self.choice) == 1:
            self.dir = 'yes_optimization/'
        elif int(self.choice) == 2:
            self.dir = 'no_optimization/'

        if int(pick) == 1:
            self.path = 'input/given/Pic_'
            self.out = 'output/' + self.dir + 'given/'
            self.count = 40
        elif int(pick) == 2:
            self.path = 'input/own/'
            self.out = 'output/' + self.dir + 'own/'
            self.count = 20

        if int(self.choice) == 1:
            self.count = 5
        self.load_image()
        self.perform_action()
        self.reprojection()

    def load_image(self):
        self.images = []
        for i in range(1, self.count + 1):
            path = self.path + str(i) + '.jpg'
            image = cv.LoadImageM(path, cv.CV_LOAD_IMAGE_COLOR)
            self.images.append(image)

    def perform_action(self):
        self.records = []
        self.h_list = []
        count = 0
        for image in self.images:
            count += 1
            edges = Canny(image)
            edges = edges.get_canny_edge()
            lines = Hough_Line(edges)
            lines = lines.get_hough_line()
            best_lines = Board_line(image, lines)
            sep = best_lines.get_dist()
            hough_image = best_lines.get_image_with_hough_line()
            best_lines = best_lines.get_bestline()
            corner = Board_corner(image, best_lines, sep)
            corner_img = corner.get_image()
            corner = corner.get_corners()
            record = Homography(corner, 1.0)
            matrix_h = record.get_homography()
            record = record.get_correspondence()
            self.h_list.append(matrix_h)
            self.records.append(record)
            path = self.out + 'edge/' + str(count) + '.jpg'
            cv.SaveImage(path, edges)
            path = self.out + 'corner/' + str(count) + '.jpg'
            cv.SaveImage(path, corner_img)
            path = self.out + 'hough_line/' + str(count) + '.jpg'
            cv.SaveImage(path, hough_image)


        w = Cam_Calibration(self.h_list)
        self.matrix_k = w.get_matrix_k()
        self.matrix_rts_list = w.get_matrix_r()

    def reprojection(self):
        k1 = 0
        k2 = 0
        print (self.matrix_k)
        if int(self.choice) == 1:
            a, b, c, d = opt.refine_param(self.matrix_k, self.matrix_rts_list,
                                          self.records, k1, k2)
            self.matrix_k = a
            self.matrix_rts_list = b
            k1 = c
            k2 = d
        

        print k1, k2
        errors = 0
        for i in range(len(self.images)):
            record = self.records[i]
            image = self.images[i]
            temp = Reprojection(image, record, self.matrix_k,
                                self.matrix_rts_list[i], k1, k2)
            error = temp.get_differences()
            if error > errors:
                errors = error
            reproj_img = temp.get_image()
            path = self.out + 'reprojection/' + str(i) + '.jpg'
            cv.SaveImage(path, reproj_img)
        print 'error max is: ' + str(errors)

if __name__ == "__main__":
    temp = HW_problem1()
