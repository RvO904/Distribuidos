'''
SERVER QUE SE UTILIZARÁ COMO BROKER QUE COMUNIQUE DOS CLIENTES

Raúl Vélez Ortíz
Juan Alejandro Perez
'''
import socket
import threading

# Configuración de red
host = '10.253.51.75'  # Dirección IPv4 del servidor
ports = [12345, 12344, 12343, 12342, 12341]  # Puertos arbitrarios

def reenviarMensaje(puertoOrigen, puertoDestino, mensaje):
    ...


def clientHandler(clientSocket, clientAddr):
    '''
    clientHandler
    
    Entradas:
        clientSocket: socket del cliente
        clientAddr: dirección del cliente
        
    Proceso: 
        El servidor recibe el mensaje del cliente, una vez lo recibe, lo devuelve
        
    Lanza:
        ConnectionResetError
    '''
    print(f"Conexión establecida desde: {clientAddr}")
    
    while True:
        try:
             # Recibir datos del cliente
            data = clientSocket.recv(1024)
            if not data:
                break
            print(f"Mensaje recibido del cliente: {data.decode('utf-8')}")

             # Enviar respuesta al cliente
            response = input("Ingrese la respuesta para el cliente: ")
            clientSocket.sendall(response.encode('utf-8'))

        except ConnectionResetError:
            break

    print(f"Connection closed with {clientAddr}")
    clientSocket.close()


def listenPort(host, port):
    '''
    listenPort
    
    Entradas:
        host: Dirección IPv4 del host
        port: Puerto específico
        
    Proceso:
        Dependiendo del puerto en el que se esté escuchando, se utiliza la librería threads para recibir múltiples
        conexiones en este puerto específico, una vez un cliente se conecta a este puerto, se crea un nuevo hilo para 
        encargarse de las comunicaciones con este
    '''
    # Crear un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Enlace del socket a la dirección y puerto
    sock.bind((host, port))

    # Escuchar conexiones entrantes
    sock.listen(5)

    print(f"Servidor escuchando en {host}:{port}")

    while True:
        # Esperar una conexión
        conn, addr = sock.accept()
        handleClient = threading.Thread(target=clientHandler, args=(conn, addr))
        handleClient.start()

def startServer(host, ports):
    '''
    startServer
    
    Entradas: 
        host: dirección IPv4 del host
        ports: Lista de puertos soportados para este servidor
        
    Proceso:
        Para cada uno de los puertos se genera un hilo para soportar comunicaciones desde diferentes puertos, de la misma forma,
        un puerto puede hacerse cargo de múltiples clientes
    '''
    threads = []
    for port in ports:
        thread = threading.Thread(target=listenPort, args=(host, port))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish before shutting down
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    startServer(host, ports)