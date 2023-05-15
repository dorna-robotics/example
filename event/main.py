from dorna2 import Dorna
import asyncio

# halt the robot and activate the alarm state when "out0" gets to 1
async def stop_event(msg, union, dorna_robot, loop_stop):
	if "out0" in msg and msg["out0"] == 1:
		print("msg: ", msg)
		# instant stop
		dorna_robot.halt()

		# change the robot state to alarm to make sure that the robot ignores all the future commands
		dorna_robot.set_alarm(1)

		# exit the while loop of the main function
		loop_stop[0] = True


def main(robot):
	# init stop
	stop = [False]

	# register an stop function
	robot.add_event(target=stop_event, kwargs={"dorna_robot": robot, "loop_stop":stop})

	# motion loop
	while not stop[0]:
		print("motion forward")
		robot.jmove(rel=1, j0=10)

		print("motion reverse")
		robot.jmove(rel=1, j0=-10)

if __name__ == '__main__':
	ip = "localhost"
	robot = Dorna()

	# connect to the robot
	if robot.connect(ip):
		main(robot)
	
	# close the connection
	robot.close()