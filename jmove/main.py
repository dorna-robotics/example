from dorna2 import Dorna

if __name__ == '__main__':
    robot = Dorna()

    # connect
    if robot.connect():
        robot.set_motor(1)
        while True:
            robot.jmove(rel=1, j0=10, vel=100, accel=500, jerk=2500)
            robot.jmove(rel=1, j0=-10)

    robot.close()