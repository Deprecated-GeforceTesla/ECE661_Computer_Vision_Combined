import numpy as np
import cv2


class PCA(object):

    def __init__(self, img_vecs, vec_means):
        self.img_vecs = img_vecs
        self.vec_means = vec_means

    def pca_operation(self):
        Xt = np.asarray(map(lambda row: row - self.vec_means, self.img_vecs))
        XtX = np.dot(Xt, Xt.T)
        eig_vals, eig_vecs = np.linalg.eig(XtX)

        index = np.argsort(eig_vals) 
        eig_vecs_sorted = eig_vecs[:, index]
        eig_num = len(eig_vecs_sorted)
        for i in range(eig_num):
            eig_vecs[:, i] = eig_vecs_sorted[:, eig_num - i - 1]
    

        result = np.dot(Xt.T, eig_vecs)

        for i in range(len(self.img_vecs)):
            result[:, i] /= np.linalg.norm(result[:, i])
    
        return result
