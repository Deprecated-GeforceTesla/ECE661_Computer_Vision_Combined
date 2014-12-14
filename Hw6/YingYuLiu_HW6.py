import sys
import cv2
sys.path.append("import/")
import Texture_Seg_Op as tex
import RGB_Seg_Op as rgb

class HW_problem1(object):

    def __init__(self):
        '''Initialize the requried parameters for each image set
        '''
        self.load_image()
        self.perform_segmentation()

    def load_image(self):
        '''Load the original image and convert them to gray level
        @param choice The image set to choose from
        '''
        self.image1 = cv2.imread('input/pic1.jpg', 1)
        self.image2 = cv2.imread('input/pic2.jpg', 1)
            

    def perform_segmentation(self):
        tex.Text_Seg(self.image1, 3, 5, 7, str(1))
        rgb.RGB_Seg(self.image1, str(1))
        tex.Text_Seg(self.image2, 3, 5, 7, str(2))
        rgb.RGB_Seg(self.image2, str(2))

if __name__ == "__main__":
    temp = HW_problem1()
