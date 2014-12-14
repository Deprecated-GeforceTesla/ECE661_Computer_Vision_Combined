import cv2
import numpy as np
import Outsu_Op

class RGB_Seg(object):
    
    def __init__(self, image, number=0):
        self.num = number
        self.image = image
        self.height, self.width = image.shape[:2]
        self.image_B, self.image_G, self.image_R = cv2.split(image)
        self.find_histogram()
        self.segmentation()
        self.contour_extraction()

    def find_histogram(self):
        self.hist_B = cv2.calcHist([self.image_B], [0], None, [256], [0,256])
        self.hist_G = cv2.calcHist([self.image_G], [0], None, [256], [0,256])
        self.hist_R = cv2.calcHist([self.image_R], [0], None, [256], [0,256])

    def apply_outsu(self, image, hist, color):
        outsu = Outsu_Op.Outsu_Op(hist, 0, 255)
        threshold = outsu.perform_outsu()
        outsu = Outsu_Op.Outsu_Op(hist, 0, threshold)
        threshold = outsu.perform_outsu()

        for i in range(self.height):
            for j in range(self.width):
                if image[i][j] > threshold:
                    image[i][j] = 0
                else:
                    image[i][j] = 255

        #cv2.imwrite('output/p1/image_' + color + '_' + self.num + '.jpg', image)
        return image

    def segmentation(self):
        self.image_B = self.apply_outsu(self.image_B, self.hist_B, 'B')
        self.image_G = self.apply_outsu(self.image_G, self.hist_G, 'G')
        self.image_R = self.apply_outsu(self.image_R, self.hist_R, 'R')

        self.image_comb = np.zeros((self.height,self.width,3), np.uint8)
        for j in range(self.height):
            for i in range(self.width):
                    self.image_comb[j][i] = [self.image_B[j][i], self.image_G[j][i], self.image_R[j][i]]

        #cv2.imwrite('output/p1/combined_' + self.num + '.jpg', self.image_comb)

    def contour_extraction(self):
        label_count = 0
        label_map = np.zeros((self.height,self.width))
        
        self.final_img = np.zeros((self.height,self.width))

        for j in range(self.height):
            for i in range(self.width):
                if (self.image_comb[j][i][0] != 0 or self.image_comb[j][i][1] != 0 or self.image_comb[j][i][2] != 0):
                    self.final_img[j][i] = 255

    def get_image(self):
        height, width = self.final_img.shape[:2]
        for j in range(height):
            for i in range(width):
                if(self.final_img[j][i] == 255):
                    self.final_img[j][i] = 0
                else:
                    self.final_img[j][i] = 255
        return self.final_img
