import sys
import cv2
import numpy as np
sys.path.append("imports/")
import projective_op as Projective
import conic_op as Conic
import image_output as Output

class HW_problem2(object):

    def __init__(self):
        choice = raw_input("Which set of image? (1-4): ")
        self.setup_coordinate(choice)
        self.load_images(choice)
        self.setup_homography_matrix()
        self.restore_distortion(choice)

    def load_images(self, choice):
        img_location = "input/Set" + str(choice) + "/"
        self.img1 = cv2.imread(img_location + "Img1.jpg")
        self.img2 = cv2.imread(img_location + "Img2.jpg")
        self.height1, self.width1 = self.img1.shape[:2]
        self.height2, self.width2 = self.img2.shape[:2]

    def setup_homography_matrix(self):
        conic1 = Conic.Conic_op(self.point1)
        self.conic_matrix1 = conic1.get_homography_matrix()
        conic2 = Conic.Conic_op(self.point2)
        self.conic_matrix2 = conic2.get_homography_matrix()

    def restore_distortion(self, choice):
        filename1 = "set" + str(choice) + "/one_step_restored_img1"
        filename2 = "set" + str(choice) + "/one_step_restored_img2"
        Output.output(self.img1, self.conic_matrix1, self.width1,
                      self.height1, filename1, option=1)
        Output.output(self.img2, self.conic_matrix2, self.width2,
                      self.height2, filename2, option=1)

    def setup_coordinate(self, selection):
        choice = int(selection)
        self.point1 = {}
        self.point2 = {}
        if choice == 1:
            # set 1 coordinates
            # Image 1 coordinates
            self.point1['A'] = [320, 90]
            self.point1['B'] = [472, 150]
            self.point1['C'] = [272, 456]
            self.point1['D'] = [430, 442]
            self.point1['E'] = [290, 298]
            self.point1['F'] = [454, 314]
            self.point1['G'] = [600, 203]
            self.point1['H'] = [666, 226]
            self.point1['I'] = [572, 445]
            self.point1['J'] = [744, 254]
            self.point1['K'] = [671, 439]
            self.point1['L'] = [720, 430]
            # Image 2 coordinates
            self.point2['A'] = [730, 111]
            self.point2['B'] = [570, 142]
            self.point2['C'] = [740, 441]
            self.point2['D'] = [583, 416]
            self.point2['E'] = [738, 346]
            self.point2['F'] = [578, 342]
            self.point2['G'] = [511, 153]
            self.point2['H'] = [413, 174]
            self.point2['I'] = [526, 408]
            self.point2['J'] = [303, 196]
            self.point2['K'] = [386, 391]
            self.point2['L'] = [320, 381]
        elif choice == 2:
            # set 2 coordinates
            # Image 1 coordinates
            self.point1['A'] = [736, 30]
            self.point1['B'] = [495, 84]
            self.point1['C'] = [735, 550]
            self.point1['D'] = [503, 472]
            self.point1['E'] = [736, 369]
            self.point1['F'] = [499, 355]
            self.point1['G'] = [437, 155]
            self.point1['H'] = [382, 164]
            self.point1['I'] = [436, 226]
            self.point1['J'] = [236, 209]
            self.point1['K'] = [276, 398]
            self.point1['L'] = [238, 384]
            # Image 2 coordinates
            self.point2['A'] = [151, 112]
            self.point2['B'] = [365, 143]
            self.point2['C'] = [158, 461]
            self.point2['D'] = [369, 421]
            self.point2['E'] = [157, 400]
            self.point2['F'] = [365, 365]
            self.point2['G'] = [468, 158]
            self.point2['H'] = [574, 172]
            self.point2['I'] = [465, 502]
            self.point2['J'] = [543, 213]
            self.point2['K'] = [501, 383]
            self.point2['L'] = [540, 373]
        elif choice == 3:
            # set 3 coordinates
            # Image 1 coordinates
            self.point1['A'] = [48, 32]
            self.point1['B'] = [448, 86]
            self.point1['C'] = [68, 518]
            self.point1['D'] = [443, 415]
            self.point1['E'] = [66, 428]
            self.point1['F'] = [442, 401]
            self.point1['G'] = [529, 171]
            self.point1['H'] = [622, 178]
            self.point1['I'] = [526, 428]
            self.point1['J'] = [619, 199]
            self.point1['K'] = [555, 382]
            self.point1['L'] = [615, 364]
            # Image 2 coordinates
            self.point2['A'] = [755, 133]
            self.point2['B'] = [609, 158]
            self.point2['C'] = [748, 514]
            self.point2['D'] = [605, 476]
            self.point2['E'] = [751, 327]
            self.point2['F'] = [606, 317]
            self.point2['G'] = [503, 147]
            self.point2['H'] = [424, 165]
            self.point2['I'] = [502, 260]
            self.point2['J'] = [391, 281]
            self.point2['K'] = [485, 391]
            self.point2['L'] = [390, 376]
        elif choice == 4:
            # set 4 coordinates
            # Image 1 coordinates
            self.point1['A'] = [185, 113]
            self.point1['B'] = [218, 154]
            self.point1['C'] = [175, 248]
            self.point1['D'] = [217, 279]
            self.point1['E'] = [180, 175]
            self.point1['F'] = [217, 201]
            self.point1['G'] = [228, 172]
            self.point1['H'] = [249, 197]
            self.point1['I'] = [228, 273]
            self.point1['J'] = [261, 237]
            self.point1['K'] = [250, 295]
            self.point1['L'] = [265, 306]
            # Image 2 coordinates
            self.point2['A'] = [541, 75]
            self.point2['B'] = [431, 99]
            self.point2['C'] = [580, 404]
            self.point2['D'] = [427, 422]
            self.point2['E'] = [552, 177]
            self.point2['F'] = [427, 204]
            self.point2['G'] = [403, 187]
            self.point2['H'] = [339, 202]
            self.point2['I'] = [394, 400]
            self.point2['J'] = [327, 262]
            self.point2['K'] = [349, 436]
            self.point2['L'] = [310, 440]

if __name__ == '__main__':
    temp = HW_problem2()
