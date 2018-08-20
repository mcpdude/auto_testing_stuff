import paramiko
import scp
import datetime
import subprocess
import pigpio

from time import sleep
from os.path import exists

test_list = ["WROD_test"]

def WROD_test(IP_address, power_pin, button_pin):

    localpi = pigpio.pi()
    host = IP_address


    
    power_pin_relay_on = localpi.write(power_pin, 1)
    power_pin_relay_off = localpi.write(power_pin, 0)
    button_on = localpi.set_servo_pulsewidth(button_pin, 1000)
    button_off = localpi.set_servo_pulsewidth(button_pin, 1500)

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
