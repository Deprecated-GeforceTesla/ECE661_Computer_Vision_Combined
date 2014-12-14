import sys
import math as m
sys.path.append("imports/")
from YYL_Homo_Matrix import Homo_Matrix as Homography
import YYL_Image_Coord_Op as Image_op
sys.path.append("include/Imaging-1.1.7/PIL")
try:
    import Image
except:
    print 'Image library not found, using library from imports folder'
    print 'make sure you have jpeg decoder that works with PIL'
    sys.path.append("include/Imaging-1.1.7/PIL")
    import Image

class HW_problem2(object):

    def __init__(self):
        '''Initialize the required resources for problem 2
        We transform the picture behind the human face
        '''
        self.with_face = 0
        self.setup_coord_for_problem2()
        self.setup_image()
        self.process_image(self.with_face)
        self.output_processed_image()

    def setup_coord_for_problem2(self):
        '''Initialize the coordinates to apply the transform
        '''
        # The coordinates of image points that we apply image towards
        point_a = {'x': 485, 'y': 201}
        point_b = {'x': 567, 'y': 211}
        point_c = {'x': 485, 'y': 422}
        point_d = {'x': 566, 'y': 407}

        point_ab = {'x': 526, 'y': 206}
        point_cd = {'x': 526, 'y': 415}
        point_ac = {'x': 485, 'y': 312}
        point_bd = {'x': 567, 'y': 309}

        # World coordinates, which refers to world plane coordinate
        wld_pt_a = {'x': 0, 'y': 0}
        wld_pt_b = {'x': 500, 'y': 0}
        wld_pt_c = {'x': 0, 'y': 508}
        wld_pt_d = {'x': 500, 'y': 508}

        wld_pt_ab = {'x': 250, 'y': 0}
        wld_pt_cd = {'x': 250, 'y': 508}
        wld_pt_ac = {'x': 0, 'y': 254}
        wld_pt_bd = {'x': 500, 'y': 254}

        self.amount_of_points = int(raw_input("How many points? (4-8): "))
        self.with_face = int(raw_input("Picture only? 1-yes, 0-no: "))

        self.world_plane = self.group_four_points(wld_pt_a, wld_pt_b,
                                                  wld_pt_c, wld_pt_d)

        self.image_plane = self.group_four_points(point_a, point_b,
                                                  point_c, point_d)

        self.world_plane += self.group_four_points(wld_pt_ab, wld_pt_cd,
                                                  wld_pt_ac, wld_pt_bd)

        self.image_plane += self.group_four_points(point_ab, point_cd,
                                                  point_ac, point_bd)

    def group_four_points(self, a, b, c, d):
        '''Group the points in a plane together
        @param a Point a
        @param b Point b
        @param c Point c
        @param d Point d
        @return a list of four points
        '''
        group_pts = []
        group_pts.append(a)
        group_pts.append(b)
        group_pts.append(c)
        group_pts.append(d)
        return group_pts

    def setup_image(self):
        '''Setup the background images
        '''
        print 'Setting up image...'
        self.world_pic = Image.open("input/Audrey.jpg")
        self.image_pic = Image.open("input/Frame.jpg")

        self.image_width, self.image_height =  self.world_pic.size

        self.output_image = Image.new("RGB", (self.image_width,
                                              self.image_height))

        for i in range(self.image_height):
            for n in range(self.image_width):
                color = self.world_pic.getpixel((n,i))
                self.output_image.putpixel((n,i), color)

    def process_image(self, option=0):
        '''Apply the transformation of image required by the problem
        @param option 0 to show picture behind face. 1 to show only  picture
        '''
        print 'Processing image...'
        homography_matrix = Homography(self.world_plane, self.image_plane,
                                       self.amount_of_points)

        homography_matrix = homography_matrix.get_homography_matrix()
        width, height = self.world_pic.size
        for i in range(height):
            for n in range(width):
                location = Image_op.convert_plane_pt(n, i, homography_matrix)
                x = float(location['x'])
                y = float(location['y'])
                a, b, c = self.world_pic.getpixel((n,i))
                if int(a) > 240 and int(b) > 240 and int(c) > 240:
                    color1 = self.image_pic.getpixel((int(x+1), int(y+1)))
                    c1 = (x - int(x)) * (y - int(y))
                    color2 = self.image_pic.getpixel((int(x+1),
                                                          int(y)))
                    c2 = (x - int(x)) * (int(y+1) - y)
                    color3 = self.image_pic.getpixel((int(x),
                                                          int(y+1)))
                    c3 = (int(x+1) - x) * (y - int(y))
                    color4 = self.image_pic.getpixel((int(x),
                                                          int(y)))
                    c4 = (int(x+1) - x) * (int(y+1) - y)
                    col1 = tuple(c1 * col for col in color1)
                    col2 = tuple(c2 * col for col in color2)
                    col3 = tuple(c3 * col for col in color3)
                    col4 = tuple(c4 * col for col in color4)
                    color = Image_op.find_sum_pixel(col1, col2,
                                                        col3, col4)
                    self.output_image.putpixel((n,i), color)
                else:
                    if option == 1:
                        color1 = self.image_pic.getpixel((int(x+1), int(y+1)))
                        c1 = (x - int(x)) * (y - int(y))
                        color2 = self.image_pic.getpixel((int(x+1),
                                                          int(y)))
                        c2 = (x - int(x)) * (int(y+1) - y)
                        color3 = self.image_pic.getpixel((int(x),
                                                          int(y+1)))
                        c3 = (int(x+1) - x) * (y - int(y))
                        color4 = self.image_pic.getpixel((int(x),
                                                          int(y)))
                        c4 = (int(x+1) - x) * (int(y+1) - y)
                        col1 = tuple(c1 * col for col in color1)
                        col2 = tuple(c2 * col for col in color2)
                        col3 = tuple(c3 * col for col in color3)
                        col4 = tuple(c4 * col for col in color4)
                        color = Image_op.find_sum_pixel(col1, col2,
                                                        col3, col4)
                        self.output_image.putpixel((n,i), color)


    def output_processed_image(self):
        '''Output the processed image to a jpg file
        '''
        self.output_image.save("output/output_image_problem2.jpg", "JPEG")

if __name__ == '__main__':
    temp = HW_problem2()
