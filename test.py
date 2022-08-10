import platform
import psutil

#Funcion que convierte el tamaño de hardware en Kb, Mb, Gb, Tb o Pb
def get_size(bytes, suffix="B"):
	factor = 1024
	for unit in ["", "K", "M", "G", "T", "P"]:
		if bytes < factor:
			return f"{bytes:.2f}{unit}{suffix}"
		bytes /= factor

#Informacion basica del sistema
uname = platform.uname()

print("="*40, "INFORMACIÓN BÁSICA DEL SISTEMA", "="*40)
print(f"Sistema: {uname.system}")
print(f"Versión: {uname.release}")
print(f"Nombre del Equipo: {uname.node}")
print(f"Arquitectura: {uname.machine}\n")

#Informacion del CPU
print("="*40, "INFORMACIÓN DEL CPU", "="*40)
print(f"Procesador: {uname.processor}")
#Número de núcleos
print("Núcleos Físicos:", psutil.cpu_count(logical=False))
print("Total de Núcleos:", psutil.cpu_count(logical=True))
#Frecuencias CPU
cpu_freq = psutil.cpu_freq()
print(f"Frecuencia Máxima: {cpu_freq.max:.2f}Mhz")
print(f"Frecuencia Mínima: {cpu_freq.min:.2f}Mhz")
print(f"Frecuencia Actual: {cpu_freq.current:.2f}Mhz")
#Uso del CPU
print("Uso del CPU por Núcleo:")
for i, porcentaje in enumerate(psutil.cpu_percent(percpu=True)):
	print(f"Núcleo {i}: {porcentaje}%")
print(f"Total de Uso del CPU: {psutil.cpu_percent()}%")

#Informacion de Memoria
print("="*40, "INFORMACIÓN DE MEMORIA", "="*40)
svmem = psutil.virtual_memory()
print(f"Total: {get_size(svmem.total)}")
print(f"Libre: {get_size(svmem.available)}")
print(f"Usado: {get_size(svmem.used)}")
print(f"Porcentaje: {svmem.percent}%")
print("="*40, "INFORMACIÓN DE MEMORIA SWAP", "="*40)
swap = psutil.swap_memory()
print(f"Total: {get_size(swap.total)}")
print(f"Libre: {get_size(swap.free)}")
print(f"Usado: {get_size(swap.used)}")
print(f"Porcentaje: {swap.percent}%")

#Informacion del Disco Duro
print("="*40, "INFORMACIÓN DE DISCO DURO", "="*40)
print("Particiones y Uso:")
partitions = psutil.disk_partitions()
for partition in partitions:
	print(f"=== Unidad: {partition.device} ===")
	print(f"   Punto de Montaje: {partition.mountpoint}")
	try:
		partition_usage = psutil.disk_usage(partition.mountpoint)
	except PermissionError:
		continue
	print(f"   Sistema de Archivo: {partition.fstype}")
	print(f"   Tamaño Total: {get_size(partition_usage.total)}")
	print(f"   Usado: {get_size(partition_usage.used)}")
	print(f"   Libre: {get_size(partition_usage.free)}")
	print(f"   Porcentaje: {partition_usage.percent}%")
disk_io = psutil.disk_io_counters()
print(f"Total Leído: {get_size(disk_io.read_bytes)}")
print(f"Total Escrito: {get_size(disk_io.write_bytes)}")

#CONTROL DE TEMPERATURAS
temps = psutil.sensors_temperatures()
print("="*40, "TEMPERATURAS", "="*40)
if not temps:
	print("No se pudo encontrar sensor")
else:
	for name, entries in temps.items():
		print(f"{name}:")
		for entry in entries:
			print("   %-20s %s °C (Alto = %s °C, Critico = %s °C)" %
				(entry.label or name, entry.current, entry.high, entry.critical))

#CONTROL DE VENTILADORES
fans = psutil.sensors_fans()
print("="*40, "VENTILADORES", "="*40)
if not fans:
	print("No se pudo encontrar sensor")
else:
	for name, entries in fans.items():
		print(f"{name}:")
		for entry in entries:
			print("   %-20s %s RPM" %
				(entry.label or name, entry.current))
