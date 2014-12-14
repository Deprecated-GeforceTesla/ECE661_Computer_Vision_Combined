import cv2
import numpy as np
from cPickle import dump

class Ada(object):

    def __init__(self, features, idx_all, stage):
        self.ada_op(features, idx_all, stage)


    def get_next(self):
        return self.next_idx_all

    def ada_op(self, features, idx_all, stage):
        pos_imgs_num = pos_train_imgs
        neg_imgs_num = len(idx_all) - pos_imgs_num
        imgs_num = pos_imgs_num + neg_imgs_num
        feature = features[:, idx_all]
    
        weights = np.zeros(imgs_num)
        labels = np.zeros(imgs_num)
    
        for i in range(imgs_num):
            if(i < pos_imgs_num):
                weights[i] = 0.5/pos_imgs_num
                labels[i] = 1
            else:
                weights[i] = 0.5/neg_imgs_num

        iteration = 30
        tp_rate = np.zeros(iteration)
        fp_rate = np.zeros(iteration)

        ht = np.zeros((4, iteration))
        ht_result = np.zeros((imgs_num, iteration))

        alpha = np.zeros(iteration)
        strong_classifer_result = np.zeros(imgs_num)
    
        for i in range(iteration):
            weights /= np.sum(weights)
            (err_min, polarity, threshold, feature_idx, best_result) =\
                self.select_classifier(feature, weights, labels, pos_imgs_num, imgs_num)
        
            ht[1, i] = polarity
            ht[2, i] = threshold
            ht[3, i] = feature_idx
            feat = feature[feature_idx]
            for x in range(imgs_num):
                if(polarity * feat[x] <= polarity*threshold):
                    ht_result[x, i] = 1

            print err_min, polarity, feature_idx
            beta = float(err_min)/(1-err_min)
            for m in range(imgs_num):
                if(labels[m] == best_result[m]):
                    weights[m] *= beta
 
            alpha[i] = np.log10(1.0/beta)
            ht[0, i] = alpha[i]
            strong_classifer = np.dot(ht_result[:, :i], alpha[:i])

            thres_strong_idx = np.argmin(strong_classifer[:pos_imgs_num])
            thres_strong = strong_classifer[thres_strong_idx]

            print alpha[i], thres_strong, thres_strong_idx

            for j in range(imgs_num):
                if(strong_classifer[j] >= thres_strong):
                    strong_classifer_result[j] = 1
                else:
                    strong_classifer_result[j] = 0
            tp_rate[i] = np.sum(strong_classifer_result[:pos_imgs_num])/pos_imgs_num
            fp_rate[i] = np.sum(strong_classifer_result[pos_imgs_num:])/neg_imgs_num

            if(tp_rate[i] == 1.0 and fp_rate[i] <= 0.5):
                break
        temp = strong_classifer_result[pos_imgs_num:]
        next_neg_idx = np.argsort(temp)
        temp = temp[next_neg_idx]
        for i in range(neg_imgs_num):
            if(temp[i] > 0):
                next_neg_idx = next_neg_idx[i:]
            break
        self.next_idx_all = np.concatenate([np.arange(pos_imgs_num), next_neg_idx + pos_imgs_num])
    
        file_name = "ht_stage_%d"%(stage) + ".p"
        dump(ht, open(file_name, 'wb'), protocol=2)
    
        cascade_num = 11
        false_pos_rate = np.zeros(cascade_num)
        for i in range(cascade_num):
            false_pos_rate = fp_rate[:i]
            for j in range(1,i):
                if(false_pos_rate[j] == 0):
                    false_pos_rate[j] = false_pos_rate[j-1]
                    break
            fp_accuracy = np.cumprod(false_pos_rate)
        
        true_pos_rate = np.zeros(cascade_num)
        for i in range(cascade_num):
            true_pos_rate = tp_rate[:i]
            for j in range(1,i):
                if(true_pos_rate[j] == 0):
                    true_pos_rate[j] = true_pos_rate[j-1]
                    break
            tp_accuracy = np.cumprod(true_pos_rate)
        figure_name = "output/train_stage_%d"%(stage) 
        figure()
        plot(range(1, len(false_pos_rate) + 1), false_pos_rate, '-x')
        plot(range(1, len(true_pos_rate) + 1), true_pos_rate, '-o')
        legend(["fp_rate", "tp_rate"], loc='best')
        title(figure_name)
        ylabel("Detection rate")
        xlabel("stages number")
        savefig(figure_name + ".png")


    def select_classifier(features, weights, labels, pos_imgs_num, imgs_num):
        err_min = 1e10
        index = 0
        polarity = 0
        threshold = 0.0
        feature_idx = 0
        neg_imgs_num = imgs_num - pos_imgs_num
        best_result = np.zeros(imgs_num)
    
        total_pos_weight = np.sum(weights[:pos_imgs_num])
        total_neg_weight = np.sum(weights[pos_imgs_num:])
        T_plus = np.tile(total_pos_weight, (imgs_num))
        T_minus = np.tile(total_neg_weight, (imgs_num))
    
        for i in range(100035):
            one_feature = features[i]
            sorted_idx = np.argsort(one_feature)
            sorted_feature = one_feature[sorted_idx]
            sorted_weight = weights[sorted_idx]
            sorted_label = labels[sorted_idx]
            s_plus = np.cumsum(sorted_weight * sorted_label)
            s_minus = np.cumsum(sorted_weight) - s_plus
        
            err_plus = s_plus + T_minus - s_minus
            err_minus = s_minus + T_plus - s_plus
        
            err = np.minimum(err_plus, err_minus)
            min_idx = np.argmin(err)
       
            result = np.zeros(imgs_num)
        

            if(err_plus[min_idx] <= err_minus[min_idx]):
                polar = -1
                result[min_idx:] = 1
                result = result[sorted_idx]
            else:
                polar = 1
                result[:min_idx] = 1
                result = result[sorted_idx]
        
            if(err[min_idx] < err_min):
                err_min = err[min_idx]
                if(min_idx == 0):
                    threshold = sorted_feature[0] - 0.5
                elif(min_idx == imgs_num-1):
                    threshold = sorted_feature[imgs_num-1] + 0.5
                else:
                    threshold = (sorted_feature[min_idx-1] + sorted_feature[min_idx])/2.0
                polarity = polar
                feature_idx = i
                best_result = result
                index = min_idx

        return err_min, polarity, threshold, feature_idx, best_result
