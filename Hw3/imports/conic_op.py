import numpy as np
import cv2


class Conic_op(object):

    def __init__(self, pts):
        self.group_points_to_line(pts)
        self.set_up_matrix_c()
        self.set_up_matrix_s()
        self.find_matrix_a()
        self.find_vector_v()
        self.find_homography_matrix()

    def convert_points_to_coordinates(self, point):
        temp = list(point)
        temp.append(1)
        return temp

    def group_points_to_line(self, pts):
        point_a = self.convert_points_to_coordinates(pts['A'])
        point_b = self.convert_points_to_coordinates(pts['B'])
        point_c = self.convert_points_to_coordinates(pts['C'])
        point_d = self.convert_points_to_coordinates(pts['D'])
        point_e = self.convert_points_to_coordinates(pts['E'])
        point_f = self.convert_points_to_coordinates(pts['F'])
        point_g = self.convert_points_to_coordinates(pts['G'])
        point_h = self.convert_points_to_coordinates(pts['H'])
        point_i = self.convert_points_to_coordinates(pts['I'])
        point_j = self.convert_points_to_coordinates(pts['J'])
        point_k = self.convert_points_to_coordinates(pts['K'])
        point_l = self.convert_points_to_coordinates(pts['L'])

        self.lines = []
        temp = {}
        # cross product to get lines.
        temp['line_a'] = np.cross(point_a, point_b)
        temp['line_b'] = np.cross(point_a, point_c)
        self.lines.append(temp)
        temp = {}
        temp['line_a']  = np.cross(point_c, point_d)
        temp['line_b'] = np.cross(point_b, point_d)
        self.lines.append(temp)
        temp = {}
        temp['line_a'] = np.cross(point_a, point_f)
        temp['line_b'] = np.cross(point_b, point_e)
        self.lines.append(temp)
        temp = {}
        temp['line_a'] = np.cross(point_g, point_h)
        temp['line_b'] = np.cross(point_g, point_i)
        self.lines.append(temp)
        temp = {}
        temp['line_a'] = np.cross(point_l, point_j)
        temp['line_b'] = np.cross(point_l, point_k)
        self.lines.append(temp)

    def set_up_matrix_c(self):
        matrix_a = np.zeros(shape=(5,5))
        matrix_b = np.zeros(shape=(5,1))
        for i in range(5):
            line1 = self.lines[i]['line_a']
            line2 = self.lines[i]['line_b']
            matrix_a[i][0] = line1[0] * line2[0]

            matrix_a[i][1] = ((line1[1] * line2[0]) +
                                   (line1[0] * line2[1])) / 2

            matrix_a[i][2] = line1[1] * line2[1]

            matrix_a[i][3] = ((line1[0] * line2[2]) +
                                   (line1[2] * line2[0])) / 2

            matrix_a[i][4] = ((line1[1] * line2[2]) +
                                   (line1[2] * line2[1])) / 2

            matrix_b[i][0] = line1[2] * line2[2] * -1

        self.result_c = np.linalg.solve(matrix_a, matrix_b)

    def set_up_matrix_s(self):
        #extract matrix s
        self.matrix_s = np.zeros(shape=(2,2))
        self.matrix_s[0][0] = self.result_c[0]
        self.matrix_s[0][1] = self.result_c[1] / 2
        self.matrix_s[1][0] = self.result_c[1] / 2
        self.matrix_s[1][1] = self.result_c[2]

    def find_matrix_a(self):
        matrix_d, matrix_v, matrix_vt = cv2.SVDecomp(self.matrix_s)
        matrix_da = np.zeros(shape=(2,2))
        matrix_da[0][0] = matrix_d[0] ** (0.5)
        matrix_da[1][1] = matrix_d[1] ** (0.5)
        self.matrix_a = np.dot(np.dot(matrix_v, matrix_da), matrix_vt)

    def find_vector_v(self):
        vector_b = np.zeros(shape=(2,1))
        vector_b[0][0] = self.result_c[3] / 2
        vector_b[1][0] = self.result_c[4] / 2
        self.vector_v = np.linalg.solve(self.matrix_a, vector_b)

    def find_homography_matrix(self):
        self.matrix_h = np.zeros(shape=(3,3))
        self.matrix_h[0][0] = self.matrix_a[0][0]
        self.matrix_h[0][1] = self.matrix_a[0][1]
        self.matrix_h[1][0] = self.matrix_a[1][0]
        self.matrix_h[1][1] = self.matrix_a[1][1]
        self.matrix_h[2][0] = self.vector_v[0][0]
        self.matrix_h[2][1] = self.vector_v[1][0]
        self.matrix_h[2][2] = 1

    def get_homography_matrix(self):
        return self.matrix_h

if __name__ == '__main__':
    test_point = {}
    test_point['A'] = [320, 90]
    test_point['B'] = [472, 150]
    test_point['C'] = [272, 456]
    test_point['D'] = [430, 442]
    test_point['E'] = [290, 298]
    test_point['F'] = [454, 314]
    test_point['G'] = [762, 262]
    test_point['H'] = [799, 273]
    test_point['I'] = [742, 428]
    test_point['J'] = [896, 302]
    test_point['K'] = [864, 409]
    test_point['L'] = [884, 405]
    temp = Conic_op(test_point)
