import sys, os
import random
import numpy as np
import cv2

class HW_problem2(object):

    def __init__(self):
        '''Initialize the requried parameters for each image set
        '''
        img_choice = int(raw_input("Which set of image to choose? : "))
        if img_choice == 1:
            self.threshold = 0.1
            self.threshold_r = 0.8
            self.hessian1 = 1000
            self.hessian2 = 2000
        elif img_choice == 2:
            self.threshold = 0.2
            self.threshold_r = 0.8
            self.hessian1 = 1000
            self.hessian2 = 2000
        elif img_choice == 3:
            self.threshold = 0.2
            self.threshold_r = 0.8
            self.hessian1 = 500
            self.hessian2 = 1000
        self.load_image(img_choice)
        self.apply_surf()
        self.correspond_points()
        self.create_output_image(img_choice)
        self.circle_output_points()
        self.output_image(img_choice)

    def load_image(self, choice):
        '''Load the original image and convert them to gray level
        @param choice The image set to choose from
        '''
        if (choice == 1):
            self.image1 = cv2.cvtColor(cv2.imread('input/Set1/pic1.jpg'),
                                       cv2.COLOR_BGR2GRAY)
            self.image2 = cv2.cvtColor(cv2.imread('input/Set1/pic2.jpg'),
                                       cv2.COLOR_BGR2GRAY)
        elif (choice >= 2):
            self.image1 = cv2.cvtColor(cv2.imread('input/Set2/pic6.jpg'),
                                       cv2.COLOR_BGR2GRAY)
            self.image2 = cv2.cvtColor(cv2.imread('input/Set2/pic7.jpg'),
                                       cv2.COLOR_BGR2GRAY)
        elif (choice >= 2):
            self.image1 = cv2.cvtColor(cv2.imread('input/custom/pic1.jpg'),
                                       cv2.COLOR_BGR2GRAY)
            self.image2 = cv2.cvtColor(cv2.imread('input/custom/pic2.jpg'),
                                       cv2.COLOR_BGR2GRAY)

    def apply_surf(self):
        ''' Apply SURF on the image set
        '''
        surf1 = cv2.SURF(self.hessian1)
        self.key_pt1, self.descriptor1 = surf1.detectAndCompute(self.image1,
                                                                None)
        surf2 = cv2.SURF(self.hessian2)
        self.key_pt2, self.descriptor2 = surf2.detectAndCompute(self.image2,
                                                                None)
        

    def correspond_points(self):
        ''' Find the corresponding points of 2 images
        '''
        self.connection = np.zeros(shape=(len(self.descriptor1),1))
        for i in range(len(self.descriptor1)):
            print str(i) + '/' + str(len(self.descriptor1))
            value = 0
            value_min = 1e10
            value_min_2 = 1e10
            for j in range(len(self.descriptor2)):
                des1 = self.descriptor1[i]
                des2 = self.descriptor2[j]
                value = np.power(np.sum(np.power(np.subtract(des1,des2),
                                                   2)), 0.5)
                if value < value_min and value < self.threshold :
                    value_min_2 = value_min
                    value_min = value
                    self.connection[i][0] = j
                elif value > value_min and value < value_min_2:
                    value_min_2 = value
                ratio = value_min / value_min_2
                if value_min_2 > 0 and ratio > self.threshold_r:
                    self.connection[i][0] = -1

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
        for i in range(len(self.descriptor1)):
            if(self.connection[i] > -1):
                count = count + 1

                x1, y1 = self.key_pt1[i].pt
                x2, y2 = self.key_pt2[int(self.connection[i][0])].pt
                col1 = random.randint(0, 255)
                col2 = random.randint(0, 255)
                col3 = random.randint(0, 255)

                cv2.circle(self.output_img,(int(x1),int(y1)),1,(col1,col2,col3),4)
                cv2.circle(self.output_img,(int(x2) + width1,int(y2)),1,
                                            (col1,col2,col3),4)

                cv2.line(self.output_img, (int(x1), int(y1)),
                        (int(x2) + width1,int(y2)), (col1,col2,col3), 1)
        print count

    def output_image(self, choice):
        '''Output the final image
        @param choice The choice of image set
        '''
        path = 'output/Surf/' + 'Image_set_' + str(choice) + '.jpg'
        cv2.imwrite(path, self.output_img)

if __name__ == "__main__":
    temp = HW_problem2()
