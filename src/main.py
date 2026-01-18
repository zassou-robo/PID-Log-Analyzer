from input.dualshock import DualShock
from control.mecanum import Mecanum
from sim.viz import Viz
import time

def main():
    pad = DualShock()
    mech = Mecanum()
    viz = Viz()

    mode = "mecanum"

    x = 0; y = 0; theta = 0
    dt = 0.02

    while True:
        lx, ly, rx = pad.read()

        wheels = mech.inverse(lx, ly, rx)
        theta += rx * dt
        x += lx * dt
        y += ly * dt

        viz.draw(x, y, theta, wheels, mode)
        time.sleep(dt)

if __name__ == "__main__":
    main()
