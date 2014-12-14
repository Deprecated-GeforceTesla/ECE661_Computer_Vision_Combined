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

class HW_problem4(object):

    def __init__(self):
        '''Initialize the required resources for problem 2
        We transform the picture behind the human face
        '''
        self.with_face = 0
        self.setup_coord_for_problem4()
        self.setup_image()
        self.apply_p2_to_p1()
        self.transform_to_world_coord()
        self.output_processed_image()

    def setup_coord_for_problem4(self):
        '''Initialize the coordinates to apply the transform
        '''
        # The coordinates of image points that we apply image towards
        point_a = {'x': 130, 'y': 41}
        point_b = {'x': 239, 'y': 33}
        point_c = {'x': 127, 'y': 336}
        point_d = {'x': 238, 'y': 346}

        point_ab = {'x': 185, 'y': 37}
        point_cd = {'x': 183, 'y': 341}
        point_ac = {'x': 129, 'y': 185}
        point_bd = {'x': 239, 'y': 190}

        # World coordinates, which refers to world plane coordinate
        wld_pt_a = {'x': 0, 'y': 0}
        wld_pt_b = {'x': 354, 'y': 0}
        wld_pt_c = {'x': 0, 'y': 310}
        wld_pt_d = {'x': 354, 'y': 310}

        wld_pt_ab = {'x': 177, 'y': 0}
        wld_pt_cd = {'x': 177, 'y': 310}
        wld_pt_ac = {'x': 0, 'y': 155}
        wld_pt_bd = {'x': 354, 'y': 155}

        #the door is around 2m high and 1m wide
        wld_coord_a = {'x': 0, 'y': 0}
        wld_coord_b = {'x': 100, 'y': 0}
        wld_coord_c = {'x': 0, 'y': 200}
        wld_coord_d = {'x': 100, 'y': 200}

        wld_coord_ab = {'x': 50, 'y': 0}
        wld_coord_cd = {'x': 50, 'y': 200}
        wld_coord_ac = {'x': 0, 'y': 100}
        wld_coord_bd = {'x': 100, 'y': 100}

        self.amount_of_points = 8

        self.world_plane = self.group_four_points(wld_pt_a, wld_pt_b,
                                                  wld_pt_c, wld_pt_d)

        self.image_plane = self.group_four_points(point_a, point_b,
                                                  point_c, point_d)

        self.world_plane += self.group_four_points(wld_pt_ab, wld_pt_cd,
                                                   wld_pt_ac, wld_pt_bd)

        self.image_plane += self.group_four_points(point_ab, point_cd,
                                                   point_ac, point_bd)

        self.world_coord = self.group_four_points(wld_coord_a, wld_coord_b,
                                                  wld_coord_c, wld_coord_d)

        self.world_coord += self.group_four_points(wld_coord_ab, wld_coord_cd,
                                                   wld_coord_ac, wld_coord_bd)



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
        # required to apply P2 solution back to graph
        self.world_pic = Image.open("input/P4_face.jpg")
        # use solution of P1 as base
        self.image_pic = Image.open("output/output_image_problem4_T1.jpg")

        self.image_width, self.image_height =  self.image_pic.size

        self.output_image = Image.new("RGB", (self.image_width,
                                              self.image_height))

        for i in range(self.image_height):
            for n in range(self.image_width):
                color = self.image_pic.getpixel((n,i))
                self.output_image.putpixel((n,i), color)

    def apply_p2_to_p1(self):
        '''Apply the transformation of output P2 back to p1 output
        @param option 0 to show picture behind face. 1 to show only  picture
        '''
        print 'Processing image...'
        homography_matrix = Homography(self.world_plane, self.image_plane,
                                       self.amount_of_points)

        homography_matrix = homography_matrix.get_homography_matrix()

        width, height = self.world_pic.size
        for i in range(height):
            for n in range(width):
                color = self.world_pic.getpixel((n,i))
                a, b, c = color
                if not (a > 253 and b > 253 and c > 253):
                    color = self.world_pic.getpixel((n,i))
                    location = Image_op.convert_plane_pt(n, i, homography_matrix)
                    self.output_image.putpixel((int(location['x']),
                                                int(location['y'])), color)

    def transform_to_world_coord(self):
        '''Apply the transformation of image to world coordinate
        '''
        print 'Final processing image...'
        homography_matrix = Homography(self.world_coord, self.image_plane,
                                       self.amount_of_points)
        homography_matrix_inv = Image_op.matrix_inverse(
            homography_matrix.get_homography_matrix())
        # Find boundry of axis
        x_bound = []
        y_bound = []
        # this is the boudry of the image that is about to be transformed
        a = [0, 0]
        b = [360, 0]
        c = [0, 360]
        d = [360, 360]
        location = Image_op.convert_plane_pt(a[0], a[1], homography_matrix_inv)
        x_bound.append(location['x'])
        y_bound.append(location['y'])
        location = Image_op.convert_plane_pt(b[0], b[1], homography_matrix_inv)
        x_bound.append(location['x'])
        y_bound.append(location['y'])
        location = Image_op.convert_plane_pt(c[0], c[1], homography_matrix_inv)
        x_bound.append(location['x'])
        y_bound.append(location['y'])
        location = Image_op.convert_plane_pt(d[0], d[1], homography_matrix_inv)
        x_bound.append(location['x'])
        y_bound.append(location['y'])
        x_min = int(min(x_bound))
        x_max = int(max(x_bound)) + 1
        y_min = int(min(y_bound))
        y_max = int(max(y_bound)) + 1
        # shrink image by 10 times
        out_width = (x_max - x_min)
        out_height = (y_max - y_min)
        self.real_output_image = Image.new("RGB", (out_width, out_height))
        #apply transformation
        width, height = self.output_image.size
        for i in range(height):
            for n in range(width):
                color = self.output_image.getpixel((n,i))
                location = Image_op.convert_plane_pt(n, i,
                                                     homography_matrix_inv)
                #it may start off as negative, so apply offsets
                target_x = (int(location['x']) - x_min)
                target_y = (int(location['y']) - y_min)
                self.real_output_image.putpixel((target_x,target_y), color)


    def output_processed_image(self):
        '''Output the processed image to a jpg file
        '''
        self.real_output_image.save("output/output_image_problem4_T3.jpg", "JPEG")

if __name__ == '__main__':
    temp = HW_problem4()
