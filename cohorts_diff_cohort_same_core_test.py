import paramiko
from time import sleep
from parse import *

host = "brava.cloud"
user = "deploy"
password = "scabios4"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


# Wait for a ssh connection
connected = False
while connected == False:
    try:

        ssh.connect(host, username = user, password = password)
        print("connected!")
        connected = True



    except:
        sleep(1)
        print("connecting...")

#cohort_name = input("Cohort name?\n")
#serial_num = input("serial_num?\n")
serial_num = "TWPT-95FP-NT00"
stdin, stdout, stderr = ssh.exec_command("cohort-serial auto_test 4RYC-16J4-9NMK")
output = stdout.readlines()
print(output)

ssh.close()

#oven_host = input("What's the IP? \n")
oven_host = "192.168.1.146"
oven_user = "root"
oven_password = "woot"
connected = False
while connected == False:
    try:

        ssh.connect(oven_host, username = oven_user, password = oven_password)
        print("connected!")
        connected = True



    except:
        sleep(1)
        print("connecting...")


#check cohort
stdin, stdout, stderr = ssh.exec_command('nc -U /var/run/bambino <<< "K1:36:S3:SETK1:24:S12:/ota/commandS5:check"')
check_cohort = stdout.readlines()
print(check_cohort)

sleep(3)
#apply cohort
stdin, stdout, stderr = ssh.exec_command('nc -U /var/run/bambino <<< "K1:37:S3:SETK1:25:S12:/ota/commandS6:commit"')
apply_cohort = stdout.readlines()
print(apply_cohort)

sleep(10)
#check vision
print("this is workinbg as intended")
stdin, stdout, stderr = ssh.exec_command('script -c"/brava/app/core/test/batman -i /root/gordon.json  -b /var/run/bambino -c -v <<< check_vision & sleep 2; pkill batman" version.txt')
sleep(1)
output = stdout.readlines()
print(output)

check_vision = ""
for i in output:
    if "check_vision" in i:
        check_vision = i.split()[1]
    if any(char.isdigit() for char in i):
        break
        
print(check_vision)

ssh.close()
# Wait for a ssh connection
connected = False
while connected == False:
    try:
        ssh.connect(host, username = user, password = password)
        print("connected!")
        connected = True



    except:
        sleep(1)
        print("connecting...")
        
#put in different cohort
#new_cohort_name = input("New Cohort name?\n")

stdin, stdout, stderr = ssh.exec_command("cohort-serial auto_test3 4RYC-16J4-9NMK ")
output = stdout.readlines()
print(output)

ssh.close()

connected = False
while connected == False:
    try:
        ssh.connect(oven_host, username = oven_user, password = oven_password)
        print("connected!")
        connected = True

    except:
        sleep(1)
        print("connecting...")
        
#check cohort
stdin, stdout, stderr = ssh.exec_command('nc -U /var/run/bambino <<< "K1:36:S3:SETK1:24:S12:/ota/commandS5:check"')
check_cohort = stdout.readlines()
print(check_cohort)

sleep(3)
#apply cohort
stdin, stdout, stderr = ssh.exec_command('nc -U /var/run/bambino <<< "K1:37:S3:SETK1:25:S12:/ota/commandS6:commit"')
apply_cohort = stdout.readlines()
print(apply_cohort)

sleep(10)
#check vision
stdin, stdout, stderr = ssh.exec_command('script -c"/brava/app/core/test/batman -i /root/gordon.json  -b /var/run/bambino -c -v <<< check_vision & sleep 2; pkill batman" version.txt')
output = stdout.readlines()

check_vision_new = ""
for i in output:
    if "check_vision" in i:
        check_vision_new = i.split()[1]
    if any(char.isdigit() for char in i):
        break
        
print(check_vision_new)

ssh.close()
if(check_vision is check_vision_new):
    print("FAIL!")
else:
    print(" PASS ")

