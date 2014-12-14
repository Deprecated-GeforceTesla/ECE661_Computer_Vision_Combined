import numpy as np
import random

class Ransac_Op(object):

    def __init__(self, key_pts1, key_pts2, correspondance, threshold, inlier_probability):
        self.pt1_org = key_pts1
        self.pt2_org = key_pts2
        self.threshold = threshold
        self.correspondance = correspondance
        self.inlier_probability = inlier_probability
        self.apply_ransac()

    def apply_ransac(self):
        self.pt1 = []
        self.pt2 = []
        for i in range(len(self.pt1_org)):
            if self.correspondance[i] != -1:
                x1, y1 = self.pt1_org[i].pt
                x2, y2 = self.pt2_org[int(self.correspondance[i])].pt
                point1 = {}
                point1['x'] = x1
                point1['y'] = y1
                point2 = {}
                point2['x'] = x2
                point2['y'] = y2
                self.pt1.append(point1)
                self.pt2.append(point2)
        self.count = len(self.pt1)
        print 'count is' + str(self.count)
        self.find_best_homography()
        while (self.inlier_prob < self.inlier_probability):
            self.find_best_homography()
            #print 'in while loop with inlier_prob as ' + str(self.inlier_prob)


    def find_best_homography(self):
        self.max_inliers = 0
        min_variance = 1e10
        N = 1e3
        trial = 0
        matrix_H = np.zeros(shape=(3,3))

        inliers1 = [] # count
        inliers2 = []
        self.inlier_prob = 0
        while trial < N:
            matrix_H = self.find_homography()
            inlier_count = 0
            total_error = 0
            error_square = 0
            inlier1 = []
            inlier2 = []
            for i in range(self.count):
                base_pt = np.zeros(3)
                base_pt[0] = self.pt1[i]['x']
                base_pt[1] = self.pt1[i]['y']
                base_pt[2] = 1
                #print self.pt1[i], self.pt2[i]
                com_pt = np.dot(matrix_H, base_pt)
                dx = (com_pt[0] / com_pt[2]) - self.pt2[i]['x']
                dy = (com_pt[1] / com_pt[2]) - self.pt2[i]['y']
                error = ((dx * dx) + (dy * dy)) ** 0.5
                #print (com_pt[0] / com_pt[2]), (com_pt[1] / com_pt[2])
                #print 'error is ' + str(error)

                if error < self.threshold:
                    point1 = {}
                    point1['x'] = self.pt1[i]['x']
                    point1['y'] = self.pt1[i]['y']
                    point2 = {}
                    point2['x'] = self.pt2[i]['x']
                    point2['y'] = self.pt2[i]['y']
                    inlier1.append(point1)
                    inlier2.append(point2)
                    inlier_count += 1
                    total_error += error
                    error_square += error ** 2

            trial += 1
            if inlier_count > self.max_inliers:
                mean = float(total_error) / float(inlier_count)
                variance = (float(error_square) / float(inlier_count)) - (mean ** 2)
                print self.inlier_prob
                if variance < min_variance:
                    self.max_inliers = inlier_count
                    min_variance = variance
                    self.best_homography_matrix = matrix_H
                    self.best_inlier1 = inlier1  # copy the inlier list as the best inlier
                    self.best_inlier2 = inlier2
                    self.inlier_prob = float(inlier_count) / float(self.count)
                    print self.inlier_prob


    def find_homography(self):
        matrix_A = np.zeros(shape=(16,8))
        matrix_B = np.zeros(16)
        vector_H = np.zeros(8)
        matrix_H = np.zeros(shape=(3,3))
        for i in range(8):
            index = random.randint(0, self.count - 1)
            #print self.pt1[index], self.pt2[index]
            matrix_A[2 * i + 1][0] = self.pt1[index]['x']
            matrix_A[2 * i + 1][1] = self.pt1[index]['y']
            matrix_A[2 * i + 1][2] = 1
            matrix_A[2 * i + 1][6] = -self.pt1[index]['x'] * self.pt2[index]['x']
            matrix_A[2 * i + 1][7] = -self.pt1[index]['y'] * self.pt2[index]['x']

            matrix_A[2 * i][3] = self.pt1[index]['x']
            matrix_A[2 * i][4] = self.pt1[index]['y']
            matrix_A[2 * i][5] = 1
            matrix_A[2 * i][6] = -self.pt1[index]['x'] * self.pt2[index]['y']
            matrix_A[2 * i][7] = -self.pt1[index]['y'] * self.pt2[index]['y']

            matrix_B[2 * i + 1] = self.pt2[index]['x']
            matrix_B[2 * i] = self.pt2[index]['y']

        matrix_At = matrix_A.T
        matrix_AtA = np.dot(matrix_At, matrix_A)
        matrix_AtB = np.dot(matrix_At, matrix_B)
        vector_H = np.dot(np.linalg.inv(matrix_AtA), matrix_AtB)

        for i in range(3):
            for j in range(3):
                if (i == 2 and j == 2):
                    matrix_H[i][j] = 1
                else:
                    matrix_H[i][j] = vector_H[i * 3 + j]
        return matrix_H

    def get_inlier1(self):
        return self.best_inlier1

    def get_inlier2(self):
        return self.best_inlier2

    def get_best_homography(self):
        return self.best_homography_matrix
