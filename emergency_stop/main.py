"""
check specific input to turn on or off
after that release the alarm
this is how you call the function
sudo python3 main.py in0 1
"""
from dorna2 import Dorna
import asyncio
import sys
import json

class Emergency(object):
	"""docstring for Emergency"""
	def __init__(self, key=None, state=None, enable=0):
		super(Emergency, self).__init__()
		self.key = key
		self.state = state
		self.enable = enable
		self.check = False

	def update(self, key, state, enable):
		self.key = key
		self.state = state
		self.enable = enable
		self.check = self.enable == 1 and self.key in ["in"+str(i) for in in range(16)] and self.state in [i for i in range(2)]


async def emergency_event(msg, union, dorna_robot, emergency):
	if emergency.check and emergency.key in msg and msg[key] == emergency.state:
		# change the robot state to alarm to make sure that the robot ignores all the future commands
		dorna_robot.set_alarm(1)

def main(robot, config_path, emergency):

	# register an stop function
	robot.add_event(target=emergency_event, kwargs={"dorna_robot": robot, "emergency": emergency})

	# motion loop
	while True:
		with open(config_path, 'r') as file:
			# Load the contents of the file
			data = json.load(file)


		# update 
		emergency.update(data["emergency"]["key"], data["emergency"]["state"], data["emergency"]["enable"])

		time.sleep(5)

if __name__ == '__main__':
	# Access the variables passed from CMD
	config_path = sys.argv[1]
	
	ip = "localhost"
	
	robot = Dorna()

	# connect to the robot
	if robot.connect(ip):
		main(robot, input_key, state)
	
	# close the connection
	robot.close()