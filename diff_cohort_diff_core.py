import paramiko
import sys
from time import sleep

from datetime import datetime
from datetime import timedelta


password = "scabios4"
host ="brava.cloud"
user = "deploy"

ovend_first_hash = str(sys.argv[1])
#first_firmware = str(sys.argv[2])
ovend_second_hash = str(sys.argv[2])
#second_firmware = str(sys.argv[4])
trials = int(sys.argv[3])

oven_host = str(sys.argv[4])
oven_user = "root"
oven_PW = "woot"

#if str(sys.argv[1]) == "help":
#	print("1st arg: initial hash \n2nd arg: initial firmware\n 3rd arg: post hash \n4th arg: post firmware\n5th arg: trials to run \n6th arg: IP address ")

if str(sys.argv[1]) == "help":
	print("1st arg: initial hash \n2nd arg: post hash \n3rd arg: trials to run \n4th arg: IP address ")

def batman_runner(batman_command, IP_address, pass_criteria):
	sleep(5)
	oven_user = "root"
	oven_PW = "woot"

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	#connect to the oven, using the provided ip 
	ssh.connect(IP_address, username = oven_user, password = oven_PW)

	start_time_batman_update = datetime.now()
	elapsed = datetime.now() - start_time_batman_update
	timeout = False
	# since the system is locked out while updating, if the following doesn't return any values, try again till it does
	test_complete = False
	while test_complete == False:
		stdin, stdout, stderr = ssh.exec_command("script -c '/brava/app/core/test/batman -i /root/gordon.json -b /var/run/bambino -c <<< " + batman_command + " & sleep 1; pkill batman' output.txt")
		sleep(3)
		stdin, stdout, stderr = ssh.exec_command("cat /root/output.txt")
		output=stdout.readlines()  
		#print(output) 

		elapsed = datetime.now() - start_time_batman_update
		if elapsed > timedelta(minutes=3):
			print("Timed out on batman")
			timeout = True
			break

		# this tests to see if there's a response from batman
		if len(output) > 0:
			test_complete = True

		elif len(output) == 0:
			print("didn't get a response from bambino.")
		#cleans up the output so it doesn't show up again later
		stdin, stdout, stderr = ssh.exec_command("rm /root/output.txt")

	if(timeout == True):
		return False

	print("Looking for : ", pass_criteria)

	#checks the batman output for the correct hash in the ovend version
	for j in output:
		if pass_criteria in j:
			print(j)
			print("pass!")
			ssh.close()
			return(True)

	ssh.close()
	return(False)


def main():

	passes = 0
	fails = 0

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	#for i in range(1, trials+1):
	sleep(5)
	print('\n', "######################################################", '\n')
	print("beginning trial #", i)

	#start on a initial cohort
	print("Moving to auto_test cohort")
	#connect to the cohort system
	ssh.connect(host, username = user, password = password)
	#move the oven to the test cohort
	stdin, stdout, stderr  = ssh.exec_command("cohort-serial auto_test TWPT-95FP-NT00 ")
	output=stdout.readlines()
	print(output[-1])
	#close the connection
	ssh.close()

	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(oven_host, username = oven_user, password = oven_PW)
	#tell the oven to check and commit the old core package
	stdin, stdout, stderr  = ssh.exec_command('nc -U /var/run/bambino <<< "K1:36:S3:SETK1:24:S12:/ota/commandS5:check"')
	print("checking cohorts...")
	
	sleep(3)

	stdin, stdout, stderr = ssh.exec_command('nc -U /var/run/bambino <<< "K1:37:S3:SETK1:25:S12:/ota/commandS6:commit"')
	output=stdout.readlines()
	print("committing old cohorts...")

	sleep(13)

	print("committed old cohort...")
	ssh.close()
	
