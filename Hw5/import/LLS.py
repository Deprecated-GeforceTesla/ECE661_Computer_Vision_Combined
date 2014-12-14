import cv2
import numpy as np

class LLS(object):

    def __init__(self, inliers1, inliers2):
        #print inliers1
        #print inliers2
        self.inliers1 = inliers1
        self.inliers2 = inliers2

    def get_homography(self):
        inliers_num = len(self.inliers1)
        matrix_A = np.zeros((inliers_num*2,8))
        matrix_B = np.zeros(inliers_num*2)
        vector_H = np.zeros(8)
        matrix_H = np.zeros((3,3))
        
        for i in range(inliers_num):
            matrix_A[2 * i + 1][0] = self.inliers1[i]['x']
            matrix_A[2 * i + 1][1] = self.inliers1[i]['y']
            matrix_A[2 * i + 1][2] = 1
            matrix_A[2 * i + 1][6] = -self.inliers2[i]['x'] * self.inliers1[i]['x']
            matrix_A[2 * i + 1][7] = -self.inliers2[i]['x'] * self.inliers1[i]['y']

            matrix_A[2 * i][3] = self.inliers1[i]['x']
            matrix_A[2 * i][4] = self.inliers1[i]['y']
            matrix_A[2 * i][5] = 1
            matrix_A[2 * i][6] = -self.inliers2[i]['y'] * self.inliers1[i]['x']
            matrix_A[2 * i][7] = -self.inliers2[i]['y'] * self.inliers1[i]['y']

            matrix_B[2 * i] = self.inliers2[i]['y']
            matrix_B[2 * i + 1] = self.inliers2[i]['x']
            
        matrix_AtA = np.dot(matrix_A.T, matrix_A)

        matrix_AtB = np.dot(matrix_A.T, matrix_B)
        vector_H = np.dot(np.linalg.inv(matrix_AtA), matrix_AtB)
        Ds, V, Vt = cv2.SVDecomp(matrix_AtA)


        for i in range(3):
            for j in range(3):
                if(i == 2 and j == 2): 
                    matrix_H[i][j] = 1
                else:
                    matrix_H[i][j] = vector_H[i*3+j]

        return matrix_H
