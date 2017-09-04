#!/usr/bin/env python
import sys
import socket
import getopt
import threading
import subprocess

# global variables to be used later
listen 				= False
command 			= False
upload 				= False
execute 			= ""
target 				= ""
upload_destination 	= ""
port 				= 0

def usage():
	print "BHP Net Tool"
	print
	print "Usage: CH_2_NETCAT_MIMIC.py -t target_host -p port"
	print "-l --listen			- listen on [host]:[port] for incoming connections."
	print "-e --execute=file_to_run 	- execute the given file upon receiving a connection."
	print "-c --command			- initialize a command shell"
	print "-u --upload=destination		- upon receiving connection upload a file and write to [destination]."
	print
	print
	print "Excamples: "
	print "CH_2_NETCAT_MIMIC.py -t 192.168.0.1 -p 4443 -l -c"

	sys.exit(0)

def client_sender(buffer):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	try:
		# try to connect to our target host
		client.connect((target, port))
		if len(buffer):
			client.send(buffer)
		while True:
			# wait for data
			recv_len = 1
			response = ""

			while recv_len:
				data = client.recv(4096)
				recv_len = len(data)
				response += data

				if recv_len < 4096:
					break

			print response

			# wait for more input
			buffer = raw_input("")
			buffer += "\n"

			# send it
			client.send(buffer)

	except:
		print "[*] Exception! Exiting..."
		client.close()

def server_loop():
	global target

	# if no target is defined, we listen to all interfaces
	if not len(target):
		target = "0.0.0.0"
	
	server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((target, port))
	server.listen(5)

	while True:
		client_socket, addr = server.accept()

		# creating a thread to handle our new client
		client_thread = threading.Thread(target=client_handler, args=(client_socket,))
		client_thread.start()

def run_command(command):
	# get rid of newline chars
	command = command.rstrip()
	
	try:
		# run command and get output
		output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
	except:
		output = "Failed to execute command.\r\n"
	# send output
	return output

def client_handler(client_socket):
	global upload
	global execute
	global command

	# check for upload
	if len(upload_destination):
		# read in all of the bytes and write to our destinations
		file_buffer = ""
		
		# keep reading data into file_buffer
		while True:
			data = client_socket.recv(1024)

			if not data:
				break
			else:
				file_buffer += data

		# now we try to put them in a file
		try:
			file_descriptor = open(upload_destination, "wb")
			file_descriptor.write(file_buffer)
			file_descriptor.close()
			
			# confirm it was written
			client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
		except:
			client_socket.send("Failed to save file to %s\r\n" % upload_destination)

	# check for command execution
	if len(execute):
		# run the command
		output = run_command(execute)

		client_socket.send(output)
	
	# we go into another loop if a command shell was requested
	if command:
		while True:
			# showing a simple prompt
			client_socket.send("<BHP:#> ")
				
			# now we receive until we see an enter key press
			cmd_buffer = ""
			while "\n" not in cmd_buffer:
				cmd_buffer += client_socket.recv(1024)

			# send back the output
			response = run_command(cmd_buffer)

			# respond back
			client_socket.send(response)

def Main():
	global listen
	global port
	global execute
	global command
	global upload_destination
	global target

	if not len(sys.argv[1:]):
		usage()
	
	# lets read the command line arguments passed in
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",
		["help", "listen", "execute", "target", "port", "command", "upload"])
	except getopt.GetoptError as err:
		print str(err)
		usage()

	for o,a in opts:
		if o in ("-h", "--help"):
			usage()
		elif o in ("-l", "--listen"):
			listen = True
		elif o in ("-e", "--execute"):
			execute = a
		elif o in ("-c", "--command"):
			command = True
		elif o in ("-u", "--upload"):
			upload_destination = a
		elif o in ("-t", "--target"):
			target = a
		elif o in ("-p", "--port"):
			port = int(a)
		else:
			assert False,"Unhandled Option"
	
	# Are we listening or sending data from stdin?
	if not listen and len(target) and port > 0:
		# We will read in the the buffer from commandline
		buffer = sys.stdin.read()

		# now we send data
		client_sender(buffer)
	
	# We are going to listen and potentially upload things,
	# Execute commands, and drop a shell back
	if listen:
		server_loop()

if __name__ == "__main__":
	Main()
