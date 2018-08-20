import paramiko
import scp
import datetime
import subprocess
import pigpio

from time import sleep
from gpiozero import LED
from os.path import exists

test_list = [WROD_test]

def WROD_test(IP_address, power_pin, button_pin):

	IP_address = host
	power_pin_relay = LED(power_pin)
	button_on = pigpio.set_servo_pulsewidth(button_pin, 1000)
	button_off = pigpio.set_servo_pulsewidth(button_pin, 1500)

# TESTING

	power_pin_relay.off()
	sleep(3)
	power_pin_relay.on()

	return("PASS")




def main():
	
	passes = 0
	fails = 0

	button_pin = 0
	power_pin = 0
	IP_address = ""

	while test_to_run != "quit" or "QUIT" or "q" or "Q":

		print(test_list, "\n")

		test_to_run = input("What test should I run?\n Type Q to quit.\n")
		print(test_list, "\n")

		if test_to_run == WROD_test:
			break





	times_to_run = input("How many times should I run this test?\n")
	
	if test_to_run == WROD_test:
		print("This test must be run on a relay of sufficient amperage.")
		print("Ignoring this warning is REALLY GODDAMN DANGEROUS.")
		power_pin = int(input("Type the power relay pin here:"))
		button_pin = int(input("Type the button servo pin here:"))
		IP_address = input("Type the oven's IP IP_address here:")
		main_relay = LED(power_pin)

		for i in range(1, times_to_run + 1):
			print("Running test WROD test, trial: ", i, "of ", times_to_run, "\n")
			result = WROD_test(IP_address, power_pin, button_pin)

			if result == "PASS":
				passes += 1
				print("Pass!")

			elif result == "FAIL":
				fails += 1
				print("Fail...")

			else:
				print("Whoops!")

				


main()
