import cv2
import numpy as np

class Surf_Op(object):

    def __init__(self, image, hessian):
        self.hessian = hessian
        self.image = image
        self.apply_surf()

    def apply_surf(self):
        ''' Apply SURF on the image set
        '''
        surf = cv2.SURF(self.hessian)
        self.key_pt, self.descriptor = surf.detectAndCompute(self.image,
                                                             None)

    def get_key_point(self):
        return self.key_pt

    def get_descriptor(self):
        return self.descriptor
