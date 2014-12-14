from Descriptor import Descriptor
import cv2
import numpy as np


class Descriptor_Op(object):

    def __init__(self, image_gray, matrix_H):
        self.gray_img = image_gray
        self.descriptors = []
        self.matrix_H = matrix_H
        self.ncc_size = 13
        self.get_descriptor()

    def get_descriptor(self):
        height, width = self.gray_img.shape[:2]
        edges = cv2.Canny(self.gray_img, 80, 255)
    
        count = 0
        x = np.zeros(3)
        for i in range(int(self.ncc_size/2), width - int(self.ncc_size/2 + 1)):
            for j in range(int(self.ncc_size/2), height - int(self.ncc_size/2 + 1)):
                if edges[j,i] != 0:
                    x[0] = i
                    x[1] = j
                    x[2] = 1
                    x_rect = np.dot(self.matrix_H, x)
                    x_rect /= x_rect[2]
                
                    self.descriptors.append(Descriptor(i,j,x_rect[0], x_rect[1]))
                    count += 1
        print "image has {} interest points".format(count)

    def get_result(self):
        return self.descriptors
