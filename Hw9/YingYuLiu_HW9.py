import numpy as np
import cv2
import sys
sys.path.append("import/")
from Fundamental_Op import Fundamental_Op
from Epipole_Op import Epipole_Op
from Rectify_Op import Rectify_Op
from Descriptor_Op import Descriptor_Op
from Ncc_Op import Ncc_Op
from msic import triangulate, draw_line, get_rectified_points, draw_3d

class Hw_Problem1(object):

    def __init__(self):
        image1 = cv2.imread('input/1.jpg', 1)
        image2 = cv2.imread('input/2.jpg', 1)
        image1_points = cv2.imread('input/1.jpg', 1)
        image2_points = cv2.imread('input/2.jpg', 1)
        height, width = image1.shape[:2]
        points1 = np.array([[25,67,1],[294,25,1],[64,241,1],[397,136,1],[75,267,1],[372,169,1],[238,164,1],[217,145,1],
                            [174,111,1],[161,90,1],[109,81,1],[151,191,1]], dtype = float)
        points2 = np.array([[43,35,1],[323,31,1],[18,197,1],[385,166,1],[36,223,1],[360,195,1],[200,162,1],[189, 140,1],
                            [159,98,1],[155,77,1],[108,60,1],[108,169,1]], dtype = float)
        for i in range(12):
            cv2.circle(image1_points, (int(points1[i,0]), int(points1[i, 1])), 2, (0, 0 ,255), 2)
            cv2.circle(image2_points, (int(points2[i,0]), int(points2[i, 1])), 2, (0, 0 ,255), 2)
        cv2.imwrite("Output/selected_points/Pic_1.jpg", image1_points)
        cv2.imwrite("Output/selected_points/Pic_2.jpg", image2_points)
        temp = Fundamental_Op(points1, points2, 12)

        F = temp.get_matrix_F()


        temp = Epipole_Op(F)

        e1 = temp.get_epipole1()
        e2 = temp.get_epipole2()
        P1 = temp.get_matrix_P1()
        P2 = temp.get_matrix_P2()


        F_refined = F


        image12_epipolar = draw_line(points1, points2, image1, image2)
        cv2.imwrite("Output/epipolar_line/Pic_123.jpg", image12_epipolar)

        temp = Rectify_Op(image1, image2, points1, points2, F_refined)

        image1_rectified = temp.get_rect_image1()
        image2_rectified = temp.get_rect_image2()
        H1 = temp.get_matrix_H1()
        H2 = temp.get_matrix_H2()
        F_new = temp.get_matrix_F()


        cv2.imwrite("Output/rectified_image/Pic_1.jpg", image1_rectified)
        cv2.imwrite("Output/rectified_image/Pic_2.jpg", image2_rectified)
        rectified_points1, rectified_points2 = get_rectified_points(H1, H2, points1, points2, 12)
        rect_lines12 = draw_line(rectified_points1, rectified_points2, image1_rectified, image2_rectified)
        cv2.imwrite("Output/rectified_epipolar_line/Pic_12.jpg", rect_lines12)


        image1 = cv2.imread('input/1.jpg', 1)
        image2 = cv2.imread('input/2.jpg', 1)
        image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        descriptor1 = Descriptor_Op(image1_gray, H1)
        descriptor1 = descriptor1.get_result()

        descriptor2 = Descriptor_Op(image2_gray, H2)
        descriptor2 = descriptor2.get_result()


        temp = Ncc_Op(descriptor1, descriptor2, image1_gray, image2_gray, F_new)
        descriptor1 = temp.get_descriptor1()
        descriptor2 = temp.get_descriptor2()

        image12 = np.zeros((height, 2*width, 3), np.uint8)
        for i in range(width):
            for j in range(height):
                image12[j][i] = image1[j][i]
                image12[j][i+width] = image2[j][i]


        for i in range(len(descriptor1)):
            cv2.circle(image12,(descriptor1[i].x,descriptor1[i].y), 1, (255,0,0), 4)

        for i in range(len(descriptor2)):
            cv2.circle(image12,(descriptor2[i].x+width, descriptor2[i].y), 1, (255,0,0), 4)
    
        cv2.imwrite("Output/correspondences.jpg", image12)


        count = 0
        for i in range(len(descriptor1)):
            if(descriptor1[i].match != -1):
                count += 1
        
        points1_correspondence = np.zeros((count, 3))
        points2_correspondence = np.zeros((count, 3))
        points1_rect = np.zeros((count,3))
        points2_rect = np.zeros((count,3))
        mm = 0
        for i in range(len(descriptor1)):
            if(descriptor1[i].match != -1):
                cv2.line(image12, (descriptor1[i].x, descriptor1[i].y), (descriptor2[descriptor1[i].match].x+width,
                    descriptor2[descriptor1[i].match].y), (0,0,255), 1)
                points1_correspondence[mm, 0] = descriptor1[i].x
                points1_correspondence[mm, 1] = descriptor1[i].y
                points1_correspondence[mm, 2] = 1
                points1_rect[mm, 0] = descriptor1[i].x_rect
                points1_rect[mm, 1] = descriptor1[i].y_rect
                points1_rect[mm, 2] = 1
        
                m = descriptor1[i].match
                points2_correspondence[mm, 0] = descriptor2[m].x
                points2_correspondence[mm, 1] = descriptor2[m].y
                points2_correspondence[mm, 2] = 1
                points2_rect[mm, 0] = descriptor2[m].x_rect
                points2_rect[mm, 1] = descriptor2[m].y_rect
                points2_rect[mm, 2] = 1
                mm += 1
        
        cv2.imwrite("Output/correspondences_conect.jpg", image12)


        temp = Fundamental_Op(points1_correspondence, points2_correspondence, count)

        F = temp.get_matrix_F()
        F2_refined = F



        temp = Epipole_Op(F2_refined)

        e1 = temp.get_epipole1()
        e2 = temp.get_epipole2()
        P1 = temp.get_matrix_P1()
        P2 = temp.get_matrix_P2()
    
        rect_lines12 = draw_line(points1_rect, points2_rect, image1_rectified, image2_rectified)
        cv2.imwrite("Output/final_epipolar/Pic_12.jpg", rect_lines12)


        world_points = triangulate(points1_correspondence, points2_correspondence, P1, P2, count)

        draw_3d(world_points, count)

if __name__ == '__main__':
    temp = Hw_Problem1()


