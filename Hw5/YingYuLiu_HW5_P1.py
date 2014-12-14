import sys
import cv2
import numpy as np
import random
sys.path.append("import/")
import Ransac_Op
import Surf_Op
import Correspondance_Op
import LLS
import Image_Op
import Dog_Leg

class HW_problem1(object):

    def __init__(self):
        '''Initialize the requried parameters for each image set
        '''
        self.max_image = 5
        self.images = []
        self.grey_images = []
        self.key_points = []
        self.descriptors = []
        self.matrix_H = []
        self.correspondences = []
        img_choice = raw_input('Select the set of image : ')
        self.choice = img_choice
        if int(img_choice) == 1:
            self.pt_threshold = 0.4  # threshold
            self.threshold_r = 0.9
            self.hessian = 15000  
            self.error_threshold = 100
            self.inlier_probability = 0.77
        elif int(img_choice) == 2:
            self.pt_threshold = 0.5  # threshold
            self.threshold_r = 0.9
            self.hessian = 18000 
            self.error_threshold = 100
            self.inlier_probability = 0.75
        self.load_image(int(img_choice))
        self.apply_surf()
        self.find_homography()
        self.combine_images()


    def load_image(self, choice):
        '''Load the original image and convert them to gray level
        @param choice The image set to choose from
        '''
        for i in range(1, self.max_image + 1):
            image = cv2.imread('input/Set' + str(choice) + '/' + str(i) + '.jpg')
            grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            self.images.append(image)
            self.grey_images.append(grey_image)
            


    def apply_surf(self):
        for i in range(self.max_image):
            surf = Surf_Op.Surf_Op(self.grey_images[i], self.hessian)
            key_point = surf.get_key_point()
            descriptor = surf.get_descriptor()
            self.key_points.append(key_point)
            self.descriptors.append(descriptor)


    def create_output_image(self):
        '''Create a base for the output image
        @param choice The choice of correspnding image set
        '''
        height1, width1 = self.images[0].shape[:2]
        height2, width2 = self.images[1].shape[:2]

        output_height = max(height1, height2)
        output_width = width1 + width2
        self.output_img = np.zeros((output_height,output_width,3), np.uint8)
        for i in range(output_width):
            for j in range(output_height):
                if i < width1:
                    self.output_img[j][i] = self.images[0][j][i]
                else:
                    self.output_img[j][i] = self.images[1][j][i - width1]

    def circle_output_points(self, correspondence):
        '''Circle and draw line for the chosen outputs. Draw connection
           between related points
        '''
        height1, width1 = self.images[0].shape[:2]
        height2, width2 = self.images[1].shape[:2]
        for i in range(len(self.key_points[0])):
            col1 = random.randint(0, 255)
            col2 = random.randint(0, 255)
            col3 = random.randint(0, 255)
            x1, y1 = self.key_points[0][i].pt
            x2, y2 = self.key_points[1][int(correspondence[i])].pt
            cv2.circle(self.output_img,(int(x1),int(y1)),1,(col1,col2,col3),10)
            cv2.circle(self.output_img,(width1 + int(x2),int(y2)),1,(col1,col2,col3),10)
            cv2.line(self.output_img, (int(x1), int(y1)),
                        (int(x2)+width1,int(y2)), (col1,col2,col3), 1)



    def output_image(self, count):
        '''Output the final image
        @param choice The choice of image set
        @param method The chosen compute method (SSD/NCC)
        @param scale The scale of Gaussian Blur
        '''

        path = ('output/Set' + str(self.choice) + '/corresponding.jpg')
        cv2.imwrite(path, self.output_img)

    def find_homography(self):
        for i in range(self.max_image - 1):
            corr = Correspondance_Op.Correspondance_Op(self.descriptors[i], self.descriptors[i + 1], self.pt_threshold, self.threshold_r)
            correspondence = corr.get_correspondance()
            self.correspondences.append(correspondence)
            if i == 0:
                self.create_output_image()
                self.circle_output_points(correspondence)
                self.output_image(i)
            ransac = Ransac_Op.Ransac_Op(self.key_points[i], self.key_points[i + 1], correspondence, self.error_threshold, self.inlier_probability)
            inlier1 = ransac.get_inlier1()
            inlier2 = ransac.get_inlier2()
            lls = LLS.LLS(inlier1, inlier2)
            self.matrix_H.append(lls.get_homography())
            matrix_H = lls.get_homography()
            #dog_leg = Dog_Leg.Dog_Leg(inlier1, inlier2, matrix_H)

    def combine_images(self):
        img = Image_Op.Image_Op(self.images, self.correspondences, self.matrix_H, self.max_image)
        output_img = img.get_combined_image()
        path = ('output/Set' + str(self.choice) + '/mosiac.jpg')
        cv2.imwrite(path, output_img)















if __name__ == "__main__":
    temp = HW_problem1()
