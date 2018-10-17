import paramiko
import sys
from time import sleep

password = "scabios4"
host ="brava.cloud"
user = "deploy"

ovend_first_hash = str(sys.argv[1])
ovend_second_hash = str(sys.argv[2]) + "\r"

oven_host = "192.168.1.144"
oven_user = "root"
oven_PW = "woot"

trials = int(sys.argv[3])
passes = 0
fails = 0

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for i in range(1, trials+1):

    first_pass = False
    test_complete = False
    
    
    ssh.connect(host, username = user, password = password)
    
    stdin, stdout, stderr  = ssh.exec_command("cohort-serial auto_test TWPT-95FP-NT00 ")
    output=stdout.readlines()
    print(output[-1])
    
    ssh.close()
    
    ssh.connect(oven_host, username = oven_user, password = oven_PW)
    
    stdin, stdout, stderr  = ssh.exec_command('nc -U /var/run/bambino <<< "K1:36:S3:SETK1:24:S12:/ota/commandS5:check"')
    print("checking cohorts...")
    
    sleep(3)

    stdin, stdout, stderr = ssh.exec_command('nc -U /var/run/bambino <<< "K1:37:S3:SETK1:25:S12:/ota/commandS6:commit"')
    output=stdout.readlines()
    print("committing cohorts...")

    sleep(10)

    print("committed cohort...")

    while test_complete == False:
        stdin, stdout, stderr = ssh.exec_command("script -c '/brava/app/core/test/batman -i /root/gordon.json -b /var/run/bambino -c <<< check_ovend & sleep 1; pkill batman' output.txt")
        sleep(1)
        stdin, stdout, stderr = ssh.exec_command("cat /root/output.txt")
        output=stdout.readlines()  
        #print(output) 

        if len(output) > 0:
            test_complete = True

        elif len(output) == 0:
            print("didn't get a response from bambino.")

        stdin, stdout, stderr = ssh.exec_command("rm /root/output.txt")

    print("Looking for ovend version: ", ovend_first_hash)

    for j in output:
        if ovend_first_hash in j:
            first_pass = True
            print(j)
            print("pass!")

        elif ovend_second_hash in j:
            print("still on the old hash...")
            

        else:
            pass
            #print(j)
            #print("fail")


    ssh.close()

    # #######SECOND PASS

    second_pass = False
    test_complete = False
    
    
    ssh.connect(host, username = user, password = password)
    
    stdin, stdout, stderr  = ssh.exec_command("cohort-serial auto_test2 TWPT-95FP-NT00 ")
    output=stdout.readlines()
    print(output[-1])
    
    ssh.close()
    
    ssh.connect(oven_host, username = oven_user, password = oven_PW)
    
    stdin, stdout, stderr  = ssh.exec_command('nc -U /var/run/bambino <<< "K1:36:S3:SETK1:24:S12:/ota/commandS5:check"')
    output=stdout.readlines()
    print("checking cohorts...")
    
    sleep(3)

    stdin, stdout, stderr = ssh.exec_command('nc -U /var/run/bambino <<< "K1:37:S3:SETK1:25:S12:/ota/commandS6:commit"')
    output=stdout.readlines()
    print("committing cohorts...")

    sleep(10)

    print("committed cohort...")

    while test_complete == False:
        stdin, stdout, stderr = ssh.exec_command("script -c '/brava/app/core/test/batman -i /root/gordon.json -b /var/run/bambino -c <<< check_ovend & sleep 1; pkill batman' output.txt")
        sleep(1)
        stdin, stdout, stderr = ssh.exec_command("cat /root/output.txt")
        output=stdout.readlines()  
        #print(output) 

        if len(output) > 0:
            test_complete = True

        elif len(output) == 0:
            print("didn't get a response from bambino.")

        #stdin, stdout, stderr = ssh.exec_command("rm /root/output.txt")

    print("Looking for ovend version: ", ovend_second_hash)

    for j in output:
        if ovend_second_hash in j:
            second_pass = True
            print(j)
            print("pass!")

        elif ovend_first_hash in j:
            print("still on the old hash...")
            

        else:
            pass
            #print(j)
            #print("fail")
            
    print(second_pass)

    if (first_pass and second_pass)  == True:
        trial_pass = True
        passes += 1
    elif trial_pass == False:
        fails += 1


    ssh.close()
    

    print("passes: ", passes, "fails: ", fails)
    
        
    
