import numpy as np
import cv2

class Accuracy_Op(object):

    def __init__(self, eig_vecs, class_num, train_img_vecs, train_mean, test_img_vecs):
        self.eig_vecs = eig_vecs
        self.class_num = class_num
        self.train_img_vecs = train_img_vecs
        self.train_mean = train_mean
        self.test_img_vecs = test_img_vecs
        self.find_accuracy()

    def find_accuracy(self):
        self.accuracy = np.zeros(self.class_num+1)
        for i in range(1, self.class_num+1):
            Wp = self.eig_vecs[:, 0:i]
        
            project_train = self.projection(Wp, self.train_img_vecs, self.train_mean)
            project_test = self.projection(Wp, self.test_img_vecs, self.train_mean)
        
            correct_num = 0
            for j in range(len(self.test_img_vecs)):
                test_proj = project_test[:, j]
                train_index = self.NN_operation(test_proj, project_train)
                if(int(train_index/21) == int(j/21)):
                    correct_num += 1
            self.accuracy[i] = (float(correct_num) / len(self.test_img_vecs)) * 8


    def projection(self, Wp, img_vecs, img_mean):
        Xt = np.asarray(map(lambda row: row - img_mean, img_vecs))
        return np.dot(Wp.T, Xt.T)
    
    
    def NN_operation(self, test_proj, project_train):
        num = project_train.shape[1]
        distance = np.zeros(num)
        for i in range(num):
            train_proj = project_train[:, i]
            dist = np.power((train_proj - test_proj), 2)
            distance[i] = np.sum(dist)
    
        return np.argmin(distance)

    def get_accuracy(self):
        return self.accuracy
