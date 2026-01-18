import pygame

class DualShock:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.js = pygame.joystick.Joystick(0)
        self.js.init()

    def read(self):
        pygame.event.pump()
        lx = self.js.get_axis(0)
        ly = -self.js.get_axis(1)  # forward+
        rx = self.js.get_axis(2)
        return lx, ly, rx
