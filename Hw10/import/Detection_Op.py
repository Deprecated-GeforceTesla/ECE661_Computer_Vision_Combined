import numpy as np

class Detection(object):

    def __init__(self, features, alpha, polarity, threshold, feature_id, count):
        ht_result = np.zeros((test_imgs_num, count))
        self.strong_classifier_result = np.zeros(test_imgs_num)
    
        for i in range(count):
            feature_val = features[feature_id[i]]
            for j in range(test_imgs_num):
                if(polarity[i] * feature_val[j] <= polarity[i]*threshold[i]):
                    ht_result[j, i] = 1
            
            strong_classifer = np.dot(ht_result[:, :i], alpha[:i])
            thres_strong_idx = np.argmin(strong_classifer[:pos_test_imgs])
            thres_strong = strong_classifer[thres_strong_idx]
        
            for m in range(test_imgs_num):
                if(strong_classifer[m] > thres_strong):
                    self.strong_classifier_result[m] = 1
                else:
                    self.strong_classifier_result[m] = 0

    def get_result(self):
        return self.strong_classifier_result
