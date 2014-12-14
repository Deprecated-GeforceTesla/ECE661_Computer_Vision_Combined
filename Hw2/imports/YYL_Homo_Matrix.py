import numpy as np


class Homo_Matrix(object):

    def __init__(self, world_pt, image_pt, points=4):
        '''Initialize the required resources to find the homography matrix.
        @param world_pt The 4 points of coordinates in world plane in format
                        of dictionary in list. ie: [{'x': 1, 'y': 2}, {}...]
        @param image_pt The 4 points of coordinates in image plane in format
                        of dictionary in list. ie: [{'x': 1, 'y': 2}, {}...]
        @param points The amount of points used to calculate the matrix
        '''
        self.amount_of_points = points
        self.set_up_calculation_matrix_for_h(world_pt, image_pt)
        self.set_up_image_matrix(image_pt)

    def set_up_image_matrix(self, image_pt):
        '''Setup the 8x1 matrix of 4 image points
        @param image_pt The 4 points of coordinates in image plane in format
                        of dictionary in list. ie: [{'x': 1, 'y': 2}, {}...]
        '''
        self.image_matrix = np.zeros(shape=(self.amount_of_points*2,1))
        pos = 0
        for i in range(self.amount_of_points * 2):
            if i % 2 == 0:
                self.image_matrix[i][0] = image_pt[pos]['x']
            else:
                self.image_matrix[i][0] = image_pt[pos]['y']
                pos += 1 
    
    def set_up_calculation_matrix_for_h(self, world_pt, image_pt):
        '''Setup the matrix that is later on used to calculate the homography
        @param world_pt The 4 points of coordinates in world plane in format
                        of dictionary in list. ie: [{'x': 1, 'y': 2}, {}...]
        @param image_pt The 4 points of coordinates in image plane in format
                        of dictionary in list. ie: [{'x': 1, 'y': 2}, {}...]
        '''
        self.matrix_a = np.zeros(shape=(self.amount_of_points * 2, 8))
        pt_pos = 0
        for i in range(self.amount_of_points * 2):
            if i % 2 == 0:
                self.matrix_a[i][0] = world_pt[pt_pos]['x']
                self.matrix_a[i][1] = world_pt[pt_pos]['y']
                self.matrix_a[i][2] = 1

                self.matrix_a[i][6] = (world_pt[pt_pos]['x'] *
                                       image_pt[pt_pos]['x'] * -1)

                self.matrix_a[i][7] = (world_pt[pt_pos]['y'] *
                                       image_pt[pt_pos]['x'] * -1)
            else:
                self.matrix_a[i][3] = world_pt[pt_pos]['x']
                self.matrix_a[i][4] = world_pt[pt_pos]['y']
                self.matrix_a[i][5] = 1

                self.matrix_a[i][6] = (world_pt[pt_pos]['x'] *
                                       image_pt[pt_pos]['y'] * -1)

                self.matrix_a[i][7] = (world_pt[pt_pos]['y'] *
                                       image_pt[pt_pos]['y'] * -1)
                pt_pos += 1

    def get_homography_matrix(self):
        '''Calculates the homography matrix
        @return the homography matrix
        '''
        if self.amount_of_points == 4:
            result = np.linalg.solve(self.matrix_a, self.image_matrix)
        else:
            # If there are more than 4 points, use (AT * A)^-1 * A^T * b = x
            matrix_a_t = np.transpose(self.matrix_a)
            matrix_a_t_a_inv = np.linalg.inv(np.dot(matrix_a_t,
                                             self.matrix_a))

            result = np.dot(np.dot(matrix_a_t_a_inv, matrix_a_t),
                            self.image_matrix)
                        
        homography_matrix = np.zeros(shape=(3,3))
        for i in range(8):
            homography_matrix[i / 3][i % 3] = result[i][0]
        homography_matrix[2][2] = 1
        return homography_matrix


if __name__ == '__main__':
    point_a = {'x': 0, 'y': 0}
    point_b = {'x': 1, 'y': 0}
    point_c = {'x': 1, 'y': 1}
    point_d = {'x': 0, 'y': 1}
    ptw = []
    ptw.append(point_a)
    ptw.append(point_b)
    ptw.append(point_c)
    ptw.append(point_d)
    mat = yyl_homo_matrix(ptw, ptw)
    print mat.get_homography_matrix()
