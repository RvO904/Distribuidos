import xmlrpc.client
import os
'''def recibir_mensajes(server, nombre):
    while True:
        try:
            respuesta = server.recibirMensaje(nombre)
            if respuesta:
                for re in respuesta:
                    print(f'\t{destinatario}: {re}')
        except KeyboardInterrupt:
            break



def enviar_mensajes(server, destinatario):
    while True:
        try:
            mensaje = input('- ')
            server.enviarMensaje(mensaje, destinatario)
        except KeyboardInterrupt:
            break'''


if __name__ == '__main__':
    host = '192.168.0.12'  # Dirección IPv4 del servidor
    nombre = input('Ingrese su nombre: ')
    
    server = xmlrpc.client.ServerProxy(f"http://{host}:12345/")

    destinatario = input('Ingrese el nombre de la persona a la que desea enviar un mensaje: ')

    os.system('cls')
    print('----------------------------------------------')
    print(f'|   CHAT DE {nombre} con {destinatario}')
    print('----------------------------------------------')

    try:
        while True:
            respuesta = server.recibirMensaje(nombre)
            if respuesta:
                print(f'{destinatario}: {respuesta}')
                '''for re in respuesta:
                    print(f'\t{destinatario}: {re}')'''
                
            mensaje = input('\t\t\tTú: ')
            server.enviarMensaje(mensaje, destinatario)
            
    except KeyboardInterrupt:
        print('Chat terminado')
    
