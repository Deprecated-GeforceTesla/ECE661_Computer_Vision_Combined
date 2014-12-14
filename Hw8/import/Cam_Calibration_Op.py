import cv
import numpy as np

class Cam_Calibration(object):

    def __init__(self, h_list):
        self.h_list = h_list
        self.find_conic()
        self.find_matrix_k()
        self.find_matrix_r()

    def get_matrix_k(self):
        return self.matrix_k

    def get_matrix_r(self):
        return self.matrix_r_list

    def find_matrix_r(self):
        self.matrix_r_list = []
        for h in self.h_list:
            h1 = h[:, 0]
            h2 = h[:, 1]
            h3 = h[:, 2]

            k_inv = np.linalg.inv(self.matrix_k)
            vec_t = np.dot(k_inv, h3)
            mg = np.linalg.norm(np.dot(k_inv, h1))
            if (vec_t[2] < 0):
                mg = -mg
            vec_t /= mg
            vec_r1 = np.dot(k_inv, h1) / mg
            vec_r2 = np.dot(k_inv, h2) / mg
            vec_r3 = np.cross(vec_r1, vec_r2)

            matrix_r = np.zeros((3,3))
            matrix_r[:, 0] = vec_r1
            matrix_r[:, 1] = vec_r2
            matrix_r[:, 2] = vec_r3
            U, D, Vt = np.linalg.svd(matrix_r)
            matrix_r = np.dot(U, Vt)

            matrix_rt = np.zeros((3,4))
            matrix_rt[:, 0] = matrix_r[:, 0]
            matrix_rt[:, 1] = matrix_r[:, 1]
            matrix_rt[:, 2] = matrix_r[:, 2]
            matrix_rt[:, 3] = vec_t
            self.matrix_r_list.append(matrix_rt)

    def find_matrix_k(self):
        yo = (self.w[0][1] * self.w[0][2] - self.w[0][0] * self.w[1][2])
        yo /= (self.w[0][0] * self.w[1][1] - self.w[0][1] * self.w[0][1])


        lam = yo * (self.w[0][1] * self.w[0][2] - self.w[0][0] * self.w[1][2])
        lam += self.w[0][2] * self.w[0][2]
        lam = self.w[2][2] - lam
        lam /- self.w[0][0]

        alpha_x = np.sqrt(lam / self.w[0][0])
        alpha_y = lam * self.w[0][0]
        alpha_y /= (self.w[0][0] * self.w[1][1] - self.w[0][1]* self.w[0][1])
        alpha_y = np.sqrt(alpha_y)

        s = -(self.w[0][1] * alpha_x * alpha_x * alpha_y) / lam
        xo = (s * yo) / alpha_y - (self.w[0][2] * alpha_x * alpha_x) / lam

        self.matrix_k = np.zeros((3,3))
        self.matrix_k[0][0] = alpha_x
        self.matrix_k[0][1] = s
        self.matrix_k[0][2] = xo
        self.matrix_k[1][0] = 0
        self.matrix_k[1][1] = alpha_y
        self.matrix_k[1][2] = yo
        self.matrix_k[2][1] = 0
        self.matrix_k[2][1] = 0
        self.matrix_k[2][2] = 1

    def find_conic(self):
        temp = []
        for matrix_h in self.h_list:
            temp.append(self.extract_homography(matrix_h))

        list_v = []

        for i in temp:
            for n in i:
                list_v.append(n)

        U, D, Vt = np.linalg.svd(list_v)
        min_sidx = D.argmin()
        minEig = Vt[min_sidx]

        self.w = np.zeros((3,3))
        self.w[0][0] = minEig[0]
        self.w[0][1] = minEig[1]
        self.w[0][2] = minEig[2]
        self.w[1][0] = self.w[0][1]
        self.w[1][1] = minEig[3]
        self.w[1][2] = minEig[4]
        self.w[2][0] = self.w[0][2]
        self.w[2][1] = self.w[1][2]
        self.w[2][2] = minEig[5]
        

    def extract_vector(self, vec1, vec2):
        return np.array([vec1[0] * vec2[0],
                         vec1[0] * vec2[1] + vec1[1] * vec2[0],
                         vec1[0] * vec2[2] + vec1[2] * vec2[0],
                         vec1[1] * vec2[1],
                         vec1[1] * vec2[2] + vec1[2] * vec2[1],
                         vec1[2] * vec2[2]])

    def extract_homography(self, matrix_h):
        v11 = self.extract_vector(matrix_h[:, 0], matrix_h[:, 0])
        v12 = self.extract_vector(matrix_h[:, 0], matrix_h[:, 1])
        v22 = self.extract_vector(matrix_h[:, 1], matrix_h[:, 1])
        return np.array([v12, v11 - v22])
            
