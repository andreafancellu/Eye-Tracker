class FaceAll:

    def __init__(self, pixel, time):
        self.pixel = pixel
        self.time = time

    def get_pixel(self):
        return self.pixel

    def get_time(self):
        return self.time

    def to_string(self):
        return "pixel: " + str(self.pixel) + " time: " + str(self.time)


class Face:

    def __init__(self, right, left, up, down, time):
        self.right = right
        self.left = left
        self.up = up
        self.down = down
        self.time = time

    def get_right(self):
        return self.right

    def get_left(self):
        return self.left

    def get_up(self):
        return self.up

    def get_down(self):
        return self.down

    def get_time(self):
        return self.time

    def to_string(self):
        return "right: " + str(self.right) + ", left: " + str(self.left) + ", up: " + str(self.up) + ", down: " + str(self.down) + ", time: " + str(self.time)