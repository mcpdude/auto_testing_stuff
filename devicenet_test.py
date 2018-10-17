import paramiko
import sys
from time import sleep
from datetime import datetime
from datetime import timedelta
import pigpio

pi = pigpio.pi()

pins = {
    "1": "18",
    "2": "3", # Ken messed this up, yell at him if it borks
    "3": "4",
    "4": "17",
    "5": "27",
    "6": "22",
    "7": "23",
    "8": "24",
    "9": "25",
    "10": "5",
    "11": "6",
    "12": "13",
    "13": "19",
    "14": "26",
    "15": "12",
    "16": "16"

}



ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


oven_host = str(sys.argv[1])
oven_user = "root"
oven_PW = "woot"

oven_pin = int(sys.argv[2])

passes = 0
fails = 0

while True:
    attempts = 0
    connected = False
    
    
    pi.write(oven_pin, 0)
    sleep(15)
    pi.write(oven_pin, 1)
    start_time = datetime.now()
		
    while connected == False:
        try:
            ssh.connect(oven_host, username = oven_user, password = oven_PW)
            stdin, stdout, stderr  = ssh.exec_command("ls /")
            output=stdout.readlines()
            print(output)
            print("Pass!")
            elapsed = datetime.now() - start_time
            print("It took ", elapsed, " before I could connect.")
            passes+=1
            connected = True
        except:
            attempts +=1
            print("Couldn't connect...")
            sleep(5)
            if attempts >24:
                elapsed = datetime.now() - start_time
                print("Couldn't connect to the oven after ", elapsed, "\nRestarting...")
                fails +=1
                
    print("passes: ", passes, "fails: ", fails)

    ssh.close()