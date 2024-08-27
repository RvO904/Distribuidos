'''
clienteRPC.py

Raul Velez Ortiz
Juan Alejandro Perez

Este archivo define funciones que sirven para enviar y recibir mensajes de un usuario utilizando un 
servidor RPC como broker que pasa los mensajes de un cliente a otro
'''

import xmlrpc.client
import os
import threading
import time


def recibir_mensajes(server, destino, origen):
    '''
    Funcion que se encarga de recibir mensajes del servidor RPC
    
    Entradas:
        server: Instancia del server RPC
        destino: nombre de la persona que esta recibiendo el mensaje
        origen: nombre de la persona que envió el mensaje
    '''
    while True:
        try:
            respuesta = server.recibirMensaje(destino)
            if respuesta:
                print(f'\n{origen}: {respuesta}')
            time.sleep(1)
        except KeyboardInterrupt:
            break



def enviar_mensajes(server, destinatario):
    '''
    Funcion que se encarga de enviar mensajes al servidor RPC
    
    Entradas:
        server: Instancia del server RPC
        destinatario: NOmbre de la persona a la que se le está enviando el mensaje
    '''
    while True:
        try:
            mensaje = f'{input('')}\n'
            server.enviarMensaje(mensaje, destinatario)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    '''
    Main
    
    Define nombre de host, nombre de la persona que maneja el chat y el destinatario
    Genera la instancia del servidor RPC para enviar y recibir mensajes
    Se utiliza la librería threading para poder recibir y enviar mensajes al mismo tiempo
    '''
    host = '192.168.0.12'  # Dirección IPv4 del servidor
    nombre = input('Ingrese su nombre: ')
    
    server = xmlrpc.client.ServerProxy(f"http://{host}:12345/")

    destinatario = input('Ingrese el nombre de la persona a la que desea enviar un mensaje: ')

    os.system('cls')
    print('----------------------------------------------')
    print(f'|   CHAT DE {nombre} con {destinatario}')
    print('----------------------------------------------')

    hiloEnviar = threading.Thread(target=enviar_mensajes, args=(server, destinatario))
    hiloRecibir = threading.Thread(target=recibir_mensajes, args=(server, nombre, destinatario))

    hiloEnviar.start()
    hiloRecibir.start()

    try:
        hiloRecibir.join()
        hiloEnviar.join()
            
    except KeyboardInterrupt:
        print('Chat terminado')
    
