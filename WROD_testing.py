import paramiko
import scp
import datetime
import subprocess
import pigpio
import subprocess

from time import sleep
from os.path import exists

test_list = ["WROD_test", "rootfs_test"]

def rootfs_test(IP_address, power_pin, button_pin, oven_serial):
    localpi = pigpio.pi()
    host = IP_address
    port = 22
    user = 'root'
    password = 'woot'
    oven_serial = oven_serial

    rootfs = ""
    
    power_pin_relay_on = localpi.write(power_pin, 1)
    power_pin_relay_off = localpi.write(power_pin, 0)

    print(datetime.date.today())
    filename = (str(datetime.date.today()) + "logfile.txt" + "_WROD")

    if exists(filename) != True:
        print("Creating a logfile...")
        target = open(filename, 'x')
        target.close()
        print("Logfile created!")

    elif exists(filename) == True:
        print("Appending to existing logfile.")   

    localpi.write(power_pin, 1) # not strictly necessary; we turned it on in main

    # CONNECT VIA SSH

    subprocess.run(["ssh-keygen", "-R", host]) #clear keys

    connected = False
    connection_attempts = 0
    while connected == False:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username = user, password = password)
            print("connected!")
            connected = True


        except:
            
            print("Retrying Connection... Attempt #:", connection_attempts + 1)
            sleep(1)
            connected = False
            connection_attempts += 1
            if connection_attempts >=50:
                print("Couldn't connect, rebooting.")
                localpi.write(power_pin, 1) 
                localpi.write(power_pin, 0) 
                sleep(10)
                localpi.write(power_pin, 1)
                connection_attempts = 0

    #CLEAR CACHE
    print("Clearing cache...")
    stdin, stdout, stderr  = ssh.exec_command("ls /brava/cache")
    output = stdout.readlines()
    print("Here's what's there.", stdout)
    ssh.exec_command("rm /brava/cache/*.bos")
    output  = ssh.exec_command("ls /brava/cache")
    print("Here's what's there now.", output)
    print("Cache cleared!")

    sleep(5)
    print('querying version')
    stdin, stdout, stderr = ssh.exec_command("cat /etc/version.txt")
    version = stdout.readlines()
    print(version)




    #CHECK OUTPUT
    
    ready_to_reboot = False

    if "keller_1.0\n" in version :
        rootfs = "A"
        print("We're on the A version.")
        subprocess.run(["ssh", "deploy@brava.cloud", "cohort-serial", "Emma-9-cohort-test", oven_serial])
        
        #return("PASS")

    elif "keller_1.01\n" in version:## Kuy will supply this
        rootfs = "B"
        print("We're on the B version.")
        subprocess.run(["ssh", "deploy@brava.cloud", "cohort-serial", "emma-gold", oven_serial])
        
        
        
        #return("PASS")

    else:
        print("Are you sure you're on the right oven?")
        return("FAIL")
        
    #prod the oven to check for a new cohort
    ssh.exec_command("nc -U /var/run/bambino <<< 'K1:36:S3:SETK1:24:S12:/ota/commandS5:check'")

    while ready_to_reboot == False:
        
        print("Checking the state of the oven...")
    
        stdin, stdout, stderr  = ssh.exec_command("journalctl -u timelord | grep NeedsInstall")
        check =  stdout.readlines()
        print(check)
        print("check type", type(check))
        sleep(10)
        
        for i in check:
            print(i)
            if "NeedsInstall" in i:
                print("time to reboot")
                ready_to_reboot = True

        #if "NeedsInstall" in check:
        #    ready_to_reboot = True
            
    localpi.write(power_pin, 0)
    
    ssh.close()
    subprocess.run(["ssh-keygen", "-R", host]) #clear keys
    sleep(10)
    localpi.write(power_pin, 1)
    
    

    
    connected = False
    while connected == False:
        try:
            ssh.connect(host, username = user, password = password)
            connected = True
        
        except :
            print("Retrying connection after the reboot...")
            connected = False
            sleep(4)
        
        
    print("connected, after reboot!")
    stdin, stdout, stderr  = ssh.exec_command("cat /etc/version.txt")
    new_version = stdout.readlines()
    print(new_version)
    if new_version == version:
        return("FAIL")
        
    elif new_version != version:
        return("PASS")
        
    ssh.close()
    
    
    








def WROD_test(IP_address, power_pin, button_pin):



    localpi = pigpio.pi()
    host = IP_address
    port = 22
    user = 'root'
    password = 'woot'

    
    power_pin_relay_on = localpi.write(power_pin, 1)
    power_pin_relay_off = localpi.write(power_pin, 0)
    button_on = localpi.set_servo_pulsewidth(button_pin, 1000)
    button_off = localpi.set_servo_pulsewidth(button_pin, 1500)

# CREATE LOGFILE
    print(datetime.date.today())
    filename = (str(datetime.date.today()) + "logfile.txt" + "_WROD")

    if exists(filename) != True:
        print("Creating a logfile...")
        target = open(filename, 'x')
        target.close()
        print("Logfile created!")

    elif exists(filename) == True:
        print("Appending to existing logfile.")

# CONNECT VIA SSH

    connected = False
    connection_attempts = 0
    localpi.write(power_pin, 1)
    while connected == False:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username = user, password = password)
            print("connected! LIES")
            connected = True
            sleep(5)
            print('running command')
            stdin, stdout, stderr = ssh.exec_command()
            out_put = stdout.readlines()
            print(out_put)

        except:
                
                print("Retrying Connection... Attempt #:", connection_attempts + 1)
                sleep(1)
                connected = False
                connection_attempts += 1
                if connection_attempts >=50:
                    print("Couldn't connect, rebooting.")
                    localpi.write(power_pin, 1) 
                    localpi.write(power_pin, 0) 
                    sleep(10)
                    localpi.write(power_pin, 1)
                    connection_attempts = 0


# TESTING

    localpi.write(power_pin, 0)
    sleep(3)
    localpi.write(power_pin, 1)

    return("PASS")




def main():
    
    passes = 0
    fails = 0

    button_pin = 0
    power_pin = 0
    IP_address = ""
    test_to_run = ""
    
    localpi = pigpio.pi()

    while test_to_run !="Q":

        print(test_list, "\n")

        test_to_run = input("What test should I run?\n Type Q to quit.\n")
        print(test_list, "\n")

        if test_to_run == "WROD_test":
            break

        if test_to_run == "rootfs_test":
            times_to_run = int(input("How many times should I run this test?\n"))
            power_pin = int(input("Type the power relay pin here:"))
            localpi.write(power_pin, 1) # turn the oven on so you can get the IP
            button_pin = "" ## we don't need the button for this test.
            IP_address = input("Type the oven's IP_address here:")
            oven_serial = input("Type the oven's serial number.")

            for i in range(1, times_to_run + 1):
                print("Running test rootfs test, trial: ", i, "of ", times_to_run, "\n", "passes/fails:", passes, "/", fails)
                result = rootfs_test(IP_address, power_pin, button_pin, oven_serial)

                if result == "PASS":
                    passes += 1
                    print("Pass!")

                elif result == "FAIL":
                    fails += 1
                    print("Fail...")

                else:
                    print("Whoops!")




    
    if test_to_run == "WROD_test":
        times_to_run = int(input("How many times should I run this test?\n"))
        print("This test must be run on a relay of sufficient amperage.")
        print("Ignoring this warning is REALLY GODDAMN DANGEROUS.")
        power_pin = int(input("Type the power relay pin here:"))
        button_pin = int(input("Type the button servo pin here:"))
        IP_address = input("Type the oven's IP IP_address here:")

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
