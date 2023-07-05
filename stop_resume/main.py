from dorna2 import Dorna
import time

# end the process of all the running programs in program_list
def end_process_event(msg, union, pid_list, in_key, in_val):
	if in_key in msg and msg[in_key] == in_val:

def run_process_event():
	

def main(robot, file_list):
	# run all the programs
	for program in program_list:

	# create event
	robot.end_process_event(target=end_process_event, kwargs={"pid_list"})

	while True:
		time.sleep(1)

if __name__ == '__main__':
	# list of all the programs
	program_list = [""]
	
	# ip
	ip = "localhost"

	robot = Dorna()

	if robot.connect()
		main(robot, program_list)

	robot.close()



	import os

	# Specify the process ID (PID) of the process you want to kill
	pid = 12345  # Replace with the actual PID

	# Send the SIGKILL signal to terminate the process
	os.kill(pid, signal.SIGKILL)
