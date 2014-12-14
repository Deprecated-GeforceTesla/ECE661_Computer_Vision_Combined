import numpy as np

def convert_plane_pt(x, y, matrix):
    '''Multiply the vector of the point with the matrix
    @param x The x axis of the point
    @param y The y axis of the point
    @param matrix The homography matrix or its inverse
    @return the converted plane's axis (image<->world)
    '''
    plane = np.zeros(shape=(3,1))
    plane[0][0] = x
    plane[1][0] = y
    plane[2][0] = 1
    result = np.dot(matrix, plane)
    return [result[0][0] / result[2][0],
            result[1][0] / result[2][0]]

def matrix_inverse(matrix):
    '''Calculate the inverse of the matrix
    @param matrix The source matrix
    @return The inverse of the input matrix
    '''
    return np.linalg.inv(matrix)

def matrix_average(matrix1, matrix2):
    '''Calculate the average of 2 matrix
    @param matrix1 The first matrix
    @param matrix2 The second matrix
    @return The average of 2 matrix
    '''
    return (matrix1 + matrix2) / 2

def find_sum_pixel(color1, color2, color3, color4):
    a1, b1, c1 = color1
    a2, b2, c2 = color2
    a3, b3, c3 = color3
    a4, b4, c4 = color4

    a = a1 + a2 + a3 + a4
    b = b1 + b2 + b3 + b4
    c = c1 + c2 + c3 + c4
    return (int(a), int(b), int(c))
   
