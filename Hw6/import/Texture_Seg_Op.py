import cv2
import numpy as np
import Outsu_Op

class Text_Seg(object):
    
    def __init__(self, image, size1, size2, size3, number):
        self.num = number
        self.height, self.width = image.shape[:2]
        self.image = image
        self.gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	self.size3 = max(size3, size1, size2)
        self.size1 = min(size3, size1)
        self.size2 = min(size3, size2)
        self.find_variance()
        self.find_histogram()
        self.final_image()

    def final_image(self):
        for j in range(self.height - 1):
            for i in range(self.width - 1):
                if (self.image_B[j][i] != 0 or self.image_G[j][i] != 0 or self.image_R[j][i] != 0):
                    if (self.image_B[j - 1][i] == 0 and self.image_G[j - 1][i] == 0 and self.image_G[j - 1][i] == 0):
                        self.image[j][i] = (255,255,255)
                    elif (self.image_B[j + 1][i] == 0 and self.image_G[j + 1][i] == 0 and self.image_G[j + 1][i] == 0):
                        self.image[j][i] = (255,255,255)
                    elif (self.image_B[j][i - 1] == 0 and self.image_G[j][i - 1] == 0 and self.image_G[j][i - 1] == 0):
                        self.image[j][i] = (255,255,255)
                    elif (self.image_B[j][i + 1] == 0 and self.image_G[j][i + 1] == 0 and self.image_G[j][i + 1] == 0):
                        self.image[j][i] = (255,255,255)
        cv2.imwrite('output/p2/final_image_set_' + self.num + '.jpg',self.image)      

    def apply_outsu(self, histogram, image, variance_max, variance_min, color):
        outsu = Outsu_Op.Outsu_Op(histogram, 0, 255)
        threshold = outsu.perform_outsu()
        scale = (variance_max - variance_min) / 256

        for i in range(self.width):
            for j in range(self.height):
                if (image[j][i] > (threshold + 1) * scale + variance_min):
                    image[j][i] = 0
                else:
                    image[j][i] = 255
        cv2.imwrite('output/p2/image_' + color + '_' + self.num + '.jpg', image)
        return image

    def find_histogram(self):
        hist_B = cv2.calcHist([self.image_B], [0], None, [256], [self.var1_min, self.var1_max + 1])
        hist_G = cv2.calcHist([self.image_G], [0], None, [256], [self.var2_min, self.var2_max + 1])
        hist_R = cv2.calcHist([self.image_R], [0], None, [256], [self.var3_min, self.var3_max + 1])
        self.image_B = self.apply_outsu(hist_B, self.image_B, self.var1_max, self.var1_min, 'B')
        self.image_G = self.apply_outsu(hist_G, self.image_G, self.var2_max, self.var2_min, 'G')
        self.image_R = self.apply_outsu(hist_R, self.image_R, self.var3_max, self.var3_min, 'R')

    def find_variance(self):
        var1_max = 0
        var1_min = 1e10
        var2_max = 0
        var2_min = 1e10
        var3_max = 0
        var3_min = 1e10

        self.image_B = np.zeros((self.height, self.width, 1), np.uint8)
        self.image_G = np.zeros((self.height, self.width, 1), np.uint8)
        self.image_R = np.zeros((self.height, self.width, 1), np.uint8)

        range_pos_height = range(int(self.size3 / 2), self.height - int(self.size3 / 2 + 1))
        range_pos_width = range(int(self.size3 / 2), self.width - int(self.size3 / 2 + 1))
        win_range = range(-int(self.size3 / 2), int(self.size3 / 2 + 1))

        for j in range_pos_height:
            for i in range_pos_width:
                mean1 = 0
                var1 = 0
                mean2 = 0
                var2 = 0
                mean3 = 0
                var3 = 0

                for m in win_range:
                    for n in win_range:
                        mean3 += self.gray_img[j + m][i + n]
                        if m >= -int(self.size1 / 2) and m <= int(self.size1 / 2):
                            if n >= -int(self.size1 / 2) and n <= int(self.size1 / 2):
                                mean1 += self.gray_img[j + m][i + n]
                        if m >= -int(self.size2 / 2) and m <= int(self.size2 / 2):
                            if n >= -int(self.size2 / 2) and n <= int(self.size2 / 2):
                                mean2 += self.gray_img[j + m][i + n]
                mean1 = float(mean1) / float(self.size1 ** 2)
                mean2 = float(mean2) / float(self.size2 ** 2)
                mean3 = float(mean3) / float(self.size3 ** 2)

                for m in win_range:
                    for n in win_range:
                        var3 += (self.gray_img[j + m][i + n] - mean3) ** 2
                        if m >= -int(self.size1 / 2) and m <= int(self.size1 / 2):
                            if n >= -int(self.size1 / 2) and n <= int(self.size1 / 2):
                                var1 += (self.gray_img[j + m][i + n] - mean1) ** 2
                        if m >= -int(self.size2 / 2) and m <= int(self.size2 / 2):
                            if n >= -int(self.size2 / 2) and n <= int(self.size2 / 2):
                                var2 += (self.gray_img[j + m][i + n] - mean2) ** 2
                #print var1
                var1_max = max(var1_max, var1)
                var2_max = max(var2_max, var2)
                var3_max = max(var3_max, var3)
                var1_min = min(var1_min, var1)
                var2_min = min(var2_min, var2)
                var3_min = min(var3_min, var3)

                self.image_B[j][i] = int(var1 / (self.size1 ** 2))
                self.image_G[j][i] = int(var2 / (self.size2 ** 2))
                self.image_R[j][i] = int(var3 / (self.size3 ** 2))

        self.var1_max = int(var1_max / (self.size1 ** 2))
        self.var2_max = int(var2_max / (self.size2 ** 2))
        self.var3_max = int(var3_max / (self.size3 ** 2))
        self.var1_min = int(var1_min / (self.size1 ** 2))
        self.var2_min = int(var2_min / (self.size2 ** 2))
        self.var3_min = int(var3_min / (self.size3 ** 2))
       
