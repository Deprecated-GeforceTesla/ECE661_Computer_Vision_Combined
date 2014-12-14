import sys
sys.path.append("imports/")
from YYL_Homo_Matrix import Homo_Matrix as Homography
import YYL_Image_Coord_Op as Image_op
try:
    import Image
except:
    print 'Image library not found, using library from imports folder'
    print 'make sure you have jpeg decoder that works with PIL'
    sys.path.append("include/Imaging-1.1.7/PIL")
    import Image 

class HW_problem1(object):

    def __init__(self):
        '''Initialize the required resources for problem 1
        We transform the human face to the door
        '''
        self.setup_coord_for_problem1()
        self.setup_image()
        self.process_image()
        self.output_processed_image()

    def setup_coord_for_problem1(self):
        '''Initialize the coordinates to apply the transform
        '''
        # The coordinates of image points that we apply image towards
        point_p = {'x': 187, 'y': 152}
        point_q = {'x': 346, 'y': 176}
        point_r = {'x': 185, 'y': 463}
        point_s = {'x': 344, 'y': 434}

        point_pq = {'x': 267, 'y': 164}
        point_rs = {'x': 265, 'y': 449}
        point_pr = {'x': 186, 'y': 308}
        point_qs = {'x': 345, 'y': 305}

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
 
        self.world_plane = self.group_four_points(wld_pt_a, wld_pt_b,
                                                  wld_pt_c, wld_pt_d)

        self.image_plane = self.group_four_points(point_p, point_q,
                                                  point_r, point_s)

        self.world_plane += self.group_four_points(wld_pt_ab, wld_pt_cd,
                                                  wld_pt_ac, wld_pt_bd)


        self.image_plane += self.group_four_points(point_pq, point_rs,
                                                  point_pr, point_qs)

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

        self.image_width, self.image_height =  self.image_pic.size

        self.output_image = Image.new("RGB", (self.image_width,
                                              self.image_height))

        for i in range(self.image_height):
            for n in range(self.image_width):
                color = self.image_pic.getpixel((n,i))
                self.output_image.putpixel((n,i), color)

    def process_image(self):
        '''Apply the transformation of image required by the problem
        '''
        print 'Processing image...'
        homography_matrix = Homography(self.world_plane, self.image_plane,
                                       self.amount_of_points)

        homography_matrix = homography_matrix.get_homography_matrix()

        width, height = self.world_pic.size
        for i in range(height):
            for n in range(width):
                color = self.world_pic.getpixel((n,i))
                location = Image_op.convert_plane_pt(n, i, homography_matrix)
                self.output_image.putpixel((int(location['x']),
                                            int(location['y'])), color)

    def output_processed_image(self):
        '''Output the processed image to a jpg file
        '''
        self.output_image.save("output/output_image_problem1.jpg", "JPEG",
                               quality=80)

if __name__ == '__main__':
    temp = HW_problem1()
