import cv2
import numpy as np

class Epipole_Op(object):

    def __init__(self, matrix_F):
        self.matrix_F = matrix_F
        self.find_epipoles_and_matrix_P()

    def find_epipoles_and_matrix_P(self):
        self.e1 = np.zeros(3)
        self.e2 = np.zeros(3)
    
        w, u, vt = cv2.SVDecomp(self.matrix_F)
        v = vt.T
 
        for i in range(3):
            self.e1[i] = v[i, 2]/v[2, 2]
            self.e2[i] = u[i, 2]/u[2, 2]
    
        self.P1 = np.zeros((3,4))
        self.P2 = np.zeros((3,4))
        epipolar_v = np.zeros((3,3))
  
        self.P1[0, 0] = 1
        self.P1[1, 1] = 1
        self.P1[2, 2] = 1
    
        epipolar_v[0, 1] = -self.e2[2]
        epipolar_v[0, 2] = self.e2[1]
        epipolar_v[1, 0] = self.e2[2]
        epipolar_v[1, 2] = -self.e2[0]
        epipolar_v[2, 0] = -self.e2[1]
        epipolar_v[2, 1] = self.e2[0]
    
        ef = np.dot(epipolar_v, self.matrix_F)
        for i in range(3):
            for j in range(3):
                self.P2[i,j] = ef[i,j]
        for i in range(3):
            self.P2[i,3] = self.e2[i]
    
    def get_epipole1(self):
        return self.e1

    def get_epipole2(self):
        return self.e2

    def get_matrix_P1(self):
        return self.P1

    def get_matrix_P2(self):
        return self.P2
