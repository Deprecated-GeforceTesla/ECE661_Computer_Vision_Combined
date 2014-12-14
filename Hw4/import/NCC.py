import numpy as np

class NCC(object):


    def __init__(self, descriptor1, descriptor2, window_size, threshold, threshold_r):
        '''Initialize the required resources to compute NCC value
        @param descriptor1 The first descriptor list
        @param descriptor2 The second descriptor list
        @param window_size The NCC window size
        @param threshold The threshold of NCC
        @param threshold_r The threshold ratio of NCC
        '''
        self.window_size = window_size
        self.threshold = threshold
        self.threshold_r = threshold_r
        self.perform_NCC(descriptor1, descriptor2)

    def get_NCC_pt(self, descriptor1, descriptor2):
        '''Calculate the points and their means and apply the NCC formula
        @param descriptor1 The descriptor 1
        @param descriptor2 The descriptor 2
        @return The value of the NCC value
        '''
        mean1 = np.mean(descriptor1['neighbour'])
        mean2 = np.mean(descriptor2['neighbour'])
        ncc_num = 0
        ncc_den1 = 0
        ncc_den2 = 0
        for i in range(self.window_size):
            for j in range(self.window_size):
                ncc_num += ((descriptor1['neighbour'][i][j] - mean1) *
                            (descriptor2['neighbour'][i][j] - mean2))
                ncc_den1 += (descriptor1['neighbour'][i][j] - mean1) ** 2
                ncc_den2 += (descriptor2['neighbour'][i][j] - mean2) ** 2
        value = ncc_num / ((ncc_den1 * ncc_den2) ** 0.5)
        return value

    def perform_NCC(self, descriptor_list_1, descriptor_list_2):
        '''Perform NCC computation on the entire list,
           add value to each descriptor element in dict data structure
        @param descriptor_list_1 The first descriptor list
        @param descriptor_list_2 The second descriptor list
        '''
        for i in range(len(descriptor_list_1)):
            value_max = -1e10
            value_second_max = -1e10
            for j in range(len(descriptor_list_2)):
                value = self.get_NCC_pt(descriptor_list_1[i],
                                        descriptor_list_2[j])
                if(value > value_max and value > self.threshold):
                    value_second_max = value_max
                    value_max = value
                    descriptor_list_1[i]['value'] = value
                    descriptor_list_1[i]['match'] = j
                    descriptor_list_2[j]['value'] = value
                    descriptor_list_2[j]['match'] = i
                elif(value > value_min and value < value_second_min):
                    value_second_max = value
                ratio = value_max / value_second_max
                if(value_second_min > 0 and ratio > self.threshold_r):
                    descriptor_list_1[i]['value'] = -1
                    descriptor_list_1[i]['match'] = -1
                    descriptor_list_2[j]['value'] = -1
                    descriptor_list_2[j]['match'] = -1
