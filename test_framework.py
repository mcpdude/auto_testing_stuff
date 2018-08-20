import paramiko
import datetime
import subprocess
from time import sleep
from gpiozero import LED
from os.path import exists


#Tests should be added here. A test should always return a result of either PASS, FAIL or INVALID. Further logging should be done
#within the test. The main wrapper records the oven serial, the name of the test, whether it passed, and it's P/F rate.
tests = {
	driver_test, # tests whether the ov5640.ko creates the /dev/video0 directory
	test_test #tests the functionality of the framework
}

ovens = {}

def test_test(oven_pin, times_to_run):
	relay = LED(oven_pin)
	relay.on()
	sleep(5)
	relay.off()
	return("PASS")

def driver_test(host, username, password, oven_pin):

	oven_relay = LED.(oven_pin)
    oven_relay.on()
    connected = False
    while connected == False:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username = user, password = password)
            print("connected!")
            connected = True
            sleep(10)
            print('running command')
            stdin, stdout, stderr = ssh.exec_command(camera_check)
            out_put = stdout.readlines()
            print(out_put)

            if '/dev/ttyS2\n' in out_put:
                print('not insane')

                if '/dev/video0\n' in out_put:
                    print("Pass!")

                    passes += 1


                else:
                    print("Fail :(")
                    fails += 1

            else:
                print('invalid result')
	

def main():

	command = ""

	print("This program will run tests on ovens if run from within a properly configured raspbery pi.")
	print("Would you like to add a test (RUN_TEST) \n add a oven to test (ADD_OVEN) \n start a test (START_TEST) \n or quit?(QUIT)\n")
	command = input("type here>")

	if command = ADD_OVEN:
		oven_to_add = ""
		while oven_to_add != "DONE":
		print("What oven should I add?")
		oven_to_add = input("Type a pin number here, or DONE if you're finished adding ovens.")
		if oven_to_add == "DONE":
			break
		elif isinstance(oven_to_add, int) and oven_to_add > 0:
			relay = LED(oven_to_add)
			relay.on()
			ovens[oven_to_add] = input("What's the IP address?")
			print(ovens[oven_to_add])
			relay.off()


	if command == "RUN_TEST":
		print("What test would you like to add?")
		print(available_tests)
		test_to_run = input("Type the test here:")
		if test_to_add in available_tests:
			print("What oven would you like to run it on?")

			while oven_to_use != "DONE":
				oven_to_use = input("Type the oven pin here, or ALL for all ovens, and DONE when you're finished adding ovens:")
				if oven_to_use == "ALL":
					print("This doesn't work yet :(")

				if oven_to_use == "DONE":
					break

			if isinstance(oven_to_use, int) == True:
				if oven_to_use in ovens:

					print("How many times should I run it?")
					times_to_run = input("Give a positive number here.")
					times_run = 0

					while times_run <= times_to_run:
						result = test_to_run()
						if result == "PASS":
							print("Pass!")
							passes += 1




