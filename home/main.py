"""
sudo python3 main.py --Index 5 --Host 192.168.254.189 --Val 0 --Dir -1
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
class Home(object):
    """docstring for Home"""
    def __init__(self, robot=None, index=5, val=0, direction=1, config=config):
        super(Home, self).__init__()
        self.robot = robot
        self.index = index
        self.val = val
        self.direction = direction
        self.config = config
    
    def begin(self):
        # disable alarm
        self.robot.set_alarm(0)

        # get initial pid
        self.pid_init = self.robot.get_pid(self.index)
        self.robot.log("pid_init: "+ str(self.pid_init))

        # activate motor, pid
        id = 2000000+10*self.index # 0
        if any([
            self.robot.set_motor(1) != 2, 
            self.robot.set_pid(self.index, self.config["pid"][0], self.config["pid"][1], self.config["pid"][2], self.config["pid"][3], self.config["pid"][4], id=id ) != 2 ,
            ]):
            # error happened
            return 0
        pid_new = self.robot.get_pid(self.index)
        self.robot.log("pid_new: "+ str(pid_new))
        return 1


    def start(self):
        # begin
        if not self.begin():
            return 0

        # motion
        id = 2000000+10*self.index+1

        # assign joint
        joint = "j"+str(int(self.index))
        # move in the given direction with the given speed
        arg = {"vel": self.config["vel_forward"], "rel":1, joint: self.config["forward"] * self.direction, "id": id}  
        if self.robot.jmove(**arg) >= 0:
            # error happened
            return 0             

        # alarm happened
        # sleep at alarm
        time.sleep(0.2)

        # clear the alarm
        id += 1 # 2
        if self.robot.set_alarm(0, id=id) != 2:
            # error happened
            return 0

        # reset thr and dur
        id += 1 # 3
        if self.robot.set_pid(self.index, p=None, i=None, d=None, threshold=self.pid_init[3], durration=self.pid_init[4], id=id) != 2:
            # error happened
            return 0
        
        for i in range(self.config["trigger_count"]):
            # move backward
            arg = {"timeout": 0, "vel": self.config["vel_backward"], "rel":1, joint: self.config["backward"] * self.direction}  
            self.robot.jmove(**arg) # move toward the homing direction until the alarm

            # set the probe
            id += 1 # 4
            iprobe = self.robot.iprobe(self.index, self.config["iprobe_val"], id=id) # wait for the input trigger
            
            # halt
            id += 1 # 5
            if self.robot.halt(self.config["halt_accel"], id=id) != 2:
                # error happened
                return 0
            
        time.sleep(1)

        # set joint
        joint_assignment = self.val + self.robot.val(joint) - iprobe[self.index]
        id += 1 # 6
        if self.robot.set_joint(self.index, joint_assignment, id=id) != 2:
            # error happened
            return 0

        # joint move

        return 1

    def end(self, success):
        if not success:
            id = 2000000+10*self.index+7 # 7
        else:
             id = 12 # 12   
        
        # disable alarm
        self.robot.set_alarm(0, id=id)
        
        # set to initial pid
        id += 1 # 8
        self.robot.set_pid(self.index, self.pid_init[0], self.pid_init[1], self.pid_init[2], self.pid_init[3], self.pid_init[4], id=id) 

        pid_end = self.robot.get_pid(self.index)
        self.robot.log("pid_end: "+ str(pid_end))


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
    if robot.connect(host):
        # connected
        robot.log("connected")
        
        for k in range(1):
            home = Home(robot, index, val, direction, config["j"+ str(index)])
            rtn = home.start()
            home.end(rtn)
    
    # close
    robot.close()
    