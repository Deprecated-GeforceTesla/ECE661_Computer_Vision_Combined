import numpy as np
import cv2

class Affine_op(object):

    def __init__(self, pt_a, pt_b, pt_c, pt_e, pt_f):
        self.group_points_to_line(pt_a, pt_b, pt_c, pt_e, pt_f)
        self.find_s_element()
        self.find_matrix_a()
        self.find_homography_matrix()

    def convert_points_to_coordinates(self, point):
        temp = point[:]
        temp.append(1)
        return temp
        
    def group_points_to_line(self, pt_a, pt_b, pt_c, pt_e, pt_f):
        point_a = self.convert_points_to_coordinates(pt_a)
        point_b = self.convert_points_to_coordinates(pt_b)
        point_c = self.convert_points_to_coordinates(pt_c)
        point_e = self.convert_points_to_coordinates(pt_e)

        point_f = self.convert_points_to_coordinates(pt_f)
        # first pair of orthogonal lines
        self.line_pair1_a = np.cross(point_a, point_b)
        self.line_pair1_b = np.cross(point_a, point_c)
        # second pair of orthogonal lines
        self.line_pair2_a = np.cross(point_a, point_f)
        self.line_pair2_b = np.cross(point_b, point_e)

    def find_s_element(self):
        matrix_a = np.zeros(shape=(2,2))
        matrix_a[0][0] = self.line_pair1_a[0] * self.line_pair1_b[0]
        matrix_a[0][1] = (self.line_pair1_a[0] * self.line_pair1_b[1] +
                          self.line_pair1_a[1] * self.line_pair1_b[0])
        matrix_a[1][0] = self.line_pair2_a[0] * self.line_pair2_b[0]
        matrix_a[1][1] = (self.line_pair2_a[0] * self.line_pair2_b[1] +
                          self.line_pair2_a[1] * self.line_pair2_b[0])

        matrix_b = np.zeros(shape=(2,1))
        matrix_b[0][0] = -1 * self.line_pair1_a[1] * self.line_pair1_b[1]
        matrix_b[1][0] = -1 * self.line_pair2_a[1] * self.line_pair2_b[1]

        result = np.linalg.solve(matrix_a, matrix_b)
        self.matrix_s = np.zeros(shape=(2,2))
        self.matrix_s[0][0] = result[0]
        self.matrix_s[0][1] = result[1]
        self.matrix_s[1][0] = result[1]
        self.matrix_s[1][1] = 1

    def find_matrix_a(self):
        matrix_d, matrix_v, matrix_vt = cv2.SVDecomp(self.matrix_s)
        matrix_da = np.zeros(shape=(2,2))
        matrix_da[0][0] = matrix_d[0] ** (0.5)
        matrix_da[1][1] = matrix_d[1] ** (0.5)
        self.matrix_a = np.dot(np.dot(matrix_v, matrix_da), matrix_vt)

    def find_homography_matrix(self):
        self.matrix_h = np.zeros(shape=(3,3))
        self.matrix_h[0][0] = self.matrix_a[0][0]
        self.matrix_h[0][1] = self.matrix_a[0][1]
        self.matrix_h[1][0] = self.matrix_a[1][0]
        self.matrix_h[1][1] = self.matrix_a[1][1]
        self.matrix_h[2][2] = 1

    def get_homography_matrix(self):
        return self.matrix_h
