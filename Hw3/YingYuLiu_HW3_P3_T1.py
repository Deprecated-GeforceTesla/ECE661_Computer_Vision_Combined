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
        choice = str(1)
        self.setup_coordinate(choice)
        self.load_images(choice)
        self.setup_homography_matrix()
        self.restore_projective_distortion(choice)
        self.restore_affine_distortion(choice)

    def load_images(self, choice):
        img_location = "input/custom/"
        self.img1 = cv2.imread(img_location + "Img1.jpg")
        self.img2 = cv2.imread(img_location + "Img2.jpg")
        self.img3 = cv2.imread(img_location + "Img3.jpg")
        self.height1, self.width1 = self.img1.shape[:2]
        self.height2, self.width2 = self.img2.shape[:2]
        self.height3, self.width3 = self.img3.shape[:2]

    def setup_homography_matrix(self):

        projective1 = Projective.Projective_op(self.pt1_A, self.pt1_B,
                                               self.pt1_C, self.pt1_D)

        projective2 = Projective.Projective_op(self.pt2_A, self.pt2_B,
                                               self.pt2_C, self.pt2_D)

        projective3 = Projective.Projective_op(self.pt3_A, self.pt3_B,
                                               self.pt3_C, self.pt3_D)

        affine1 = Affine.Affine_op(self.pt1_A, self.pt1_B, self.pt1_C,
                                   self.pt1_E, self.pt1_F)

        affine2 = Affine.Affine_op(self.pt2_A, self.pt2_B, self.pt2_C,
                                   self.pt2_E, self.pt2_F)

        affine3 = Affine.Affine_op(self.pt3_A, self.pt3_B, self.pt3_C,
                                   self.pt3_E, self.pt3_F)

        self.projective_homo_matrix1 = projective1.get_homography_matrix()
        self.affine_homo_matrix1 = affine1.get_homography_matrix()
        self.projective_homo_matrix2 = projective2.get_homography_matrix()
        self.affine_homo_matrix2 = affine2.get_homography_matrix()
        self.projective_homo_matrix3 = projective3.get_homography_matrix()
        self.affine_homo_matrix3 = affine3.get_homography_matrix()

    def restore_projective_distortion(self, choice):
        filename1 = "custom/projective_restored_img1"
        filename2 = "custom/projective_restored_img2"
        filename3 = "custom/projective_restored_img3"

        Output.output(self.img1, self.projective_homo_matrix1, self.width1,
                      self.height1, filename1)
        Output.output(self.img2, self.projective_homo_matrix2, self.width2,
                      self.height2, filename2)
        Output.output(self.img3, self.projective_homo_matrix3, self.width3,
                      self.height3, filename3)

    def restore_affine_distortion(self, choice):
        filename1 = "custom/affine_restored_img1"
        filename2 = "custom/affine_restored_img2"
        filename3 = "custom/affine_restored_img3"

        proj_mat1_inv = Image_op.matrix_inverse(self.projective_homo_matrix1)
        proj_mat2_inv = Image_op.matrix_inverse(self.projective_homo_matrix2)
        proj_mat3_inv = Image_op.matrix_inverse(self.projective_homo_matrix3)

        homo_matrix1 = np.dot(proj_mat1_inv, self.affine_homo_matrix1)
        homo_matrix2 = np.dot(proj_mat2_inv, self.affine_homo_matrix2)
        homo_matrix3 = np.dot(proj_mat3_inv, self.affine_homo_matrix3)

        Output.output(self.img1, homo_matrix1, self.width1,
                      self.height1, filename1, 1)
        Output.output(self.img2, homo_matrix2, self.width2,
                      self.height2, filename2, 1)
        Output.output(self.img3, homo_matrix3, self.width3,
                      self.height3, filename3, 1)


    def setup_coordinate(self, selection):
        choice = int(selection)
        if choice == 1:
            # set 1 coordinates
            # Image 1 coordinates
            self.pt1_A = [959, 49]
            self.pt1_B = [793, 93]
            self.pt1_C = [980, 474]
            self.pt1_D = [802, 469]
            self.pt1_E = [971, 255]
            self.pt1_F = [274, 796]
            # Image 2 coordinates
            self.pt2_A = [58, 2]
            self.pt2_B = [219, 82]
            self.pt2_C = [45, 633]
            self.pt2_D = [218, 609]
            self.pt2_E = [52, 170]
            self.pt2_F = [216, 231]
            # Image 3 coordinates
            self.pt3_A = [1001, 150]
            self.pt3_B = [749, 204]
            self.pt3_C = [1012, 656]
            self.pt3_D = [749, 634]
            self.pt3_E = [1008, 393]
            self.pt3_F = [748, 419]

if __name__ == '__main__':
    temp = HW_problem1()
