import cv2
import numpy as np

class Harris(object):

    def __init__(self, image, scale):
        self.height, self.width = image.shape[:2]
        self.window_size = 5
        self.initialize_dx_dy(image, scale)

    def apply_gaussian(self, image, scale):
        gaussian_image = cv2.GaussianBlur(image, (scale,scale), 0)
        return gaussian_image

    def initialize_dx_dy(self, image, scale):
        gaussian_image = self.apply_gaussian(image, scale)
        self.image_dx = cv2.Sobel(gaussian_image, cv2.CV_64F, 1, 0, ksize=5)
        self.image_dy = cv2.Sobel(gaussian_image, cv2.CV_64F, 0, 1, ksize=5)

    def get_harris_image(self):
        output = np.zeros((self.height,self.width))
        lower_bound = int(self.window_size / 2)
        upper_bound = int(self.window_size / 2 + 1)

        for i in range(lower_bound, self.width - upper_bound):
            for j in range(lower_bound, self.height - upper_bound):
                matrix_c = np.zeros(shape=(2,2))
                for m in range(-lower_bound, upper_bound):
                    for n in range(-lower_bound, upper_bound):
                        matrix_c[0][0] += (self.image_dx[j+n][i+m] *
                                           self.image_dx[j+n][i+m] /
                                           self.window_size)
                        matrix_c[0][1] += (self.image_dx[j+n][i+m] *
                                           self.image_dy[j+n][i+m] /
                                           self.window_size)
                        matrix_c[1][1] += (self.image_dy[j+n][i+m] *
                                           self.image_dy[j+n][i+m] /
                                           self.window_size)

                matrix_c[1][0] = matrix_c[0][1]
                ds, v, vt = cv2.SVDecomp(matrix_c) 
                output[j][i] = (ds[0] * ds[1] - 0.04 *
                                (ds[0] + ds[1]) * (ds[0] + ds[1]))

        check = 0  
        for i in range(lower_bound, self.width - upper_bound):
            for j in range(lower_bound, self.height - upper_bound):
                for m in range(-lower_bound, upper_bound):
                    if(check == 1):
                        check = 0
                        break
                    for n in range(-lower_bound, upper_bound):
                        if(output[j][i] < output[j+n][i+m]):
                            output[j][i] = 0
                            check = 1
                            break
        return output
