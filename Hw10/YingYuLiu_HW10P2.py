from pylab import*
import numpy as np
import cv2
import sys
from glob import glob
from cPickle import load
sys.path.append("import/")
from Image_Op import Image_Op
from Feature_Op import Feature_Op
from Ada import Ada
from Detection_Op import Detection


class Hw_Problem2(object):

    def __init__(self):
        self.pos_train_imgs = 710
        self.neg_train_imgs = 1758
        self.train_imgs_num = self.pos_train_imgs + self.neg_train_imgs
        self.pos_test_imgs = 178
        self.neg_test_imgs = 440
        self.test_imgs_num = self.pos_test_imgs + self.neg_test_imgs
        self.test_images = []
        self.test_neg_imgs = []
        self.test_pos_imgs = []
        self.feature_num = 100035
        self.pos_test_imgs = 178
        self.neg_test_imgs = 440
        self.test_imgs_num = self.pos_test_imgs + self.neg_test_imgs
        self.features_test = load(open("feature_test.p", 'rb'))
        self.stage_num = 10
        self.train_images = []
        self.train_neg_imgs = []
        self.train_pos_imgs = []


    def load_image(self):
        path_test_neg = 'input/car/test/negative/*.png'
        for image in glob(path_test_neg):
            test_neg = cv2.imread(image, 0)
            temp = Image_Op(test_neg)
            test_neg = Image_Op.get_normalization()
            self.test_neg_imgs.append(test_neg)

        path_test_pos = 'input/car/test/positive/*.png'
        for image in glob(path_test_pos):
            test_pos = cv2.imread(image, 0)
            temp = Image_Op(test_pos)
            test_pos = Image_Op.get_normalization()
            self.test_pos_imgs.append(test_pos)

        test_images = self.test_pos_imgs + self.test_neg_imgs
        file_name_test = "feature_test.p"
        temp = Feature_Op(self.test_images, self.test_imgs_num)
        temp.extract_feature()

        path_train_neg = 'input/car/train/negative/*.png'
        for image in glob(path_train_neg):
            train_neg = cv2.imread(image, 0)
            temp = Image_Op(train_neg)
            train_neg = Image_Op.get_normalization()
            self.train_neg_imgs.append(train_neg)

        path_train_pos = 'input/car/train/positive/*.png'
        for image in glob(path_train_pos):
            train_pos = cv2.imread(image, 0)
            temp = Image_Op(train_pos)
            train_pos = Image_Op.get_normalization()
            self.train_pos_imgs.append(train_pos)

        train_images = self.train_pos_imgs + self.train_neg_imgs
        file_name_train = "feature.p"
        temp = Feature_Op(self.train_images, self.train_imgs_num)
        temp.extract_feature()


    def extract_feature(self):
        features = load(open(file_name_train, 'rb'))
        stage_num = 10
        next_idx = np.arange(train_imgs_num)
        for i in range(stage_num):
            print "stage {} begin, len is {}".format(i, len(next_idx))
            temp = Ada(features, next_idx, i)
            next_idx = temp.get_next()
            L = len(next_idx)
            if(L == pos_train_imgs):
                break


    def detection(self):
        self.fp_rate = np.zeros(self.stage_num)
        self.fn_rate = np.zeros(self.stage_num)

        for i in range(self.stage_num):
            file_name = "ht_stage_" + str(i) + ".p"
            ht = load(open(file_name, 'rb'))
            count = 0
            for j in range(ht.shape[1]):
                if(ht[0, j] == 0):
                    break
                count +=1
            alpha = ht[0, :count]
            polarity = ht[1, :count]
            threshold = ht[2, :count]
            feature_id = ht[3, :count]

            temp = Detection(features_test, alpha, polarity, threshold, feature_id, count)
            result = temp.get_result()
    
            self.fn_rate[i] = (pos_test_imgs - np.sum(result[:pos_test_imgs]))/pos_test_imgs
            self.fp_rate[i] = np.sum(result[pos_test_imgs:])/neg_test_imgs
            print "fn rate is " + str(self.fn_rate[i])
            print "fp rate is " + str(self.fp_rate[i])
 
if __name__ == '__main__':
    temp = Hw_Problem2()
