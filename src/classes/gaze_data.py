class GazeData:

    def __init__(self, gaze, time, height):
        self.gaze = gaze
        self.time = time

    def get_gaze(self):
        return self.gaze

    def get_time(self):
        return self.time

    def get_height(self):
        return self.height

    def set_gaze(self, gaze):
        self.gaze = gaze

    def set_time(self, time):
        self.time = time

    def set_height(self, height):
        self.height = height

    def to_string(self):
        return "Gaze: " + str(self.gaze) + " Time: " + str(self.time) + " Height: " + str(self.height)
