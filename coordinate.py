# For easy physical location (=position) access
class Coordinate2D:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    @property
    def x(self):
        return self.x

    @property
    def y(self):
        return self.y