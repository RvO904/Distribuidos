from xmlrpc.server import SimpleXMLRPCServer
import threading

# Definir la función que se puede llamar remotamente
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

# Configurar el servidor XML-RPC
server = SimpleXMLRPCServer(("127.0.0.1", 12345))
print("Servidor XML-RPC escuchando en 127.0.0.1:12345")

# Registrar las funciones para que estén disponibles remotamente
server.register_function(add, "add")
server.register_function(subtract, "subtract")

# Iniciar el servidor en un hilo separado
def serve():
    server.serve_forever()

server_thread = threading.Thread(target=serve)
server_thread.start()