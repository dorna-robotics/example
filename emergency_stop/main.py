"""
check specific input to turn on or off
after that release the alarm
this is how you call the function
sudo python3 main.py in0 1
"""
from dorna2 import Dorna
import asyncio
import sys

# halt the robot and activate the alarm state when "out0" gets to 1
async def emergency_event(msg, union, dorna_robot, input_key, state):
	if input_key in msg and msg[input_key] == state:
		# change the robot state to alarm to make sure that the robot ignores all the future commands
		dorna_robot.set_alarm(1)

def main(robot, input_key, state):

	# register an stop function
	robot.add_event(target=emergency_event, kwargs={"dorna_robot": robot, "input_key": input_key, "state":state})

	# motion loop
	while True:
		time.sleep(1)

if __name__ == '__main__':
	# Access the variables passed from CMD
	input_key = sys.argv[1]
	state = int(sys.argv[2])

	ip = "localhost"
	robot = Dorna()

	# connect to the robot
	if robot.connect(ip):
		main(robot, input_key, state)
	
	# close the connection
	robot.close()