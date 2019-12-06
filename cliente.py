
import socket
import os, os.path
import sys

"""server_name = argv[1]"""
if len(sys.argv)>= 2:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	port = 10000
	host = (sys.argv[2]) 
	server_adress = (host,port)
else:
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	server_adress = ('/tmp/db.tuples.sock.')

sock.connect(server_adress)
print(sock.recv(1024))
while True:
	m = raw_input()
	sock.send(m)
	data = sock.recv(1024)
	if not data:
		break
	print(data)
sock.close()
