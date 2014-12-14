import cv2
import numpy as np
from Epipole_Op import Epipole_Op

class Ncc_Op(object):

    def __init__(self, des1, des2, img1, img2, matrix_F):
        self.descriptor1 = des1
        self.descriptor2 = des2
        self.img1 = img1
        self.img2 = img2
        self.matrix_F = matrix_F
        self.ncc_size = 13
        self.threshold = 0.8
        self.ncc_calculation()

    def get_neighbor(self, x, y, gray_image):
        size = self.ncc_size
        size_half = int(size/2)

        neighbor = np.zeros((size,size))

        for m in range(-size_half, (size_half+1)):
            for n in range(-size_half, (size_half+1)):
                neighbor[n+size_half][m+size_half] = gray_image[y+n][x+m]
        return neighbor

    def get_ncc_point(self, neighbor1, neighbor2):
        point = 0
        mean1 = 0
        mean2 = 0
        ncc_numerator = 0
        ncc_denominator1 = 0
        ncc_denominator2 = 0

        Wncc = self.ncc_size
        for i in range(Wncc):
            for j in range(Wncc):
                mean1 += neighbor1[i][j]
                mean2 += neighbor2[i][j]
        mean1 = mean1/(Wncc*Wncc)
        mean2 = mean2/(Wncc*Wncc)
    
        for i in range(Wncc):
            for j in range(Wncc):
                ncc_numerator += (neighbor1[i][j]-mean1)*(neighbor2[i][j]-mean2)
                ncc_denominator1 += np.square(neighbor1[i][j]-mean1)
                ncc_denominator2 += np.square(neighbor2[i][j]-mean2)
        ncc_denominator = np.sqrt(ncc_denominator1*ncc_denominator2)
        point = ncc_numerator/ncc_denominator

        return point

    def ncc_calculation(self):
        for i in self.descriptor1:
            i.neighbor = self.get_neighbor(i.x, i.y, self.img1)
        for i in self.descriptor2:
            i.neighbor = self.get_neighbor(i.x, i.y, self.img2)


        for i in range(len(self.descriptor1)):
            point = 0
            point_max = -1e10
            matched_point = 0
            x1 = np.zeros(3)
            x2 = np.zeros(3)
            row = int(self.descriptor1[i].y_rect)
        
            for j in range(len(self.descriptor2)):
                if(int(self.descriptor2[j].y_rect) < row -4 or int(self.descriptor2[j].y_rect) > row + 4):
                    continue
            
                x2[0] = self.descriptor2[j].x
                x2[1] = self.descriptor2[j].y
                x2[2] = 1
                constraint1 = np.dot(np.dot(x2.T, self.matrix_F), x1)
                if constraint1 > 0.055:
                    continue

                point = self.get_ncc_point(self.descriptor1[i].neighbor, self.descriptor2[j].neighbor)

                if(point > point_max):
                    point_max = point
                    self.descriptor1[i].point = point_max
                    self.descriptor1[i].match = j
                    self.descriptor2[j].point = point_max
                    self.descriptor2[j].match = i

            for j in range(i):
                if(self.descriptor1[j].match == self.descriptor1[i].match):
                    if(self.descriptor1[j].point < self.descriptor1[i].point):
                        self.descriptor1[j].match = -1
                        self.descriptor1[j].score = -1
                    else:
                        self.descriptor1[i].match = -1
                        self.descriptor1[i].score = -1
                    break

    def get_descriptor1(self):
        return self.descriptor1

    def get_descriptor2(self):
        return self.descriptor2

