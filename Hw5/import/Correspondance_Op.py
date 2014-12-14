import numpy as np

class Correspondance_Op(object):

    def __init__(self, descriptor1, descriptor2, threshold, threshold_r):
        self.descriptor1 = descriptor1
        self.descriptor2 = descriptor2
        self.threshold = threshold
        self.threshold_r = threshold_r
        self.correspond_points()

    def correspond_points(self):
        ''' Find the corresponding points of 2 images
        '''
        self.connection = np.zeros(len(self.descriptor1))
        for i in range(len(self.descriptor1)):
            #print str(i) + '/' + str(len(self.descriptor1))
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
                    self.connection[i] = j
                elif value > value_min and value < value_min_2:
                    value_min_2 = value
                ratio = value_min / value_min_2
                if value_min_2 > 0 and ratio > self.threshold_r:
                    self.connection[i] = -1
        self.count = 0
        for i in self.connection:
            if not (i == -1):
                self.count += 1
        print 'for correspond points, there are ' + str(self.count) + ' points'


    def get_correspondance(self):
        return self.connection

    def get_correspondance_count(self):
        return self.count
