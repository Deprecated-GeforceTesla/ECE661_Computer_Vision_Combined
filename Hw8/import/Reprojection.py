import cv
import numpy as np

class Reprojection(object):

    def __init__(self, image, records, matrix_k, matrix_r, k1, k2):
        self.image = image
        self.k1 = k1
        self.k2 = k2
        self.records = records
        self.matrix_k = matrix_k
        self.matrix_r = matrix_r
        self.find_world_img_points()
        self.find_projection_vector()
        self.circle_corners()

    def get_differences(self):
        diff = 0

        for i in range(len(self.project_vec)):
            p1 = abs(self.project_vec[i][0] - self.image_pt[i][0])
            p2 = abs(self.project_vec[i][1] - self.image_pt[i][1])
            p = max(p1, p2)
            if p > diff:
                diff = p
        return diff
        
        #return self.project_vec - self.image_pt

    def get_image(self):
        return self.image

    def radial_dist(self, vec, K, k1, k2):
        vec = [vec[0], vec[1], 1.0]
        K_inv = np.array([[1 / K[0][0], 0, -K[0][2]/K[0][0]],
                         [0, 1/K[1][1], -K[1][2]/K[1][1]],
                         [0, 0, 1]])
        xyz = np.dot(K_inv, vec)
        rSqr = xyz[0] * xyz[0] + xyz[1] * xyz[1]
        rSqrSqr = rSqr * rSqr

        xyz_dist = xyz * (1 + k1 * rSqr + k2 / rSqrSqr)
        xyz_dist[2] = 1.0

        result = np.dot(K, xyz_dist)

        return [result[0], result[1]]

    def find_world_img_points(self):
        self.world_pt = []
        for i in self.records:
            self.world_pt.append(i[0])

        self.world_vec = np.array([[i[0], i[1], 0, 1] for i in self.world_pt])

        self.image_pt = []
        for i in self.records:
            self.image_pt.append(i[1])

        self.img_vec = np.array([[i[0], i[1], 1] for i in self.image_pt])
        self.img_vec = self.img_vec[: ,0 : 2]

    def find_projection_vector(self):
        temp = np.dot(self.matrix_k, self.matrix_r)
        project_vec = np.dot(temp, np.transpose(self.world_vec))
        project_vec = np.transpose(project_vec)
        self.project_vec = []
        #print project_vec
        for i in project_vec:
            temp = []
            temp.append(i[0] / i[2])
            temp.append(i[1] / i[2])
            temp.append(1)
            #print i
            self.project_vec.append(temp)
        self.project_vec = np.array(self.project_vec)
        self.project_vec = self.project_vec[:,0:2]
        
        temp = []
        for i in self.project_vec:
            temp.append(self.radial_dist(i, self.matrix_k, self.k1, self.k2))

        self.project_vec = temp

    def circle_corners(self):
        for i in self.project_vec:
            ptx = int(i[0])
            pty = int(i[1])
            cv.Circle(self.image, (ptx,pty), 20, (0,0,255), -1)


    
