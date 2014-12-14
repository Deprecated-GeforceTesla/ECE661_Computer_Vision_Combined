from pylab import*
import cv2
import sys
from glob import glob
sys.path.append("import/")
from Vector_Op import Vector_Op
from PCA_Op import PCA
from LDA_Op import LDA
from Accuracy_Op import Accuracy_Op

class Hw_Problem1(object):

    def __init__(self):
        self.class_size = 21
        self.class_num = 30
        self.load_image()
        self.vector_operation()
        self.pca_operation()
        self.lda_operation()
        self.find_accuracy()
        self.output_plot()

    def load_image(self):

        self.train_images = []
        self.test_images = []

        for image in glob('input/face/train/*.png'):
            image_train = cv2.imread(image, 1)
            self.train_images.append(image_train)

        for image in glob('input/face/test/*.png'):
            image_test = cv2.imread(image, 1)
            self.test_images.append(image_test)


    def vector_operation(self):
        temp = Vector_Op(self.test_images, self.train_images)

        self.train_images_vecs = temp.get_train_vector()
        self.test_images_vecs = temp.get_test_vector()
        self.train_mean = temp.get_train_mean()

    def pca_operation(self):
        temp = PCA(self.train_images_vecs, self.train_mean)
        self.W_pca = temp.pca_operation()


    def lda_operation(self):
        temp = LDA(self.train_images_vecs, self.class_size, self.class_num, self.train_mean)
        self.W_lda = temp.get_result()

    def find_accuracy(self):
        temp = Accuracy_Op(self.W_pca, self.class_num, self.train_images_vecs, self.train_mean, self.test_images_vecs)
        self.pca_accuracy = temp.get_accuracy()

        temp = Accuracy_Op(self.W_lda, self.class_num, self.train_images_vecs, self.train_mean, self.test_images_vecs)
        self.lda_accuracy = temp.get_accuracy()

    def output_plot(self):
        plot(range(0, 31), self.pca_accuracy, '-o', label="PCA")
        title("Accuracy vs Dimension")
        ylabel("Accuracy")
        xlabel("Dimension")
        plot(range(0,31), self.lda_accuracy, '-x', label="LDA")
        legend(loc='lower right')
        savefig("output.png")

if __name__ == '__main__':
    temp = Hw_Problem1()