#		for k in range(0, 6):
	#check to see the old ovend version
	if batman_runner("check_ovend", oven_host, ovend_first_hash) == True:
		print("the oven is on the correct ovend version. Checking if there is update on the fw")

		start_time_fw_update = datetime.now()
		elapsed = datetime.now() - start_time_fw_update
		timeout = False

		#checking to see if the FW is updated
		while batman_runner("check_updateStat", oven_host, "check_updateStat 0") == False and \
			batman_runner("check_updateProgress", oven_host, "check_updateProgress 100") == False:
			#Worst case wait for 15 mins in total for lvmcu and hvmcu to be updated
			elapsed = datetime.now() - start_time_fw_update
			if elapsed > timedelta(minutes=15):
				timeout = True
				break
			print("waiting another 10 seconds for the fw update to finish...")
			sleep(10)
		
		if timeout == True:
			print("Timeout while updating the fw")
			fails += 1
			pass
		else:
			print("Time taken to update to the old fw is ", elapsed.total_seconds()/60)
			print("done updating the fw!")
		
		sleep(5)
		
#			print("the oven is on the correct ovend version. poking the oven to update now.")
#			batman_runner("set_updateEnableTrue", oven_host, "def_NOT_gonna_pass")
		#check the hvmcu and lvmcu versions
		if batman_runner("check_lvmcu", oven_host, ovend_first_hash) == True and \
			batman_runner("check_hvmcu", oven_host, ovend_first_hash) == True:
			print("The lvmcu and hvmcu versions match")
			print("The First Update is finished")
#				batman_runner("set_updateEnableFalse", oven_host, "def_NOT_gonna_pass")
		else:
			print("The lvmcu and hvmcu versions do not match")
			return False

	else:
		print("dang it, the old ovend version is not correct")
		return False
	
	sleep(10)
	#connect to the new cohort system
	print("Moving to auto_test2 cohort")
	ssh.connect(host, username = user, password = password)
	#move the oven to the test cohort
	stdin, stdout, stderr  = ssh.exec_command("cohort-serial auto_test2 TWPT-95FP-NT00 ")
	output=stdout.readlines()
	print(output[-1])
	#close the connection
	ssh.close()

	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(oven_host, username = oven_user, password = oven_PW)
	#tell the oven to check and commit the old core package
	stdin, stdout, stderr  = ssh.exec_command('nc -U /var/run/bambino <<< "K1:36:S3:SETK1:24:S12:/ota/commandS5:check"')
	print("checking cohorts...")
	
	sleep(3)

	stdin, stdout, stderr = ssh.exec_command('nc -U /var/run/bambino <<< "K1:37:S3:SETK1:25:S12:/ota/commandS6:commit"')
	output=stdout.readlines()
	print("committing new cohorts...")

	sleep(13)

	print("committed new cohort...")
	ssh.close()
	
#		for k in range(0, 6):
	#check to see the old ovend version
	if batman_runner("check_ovend", oven_host, ovend_second_hash) == True:
		print("the oven is on the correct ovend version. Checking if there is update on the fw")

		start_time_fw_update = datetime.now()
		elapsed = datetime.now() - start_time_fw_update
		timeout = False

		#checking to see if the FW is updated
		while batman_runner("check_updateStat", oven_host, "check_updateStat 0") == False and \
			batman_runner("check_updateProgress", oven_host, "check_updateProgress 100") == False:
			#Worst case wait for 15 mins in total for lvmcu and hvmcu to be updated
			elapsed = datetime.now() - start_time_fw_update
			if elapsed > timedelta(minutes=15):
				timeout = True
				break
			print("waiting another 10 seconds for the fw update to finish...")
			sleep(10)
		
		if timeout == True:
			print("Timeout while updating the fw")
			return False
		else:
			print("Time taken to update to the new fw is ", elapsed.total_seconds()/60)
			print("done updating the fw!")
		
		sleep(15)
#			print("the oven is on the correct ovend version. poking the oven to update now.")
#			batman_runner("set_updateEnableTrue", oven_host, "def_NOT_gonna_pass")
		if batman_runner("check_lvmcu", oven_host, ovend_second_hash) == True and \
			batman_runner("check_hvmcu", oven_host, ovend_second_hash) == True:
			print("The lvmcu and hvmcu versions match")
			print("The Secpond Update is finished")
			print("The test has PASSED!! Hurray")
			return True
			
		else:
			print("The lvmcu and hvmcu versions do not match")
			return False

	else:
		print("dang it, the new ovend version is not correct")
		return False


if __name__ == "__main__":

	fails = 0
	passes = 0
	for i in range(0, trials):
		if(main()== False):
			fails+=1
		else:
			passes+=1

	print("Passes ", passes, "fails ", fails, "Trials ", trials)
