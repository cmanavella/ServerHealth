import socket
import sys
import os
from termcolor import colored
import platform
import json
import psutil

#Instancio un objeto para poder trabajar con el Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Seteo las variables de escucha. Ip en blanco es localhost para recibir
#externas.
server_host = ''
server_port = 1992

#Con bind conecto al server. Lo hago por Try para manejar error en la escucha.
try:
	server.bind((server_host, server_port))
	#Defino la cantidad de conexiones entrantes simultáneas. De momento solo una.
	server.listen(1)

	print("Estado del Servidor [", colored('OK', 'green'), "]")
	print("Puerto de escucha:", colored(server_port, 'cyan'))
	#Capturo la excepcion de cancelacion del teclado para salir del server
	while True:
		#Instancio un objeto cliente. Esto me premite recibir datos.
		client, address = server.accept()

		client_data = client.recv(1024)

		if not client_data:
			break

		#Instancio el objeto Platform que me trae la Informacion
		#basica del sistema operativo.
		uname = platform.uname()

		memory = psutil.virtual_memory()
		cpu_freq = psutil.cpu_freq()
		#Armo el array para enviar al cliente.
		data = {
			"system": uname.system,
			"release": uname.release,
			"processor": uname.processor,
			"phisical_cores": psutil.cpu_count(logical=False),
			"total_cores": psutil.cpu_count(logical=True),
			"max_frec": cpu_freq.max,
			"min_frec": cpu_freq.min,
			"current_frec": cpu_freq.current,
			"total_memory": memory.total,
			"free_memory": memory.available,
			"used_memory": memory.used,
			"percent_memory": memory.percent
			}

		#Transformo el Array en un Objeto JSON
		data = json.dumps(data)

		#Envio el Objeto JSON
		client.send(data.encode())

	#Cierro las instancias de cliente y servidor
	client.close()
	print("El cliente se ha desconectado.")
except socket.error as mensaje_error:
	print(colored('Se produjo un error al escuchar ' +
		'por el puerto:', 'red'), server_port)
	print(colored(mensaje_error, 'red'))
except KeyboardInterrupt:
	print(colored('\nServidor apagado.', 'red'))
	try:
		sys.exit(0)
		server.close()
	except SystemExit:
		os._exit(0)
		server.close()
