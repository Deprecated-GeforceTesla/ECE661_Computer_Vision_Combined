import numpy as np
import cv2
from cPickle import dump

class Feature_Op(object):

    def __init__(self, test_img, count):
        self.test_imgs = test_img
        self.count = count

    def extract_feature(self):
        integral_images = map(self.integral_imgs, self.test_imgs)
        features = np.zeros((feature_num, self.count))
        for i in range(self.count):
            features[:, i] = get_haar_features(integral_images[i])
 
        dump(features, open("feature.p", 'w'), protocol=2)

    def integral_imgs(self, image):
        height, width = image.shape[0:2]
        image_integral = np.zeros((height+1, width+1))
        image_integral[1:, 1:] = np.cumsum(np.cumsum(image, axis=0, dtype=float), axis=1, dtype=float)
        return image_integral

