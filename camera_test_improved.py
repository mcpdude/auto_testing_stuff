import paramiko
import datetime
from time import sleep
from gpiozero import LED
from os.path import exists
 
main_relay = LED(int(input("Type the pin here:")))
 
camera_check = 'ls /dev/ttyS2 /dev/video0'
 

 
 
def main():

    #Initialize variables and get the target for the Oven's IP
    # also get the pion from the raspberry pi to toggle. 
    passes = 0
    fails = 0
 
    main_relay.on()
    host = input("Type the IP here:")
    port = 22
    user = 'root'
    password = 'woot'
 
    connection_attempts = 0
    reboots = 0

    
    filename = (str(datetime.date.today()) + "logfile.txt")

    if exists(filename) != True:
        print("Creating a logfile...")
        target = open(filename, 'x')
        target.close()
        print("Logfile created!")

    elif exists(filename) == True:
        print("Appending to existing logfile.")

    
    while True:

        
        #main_relay.off()
        #sleep(1)
        main_relay.on()
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


 
            except:
                
                print("Retrying Connection... Attempt #:", connection_attempts)
                sleep(1)
                connected = False
                connection_attempts += 1
                if connection_attempts >=50:
                    print("Couldn't connect, rebooting.")
                    main_relay.on()
                    main_relay.off()
                    sleep(10)
                    main_relay.on()
                    connection_attempts = 0
                    reboots += 1


        log_file = open(filename, 'a')
        trial_number = passes + reboots + fails
        log_out = "Trial #: " + str(trial_number) + ", passes:", str(passes), ", fails:", str(fails), ", reboots:", str(reboots), "\n"
        log_out =  str(log_out)
        print(log_out)
        log_file.write(log_out)
        log_file.close()
        
        connection_attempts = 0
        ssh.close()
        main_relay.on()
        main_relay.off()
        print("waiting ... (oven should be off)")
        sleep(15)
        print('Passes: ', passes)
        print("Fails: ", fails)
        print("Total: ", passes + fails)
        if fails >= 1:
            print("Fail rate: ", (fails / (fails + passes)) * 100,"%")
            
        if reboots >= 1:
            print("Reboots: ", reboots)

main()
 
