'''
servidorRPC.py

Raul Velez Ortiz
Juan Alejandro Perez

Este archivo define funciones de llamado remoto para gestionar mensajes entre usuarios
'''
from xmlrpc.server import SimpleXMLRPCServer
import threading


colaMensajes = {}

def enviarMensaje(msg:str, destino:str):
    '''
    Función para llamado remoto, se encarga de guardar en la cola de mensajes del usuario destino
    el mensaje enviado
    
    Entradas:
        msg: mensaje
        destino: usuario destino del mensaje
    '''
    if destino not in colaMensajes.keys():
        colaMensajes[destino] = []
    colaMensajes[destino].append(msg)
    print(colaMensajes[destino])
    return True


def recibirMensaje(destino):
    '''
    Función para llamado remoto, se encarga de sacar de la cola de mensajes el mensaje destinado al usuario
    
    Entradas:
        destino: usuario destino del mensaje
    '''
    if not colaMensajes.get(destino, None):
        return ''
    if len(colaMensajes[destino]) == 0:
        return ''
    
    print(colaMensajes[destino])
    return colaMensajes[destino].pop(-1)




# Configurar el servidor XML-RPC
def iniciarServidor(host, puerto):
    '''
    Función que genera el servidor RPC
    
    Entradas:  
        host: IP del host
        puerto: Puerto de comunicaciones
    '''

    server = SimpleXMLRPCServer((host, puerto))
    print(f"Servidor XML-RPC escuchando en {host}:{puerto}")

    # Registrar las funciones para que estén disponibles remotamente
    server.register_function(enviarMensaje, "enviarMensaje")
    server.register_function(recibirMensaje, "recibirMensaje")
    server.serve_forever()


if __name__ == '__main__':
    host = "192.168.0.12"
    puertos = [12345, 12344, 12343, 12342, 12341]
    iniciarServidor(host, puertos[0])

    