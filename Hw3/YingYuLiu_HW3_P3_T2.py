import sys
import cv2
import numpy as np
sys.path.append("imports/")
import projective_op as Projective
import conic_op as Conic
import image_output as Output

class HW_problem3_T2(object):

    def __init__(self):
        choice = str(1)
        self.setup_coordinate(choice)
        self.load_images(choice)
        self.setup_homography_matrix()
        self.restore_distortion(choice)

    def load_images(self, choice):
        img_location = "input/custom/"
        self.img1 = cv2.imread(img_location + "Img1.jpg")
        self.img2 = cv2.imread(img_location + "Img2.jpg")
        self.img3 = cv2.imread(img_location + "Img3.jpg")
        self.height1, self.width1 = self.img1.shape[:2]
        self.height2, self.width2 = self.img2.shape[:2]
        self.height3, self.width3 = self.img3.shape[:2]

    def setup_homography_matrix(self):
        conic1 = Conic.Conic_op(self.point1)
        self.conic_matrix1 = conic1.get_homography_matrix()
        conic2 = Conic.Conic_op(self.point2)
        self.conic_matrix2 = conic2.get_homography_matrix()
        conic3 = Conic.Conic_op(self.point3)
        self.conic_matrix3 = conic3.get_homography_matrix()

    def restore_distortion(self, choice):
        filename1 = "custom/one_step_restored_img1"
        filename2 = "custom/one_step_restored_img2"
        filename3 = "custom/one_step_restored_img3"
        Output.output(self.img1, self.conic_matrix1, self.width1,
                      self.height1, filename1, option=1)
        Output.output(self.img2, self.conic_matrix2, self.width2,
                      self.height2, filename2, option=1)
        Output.output(self.img3, self.conic_matrix3, self.width3,
                      self.height3, filename3, option=1)

    def setup_coordinate(self, selection):
        choice = int(selection)
        self.point1 = {}
        self.point2 = {}
        self.point3 = {}
        if choice == 1:
            # set 1 coordinates
            # Image 1 coordinates
            self.point1['A'] = [959, 49]
            self.point1['B'] = [793, 93]
            self.point1['C'] = [980, 474]
            self.point1['D'] = [802, 469]
            self.point1['E'] = [971, 255]
            self.point1['F'] = [274, 796]
            self.point1['G'] = [655, 147]
            self.point1['H'] = [566, 169]
            self.point1['I'] = [666, 479]
            self.point1['J'] = [227, 256]
            self.point1['K'] = [304, 469]
            self.point1['L'] = [228, 470]
            # Image 2 coordinates
            self.point2['A'] = [58, 2]
            self.point2['B'] = [219, 82]
            self.point2['C'] = [45, 633]
            self.point2['D'] = [218, 609]
            self.point2['E'] = [52, 170]
            self.point2['F'] = [216, 231]
            self.point2['G'] = [340, 135]
            self.point2['H'] = [418, 175]
            self.point2['I'] = [352, 567]
            self.point2['J'] = [512, 244]
            self.point2['K'] = [470, 564]
            self.point2['L'] = [526, 554]
            # Image 3 coordinates
            self.point3['A'] = [1001, 150]
            self.point3['B'] = [749, 204]
            self.point3['C'] = [1012, 656]
            self.point3['D'] = [749, 634]
            self.point3['E'] = [1008, 393]
            self.point3['F'] = [748, 419]
            self.point3['G'] = [653, 246]
            self.point3['H'] = [559, 262]
            self.point3['I'] = [648, 616]
            self.point3['J'] = [390, 240]
            self.point3['K'] = [505, 412]
            self.point3['L'] = [382, 425]

if __name__ == '__main__':
    temp = HW_problem3_T2()
