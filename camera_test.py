import paramiko
from time import sleep
from gpiozero import LED
 
main_relay = LED(14)
 
camera_check = 'ls /dev/ttyS2 /dev/video0'
 
 
 
 
def main():
    passes = 0
    fails = 0

    host = '10.10.0.201'
    port = 22
    user = 'root'
    password = 'woot'

 
 
    while True:

        main_relay.off()
        print("turning off")
        sleep(1)
        main_relay.on()
        print("turning on")
        connected = False
        while connected == False:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, username = user, password = password)
                sleep(10)
                stdin, stdout, stderr = ssh.exec_command(camera_check)
                out_put = stdout.readlines()
                print(out_put)
 
                if '/dev/ttyS2n' in out_put:
                    print('not insane')
 
                    if '/dev/video0n' in out_put:
                        print("Pass!")
                        passes += 1
                        connected = True
                    else:
                        print("Fail :(")
                        fails += 1
                        connected = True
                else:
                    print('invalid result')

 
            except:
                print("Retrying Connection...")
                sleep(1)
                connected = False
               
 
        ssh.close()
        main_relay.on()
        main_relay.off()
        print("Fails: ", fails)
        print("Total: ", passes + fails)


main()
