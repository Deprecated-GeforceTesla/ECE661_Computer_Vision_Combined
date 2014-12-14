import cv2
import numpy as np

class Recongnition(object):

    def __init__(self, image_count, descriptor, descriptor1, label_count, label_count1):
        self.image_count = image_count
        self.descriptor = descriptor
        self.target_descriptor = descriptor1
        self.label_count = label_count
        self.target_label_count = label_count1
        self.image_Recognition()


    def image_Recognition(self):
        radius_base = self.descriptor.radius
        radius1 = self.target_descriptor.radius
        ratio = float(radius_base)/float(radius1)

        for i in range(self.target_label_count):
            Input_image = self.target_descriptor.image[i]
            cv2.imwrite("Output/image" + str(self.image_count) + "/characters/input" + str(i) + ".jpg", Input_image)
            #cv2.imshow('Output', Input_image)
            #cv2.waitKey(0) 
            arc_length = self.target_descriptor.Arc_length[i]
            arc_num = len(arc_length)
            distance_min = 1e10
            for j in range(self.label_count):
                arc_length_base = self.descriptor.Arc_length[j]
                arc_num_base = len(arc_length_base)

                if(arc_num < 2):
                    label_match = 14
                    distance_min = 0
                    break
                if(arc_num_base - arc_num > 1 or arc_num - arc_num_base > 1):
                    continue
                distance = self.arc_Comparsion(arc_length_base, arc_length, ratio)

                if(distance < distance_min):
                    distance_min = distance
                    label_match = j

            Matched_image = self.descriptor.image[label_match]
            cv2.imwrite("Output/image" + str(self.image_count) + "/Matched/output" + str(i) + ".jpg", Matched_image)

    def arc_Comparsion(self, arc_base, arc_len, ratio):
        arc_num_base = len(arc_base)
        arc_num = len(arc_len)
        check = 0

        if(arc_num_base < arc_num):
            temp = arc_base
            arc_base = arc_len
            arc_len = temp
            temp = arc_num_base
            arc_num_base = arc_num
            arc_num = temp
            check = 1

        for i in range(arc_num_base):
            arc_base.append(arc_base[i])
        distance_min = 1e10
        for i in range(arc_num_base):
            distance = 0
            for j in range(arc_num):
                if(check == 0):
                    distance += np.power((arc_base[j + i] - arc_len[j] * ratio),2)
                if(check == 1):
                   distance += np.power((arc_base[j + i] * ratio - arc_len[j]),2)
            if(distance < distance_min):
                distance_min = distance
    
        for i in range(arc_num_base):
            arc_base.remove(arc_base[0])
    
        distance_min = distance_min / arc_num
    
        return distance_min


