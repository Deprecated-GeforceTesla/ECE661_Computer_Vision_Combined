import cv2
from glob import glob
import numpy as np

class Vector_Op(object):

    def __init__(self, test_images, train_images):
        self.test_images = test_images
        self.train_images = train_images
        self.train_img_vec = []
        self.test_img_vec = []
        self.normalize_vectorize()
        self.find_mean_train()

    def normalize_vectorize(self):
        for image in self.test_images:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_vec = np.ravel(gray_image)
            self.test_img_vec.append(gray_vec/np.linalg.norm(gray_vec))

        for image in self.train_images:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_vec = np.ravel(gray_image)
            self.train_img_vec.append(gray_vec/np.linalg.norm(gray_vec))

    def find_mean_train(self):
        print len(self.train_img_vec)
        self.sum_vecs = reduce(lambda vec, sum_vec: vec + sum_vec, self.train_img_vec)
        self.sum_vecs /= len(self.train_img_vec)

    def get_train_vector(self):
        return self.train_img_vec

    def get_test_vector(self):
        return self.test_img_vec

    def get_train_mean(self):
        return self.sum_vecs
