import cv

class Canny(object):

    def __init__(self, image):
        self.edges = cv.CreateMat(image.height, image.width, cv.CV_8UC1)
        self.image = cv.CreateMat(image.height, image.width, cv.CV_8UC1)
        cv.CvtColor(image, self.image, cv.CV_RGB2GRAY)

    def get_canny_edge(self):
        cv.Canny(self.image, self.edges, 255* 1.5, 255)
        return self.edges
        
        
