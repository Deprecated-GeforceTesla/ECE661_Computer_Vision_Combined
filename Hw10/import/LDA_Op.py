import numpy as np
import cv2
from Vector_Op import Vector_Op

class LDA(object):

    def __init__(self, image_vecs, class_size, class_num, vecs_mean):
        self.class_mean_vecs = []
        self.all_class_vecs = []
        self.img_vecs = image_vecs
        self.class_size = class_size
        self.class_num = class_num
        self.vecs_mean = vecs_mean
        self.get_class_mean()
        self.perform_operation()
        self.sort_eigen()
        self.retrieve_pos_eigen()
        self.find_matrix_Zt()


    def calc_mean(self, image_vectors):
        sum_vecs = reduce(lambda vec, sum_vec: vec + sum_vec, image_vectors)
        return sum_vecs/len(image_vectors)

    def get_class_mean(self):
        for i in range(1, self.class_num+1):
            self.class_vecs = []
            num_l = self.class_size *(i - 1)
            num_h = num_l + self.class_size
            for j in range(num_l, num_h):
                self.class_vecs.append(self.img_vecs[j])
            
            self.all_class_vecs.append(self.class_vecs)
            class_mean_vec = self.calc_mean(self.class_vecs)
            self.class_mean_vecs.append(class_mean_vec)


    def perform_operation(self):
        self.Mt = np.asarray(map(lambda row: row - self.vecs_mean, self.class_mean_vecs))
        self.MtM = np.dot(self.Mt, self.Mt.T)
        self.eig_vals, self.eig_vecs = np.linalg.eig(self.MtM)
    

    def sort_eigen(self):
        self.index = np.argsort(self.eig_vals) 
        self.eig_vals_sorted = self.eig_vals[self.index]
        self.eig_vecs_sorted = self.eig_vecs[:, self.index]
        eig_num = len(self.eig_vecs_sorted)
        for i in range(eig_num):
            self.eig_vals[i] = self.eig_vals_sorted[eig_num - i - 1]
            self.eig_vecs[:, i] = self.eig_vecs_sorted[:, eig_num - i - 1]

    def retrieve_pos_eigen(self):
        self.V = []
        self.DB = []

        for i in range(len(self.eig_vals)):
            if(self.eig_vals[i] > 0):
                self.DB.append(self.eig_vals[i])
                self.V.append(self.eig_vecs_sorted[i])
        self.V = np.asarray(self.V)
    
        Y = np.dot(self.Mt.T, self.V)
        self.DB = np.asarray(self.DB)
        self.DB = self.DB/float(self.class_num)
    
        self.Z = np.dot(Y, np.diag(1/np.sqrt(self.DB)))
    
        self.remained_eig = len(self.DB)
        self.ZtSwZ = np.zeros((self.remained_eig, self.remained_eig))


    def find_matrix_Zt(self):
        for i in range(self.class_num):
            self.class_vecs = self.all_class_vecs[i]
            Ti = np.zeros((self.remained_eig, self.remained_eig))
        
            for j in range(len(self.class_vecs)):
                image_vec = self.class_vecs[j]
                zero_mean = image_vec - self.class_mean_vecs[i]
                zero_mean = np.asarray(zero_mean)
                zero_mean = zero_mean.reshape(zero_mean.shape[0], 1)
                G = np.dot(self.Z.T, zero_mean)
                Ti += np.dot(G, G.T)
        
            self.ZtSwZ += (Ti/len(self.class_vecs))
    
        self.ZtSwZ /= self.class_num
    
        self.eig_vals, self.eig_vecs = np.linalg.eig(self.ZtSwZ)
    
        self.index = np.argsort(self.eig_vals) 
        self.eig_vals_sorted = self.eig_vals[self.index]
        self.eig_vecs_sorted = self.eig_vecs[:, self.index]
    
        self.W = np.dot(self.Z, self.eig_vecs_sorted)
        for i in range(self.remained_eig):
            self.W[:, i] /= np.linalg.norm(self.W[:, i])


    def get_result(self):
        return self.W
