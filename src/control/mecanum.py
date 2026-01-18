import numpy as np

class Mecanum:
    def __init__(self, wheel_base=0.3, track=0.3, wheel_radius=0.05):
        self.L = wheel_base
        self.W = track
        self.R = wheel_radius

    def inverse(self, vx, vy, omega):
        L = self.L
        W = self.W
        R = self.R

        w1 = (1/R) * (vx - vy - (L + W)*omega)
        w2 = (1/R) * (vx + vy + (L + W)*omega)
        w3 = (1/R) * (vx + vy - (L + W)*omega)
        w4 = (1/R) * (vx - vy + (L + W)*omega)

        return np.array([w1, w2, w3, w4])
