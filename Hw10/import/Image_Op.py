import numpy as np
import cv2

class Image_Op(object):

    def __init__(self, gray_img):
        self.height, self.width = gray_img.shape[0:2]
        self.gray_vec = np.ravel(gray_img)
        self.gray_norm = np.linalg.norm(self.gray_vec)
        if self.gray_norm != 0:
            self.gray_vec /= self.gray_norm
        self.gray_vec = 255.0

    def get_normalization(self):
        return np.reshape(self.gray_vec, (self.height,self.width))
