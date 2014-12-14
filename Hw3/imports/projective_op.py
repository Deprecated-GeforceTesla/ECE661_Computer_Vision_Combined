import numpy as np


class Projective_op(object):

    def __init__(self, pt_a, pt_b, pt_c, pt_d):
        self.group_points_to_line(pt_a, pt_b, pt_c, pt_d)
        self.compute_vanishing_line()
        self.set_up_matrix_h()

    def convert_points_to_coordinates(self, point):
        temp = list(point)
        temp.append(1)
        return temp

    def group_points_to_line(self, pt_a, pt_b, pt_c, pt_d):
        point_a = self.convert_points_to_coordinates(pt_a)
        point_b = self.convert_points_to_coordinates(pt_b)
        point_c = self.convert_points_to_coordinates(pt_c)
        point_d = self.convert_points_to_coordinates(pt_d)
        # cross product to get lines. hor-> supposed horizontal
        self.line_hor1 = np.cross(point_a, point_b)
        self.line_hor2 = np.cross(point_c, point_d)
        # ver -> supposed vertical lile
        self.line_ver1 = np.cross(point_a, point_c)
        self.line_ver2 = np.cross(point_b, point_d)

    def compute_vanishing_line(self):
        point_1 = np.cross(self.line_hor1, self.line_hor2)
        point_2 = np.cross(self.line_ver1, self.line_ver2)
        self.van_line = np.cross(point_1, point_2)

    def set_up_matrix_h(self):
        self.matrix_h = np.zeros(shape=(3,3))
        self.matrix_h[0][0] = 1
        self.matrix_h[1][1] = 1
        self.matrix_h[2] = self.van_line

    def get_homography_matrix(self):
        return self.matrix_h

if __name__ == '__main__':
    temp = Projective_op([320,90], [472,150], [272,465], [430,442])
