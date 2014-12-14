import cv2
import numpy as np
from Node import Node

class Labeling(object):

    def __init__(self, image):
        self.image = image
        self.height, self.width = self.image.shape[:2]
        self.label_count = 0
        self.label_record = np.zeros((self.height, self.width), dtype=np.int)
        self.labels = []
        self.labels.append(Node(0,0))
        self.label_component()

    def label_component(self):
     
        for j in range(1,self.height - 1):
            for i in range(1,self.width - 1):
                if(self.image[j][i] == 0):
                    if(self.label_record[j][i - 1] != 0 and self.label_record[j - 1][i] == 0):
                        self.label_record[j][i] = self.label_record[j][i - 1]
                    elif(self.label_record[j][i - 1] == 0 and self.label_record[j - 1][i] != 0):
                        self.label_record[j][i] = self.label_record[j - 1][i]
                    elif(self.label_record[j][i - 1] != 0 and self.label_record[j - 1][i] != 0):
                        if(self.label_record[j][i - 1] == self.label_record[j - 1][i]):
                            self.label_record[j][i] = self.label_record[j][i - 1]
                        else:
                            rootA = self.get_root(self.label_record[j][i - 1], self.labels)
                            rootB = self.get_root(self.label_record[j - 1][i], self.labels)
                            if(rootA > rootB):
                                self.label_record[j][i] = rootB
                                self.labels[rootA].parent = rootB
                            else:
                                self.label_record[j][i] = rootA
                                self.labels[rootB].parent = rootA
                        
                    else:
                        self.label_count += 1
                        self.label_record[j][i] = self.label_count
                        self.labels.append(Node(self.label_count, 0))
    
        #map labels
        count = 0
        for i in range(1, len(self.labels)):
            if(self.labels[i].parent != i):
                root_label = self.get_root(i, self.labels)
                self.labels[i].parent = root_label
            else:
                count += 1
    
        #get countsand store it in label_mat
        label_mat = np.zeros(self.label_count + 1)
                    
        for j in range(1, self.height - 1):
            for i in range(1, self.width - 1):
                if(self.label_record[j][i] != 0):
                    label_index = self.label_record[j][i]
                    label_index = self.labels[label_index].parent
                    self.label_record[j][i] = label_index
                    label_mat[label_index] += 1
    
        image_color= np.zeros((self.height, self.width, 3), np.uint8)
        for j in range(self.height):
            for i in range(self.width):
                if(self.image[j][i] == 0):
                    label_index = self.label_record[j][i]
                    if(label_mat[label_index] > 100):
                       if (label_mat[label_index] < 50000):
                            self.image[j][i] = 0
                    else:
                        self.label_record[j][i] = 0
                        label_mat[label_index] = 0
                        self.image[j][i] = 255
    
        self.count = 0
        for i in range(1, self.label_count + 1):
            if(label_mat[i] != 0):
                self.count += 1
                self.labels[i].new_label = self.count
    
        for j in range(self.height):
            for i in range(self.width):
                if(self.label_record[j][i] != 0):
                    self.label_record[j][i] = self.labels[self.label_record[j][i]].new_label

    def get_root(self, label_num, Labeling):
        while(Labeling[label_num].parent != label_num):
            label_num = Labeling[label_num].parent
        return label_num

    def get_image(self):
        return self.image

    def get_record(self):
        return self.label_record

    def get_count(self):
        return self.count
