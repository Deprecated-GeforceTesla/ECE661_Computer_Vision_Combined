class Descriptor():

    def __init__(self, x, y, x_rect, y_rect):
        self.x = x
        self.y = y
        self.x_rect = x_rect
        self.y_rect = y_rect
        self.match = -1
        self.score = -1
        self.point = -1
        self.neighbor = 0
