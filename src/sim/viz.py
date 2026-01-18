import matplotlib.pyplot as plt
import numpy as np

class Viz:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.robot_size = (0.4, 0.3)

    def draw(self, x=0, y=0, theta=0, wheels=None, mode="mecanum"):
        self.ax.cla()
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)

        w, h = self.robot_size
        c = np.array([x, y])
        R = np.array([[np.cos(theta), -np.sin(theta)],
                      [np.sin(theta), np.cos(theta)]])
        corners = np.array([[ w/2,  h/2],
                            [ w/2, -h/2],
                            [-w/2, -h/2],
                            [-w/2,  h/2]]).T
        rot = (R @ corners).T + c
        self.ax.plot(rot[:,0], rot[:,1], 'b-')

        self.ax.text(-0.9, 0.9, f"mode: {mode}")
        plt.pause(0.01)
