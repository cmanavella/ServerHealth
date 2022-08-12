import socket

#Variables
host = 'localhost'
port = 1992

#Creo el objeto Socket
obj = socket.socket()

#Conecto con el servidor
obj.connect((host, port))
print("Conectado al servidor")

#Bucle que retiene la conexión

mensaje = obj.recv(1024)
print(mensaje.decode())

#Cierro la conexión
obj.close()
