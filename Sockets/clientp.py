'''
CLIENTE

Raúl Vélez Ortíz
Juan Alejandro Perez
'''

import socket
import random

# Configuración de red
host = '192.168.0.12'  # Dirección IPv4 del servidor
ports = [12345, 12344, 12343, 12342]  # Puertos arbitrarios 
port = random.choice(ports) #Se escoge de manera aleatoria el puerto que el cliente utilizará
print(f'Conectandose desde puerto {port}') #Se imprime el puerto desde el que se conecta para informar al usuario

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar el socket al servidor remoto
sock.connect((host, port))

while True:
    # Enviar datos al servidor
    message = input("Ingrese un mensaje para el servidor: ")
    sock.sendall(message.encode('utf-8'))

    # Recibir respuesta del servidor
    data = sock.recv(1024)
    print(f"Respuesta del servidor: {data.decode('utf-8')}")

    # Preguntar al usuario si desea enviar otro mensaje
    continuar = input("¿Desea enviar otro mensaje? (s/n): ")
    if continuar.lower() != 's':
        break

# Cerrar la conexión
sock.close()