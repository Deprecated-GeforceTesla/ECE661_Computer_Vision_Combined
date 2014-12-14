import sys
import cv2
import numpy as np
import random
sys.path.append("import/")
import Harris_Op
import Descriptor
import SSD
import NCC

class HW_problem1(object):

    def __init__(self):
        '''Initialize the requried parameters for each image set
        '''
        img_choice = int(raw_input("Which set of image to choose? : "))
        method = int(raw_input("Which method to choose? : SSD: 1, NCC: 2: "))
        scale = int(raw_input("Enter the scale: "))
        if img_choice == 1:
            self.threshold = 3e14  # threshold
            self.ssd_window = 55  # ssd window size
            self.ncc_window = 53  # nvv window size
            self.ssd_threshold = 1400  # ssd threshold
            self.ssd_ratio_threshold = 0.8  # ssd threshold ratio
            self.ncc_threshold = 1200  # ncc threshold
            self.ncc_ratio_threshold = 0.8  # ncc threshold ratio
            self.descriptor_count = 200  # max amount of descriptor allowed
        elif img_choice == 2:
            self.threshold = 1e11
            self.ssd_window = 35
            self.ncc_window = 15
            self.ssd_threshold = 1500
            self.ssd_ratio_threshold = 0.9
            self.ncc_threshold = 1000
            self.ncc_ratio_threshold = 0.9
            self.descriptor_count = 200
        elif img_choice == 3:
            self.threshold = 3e14
            self.ssd_window = 55
            self.ncc_window = 53
            self.ssd_threshold = 1400
            self.ssd_ratio_threshold = 0.8
            self.ncc_threshold = 1200
            self.ncc_ratio_threshold = 0.8
            self.descriptor_count = 200
        self.load_image(img_choice)
        self.apply_harris(scale)
        if method == 1:
            self.apply_SSD()
        elif method == 2:
            self.apply_NCC()
        self.create_output_image(img_choice)
        self.circle_output_points()
        self.output_image(img_choice, method, scale)

    def load_image(self, choice):
        '''Load the original image and convert them to gray level
        @param choice The image set to choose from
        '''
        if (choice == 1):
            self.image1 = cv2.cvtColor(cv2.imread('input/Set1/pic1.jpg'),
                                       cv2.COLOR_BGR2GRAY)
            self.image2 = cv2.cvtColor(cv2.imread('input/Set1/pic2.jpg'),
                                       cv2.COLOR_BGR2GRAY)
        elif (choice == 2):
            self.image1 = cv2.cvtColor(cv2.imread('input/Set2/pic6.jpg'),
                                       cv2.COLOR_BGR2GRAY)
            self.image2 = cv2.cvtColor(cv2.imread('input/Set2/pic7.jpg'),
                                       cv2.COLOR_BGR2GRAY)
        elif (choice == 3):
            self.image1 = cv2.cvtColor(cv2.imread('input/custom/pic1.jpg'),
                                       cv2.COLOR_BGR2GRAY)
            self.image2 = cv2.cvtColor(cv2.imread('input/custom/pic2.jpg'),
                                       cv2.COLOR_BGR2GRAY)

    def apply_harris(self, scale):
        ''' Apply Harris corner detection on the image set
        @param scale The scale of the Gaussian Blurr
        '''
        harris1 = Harris_Op.Harris(self.image1, scale)
        harris2 = Harris_Op.Harris(self.image2, scale)
        self.harris_img1 = harris1.get_harris_image()
        self.harris_img2 = harris2.get_harris_image()

    def apply_SSD(self):
        '''Apply the SSD on the image set. Expected to find descriptors/pts
        '''
        descriptor1 = Descriptor.Descriptor(self.harris_img1,
                                            self.image1,
                                            self.descriptor_count,
                                            self.ssd_window,
                                            self.threshold)
        descriptor2 = Descriptor.Descriptor(self.harris_img2,
                                            self.image2,
                                            self.descriptor_count,
                                            self.ssd_window,
                                            self.threshold)
        self.descriptor1 = descriptor1.get_descriptor_list()
        print len(self.descriptor1)
        self.descriptor2 = descriptor2.get_descriptor_list()
        print len(self.descriptor2)
        SSDet = SSD.SSD(self.descriptor1, self.descriptor2, self.ssd_window,
                        self.ssd_threshold, self.ssd_ratio_threshold)

    def apply_NCC(self):
        '''Apply the NCC on the image set. Expected to find descriptors/pts
        '''
        descriptor1 = Descriptor.Descriptor(self.harris_img1,
                                            self.image1,
                                            self.descriptor_count,
                                            self.ncc_window,
                                            self.threshold)
        descriptor2 = Descriptor.Descriptor(self.harris_img2,
                                            self.image2,
                                            self.descriptor_count,
                                            self.ncc_window,
                                            self.threshold)
        self.descriptor1 = descriptor1.get_descriptor_list()
        print len(self.descriptor1)
        self.descriptor2 = descriptor2.get_descriptor_list()
        print len(self.descriptor2)
        SSDet = SSD.SSD(self.descriptor1, self.descriptor2, self.ncc_window,
                        self.ncc_threshold, self.ncc_ratio_threshold)

    def create_output_image(self, choice):
        '''Create a base for the output image
        @param choice The choice of correspnding image set
        '''
        if (choice == 1):
            self.image1 = cv2.imread('input/Set1/pic1.jpg')
            self.image2 = cv2.imread('input/Set1/pic2.jpg')
        elif (choice == 2):
            self.image1 = cv2.imread('input/Set2/pic6.jpg')
            self.image2 = cv2.imread('input/Set2/pic7.jpg')
        elif (choice == 3):
            self.image1 = cv2.imread('input/custom/pic1.jpg')
            self.image2 = cv2.imread('input/custom/pic2.jpg')

        height1, width1 = self.image1.shape[:2]
        height2, width2 = self.image1.shape[:2]

        output_height = max(height1, height2)
        output_width = width1 + width2
        self.output_img = np.zeros((output_height,output_width,3), np.uint8)
        for i in range(output_width):
            for j in range(output_height):
                if i < width1:
                    self.output_img[j][i] = self.image1[j][i]
                else:
                    self.output_img[j][i] = self.image2[j][i - width1]

    def circle_output_points(self):
        '''Circle and draw line for the chosen outputs. Draw connection
           between related points
        '''
        height1, width1 = self.image1.shape[:2]
        count = 0
        for i in self.descriptor1:
            if(i['match'] > -1):
                count = count + 1
                col1 = random.randint(0, 255)
                col2 = random.randint(0, 255)
                col3 = random.randint(0, 255)
                cv2.circle(self.output_img,(i['x'],i['y']),1,(col1,col2,col3),4)
                cv2.circle(self.output_img,
                           (self.descriptor2[i['match']]['x'] + width1,
                            self.descriptor2[i['match']]['y']),1,(col1,col2,col3),4)
                cv2.line(self.output_img, (i['x'], i['y']),
                        (self.descriptor2[i['match']]['x']+width1,
                         self.descriptor2[i['match']]['y']), (col1,col2,col3), 1)
        print count


    def output_image(self, choice, method, scale):
        '''Output the final image
        @param choice The choice of image set
        @param method The chosen compute method (SSD/NCC)
        @param scale The scale of Gaussian Blur
        '''
        if method == 1:
            folder = 'SSD'
        elif method == 2:
            folder = 'NCC'
        path = ('output/harris/' + folder + '/Set' + str(choice) + '/Scale_' +
                str(scale) + '.jpg')
        print path
        cv2.imwrite(path, self.output_img)

if __name__ == "__main__":
    temp = HW_problem1()
