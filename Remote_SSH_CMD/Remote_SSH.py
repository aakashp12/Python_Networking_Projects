import threading
import paramiko
import subprocess

def shh_command(ip, prt, user, passwd, command):
	client = paramiko.SSHClient()
	# client.load_host_keys('/home/justin/.ssh/known_hosts')
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(str(ip),port=int(prt),username=str(user),password=str(passwd))
	ssh_session = client.get_transport().open_session()
	if ssh_session.active:
		ssh_session.exec_command(str(command))
		print(ssh_session.recv(1024))
	return

ssh_command('192.168.1.4', '45', 'aakash', 'aakash', 'id')
