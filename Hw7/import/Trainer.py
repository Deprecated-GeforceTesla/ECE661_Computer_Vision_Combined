import cv2
import numpy as np

class Trainer(object):

    def __init__(self, image):
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.height, self.width = self.image.shape[:2]

    def convert_image_to_binary(self):

        for j in range(self.height):
            for i in range(self.width):
                if(self.image[j][i] > 150):
                    self.image[j][i] = 255
                else:
                    self.image[j][i] = 0
    
        return self.image


