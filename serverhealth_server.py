import socket
import sys
import os
from termcolor import colored

#Instancio un objeto para poder trabajar con el Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Seteo las variables de escucha. Ip en blanco es localhost para recibir
#externas.
server_host = ''
server_port = 1992

#Con bind conecto al server. Lo hago por Try para manejar error en la escucha.
try:
	server.bind((server_host, server_port))
except socket.error as mensaje_error:
	print(colored('Se produjo un error al escuchar ' +
		'por el puerto:', 'red'), server_port)
	print(colored(mensaje_error, 'red'))

#Defino la cantidad de conexiones entrantes simultáneas. De momento solo una.
server.listen(1)

print("Estado del Servidor [", colored('OK', 'green'), "]")
print("Puerto de escucha:", colored(server_port, 'cyan'))
while True:
	#Capturo la excepcion de cancelacion del teclado para salir del server
	try:
		#Instancio un objeto cliente. Esto me premite recibir datos.
		client, address = server.accept()
		mensaje = "Hola Mundo"
		client.send(mensaje.encode())

		#Cierro las instancias de cliente y servidor
		client.close()
	except KeyboardInterrupt:
		print(colored('\nServidor apagado.', 'red'))
		try:
			sys.exit(0)
			server.close()
		except SystemExit:
			os._exit(0)
			server.close()
