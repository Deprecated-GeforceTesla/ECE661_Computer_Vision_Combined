import cv2
import numpy as np
from Epipole_Op import Epipole_Op


class Rectify_Op(object):

    def __init__(self, image1, image2, pt1, pt2, matrix_F):
        self.image1 = image1
        self.image2 = image2
        self.pt1 = pt1
        self.pt2 = pt2
        self.matrix_F = matrix_F
        self.pt_count = 12
        self.image_recitify()


    def find_rectified_image(self, image, H_inv):
        height, width = image.shape[:2]
    
        image_rectified = np.zeros((height, width, 3), np.uint8)
        P_Vector = np.zeros(3)
        Q_Vector = np.zeros(3)
        P_Vector[2] = 1

        for i in range(height):
            for j in range(width):

                P_Vector[0] = j
                P_Vector[1] = i
                Q_Vector = np.dot(H_inv, P_Vector)

                Q_Vector[0] /= Q_Vector[2]
                Q_Vector[1] /= Q_Vector[2]
                x = Q_Vector[0]
                y = Q_Vector[1]

                pixel_xy = [0, 0, 0]
                if x>=0 and y>=0 and x < width-1 and y < height-1:
                    pixel_xy1 = (x-int(x))*(y-int(y))*(image[int(y+1)][int(x+1)])
                    pixel_xy2 = (int(x+1)-x)*(y-int(y))*image[int(y+1)][int(x)]
                    pixel_xy3 = (x-int(x))*(int(y+1)-y)*image[int(y)][int(x+1)]
                    pixel_xy4 = (int(x+1)-x)*(int(y+1)-y)*image[int(y)][int(x)]
                    pixel_xy = pixel_xy1 + pixel_xy2 + pixel_xy3 + pixel_xy4
               
                image_rectified[i][j] = pixel_xy
    
    
        return image_rectified

    def image_recitify(self):
        G = np.zeros((3,3))
        R = np.zeros((3,3))
        T = np.zeros((3,3))
        T2 = np.zeros((3,3))
        height, width = self.image1.shape[:2]

        temp = Epipole_Op(self.matrix_F)
        e2 = temp.get_epipole2()
        P1 = temp.get_matrix_P1()
        P2 = temp.get_matrix_P2()
    
        angle = np.arctan(-(height/2 - e2[1])/(width/2 - e2[0]))
        f = np.cos(angle) * (-width/2 + e2[0]) - np.sin(angle) * (-height/2 + e2[1])
    
        R[0, 0] = np.cos(angle)
        R[0, 1] = -np.sin(angle)
        R[1, 0] = np.sin(angle)
        R[1, 1] = np.cos(angle)
        R[2, 2] = 1
    
        G[0, 0] = 1
        G[1, 1] = 1
        G[2, 0] = -1/f
        G[2, 2] = 1
    
        T[0, 0] = 1
        T[1, 1] = 1
        T[2, 2] = 1
        T[0, 2] = -width/2
        T[1, 2] = -height/2
    
        self.H2 = np.dot(np.dot(G, R), T)
    
        center_point = np.zeros(3)
        center_point[0] = width/2
        center_point[1] = height/2
        center_point[2] = 1
        center_point = np.dot(self.H2, center_point)
    
        T2[0, 0] = 1
        T2[1, 1] = 1
        T2[2, 2] = 1
        T2[0, 2] = width/2 - center_point[0]/center_point[2]
        T2[1, 2] = height/2 - center_point[1]/center_point[2]
    
        self.H2 = np.dot(T2, self.H2)
    
        P1_inv = np.linalg.pinv(P1)
        H0 = np.dot(self.H2, np.dot(P2, P1_inv))
    
        A = np.zeros((self.pt_count, 3))
        b = np.zeros(self.pt_count)
    
        for i in range(self.pt_count):
            x1 = self.pt1[i, :]
            x1_new = np.dot(H0, x1.T)
            x1_new[0] /= x1_new[2]
            x1_new[1] /= x1_new[2]
        
            x2 = self.pt2[i, :]
            x2_new = np.dot(self.H2, x2.T)
            x2_new[0] /= x2_new[2]
            x2_new[1] /= x2_new[2]
            A[i, 0] = x1_new[0]
            A[i, 1] = x1_new[1]
            A[i, 2] = 1
            b[i] = x2_new[0]
        
        h = np.linalg.lstsq(A, b)

        HA = np.zeros((3,3))
        HA[0, 0] = h[0][0]
        HA[0, 1] = h[0][1]
        HA[0, 2] = h[0][2]
        HA[1, 1] = 1
        HA[2, 2] = 1
        self.H1 = np.dot(HA, H0)

    
        center_point1 = np.zeros(3)
        center_point1[0] = width/2
        center_point1[1] = height/2
        center_point1[2] = 1
        center_point_new = np.dot(self.H1, center_point1)

    
        T2[0, 0] = 1
        T2[1, 1] = 1
        T2[2, 2] = 1
        T2[0, 2] = width/2 - center_point_new[0]/center_point_new[2]
        T2[1, 2] = height/2 - center_point_new[1]/center_point_new[2]
        self.H1 = np.dot(T2, self.H1)
    
        H1_inv = np.linalg.inv(self.H1)
        H2_inv = np.linalg.inv(self.H2)

        self.matrix_f = np.dot(np.dot(H2_inv.T, self.matrix_F), H1_inv)

        self.image1_rectified = self.find_rectified_image(self.image1, H1_inv)
        self.image2_rectified = self.find_rectified_image(self.image2, H2_inv)

    def get_rect_image1(self):
        return self.image1_rectified

    def get_rect_image2(self):
        return self.image2_rectified

    def get_matrix_H1(self):
        return self.H1

    def get_matrix_H2(self):
        return self.H2

    def get_matrix_F(self):
        return self.matrix_f

