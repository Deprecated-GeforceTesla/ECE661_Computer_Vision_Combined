import numpy as np

class Descriptor(object):

    def __init__(self, harris_img, orig_img, max_amount,
                 window_size, threshold):
        '''Initialize the required resources for the descriptors
        @param harris_img The result of harris corner detection
        @param orig_img The original image
        @param max_amount Max amount of descriptors allowed
        @param window_size The window size for finding descriptor
        @param thresgold The threshold value for interesting points
        '''
        self.window_size = window_size
        self.threshold = threshold
        self.max_amount = max_amount
        self.find_descriptors(harris_img, orig_img)
        self.find_all_neighbour(orig_img)


    def find_descriptors(self, harris_img, orig_img):
        '''Define interesting points as harris value is larger than threshold
        @param harris_img Thge result of harris corner detection
        @param orig_img The original image
        '''
        self.descriptor = []
        height, width = orig_img.shape[:2]
        lower_bound = self.window_size / 2
        width_upper_bound = width - lower_bound - 1
        height_upper_bound = height - lower_bound - 1

        for i in range(lower_bound, width_upper_bound):
            if(len(self.descriptor) > self.max_amount):
                break
            for j in range(lower_bound, height_upper_bound):
                if (harris_img[j][i] >= self.threshold):
                    if(len(self.descriptor) > self.max_amount):
                        break
                    temp_descriptor = {}
                    temp_descriptor['x'] = i
                    temp_descriptor['y'] = j
                    self.descriptor.append(temp_descriptor)

    def find_all_neighbour(self, orig_img):
        '''Find all the neighborurs within the descruptors
        @param orig_img The original image
        '''
        for i in self.descriptor:
            i['neighbour'] = self.find_neighbour(orig_img, i['x'], i['y'])

    def find_neighbour(self, orig_img, x, y):
        ranges = self.window_size / 2
        neighbour = np.zeros(shape=(self.window_size,self.window_size))
        for i in range(-ranges, ranges + 1):
            for j in range(-ranges, ranges + 1):
                neighbour[j + ranges][i + ranges] = orig_img[y + j][x + i]
        return neighbour

    def get_descriptor_list(self):
        return self.descriptor
