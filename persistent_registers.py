import paramiko
from time import sleep
import pigpio
from os.path import exists

def main():
	user =  "root"
	password = "woot"
	host = ""
	localpi = pigpio.pi()

	power_pin = 0

	serial_passes = 0
	plugin_passes = 0
	serial_fails = 0
	plugin_fails = 0

	A_firmware = ""
	B_firmware = ""

	initial_run = True
	initial_plugins = 0
	current_plugins = 0
	trial_number = 0
	plugin_trial_number = 0
	returned_serial = ""

	#while A_firmware and B_firmware == "":
		#A_firmware = input("What's the normal firmware's git hash?:\n")
		#B_firmware = input("What's the alternate firmware's git hash?: \n")

	while host == "":

		host = input("What's the IP?\n")
		expected_serial = input("and what's the serial?\n")
		power_pin = int(input("What's the power pin to use?"))

	filename = (expected_serial + "logfile.txt")
	
	if exists(filename) != True:
		print("Creating a logfile...")
		target = open(filename, 'x')
		target.close()
		print("Logfile created!")

	elif exists(filename) == True:
		print("Appending to existing logfile.")

	while True:

		print("Trial #", trial_number)

		# Boot the oven


		localpi.write(power_pin, 1)
	# Wait for a ssh connection
		connected = False
		while connected == False:
			try:
				ssh = paramiko.SSHClient()
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				ssh.connect(host, username = user, password = password)
				print("connected!")
				connected = True



			except:
				sleep(1)
				print("connecting...")

	# When connected, query the serial number and plug in events.

		returned_serial = check_serial(host)
		print("the serial is", returned_serial)

			#read the plugins
		current_plugins = check_plugins(host)
		print("the plugins are ", current_plugins)

	# If this is the initial run of the test, store the plug in events.

		if initial_run == True:
			print("this is an initial run of this test.\n")
			initial_plugins = current_plugins
			initial_run = False
	# Wait 1 minute.

		for i in range(1,90):
			print(i, "...")
			sleep(1)
	# On five second intervals, query the serial number and plug in events. Do this 6 times

		for i in range(1,2):
			print("Check #", i, "checking the serial...")
			check = check_serial(host)

			if check in expected_serial:
				print("The serial is correct")
				serial_passes += 1

	# If the serial is corrupted, fail
			elif check != expected_serial:
				print(check)
				print("Wrong serial! fail:(")
				serial_fails += 1
	# If the serial is blank, fail
			elif check == "":
				print("no serial. Fail:(")
				serial_fails += 1
	# On the 6th query, check the plugin events is correct.
			print("checking plugins...")
			check = check_plugins(host)
			
			sleep(5)


	# If plugin is incorrect, fail and restart the initial plugin events check
			if check == (initial_plugins +	plugin_trial_number):
				print("there are ", check, "plugins, which is expected. Pass!")
				plugin_passes += 1

			elif check != (initial_plugins + plugin_trial_number):
				print("there are ", check, "plugins. There should be: ", initial_plugins +	plugin_trial_number, "fail:(")
				plugin_fails += 1
				
				#reset the plugins 
				
				initial_plugins = 0
				plugin_trial_number = 0
				initial_run = True
				
			else:
				print("whoops. Check the initial plugin stuff")


	# Close the SSH connection
		ssh.close()
	# Print test conditions
		serial = "serial fails: ", serial_fails, "and passes: ", serial_passes 
		print(serial)
		plugins = "plugin fails: ", plugin_fails, "and passes: ", plugin_passes
		print(plugins)
	# Goto 1
		trial_number += 1
		print("Turning off the oven!")
		localpi.write(power_pin, 1)
		localpi.write(power_pin, 0)
		
		print("logging results...")
		log_file = open(filename, 'a+')
		log_file.write(str(serial))
		log_file.write(str(plugins))
		log_file.write("\n")
		log_file.close()

		
		
		for i in range(1,15):
			print(i, "...")
			sleep(1)

def check_serial(host):
	
	user =  "root"
	password = "woot"

	host = host
	connected = False
	while connected == False:
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(host, username = user, password = password)
			print("connected!")
			connected = True



		except:
			sleep(1)
			print("connecting...")
	
	
	stdin, stdout, stderr = ssh.exec_command("echo 'serial' | nc -q 1 -U /var/run/bosh")
	output = stdout.readlines()
	#print(output)

	output = output[2]
	#print(output)

	output = output[35:49]
	print(output)
	ssh.close()

	return(output)

def check_plugins(host):

	user =  "root"
	password = "woot"

	host = host
	connected = False
	while connected == False:
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(host, username = user, password = password)
			print("connected!")
			connected = True



		except:
			sleep(1)
			print("connecting...")

	good_output = False
	
	while good_output == False:


		stdin, stdout, stderr = ssh.exec_command("echo 'reg 262' | nc -q 2 -U /var/run/bosh")
		output = stdout.readlines()
		#print(output)

		output = output[3]
		#print(output)

		output = output[38:46]
		print(output, type(output)
		if "meout" in output:
			good_output = False
			print(output)
			
		else:
			print(output)
			good_output = True

	clear_leading = output[0]
	while clear_leading == 0:
		output = output[1:]
		clear_leading = output[0]
		
	ssh.close()
	return(int(output))
	


main()
