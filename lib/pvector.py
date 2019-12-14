from kivy.vector import Vector
import math

class PVector(Vector):

    def __init__(self, *args):
        super(PVector, self).__init__(*args)

    def limit(self, val):
        if self.length() > val:
            self[0], self[1] = self.normalize() * val

    @staticmethod
    def acc_to_rad(self, acc):
        return PVector(list(map(math.cos, acc * math.pi / 180)))