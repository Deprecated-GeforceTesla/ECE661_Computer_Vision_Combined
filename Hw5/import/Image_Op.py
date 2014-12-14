import cv2
import numpy as np

class Image_Op(object):

    def __init__(self, images, correspondances, homographys, max_image):
        self.images = images
        self.correspondances = correspondances
        self.homographys = homographys
        self.max_image = max_image
        self.combine_all_image(images, homographys)

    def get_combined_image(self):
        return self.combine_image

    def combine_all_image(self, images, homographys):
        for i in range(len(homographys)):
            print len(homographys) - i
            homography = homographys[len(homographys) - 1 - i]
            if i == 0:
                combine_image = self.combine_image(images[-2], images[-1], homography)
            else:
                combine_image = self.combine_image(images[len(homographys) - i - 1], combine_image, homography)
        self.combine_image = combine_image

    def combine_image(self, image1, image2, homography):
        height1, width1= image1.shape[:2]
        height2, width2 = image2.shape[:2]

        vector = np.zeros(3)
        vector[0] = width2
        vector[1] = height2
        vector[2] = 1

        matrix_h = np.linalg.inv(homography)
        location = np.dot(matrix_h, vector)
        width = max(int(location[0] / location[2]), width1)
        height = max(int(location[1] / location[2]), height1)
        #print width, height
        combined_image = np.zeros((height,width,3), np.uint8)
        #print combined_image.shape[:2]

        for n in range(height):
            for i in range(width):
                #print i, n
                vector[0] = i
                vector[1] = n
                vector[2] = 1
                location = np.dot(homography, vector)
                x = int(location[0] / location[2])
                y = int(location[1] / location[2])
                 
                if self.location_in_range(i, n, width1, height1):
                    combined_image[n][i] = image1[n][i]
                elif self.location_in_range(x, y, width2, height2):
                    combined_image[n][i] = self.bilinear_interpolation(image2, x, y)
        return combined_image


    def location_in_range(self, x, y, width, height):
        #print x, y, width, height
        if int(x) < (width - 1) and int(x) > 0:
            if int(y) < (height - 1) and int(y) > 0:
                #print 'true'
                return True
        #print 'false'
        return False

    def bilinear_interpolation(self, image, x, y):
        point1 = (x - int(x)) * (y - int(y)) * (image[int(y + 1)][int(x + 1)])
        point2 = (int(x + 1) - x) * (y - int(y)) * image[int(y + 1)][int(x)]
        point3 = (x - int(x)) * (int(y + 1) - y) * image[int(y)][int(x + 1)]
        point4 = (int(x + 1) - x) * (int(y + 1) - y) * image[int(y)][int(x)]
        return point1 + point2 + point3 + point4
