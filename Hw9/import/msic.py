import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

def triangulate(points1, points2, P1, P2, count):
    A = np.zeros((4, 4))
    X = np.zeros(3)
    world_points = np.zeros((count, 4))

    for i in range(count):
        for j in range(4):
            A[0, j] = points1[i, 0] * P1[2, j] - P1[0, j]
            A[1, j] = points1[i, 1] * P1[2, j] - P1[1, j]
            A[2, j] = points2[i, 0] * P2[2, j] - P2[0, j]
            A[3, j] = points2[i, 1] * P2[2, j] - P2[1, j]
        ATA = np.dot(A.T, A)
        w, u, vt = cv2.SVDecomp(ATA)
        min_index = w.argmin()

        world_points[i,0] = vt[min_index][0]/vt[min_index][3]
        world_points[i,1] = vt[min_index][1]/vt[min_index][3]
        world_points[i,2] = vt[min_index][2]/vt[min_index][3]
        world_points[i,3] = 1
    
    return world_points
    
def draw_line(points1, points2, image1, image2):
    height1, width1 = image1.shape[:2]
    img1 = image1
    img2 = image2

    image12 = np.zeros((height1, 2*width1, 3), np.uint8)
    for i in range(width1):
        for j in range(height1):
            image12[j][i] = img1[j][i]
            image12[j][i+width1] = img2[j][i]
            
    for i in range(len(points1)):
        x1 = points1[i, :]
        x2 = points2[i, :]
        cv2.circle(image12, (int(x1[0]), int(x1[1])), 2, (255, 0 ,0), 2)
        cv2.circle(image12, (int(x2[0]+width1), int(x2[1])), 2, (0, 255 ,0), 2)
        cv2.line(image12, (int(x1[0]), int(x1[1])), (int(x2[0]+width1), int(x2[1])), (0,0,255), 1)
    return image12
    
def get_rectified_points(H1, H2, points1, points2, count):
    rectified_points1 = np.zeros((count, 3))
    rectified_points2 = np.zeros((count, 3))
    
    for i in range(count):
        x1_orig = points1[i, :]
        x1_rect = np.dot(H1, x1_orig.T)
        x1_rect /= x1_rect[2]
        rectified_points1[i,0] = int(x1_rect[0])
        rectified_points1[i,1] = int(x1_rect[1])
        rectified_points1[i,2] = 1
        
        x2_orig = points2[i, :]
        x2_rect = np.dot(H2, x2_orig.T)
        x2_rect /= x2_rect[2]
        rectified_points2[i,0] = int(x2_rect[0])
        rectified_points2[i,1] = int(x2_rect[1])
        rectified_points2[i,2] = 1
    return rectified_points1, rectified_points2
        
def draw_3d(world_points, count):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    x = []
    y = []
    z = []
    
    for i in range(count):
        if np.abs(world_points[i, 2]) < 50:
            x.append(world_points[i, 0])
            y.append(world_points[i, 1])
            z.append(world_points[i, 2])
    
    ax.scatter(x, y, z, zdir = 'z', s = 1)
    ax.set_xlabel('X_Label')
    ax.set_ylabel('Y_Label')
    ax.set_zlabel('Z_Label')
    
    plt.show()
    plt.savefig("plot_3d.jpg")
