import socket
import random
import os, os.path
import sys
total = random.randint(0,1000)
bbdd = {}
'''creacion base de datos siempre exitosa a lo menos tiene 0 valores'''
try:
	for i in range(total):
		bbdd[str(i)] = i+10
	print("base de datos creada con exito")
except IndexError:
	print("no se pudo crear la base de datos")
	exit(1)
if len(sys.argv)>= 3:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	port= 10000
	server_name = sys.argv[2]
	adress = (server_name,port)
else:
	path = ('/tmp/db.tuples.sock.')
	adress = path
	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.bind(adress)
s.listen(5)
while True:
	c,addr = s.accept()
	print('got connection from ',addr)
	c.send('[1] \n Thanks for connecting')
	while True:
		data = c.recv(1024)
		if not data:
			break
		peticion = str(data).upper()
		peticionc = peticion.split(" ")
		if peticionc[0] == "DISCONECT":
			c.send("[0] \n desconectando...")
			break
			print("desconectando...")
		if peticionc[0] == "GET":
			try:
				key = int(peticionc[1])
				dats = bbdd[str(key)]
				print("[999] \n  entregando valor " + str(dats) + " que pertenece a la llave " + str(key))
				c.send(str(dats))
			except KeyError:
				mensaje = "error [300] de peticion GET"
				print("cliente a solicitado una clave erronea")
				c.send(mensaje)
		elif peticionc[0].lower() == "delete":
			try:
				key = int(peticionc[1])
				datas = bbdd[str(key)]
				if datas:
					del bbdd[str(key)]	
					c.send("[999]\n  True")
					print("se ha borrado el valor para la llave "+ str(key))		
			except KeyError:
				print("no se ha encontrado la llave especificada : " + (peticionc[1]))
				c.send("error [200] de peticion DELETE")
		elif peticionc[0].lower() == "update":
			try:
				key = int(peticionc[1])
				datas = bbdd[str(key)]
				if datas:
					bbdd[str(key)] = peticionc[2]
					c.send("[999] \n llave actualizada con exito!")
					print("nuevo valor "+ str(peticionc[2]) + " para la llave "+ str(peticionc[1]))			
			except KeyError:
				print("no se ha encontrado la llave especificada : " + (peticionc[1]))
				c.send("error [100] de peticion DELETE")
		elif peticionc[0] == "LIST":
			pass
		elif peticionc[0] == "PEEK":
			pass
		elif peticionc[0].lower() == "insert":
			try:
				key = int(peticionc[1])
				datas = bbdd[str(key)]
				if datas:
					print("La llave propuesta tiene un valor, recomendamos usar : \n [UPDATE]")
					c.send("error [400] de peticion INSERT")
			except KeyError:
				print("ingresando dato de llave " + str(key) + " y de valor " + peticionc[2] )
				keyy = int(peticionc[1])
				bbdd[keyy] = peticionc[2]
				c.send("[999] \n  True")
		else:
			print("peticion no reconocida")
			c.send("[666] \n error desconocido")
						
	c.close()
