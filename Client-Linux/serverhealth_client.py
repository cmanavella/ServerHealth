import socket
import sys
import os
from termcolor import colored
import json
import time
from decimal import Decimal

#Variables
host = 'localhost'
port = 1992

#Funcion que convierte el tamaño de hardware en Kb, Mb, Gb, Tb o Pb
def get_size(bytes, suffix="B"):
	factor = 1024
	for unit in ["", "K", "M", "G", "T", "P"]:
		if bytes < factor:
			return f"{bytes:.2f}{unit}{suffix}"
		bytes /= factor

#Bucle que retiene la conexión
while True:
    #Borro la pantalla
    os.system('clear')

    #Creo el objeto Socket
    server = socket.socket()

    #Trato de conectar con el servidor
    try:
        server.connect((host, port))

        print("Conectado al servidor [", colored('OK', 'green'), "]")

        #Envio esto al servidor para que sepa que estoy conectado
        server.sendall(b"get")

        #Recibo los datos del servidor
        data = server.recv(1024)
        data = data.decode("utf-8")
        data = json.loads(data)

        print(colored('Sistema:', 'cyan'), data["system"])
        print(colored('Version:', 'cyan'), data["release"])

        print(colored('\nProcesador:', 'cyan'), data["processor"])
        print(colored('Nucleos Fisicos:', 'cyan'), data["phisical_cores"])
        print(colored('Total de Nucleos:', 'cyan'), data["total_cores"])
        print(colored('Frecuencia Maxima:', 'cyan'), data["max_frec"], 'Mhz')
        print(colored('Frecuencia Minima:', 'cyan'), data["min_frec"], 'Mhz')
        print(colored('Frecuencia Actual:', 'cyan'), data["current_frec"], 'Mhz')

        print(colored('\nMemoria Total:', 'cyan'), get_size(data["total_memory"]))
        print(colored('Memoria Libre:', 'cyan'), get_size(data["free_memory"]))
        print(colored('Memoria Usada:', 'cyan'), get_size(data["used_memory"]))
        print(colored('Porcentaje:', 'cyan'), data["percent_memory"], '%')

        server.close()
        time.sleep(1)
    except socket.error as mensaje_refused:
        print(colored('Se produjo un error al intentar conectar con ' +
            'host:', 'red'), host, colored('por el puerto:', 'red'),
            port)
        print(colored(mensaje_refused, 'red'))
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    #Capturo la excepcion de cancelacion del teclado para salir del server
    except KeyboardInterrupt:
        print(colored('\nConexion interrumpida.', 'red'))
        try:
            sys.exit(0)
            server.close()
        except SystemExit:
            os._exit(0)
            server.close()
