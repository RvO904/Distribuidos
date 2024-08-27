'''
CLIENTE

Raúl Vélez Ortíz
Juan Alejandro Perez
'''

import socket
import os
import threading

# Crear un socket TCP/IP


'''while True:
    # Enviar datos al servidor
    message = input("Ingrese un mensaje para el servidor: ")
   

    # Recibir respuesta del servidor
    data = sock.recv(1024)
    print(f"Respuesta del servidor: {data.decode('utf-8')}")'''

def recibirMensaje(sock):
    while True:
        try:
            # Recibir mensajes del servidor
            respuesta = sock.recv(1024).decode('utf-8')
            if respuesta:
                print(f'\nRespuesta del servidor: {respuesta}')
            else:
                # Si el servidor cierra la conexión
                print("El servidor ha cerrado la conexión.")
                break
        except ConnectionResetError:
            print("Conexión cerrada inesperadamente.")
            break
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            break



if __name__ == '___main__':
    host = '192.168.0.12'  # Dirección IPv4 del servidor
    puerto = int(input('Ingrese su puerto (puede ser cualquier número): '))
    
    # Crear el socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectar el socket al servidor remoto
    sock.connect((host, puerto))


    hilo_receptor = threading.Thread(target=recibirMensaje, args=(sock))
    hilo_receptor.daemon = True
    hilo_receptor.start()


    while True:
        os.system('cls')
        print(f'Su puerto: {puerto}')
        destinationPort = int(input('Ingrese el puerto al que desea enviar un mensaje: '))
        mensaje = input(f'Ingrese el mensaje a enviar al puerto {destinationPort}: ')
        sock.sendall(mensaje.encode('utf-8'))

        if input('Desea enviar otro mensaje? (s/n): ').lower() != 's':
            break

    # Cerrar la conexión
    sock.close()

