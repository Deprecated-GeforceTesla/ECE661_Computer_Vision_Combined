import cv2
import numpy as np
import Outsu_Op

class RGB_Seg(object):
    
    def __init__(self, image, number):
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

        cv2.imwrite('output/p1/image_' + color + '_' + self.num + '.jpg', image)
        return image

    def segmentation(self):
        self.image_B = self.apply_outsu(self.image_B, self.hist_B, 'B')
        self.image_G = self.apply_outsu(self.image_G, self.hist_G, 'G')
        self.image_R = self.apply_outsu(self.image_R, self.hist_R, 'R')

        self.image_comb = np.zeros((self.height,self.width,3), np.uint8)
        for j in range(self.height):
            for i in range(self.width):
                if (self.image_B[j][i] == 0 and self.image_G[j][i] == 0 and self.image_R[j][i] == 0):
                    self.image_comb[j][i] = self.image[j][i]

        cv2.imwrite('output/p1/combined_' + self.num + '.jpg', self.image_comb)

    def contour_extraction(self):
        label_count = 0
        label_map = np.zeros((self.height,self.width))
        
        self.final_img = np.zeros((self.height,self.width,3), np.uint8)

        for j in range(self.height):
            for i in range(self.width):
                if (self.image_comb[j][i][0] != 0 or self.image_comb[j][i][1] != 0 or self.image_comb[j][i][2] != 0):
                    self.final_img[j][i] = self.image[j][i]
                else:
                    self.final_img[j][i] = (0,0,0)

        for j in range(1, self.height - 1):
            for i in range(1, self.width - 1):
                if (self.final_img[j][i].all() == 0):
                    if (label_map[j + 1][i] != 0):
                        label_map[j][i] = label_map[j + 1][i]
                    elif (label_map[j - 1][i] != 0):
                        label_map[j][i] = label_map[j - 1][i]
                    elif (label_map[j][i + 1] != 0):
                        label_map[j][i] = label_map[j][i + 1]
                    elif (label_map[j][i - 1] != 0):
                        label_map[j][i] = label_map[j][i - 1]
                    else:
                        label_count += 1
                        label_map[j][i] = label_count

        label_list = np.zeros(label_count + 1)
        for j in range(self.height):
            for i in range(self.width):
                if (label_map[j][i].any() != 0):
                    temp = label_map[j][i]
                    label_list[temp] += 1

        for j in range(self.height):
            for i in range(self.width):
                if (self.final_img[j][i].all() == 0):
                    temp = label_map[j][i]
                    if (label_list[temp] > 80):
                        self.final_img[j][i] = (0,0,0)
                    else:
                        self.final_img[j][i] = self.image[j][i]

        cv2.imwrite('output/p1/final_image_' + self.num + '.jpg', self.final_img)
