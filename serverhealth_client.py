import socket
import sys
import os
from termcolor import colored

#Variables
host = 'localhost'
port = 1992

#Creo el objeto Socket
server = socket.socket()

#Trato de conectar con el servidor
try:
    server.connect((host, port))
except socket.error as mensaje_refused:
    print(colored('Se produjo un error al intentar conectar con ' +
        'host:', 'red'), host, colored('por el puerto:', 'red'),
        port)
    print(colored(mensaje_refused, 'red'))
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

print("Conectado al servidor [", colored('OK', 'green'), "]")

#Bucle que retiene la conexión

mensaje = server.recv(1024)
print(mensaje.decode())

#Cierro la conexión
server.close()
