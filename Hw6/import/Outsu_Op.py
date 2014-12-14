import cv2
import numpy as np

class Outsu_Op(object):

    def __init__(self, histogram, min_value, max_value):
        self.hist = histogram
        self.min_value = min_value
        self.max_value = max_value


    def perform_outsu(self):
        prob = np.zeros(self.max_value - self.min_value + 1)
        total_pixels = 0
        mean = 0

        total_pixels = sum(self.hist)

        for i in range(self.min_value, self.max_value + 1):
            prob[i] = self.hist[i] / total_pixels
            mean += i * prob[i]

        max_variance = 0
        w0 = 0
        uk = 0

        for i in range(self.min_value, self.max_value + 1):
            w0 += prob[i]
            if (w0 != 1 and w0 != 0):
                uk += i * prob[i]
                variance = ((mean * w0 - uk) ** 2) / (w0 * (1 - w0))
                if variance > max_variance:
                    max_variance = variance
                    threshold = i

        return threshold
