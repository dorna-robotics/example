"""
sudo python3 home.py -i 5 -p 10.0.0.4
"""
from dorna2 import Dorna
import json
from config import config
import time
import argparse

"""
id starts from 2,000,000
homing process for joint i starts
2,000,0i0: set pid
2,000,0i1: alarm motion
2,000,0i2: clear alarm
2,000,0i3: reset pid
2,000,0i4: move backwards and set iprobe
2,000,0i5: halt
2,000,0i6: joint assignment
2,000,0i7: error, clear alarm
2,000,0i8: error, reset pid 
"""
def home(robot, index, val, direction, thr, dur, **kwargs):
    # activate the motors
    if robot.set_motor(1) != 2:
        # error happened
        return home_error_handling(robot, index, thr, dur)     
    
    # set threshold
    id = 2000000+10*index # 0
    if robot.set_err_thr(10) != 2 or robot.set_err_dur(5, id=id) != 2:
        # error happened
        return home_error_handling(robot, index, thr, dur) 
    
    print("after: ",robot.get_err_thr(), robot.get_err_dur())
    # motion
    id += 1 # 1
    joint = "j"+str(index)
    # move in the given direction with the given speed
    arg = {"vel": kwargs["vel_forward"], "rel":1, joint: kwargs["forward"] * direction, "id": id}  
    if robot.jmove(**arg) >= 0:
        # error happened
        return home_error_handling(robot, index, thr, dur) 

    # sleep at alarm
    time.sleep(0.2)

    # clear the alarm
    id += 1 # 2
    if robot.set_alarm(0, id=id) != 2:
        # error happened
        return home_error_handling(robot, index, thr, dur)

    # reset pid
    id += 1 # 3
    if robot.set_err_thr(thr) !=2 or robot.set_err_dur(dur, id=id) !=2:
        # error happened
        return home_error_handling(robot, index) 
    
    for i in range(kwargs["trigger_count"]):
        # move backward
        arg = {"timeout": 0, "vel": kwargs["vel_backward"], "rel":1, joint: kwargs["backward"] * direction}  
        robot.jmove(**arg) # move toward the homing direction until the alarm

        # set the probe
        id += 1 # 4
        iprobe = robot.iprobe(index, kwargs["iprobe_val"], id=id) # wait for the input trigger
        
        # halt
        id += 1 # 5
        if robot.halt(kwargs["halt_accel"], id=id) != 2:
            # error happened
            return home_error_handling(robot, index, thr, dur)
        
    time.sleep(1)

    # set joint
    joint_assignment = val + robot.val(joint) - iprobe[index]
    id += 1 # 6
    if robot.set_joint(index, joint_assignment, id=id) != 2:
        # error happened
        return home_error_handling(robot, index, thr, dur)

    return True


def home_error_handling(robot, index, thr, dur):
    id = 2000000+10*index+7 # 7
    robot.set_alarm(0, id=id)
    id += 1 # 8
    robot.set_err_thr(thr)
    robot.set_err_dur(dur, id=id)

if __name__ == '__main__':
    # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("--Index")
    parser.add_argument("--Host")
    parser.add_argument("--Value")
    parser.add_argument("--Dir")
    # Read arguments from command line
    args = parser.parse_args()
    
    # assign index
    index = int(args.Index)        
    host = args.Host
    val = float(args.Value)
    direction = float(args.Dir)

    robot = Dorna()
    robot.connect(host)

    # original thr, dur
    thr = robot.get_err_thr()
    dur = robot.get_err_dur()
    p, i, d = robot.get_pid(index)
    robot.log("initial_pid" + str([p, i, d]))
    robot.set_pid(index, 0, 0, 0)
    robot.log("connected")
    for k in range(1):
        home(robot, index, val, direction, thr, dur, **config["j"+ str(index)])
        time.sleep(1)
    
    print("before: ", robot.get_err_thr(), robot.get_err_dur())
    robot.set_pid(index, p, i, d)
    robot.log("final_pid" + str(robot.get_pid(index)))
    robot.close()
    