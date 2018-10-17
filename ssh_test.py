import paramiko


password = "scabios4"
host ="brava.cloud"
user = "deploy"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(host, username = user, password = password)

stdin, stdout, stderr  = ssh.exec_command("cohort-create auto_test aredfern")
output=stdout.readlines()
print(output)
