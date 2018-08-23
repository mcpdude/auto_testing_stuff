import paramiko
import scp
import datetime
import subprocess
import pigpio
import subprocess

from time import sleep
from os.path import exists

test_list = ["WROD_test", "rootfs_test"]

def rootfs_test(IP_address, power_pin, button_pin):
    localpi = pigpio.pi()
    host = IP_address
    port = 22
    user = 'root'
    password = 'woot'

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

    power_pin_relay_on

    # CONNECT VIA SSH

    connected = False
    while connected == False:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username = user, password = password)
            print("connected!")
            connected = True
            sleep(5)
            print('querying version')
            stdin, stdout, stderr = ssh.exec_command("cat /etc/version.txt")
            version = stdout.readlines()
            print(version)





        except:
                
            print("Retrying Connection... Attempt #:", connection_attempts + 1)
            sleep(1)
            connected = False
            connection_attempts += 1
            if connection_attempts >=50:
                print("Couldn't connect, rebooting.")
                power_pin_relay_on 
                power_pin_relay_off 
                sleep(10)
                power_pin_relay_on
                connection_attempts = 0

    #CLEAR CACHE
    print("Clearing cache...")
    ssh.exec_command("rm /brava/cache/*.bos")
    print("Cache cleared!")

    sleep(5)
    print('querying version')
    stdin, stdout, stderr = ssh.exec_command("cat /etc/version.txt")
    version = stdout.readlines()
    print(version)




    #CHECK OUTPUT

    if version == "keller_0.12_1d8bb70\n":
        rootfs = "A"
        print("We're on the A version.")
        return("PASS")

    elif version == "keller_1.0\n":## Kuy will supply this
        rootfs = "B"
        print("We're on the B version.")
        return("PASS")

    else:
        print("Are you sure you're on the right oven?")
        return("FAIL")








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
    power_pin_relay_on
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
                    power_pin_relay_on 
                    power_pin_relay_off 
                    sleep(10)
                    power_pin_relay_on
                    connection_attempts = 0


# TESTING

    power_pin_relay_off
    sleep(3)
    power_pin_relay_on

    return("PASS")




def main():
    
    passes = 0
    fails = 0

    button_pin = 0
    power_pin = 0
    IP_address = ""
    test_to_run = ""

    while test_to_run !="Q":

        print(test_list, "\n")

        test_to_run = input("What test should I run?\n Type Q to quit.\n")
        print(test_list, "\n")

        if test_to_run == "WROD_test":
            break

        if test_to_run == "rootfs_test":
            times_to_run = int(input("How many times should I run this test?\n"))
            power_pin = int(input("Type the power relay pin here:"))
            button_pin = 5 ## we don't need the button for this test.
            IP_address = input("Type the oven's IP IP_address here:")

            for i in range(1, times_to_run + 1):
                print("Running test rootfs test, trial: ", i, "of ", times_to_run, "\n")
                result = WROD_test(IP_address, power_pin, button_pin)

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
