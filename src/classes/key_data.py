class KeyTime:

    def __init__(self, key, ms):
        self.key = key
        self.ms = ms

    def get_key(self):
        return self.key

    def get_ms(self):
        return self.ms

    def to_string(self):
        return "Key: " + str(self.key) + " Time: " + str(self.ms)

