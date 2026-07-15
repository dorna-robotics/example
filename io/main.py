from dorna2 import Dorna

if __name__ == '__main__':
    robot = Dorna()

    # connect
    if robot.connect():
        output_setting = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(min(len(output_setting), 16)):
            robot.set_output(i, output_setting[i])
    robot.close()