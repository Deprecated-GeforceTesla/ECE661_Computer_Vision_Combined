import numpy as np
import cv2
import Image_Coord_Op as Image_op

def output(image, homography, width, height, name, option=0):
    if option == 0:
        matrix_h = homography
        matrix_h_inv = Image_op.matrix_inverse(homography)
    else:
        matrix_h = Image_op.matrix_inverse(homography)
        matrix_h_inv = homography

    # a fixed scale to make image larger

    boundry = find_boundry(width, height, matrix_h, 1)
    #auto resize the smallest size to 1000px
    length_y = boundry[3] - boundry[1]
    length_x = boundry[2] - boundry[0]
    min_length = min(length_y, length_x)    
    scale = 1000 / min_length

    boundry = find_boundry(width, height, matrix_h, scale)    
    offset_x = boundry[0]
    offset_y = boundry[1]
    print boundry
    output_width = int(boundry[2] - boundry[0])
    output_height = int(boundry[3] - boundry[1])
    output_image = np.zeros((output_width, output_height,3), np.uint8)

    for n in range(output_height):
        for i in range(output_width):
            x = (i + offset_x)/ scale 
            y = (n + offset_y) / scale
            location = Image_op.convert_plane_pt(x, y, matrix_h_inv)
            if location_in_range(location, width, height):
                output_image[i][n] = bilinear_interpolation(image,
                                                            location[0],
                                                            location[1])
    cv2.imwrite("output/" + name + ".jpg", output_image)

def location_in_range(location, width, height):
    if int(location[0]) < width - 1 and location[0] > 0:
        if int(location[1]) < height - 1 and location[1] > 0:
            return True
    return False

def bilinear_interpolation(image, x, y):
    point1 = (x - int(x)) * (y - int(y)) * (image[int(y + 1)][int(x + 1)])
    point2 = (int(x + 1) - x) * (y - int(y)) * image[int(y + 1)][int(x)]
    point3 = (x - int(x)) * (int(y + 1) - y) * image[int(y)][int(x + 1)]
    point4 = (int(x + 1) - x) * (int(y + 1) - y) * image[int(y)][int(x)]
    return point1 + point2 + point3 + point4

def find_boundry(width, height, matrix_h, scale):
    left_up = Image_op.convert_plane_pt(0, 0, matrix_h)
    right_up = Image_op.convert_plane_pt(width, 0, matrix_h)
    left_bottom = Image_op.convert_plane_pt(0, height, matrix_h)
    right_bottom = Image_op.convert_plane_pt(width, height, matrix_h)

    max_y =  max([left_up, right_up, left_bottom, right_bottom],
                 key=lambda x:x[1])
    min_y =  min([left_up, right_up, left_bottom, right_bottom],
                  key=lambda x:x[1])
    max_x =  max([left_up, right_up, left_bottom, right_bottom],
                  key=lambda x:x[0])
    min_x =  min([left_up, right_up, left_bottom, right_bottom],
                  key=lambda x:x[0])

    return [min_x[0] * scale, min_y[1] * scale,
            max_x[0] * scale, max_y[1] * scale]

    
