import cv
import numpy as np


class Homography(object):

    def __init__(self, corner, sep):
        self.corner = corner
        self.sep = sep
        self.correspond_corners()
        self.find_homography()

    def get_homography(self):
        return self.matrix_H

    def get_correspondence(self):
        return self.correspondance

    def correspond_corners(self):
        corner_list = []
        correspondance = []
        self.corres = []
        count = 0

        for i in self.corner:
            for n in i:
                corner_list.append(n)
                correspondance.append(())

        for i in range(len(self.corner)):
            for n in range(len(self.corner[0])):
                x = float(n) * self.sep
                y = float(i) * self.sep
                correspondance[count] = [(x,y), self.corner[i][n]]
                count += 1
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0

        for i in correspondance:
            x1 += i[0][0]
            y1 += i[0][1]
            x2 += i[1][0]
            y2 += i[1][1]

        mean_x1 = float(x1) / float(len(correspondance))
        mean_y1 = float(y1) / float(len(correspondance))
        mean_x2 = float(x2) / float(len(correspondance))
        mean_y2 = float(y2) / float(len(correspondance))

        for i in correspondance:
            x_1 = i[0][0]
            y_1 = i[0][1]
            x_2 = i[1][0]
            y_2 = i[1][1]
            self.corres.append([(x_1-mean_x1,y_1-mean_y1),
                                (x_2-mean_x2,y_2-mean_y2)])
        self.h1 = np.array([[1, 0, -mean_x1], [0, 1, -mean_y1], [0, 0, 1]],
                           dtype=float)
        self.h2 = np.array([[1, 0, -mean_x2], [0, 1, -mean_y2], [0, 0, 1]],
                           dtype=float)
        self.correspondance = correspondance
            
    def find_homography(self):
        temp = []
        for i in self.corres:
            x1 = i[0][0]
            y1 = i[0][1]
            x2 = i[1][0]
            y2 = i[1][1]
            temp.append([0, 0, 0, -x1, -y1, -1, y2*x1, y2*y1, y2,
                         x1, y1, 1, 0, 0, 0, -x2*x1, -x2*y1, -x2])

        temp = np.array(temp)
        matrix_A = temp.reshape(len(self.corres) * 2, 9)

        U, D, V = np.linalg.svd(matrix_A)
        min_sidx = D.argmin()
        min_eig = V[min_sidx]
        matrix_H = min_eig.reshape(3,3)
        temp = np.dot(matrix_H, self.h1)
        self.matrix_H = np.dot(np.linalg.inv(self.h2), temp)
        

        
