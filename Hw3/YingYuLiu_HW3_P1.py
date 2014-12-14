import sys
import cv2
import numpy as np
sys.path.append("imports/")
import projective_op as Projective
import affine_op as Affine
import Image_Coord_Op as Image_op
import image_output as Output

class HW_problem1(object):

    def __init__(self):
        choice = raw_input("Which set of image? (1-4): ")
        self.setup_coordinate(choice)
        self.load_images(choice)
        self.setup_homography_matrix()
        self.restore_projective_distortion(choice)
        self.restore_affine_distortion(choice)

    def load_images(self, choice):
        img_location = "input/Set" + str(choice) + "/"
        self.img1 = cv2.imread(img_location + "Img1.jpg")
        self.img2 = cv2.imread(img_location + "Img2.jpg")
        self.height1, self.width1 = self.img1.shape[:2]
        self.height2, self.width2 = self.img2.shape[:2]

    def setup_homography_matrix(self):

        projective1 = Projective.Projective_op(self.pt1_A, self.pt1_B,
                                               self.pt1_C, self.pt1_D)

        projective2 = Projective.Projective_op(self.pt2_A, self.pt2_B,
                                               self.pt2_C, self.pt2_D)

        affine1 = Affine.Affine_op(self.pt1_A, self.pt1_B, self.pt1_C,
                                   self.pt1_E, self.pt1_F)

        affine2 = Affine.Affine_op(self.pt2_A, self.pt2_B, self.pt2_C,
                                   self.pt2_E, self.pt2_F)

        self.projective_homo_matrix1 = projective1.get_homography_matrix()
        self.affine_homo_matrix1 = affine1.get_homography_matrix()
        self.projective_homo_matrix2 = projective2.get_homography_matrix()
        self.affine_homo_matrix2 = affine2.get_homography_matrix()

    def restore_projective_distortion(self, choice):
        filename1 = "set" + str(choice) + "/projective_restored_img1"
        filename2 = "set" + str(choice) + "/projective_restored_img2"

        Output.output(self.img1, self.projective_homo_matrix1, self.width1,
                      self.height1, filename1)
        Output.output(self.img2, self.projective_homo_matrix2, self.width2,
                      self.height2, filename2)

    def restore_affine_distortion(self, choice):
        filename1 = "set" + str(choice) + "/affine_restored_img1"
        filename2 = "set" + str(choice) + "/affine_restored_img2"

        proj_mat1_inv = Image_op.matrix_inverse(self.projective_homo_matrix1)
        proj_mat2_inv = Image_op.matrix_inverse(self.projective_homo_matrix2)

        homo_matrix1 = np.dot(proj_mat1_inv, self.affine_homo_matrix1)
        homo_matrix2 = np.dot(proj_mat2_inv, self.affine_homo_matrix2)

        Output.output(self.img1, homo_matrix1, self.width1,
                      self.height1, filename1, 1)
        Output.output(self.img2, homo_matrix2, self.width2,
                      self.height2, filename2, 1)


    def setup_coordinate(self, selection):
        choice = int(selection)
        if choice == 1:
            # set 1 coordinates
            # Image 1 coordinates
            self.pt1_A = [320, 90]
            self.pt1_B = [472, 150]
            self.pt1_C = [272, 456]
            self.pt1_D = [430, 442]
            self.pt1_E = [290, 298]
            self.pt1_F = [454, 314]
            # Image 2 coordinates
            self.pt2_A = [730, 111]
            self.pt2_B = [570, 142]
            self.pt2_C = [740, 441]
            self.pt2_D = [583, 416]
            self.pt2_E = [738, 346]
            self.pt2_F = [578, 342]
        elif choice == 2:
            # set 2 coordinates
            # Image 1 coordinates
            self.pt1_A = [736, 30]
            self.pt1_B = [495, 84]
            self.pt1_C = [735, 550]
            self.pt1_D = [503, 472]
            self.pt1_E = [736, 369]
            self.pt1_F = [499, 355]
            # Image 2 coordinates
            self.pt2_A = [151, 112]
            self.pt2_B = [365, 143]
            self.pt2_C = [158, 461]
            self.pt2_D = [369, 421]
            self.pt2_E = [157, 400]
            self.pt2_F = [365, 365]
        elif choice == 3:
            # set 3 coordinates
            # Image 1 coordinates
            self.pt1_A = [48, 32]
            self.pt1_B = [448, 86]
            self.pt1_C = [68, 518]
            self.pt1_D = [443, 415]
            self.pt1_E = [66, 428]
            self.pt1_F = [442, 401]
            # Image 2 coordinates
            self.pt2_A = [755, 133]
            self.pt2_B = [609, 158]
            self.pt2_C = [748, 514]
            self.pt2_D = [605, 476]
            self.pt2_E = [751, 327]
            self.pt2_F = [606, 317]
        elif choice == 4:
            # set 4 coordinates
            # Image 1 coordinates
            self.pt1_A = [185, 113]
            self.pt1_B = [218, 154]
            self.pt1_C = [175, 248]
            self.pt1_D = [217, 279]
            self.pt1_E = [180, 175]
            self.pt1_F = [217, 201]
            # Image 2 coordinates
            self.pt2_A = [541, 75]
            self.pt2_B = [431, 99]
            self.pt2_C = [580, 404]
            self.pt2_D = [427, 422]
            self.pt2_E = [552, 177]
            self.pt2_F = [427, 204]

if __name__ == '__main__':
    temp = HW_problem1()
