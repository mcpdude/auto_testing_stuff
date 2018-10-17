
import pigpio
from time import sleep
from random import randint
from datetime import datetime


def main():
    print('beginning testing...')
    localpi = pigpio.pi()
    localpi.write(3, 0)
    sleep(5)
    localpi.write(3, 1)
    connected = False
    while connected == False:
        connection_question = input("Have you connected all the oven's to the test network?Y/N\n")
        if connection_question == "Y":
            connected = True
        else:
            print("Okay! do your best...")
            
    print(datetime.now())
            
    while True:
        
            
        for i in range(1, 240):
            sleep(1)
            print(i, end="", flush=True)
        
        turnoff_time = randint(10, 60)
        
        localpi.write(3,0)
        
        print("turning the router off for ", turnoff_time, "seconds, at ", datetime.now())
        for k in range(1, turnoff_time):
            print(k, end="", flush=True)
        
        print("turning the router on for 420 seconds, at ", datetime.now())
        localpi.write(3,1)
            
        
main()
