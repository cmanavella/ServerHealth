import socket

#Instancio un objeto para poder trabajar con el Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Seteo el puerto de escucha
server.bind("", 1992)

#Defino la cantidad de conexiones entrantes simultáneas. De momento solo una.
server.listen(1)

#Instancio un objeto cliente. Esto me premite recibir datos.
client, address = server.accept()

while True:
	

#Cierro las instancias de cliente y servidor
client.close()
server.close()
