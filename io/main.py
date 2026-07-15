import argparse
from dorna2 import Dorna

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--Host", default=None)
    parser.add_argument(
        "--OutputSetting",
        nargs="+",
        type=int,
        default=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        help="Space-separated 0/1 values, one per output pin (max 16).",
    )
    args = parser.parse_args()

    output_setting = args.OutputSetting

    robot = Dorna()

    # connect
    connected = robot.connect(args.Host) if args.Host else robot.connect()
    if connected:
        for i in range(min(len(output_setting), 16)):
            robot.set_output(i, output_setting[i])
    robot.close()