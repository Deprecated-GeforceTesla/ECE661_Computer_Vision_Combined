import cv2
import numpy as np
from Harris_Op import Harris
from Character import Character

class Img_Property(object):

    def __init__(self, image, image_count, label_record, label_count):
        self.image = image
        self.height, self.width = self.image.shape[:2]
        self.image_count = image_count
        self.label_record = label_record
        self.label_count = label_count
        self.get_character_boundary()

    def get_character_boundary(self):       
        self.label_shape = np.zeros((self.label_count+1,4))
        for i in range(1,self.label_count+1):
            self.label_shape[i][1] = 2000
            self.label_shape[i][3] = 2000
    
        #get the max self.width and max self.height for a character
        self.height_max = 0
        self.width_max = 0

        for j in range(self.height):
            for i in range(self.width):
                label = self.label_record[j][i]
                if(label != 0):
                    if(j > self.label_shape[label][0]):
                        self.label_shape[label][0] = j
                    if(j < self.label_shape[label][1]):
                        self.label_shape[label][1] = j
                    if(i > self.label_shape[label][2]):
                        self.label_shape[label][2] = i
                    if(i < self.label_shape[label][3]):
                        self.label_shape[label][3] = i
        #get the maximal self.height and self.width            
        for i in range(1,self.label_count+1):
            if(self.label_shape[i][0] - self.label_shape[i][1]> self.height_max):
                self.height_max = self.label_shape[i][0] - self.label_shape[i][1]
            if(self.label_shape[i][2] - self.label_shape[i][3] > self.width_max):
                self.width_max = self.label_shape[i][2] - self.label_shape[i][3]

        self.boundary = [self.height_max, self.width_max]

    def get_character_property(self):
        height_max = self.boundary[0]
        width_max = self.boundary[1]
        height_half = int(height_max/2)
        width_half = int(width_max/2)
        vector0 = np.zeros(2)
        vector1 = np.zeros(2)
        vector0[1] = 1
    
        #character_img = np.zeros((height_max+7, width_max+7))
        character_height_center = int((height_max+7)/2)
        character_width_center = int((width_max+7)/2)


        if(height_half > width_half):
            radius = height_half
        else:
            radius = width_half
        
        Character_Descriptor = Character(self.label_count, radius)
    
        for i in range(1, self.label_count + 1):
            character_img = np.zeros((height_max + 7, width_max + 7, 1), np.uint8)
            character_color = np.zeros((height_max + 7, width_max + 7, 3), np.uint8)
            height_center = int((self.label_shape[i][0] + self.label_shape[i][1]) / 2)
            width_center = int((self.label_shape[i][2] + self.label_shape[i][3]) / 2)
            origin_height = height_center - height_half - 3
            origin_width = width_center - width_half - 3
            #print 'loop m : ' + str(origin_height) + ' to ' + str(height_center + height_half + 4)
            #print 'loop n : ' + str(origin_width) + ' to ' + str(width_center + width_half + 4)

            if (origin_height < 0):
                origin_height = 0

            if (origin_width < 0):
                origin_width = 0

            if height_center + height_half + 4 < self.height: 
                height_upper = height_center + height_half + 4
            else:
                height_upper = self.height

            if width_center + width_half + 4 < self.width:
                width_upper = width_center + width_half + 4
            else:
                width_upper = self.width
            
            for m in range(origin_height, height_upper):
                for n in range(origin_width, width_upper):
                    #print m, n
                    #print 'size is : ' + str(len(self.label_record)) + ' and ' + str(len(self.label_record[0])) 
                    if(self.label_record[m][n] == i):
                        character_img[m - origin_height][n - origin_width] = 0
                        character_color[m - origin_height][n - origin_width] = self.image[m][n]
                    else:
                        character_img[m - origin_height][n - origin_width] = 255
                        character_color[m - origin_height][n - origin_width] = [255, 255, 255]

            # use harris to find corner
            Response = Harris(character_img, 1)
            Response = Response.get_harris_image()

            corners, corner_num = self.get_corners(Response, int(height_max + 7), int(width_max + 7))
            character_corner = character_color
        
            for k in range(corner_num):
                response, height_c, width_c = corners[k]

                cv2.circle(character_corner,(width_c,height_c),2,(255,0,0),2)
            cv2.imwrite("Output/image" + str(self.image_count) + "/Characters_corner/" + str(i) + ".jpg", character_corner)
            print "Output/image" + str(self.image_count) + "/Characters_corner/" + str(i) + ".jpg"
        
            Angles = []
            Arc_length = []
        
            if(corner_num == 0 or corner_num == 1):
                arc_length = 2*np.pi*radius
                Arc_length.append(arc_length)
                Character_Descriptor.Arc_length.append(Arc_length)
                Character_Descriptor.image.append(character_img)
                continue
        
            for m in range(corner_num):
                response, height_corner, width_corner = corners[m]
                vector1[0] = height_corner - character_height_center
                vector1[1] = width_corner - character_width_center
                cosine = np.dot(vector0, vector1.T)/np.linalg.norm(vector1)
                radian = np.arccos(cosine)
                if(height_corner >  character_height_center):
                    radian = 2*np.pi - radian
                arc_length = radius*radian
                Angles.append((radian,height_corner,width_corner,arc_length))


            number = corner_num

            if len(Angles) < number:
                number = len(Angles)

            for m in range(number):
                for n in range(m + 1, number):
                    print 'hihi : ' + str(m) + " ; " + str(n)
                    if(Angles[m][0] > Angles[n][0]):
                        temp = Angles[n]
                        Angles[n] = Angles[m]
                        Angles[m] = temp
                    elif(Angles[m][0] == Angles[n][0]):
                        print 'remove'
                        #Angles.remove(Angles[n])
                        number -= 1
                        n -= 1

            for m in range(number - 1):
                arc_length = Angles[m + 1][3] - Angles[m][3]
                Arc_length.append(arc_length)
            arc_length = 2 * np.pi * radius - Angles[number - 2][3] + Angles[0][3]
            Arc_length.append(arc_length)
            print "Arc length {}".format(Arc_length)
            Character_Descriptor.Arc_length.append(Arc_length)
            Character_Descriptor.image.append(character_img)
        
        return Character_Descriptor

    def get_corners(self, Response, height, width):
        count = 0
        corners = []

        for j in range(height):
            for i in range(width):
                if(Response[j][i] > 10e15):
                    corners.append((Response[j][i],j,i))
                    count = count + 1
        corner_count = count
        if(count > 5):
            for i in range(corner_count - 5):
                corner_min = corners[0]
                corner_remove = 0
                for j in range(1, count):
                    if(corners[j][0] < corner_min[0]):
                        corner_min = corners[j]
                        corner_remove = j
                corners.remove(corners[corner_remove])
                count -= 1
      
        return corners, len(corners)
