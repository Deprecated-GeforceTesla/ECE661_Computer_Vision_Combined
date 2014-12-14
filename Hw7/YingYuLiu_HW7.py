import sys
import cv2
sys.path.append("import/")
from RGB_Seg_Op import RGB_Seg
from Harris_Op import Harris
from Img_Property import Img_Property
from Labeling import Labeling
from Trainer import Trainer
from Recongnition import Recongnition
from Outsu_Op import Outsu_Op

class Hw_Problem1(object):


    def __init__(self):
        self.base_image = cv2.imread('Pics/Training.jpg',1)
        self.choice = raw_input('which set of image? (1-6) : ')
        self.compute_base_parameter()
        self.choose_image()

    def compute_base_parameter(self):

        train_binary = Trainer(self.base_image)
        train_binary = train_binary.convert_image_to_binary()
        temp = Labeling(train_binary)
        self.image_binary = temp.get_image()
        self.label_map = temp.get_record()
        self.label_num = temp.get_count()
        temp = Img_Property(self.base_image, 0, self.label_map, self.label_num)
        self.descriptors_base = temp.get_character_property()


    def choose_image(self):
        self.image = cv2.imread('Pics/Testing Data/Image' + str(self.choice) + '.jpg')     
        height, width = self.image.shape[:2]
        image_binary = RGB_Seg(self.image)
        image_binary = image_binary.get_image()
        temp = Labeling(image_binary)
        label_map = temp.get_record()
        label_num = temp.get_count()
        temp = Img_Property(self.image, str(self.choice), label_map, label_num)
        descriptors = temp.get_character_property()
 
        temp = Recongnition(str(self.choice), self.descriptors_base, descriptors, self.label_num, label_num)

if __name__ == '__main__':
    temp = Hw_Problem1()

