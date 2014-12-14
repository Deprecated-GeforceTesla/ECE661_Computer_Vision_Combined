import cv2
import numpy as np

class Fundamental_Op(object):

    def __init__(self, pt1, pt2, count):
        self.pt1 = pt1
        self.pt2 = pt2
        self.count = count
        self.T1 = self.get_normalization_matrix(self.pt1)
        self.T2 = self.get_normalization_matrix(self.pt2)
        self.compute_matrix_F()

    def get_normalization_matrix(self, pts):
        norm_matrix = np.zeros((3,3))
        x_mean = 0
        y_mean = 0
        variance = 0

        for i in range(self.count):
            x_mean += pts[i, 0]
            y_mean += pts[i, 1]
        x_mean /= float(self.count)
        y_mean /= float(self.count)

        for i in range(self.count):
            variance += (np.sqrt(np.power((pts[i, 0] - x_mean), 2) +
                         np.power((pts[i, 1] - y_mean), 2)))

        variance /= float(self.count)
    
        scale = np.sqrt(2) / variance
        norm_x = -x_mean * scale
        norm_y = -y_mean * scale
        norm_matrix[0, 0] = scale
        norm_matrix[0, 2] = norm_x
        norm_matrix[1, 2] = norm_y
        norm_matrix[1, 1] = scale
        norm_matrix[2, 2] = 1

        return norm_matrix        

    def compute_matrix_F(self):
        A = np.zeros((self.count, 9))
        F = np.zeros((3, 3))

        self.pt1_norm = np.dot(self.pt1, self.T1.T)
        self.pt2_norm = np.dot(self.pt2, self.T2.T)
    
        for i in range(self.count):
            A[i, 0] = self.pt1_norm[i, 0] * self.pt2_norm[i, 0]
            A[i, 1] = self.pt1_norm[i, 1] * self.pt2_norm[i, 0]
            A[i, 2] = self.pt2_norm[i, 0]
            A[i, 3] = self.pt1_norm[i, 0] * self.pt2_norm[i, 1]
            A[i, 4] = self.pt1_norm[i, 1] * self.pt2_norm[i, 1]
            A[i, 5] = self.pt2_norm[i, 1] 
            A[i, 6] = self.pt1_norm[i, 0]
            A[i, 7] = self.pt1_norm[i, 1]
            A[i, 8] = 1

        Ds_A, V_A, Vt_A = cv2.SVDecomp(A)
        min_index = Ds_A.argmin()
        F = Vt_A[min_index].reshape(3,3)

        Ds_F_new = np.zeros((3,3))
        Ds_F, V_F, Vt_F = cv2.SVDecomp(F)
        min_index = Ds_F.argmin()
    
        Ds_F_new[0,0] = Ds_F[0]
        Ds_F_new[1,1] = Ds_F[1]
        Ds_F_new[2,2] = Ds_F[2]
        Ds_F_new[min_index,min_index] = 0
    
        self.matrix_F = np.dot(np.dot(V_F, Ds_F_new), Vt_F)

        self.matrix_F = np.dot(np.dot(self.T2.T, self.matrix_F), self.T1)
    
    def get_matrix_F(self):
        return self.matrix_F
