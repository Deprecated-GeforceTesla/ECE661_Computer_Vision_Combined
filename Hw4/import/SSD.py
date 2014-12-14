import numpy as np


class SSD(object):


    def __init__(self, descriptor1, descriptor2, window_size, threshold, threshold_r):
        '''Initialize the required resources to compute SSD value
        @param descriptor1 The first descriptor list
        @param descriptor2 The second descriptor list
        @param window_size The NCC window size
        @param threshold The threshold of SSD
        @param threshold_r The threshold ratio of SSD
        '''
        self.window_size = window_size
        self.threshold = threshold
        self.threshold_r = threshold_r
        self.perform_SSD(descriptor1, descriptor2)

    def get_SSD_pt(self, descriptor1, descriptor2):
        '''Calculate the points and their means and apply the SSD formula
        @param descriptor1 The descriptor 1
        @param descriptor2 The descriptor 2
        @return The value of the SSD value
        '''
        value = 0
        for i in range(self.window_size):
            for j in range(self.window_size):
                 value += (descriptor1['neighbour'][i][j] -
                           descriptor2['neighbour'][i][j]) ** 2
        return value / (self.window_size ** 2)

    def perform_SSD(self, descriptor_list_1, descriptor_list_2):
        '''Perform SSD computation on the entire list,
           add value to each descriptor element in dict data structure
        @param descriptor_list_1 The first descriptor list
        @param descriptor_list_2 The second descriptor list
        '''
        for i in range(len(descriptor_list_1)):
            value_min = 1e10
            value_second_min = 1e10
            for j in range(len(descriptor_list_2)):
                value = self.get_SSD_pt(descriptor_list_1[i],
                                        descriptor_list_2[j])
                if(value < value_min and value < self.threshold):
                    value_second_min = value_min
                    value_min = value
                    descriptor_list_1[i]['value'] = value
                    descriptor_list_1[i]['match'] = j
                    descriptor_list_2[j]['value'] = value
                    descriptor_list_2[j]['match'] = i
                elif(value > value_min and value < value_second_min):
                    value_second_min = value
                ratio = value_min / value_second_min
                if(value_second_min > 0 and ratio > self.threshold_r):
                    descriptor_list_1[i]['value'] = -1
                    descriptor_list_1[i]['match'] = -1
                    descriptor_list_2[j]['value'] = -1
                    descriptor_list_2[j]['match'] = -1
